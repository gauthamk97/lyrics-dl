from bs4 import BeautifulSoup
import urllib, requests, json, os, eyed3

flag=False
searchEngineID='013005384117311148169%3A7rehj54nzye'
APIKey='AIzaSyAcBWajtXvUDXlv08CtFr7mJamWugAcxmM'

for subdir, dir, files in os.walk(os.getcwd()):
    for fileName in files:
        if fileName.endswith(".mp3"):
            path=subdir+'/'+fileName
            try:
                audio = eyed3.load(path)
            except ValueError:
                print "Encoding problem with "+fileName
                break

            band = audio.tag.artist
            song = audio.tag.title
            tempBand = band
            tempSong = song
            lyrics=""
            band=band.lower().replace(' ','-')
            song=song.lower().replace(' ','-')

            print "Getting lyrics for "+tempBand+" - "+tempSong

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
                                lyrics+=para.text
                                lyrics+='\r\r'
                            break

                if flag==False:
                    print "Couldn't find lyrics for "+tempBand+" - "+tempSong
                else:
                    lyrics = lyrics[:len(lyrics)-2]
                    audio.tag.lyrics.set(lyrics)
                    try:
                        audio.tag.save()
                    except NotImplementedError:
                        print "Error - ID3v2.2 for "+tempBand+" - "+tempSong
                    
            else:
                print "Couldn't find lyrics for "+tempBand+" - "+tempSong
