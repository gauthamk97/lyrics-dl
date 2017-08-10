#Gets lyrics for a single song from the Google API + Metrolyrics

from bs4 import BeautifulSoup
import urllib
import requests
import json

flag=False
band=raw_input('Enter band name : ')
song=raw_input('Enter song name : ')
searchEngineID='013005384117311148169%3A7rehj54nzye'
APIKey='AIzaSyAcBWajtXvUDXlv08CtFr7mJamWugAcxmM'
print

band=band.lower().replace(' ','-')
song=song.lower().replace(' ','-')

searchUrl='https://www.googleapis.com/customsearch/v1?q='+band+'+'+song+'&cx='+searchEngineID+'&num=1&key='+APIKey
a = requests.get(searchUrl)
b = json.loads(a.text)

if b.has_key('items'):
    url = b['items'][0]['link']

    mainPage=urllib.urlopen(url).read()
    soup = BeautifulSoup(mainPage, 'html.parser')

    for div in soup.find_all('div'):
        if div.has_attr('id'):
            if div['id']=='lyrics-body-text':
                flag=True
                mainDiv=div
                for para in mainDiv.find_all('p'):
                    print para.text
                    print
                break

    if flag==False:
        print "Couldn't find lyrics for "+band+" - "+song
        
else:
    print "Couldn't find lyrics for "+band+" - "+song
