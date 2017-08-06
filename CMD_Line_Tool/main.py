import click
from bs4 import BeautifulSoup
import urllib, requests, json, os, eyed3

@click.command()
def maingl():
    """Welcome to getlyrics.
    
    Enter artist and song name when prompted, and watch the magic happen :)"""
    
    artist = raw_input('Enter Artist Name : ')
    song = raw_input('Enter Song Name : ')
    searchUrl='http://search.azlyrics.com/search.php?q='+artist+'+'+song
    searchPage = urllib.urlopen(searchUrl).read()
    searchSoup = BeautifulSoup(searchPage, 'html.parser')
    lyrics=u''
    lyricsFound = False

    #First Attempt - AZ Lyrics
    try:
        url = searchSoup.find_all('td')[0].a['href']
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
                            click.echo(div.text) #Prints Lyrics from AZLyrics
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
            else:
                lyrics = lyrics[:len(lyrics)-2] #Removes \n from the end
                click.echo('\n\n'+lyrics) #For readability
        else:
                click.echo("Couldn't find lyrics through Google's API")
