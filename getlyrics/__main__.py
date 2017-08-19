import click
from bs4 import BeautifulSoup
import urllib, requests, json, os, eyed3

@click.command()
@click.option('-a',is_flag=True,help='If FILES is provided, this option will not ask the user to input artist and song details when it\'s absent in the file\'s metadata. Instead, the file will be skipped')
@click.option('-l',is_flag=True,help='If FILES is provided, this option will skip songs for which lyrics already exists')
@click.option('-o',is_flag=True,help='If FILES is provided, this option will suppress the output of the obtained lyrics on to the standard output')
@click.option('-s',is_flag=True,help='If FILES is provided, this option will save the obtained lyrics in the file\'s metadata')
@click.argument('files',nargs=-1, type=click.File('rw'))
def maingl(files,a,l,o,s):
    """Welcome to lyrics-dl.
    
    There are two ways to use this tool :-
        

        1. lyrics-dl -> Prompt will ask you for the artist and song name. The obtained lyrics will be printed on the standard output.

        2. lyrics-dl [FILES] -> Tool will access artist and song information from the metadata of the provided files, and prints the obtained lyrics on the standard output.

    Note : Only mp3 files supported for now. Support for other files coming soon!

    Enjoy! :)

    Use the following options to make the most of this tool :-

    
    """

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
                if a:
                    click.echo('Artist/Song information missing for '+path+'. Moving on to next song')
                    continue
                else:
                    click.echo('Artist/Song information missing for '+path+'. Please enter details :-')
                    artist = raw_input('Enter Artist Name : ')
                    song = raw_input('Enter Song Name : ')
                    tempArtist = artist
                    tempSong = song
                    artist=artist.lower().replace(' ','-') #for query purposes
                    song=song.lower().replace(' ','-') #for query purposes

                    audio.tag.artist = tempArtist.decode('utf-8')
                    audio.tag.title = tempSong.decode('utf-8')
            
            #Skipping songs if lyrics are already present
            if l:
                if audio.tag.lyrics[0]:
                    click.echo('Lyrics already exist for '+tempArtist+' - '+tempSong)
                    continue
                    
            click.echo('Finding lyrics for '+tempArtist+' - '+tempSong)
            lyrics = findlyrics(artist, song)
            if not lyrics:
                continue

            #Removes newline characters from the beginning of lyrics
            for char in lyrics:
                if char=='\n' or char=='\r':
                    lyrics = lyrics[1:]
                else:
                    break

            #Removes newline characters from the end of lyrics
            for i in range(len(lyrics)-1,0,-1):
                if lyrics[i]=='\n' or lyrics[i]=='\r':
                    lyrics = lyrics[:len(lyrics)-1]
                else:
                    break
                    
            if not o:
                click.echo('\n'+tempArtist.upper()+" - "+tempSong.upper()+" LYRICS\n"+lyrics+'\n')
            if s:
                #Saves lyrics in mp3 metadata
                audio.tag.lyrics.set(lyrics)

                try:
                    audio.tag.save()
                    click.echo("Saved lyrics for "+tempArtist+" - "+tempSong+"\n")
                except NotImplementedError:
                    click.echo("Error - ID3v2.2 for "+tempArtist+" - "+tempSong+"\n")

    else:
		artist = raw_input('Enter Artist Name : ')
		song = raw_input('Enter Song Name : ')
		artist=artist.lower().replace(' ','-') #for query purposes
		song=song.lower().replace(' ','-') #for query purposes
		lyrics = findlyrics(artist, song)
		if lyrics:
			click.echo(lyrics) #Prints lyrics

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
                            return div.text#Returns Lyrics from AZLyrics
                    break

    else:
        return
