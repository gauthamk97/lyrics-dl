import click
from bs4 import BeautifulSoup
import urllib, requests, json, os, eyed3

@click.command()
@click.argument('files',nargs=-1, type=click.File('rw'))
def maingl(files):
    """Welcome to getlyrics.
    
    Enter artist and song name when prompted, and watch the magic happen :)"""

    eyed3.log.setLevel("ERROR") #only print errors, not wornings

    if files:
        songList=[]
        for fileName in files:
            if fileName.name.endswith(".mp3"):
                songList.append(fileName.name) #songList contains path of all songs

        for path in songList:
            try:
                audio = eyed3.load(path)
            except ValueError:
                click.echo("Encoding problem with "+path)
                continue

            try:
                artist = audio.tag.artist
                song = audio.tag.title
                tempArtist = artist
                tempSong = song
                artist=artist.lower().replace(' ','-') #for query purposes
                song=song.lower().replace(' ','-') #for query purposes
            except AttributeError:
                click.echo('Artist/Song information missing for '+path)
                continue

            click.echo("Finding lyrics for "+tempArtist+" - "+tempSong)
            lyrics = findlyrics(artist, song)
            click.echo('\n'+tempArtist.upper()+" - "+tempSong.upper()+" LYRICS\n"+lyrics)

    else:
		artist = raw_input('Enter Artist Name : ')
		song = raw_input('Enter Song Name : ')
		artist=artist.lower().replace(' ','-') #for query purposes
		song=song.lower().replace(' ','-') #for query purposes
		lyrics = findlyrics(artist, song)
		click.echo("\n\n"+lyrics) #Prints lyrics

def findlyrics(artist, song):
    
    searchUrl='http://search.azlyrics.com/search.php?q='+artist+'+'+song
    searchPage = urllib.urlopen(searchUrl).read()
    searchSoup = BeautifulSoup(searchPage, 'html.parser')
    lyrics=u''
    lyricsFound = False

    #First Attempt - AZ Lyrics
    try:
        alltds = searchSoup.find_all('td')
        url = alltds[0].a['href'] #Will invoke Index Error search results empty
        for td in alltds:
            if td.has_attr('class'):
                url = td.a['href']
                break
        lyricsFound=True
    except IndexError:
        click.echo("Couldn't find that song on AZLyrics.")

    if lyricsFound:
        mainPage = urllib.urlopen(url).read()
        soup = BeautifulSoup(mainPage, 'html.parser')

        #Finding div that contains the div that contains the lyrics
        for div in soup.find_all('div'):
            if div.has_attr('class'):
                if [u'col-xs-12', u'col-lg-8', u'text-center'] == div['class']:
                    mainDiv = div
                    for div in mainDiv.find_all('div'):
                        if not div.has_attr('class'):
                            return div.text[2:] #Returns Lyrics from AZLyrics
                    break

    else:
        #Second Attempt - Google API + Metrolyrics

        searchEngineID='013005384117311148169%3A7rehj54nzye'
        APIKey='AIzaSyAcBWajtXvUDXlv08CtFr7mJamWugAcxmM'

        searchUrl='https://www.googleapis.com/customsearch/v1?q='+artist+'+'+song+'&cx='+searchEngineID+'&num=1&key='+APIKey
        a = requests.get(searchUrl)
        b = json.loads(a.text)

        if b.has_key('items'):
            url = b['items'][0]['link']

            mainPage=urllib.urlopen(url).read()
            soup = BeautifulSoup(mainPage, 'html.parser')

            for div in soup.find_all('div'):
                if div.has_attr('id'):
                    if div['id']=='lyrics-body-text':
                        lyricsFound=True
                        mainDiv=div
                        for para in mainDiv.find_all('p'):
                            lyrics+=para.text
                            lyrics+='\n\n'
                        break

            if not lyricsFound:
                click.echo("Couldn't find lyrics on MetroLyrics")
                return
            else:
                lyrics = lyrics[:len(lyrics)-1] #Removes \n from the end
                return lyrics
        else:
                click.echo("Couldn't find lyrics through Google's API")
                return
