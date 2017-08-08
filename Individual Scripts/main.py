from bs4 import BeautifulSoup
import urllib, requests, json, os, eyed3

eyed3.log.setLevel("ERROR") #only print errors, not wornings
flag=False
searchEngineID='013005384117311148169%3A7rehj54nzye'
APIKey='AIzaSyAcBWajtXvUDXlv08CtFr7mJamWugAcxmM'

forbiddenArtists = ['TamilBeat.Com', 'www.Songs.PK', 'Hans Zimmer', 'The Indian Jam Project']
songList = []
for subdir, dir, files in os.walk(os.getcwd()):
    for fileName in files:
        if fileName.endswith(".mp3"):
            path=subdir+'/'+fileName
            songList.append(path) #songList contains path of all songs

choice = raw_input("Enter \n1. Google API & MetroLyrics\n2. AZ Lyrics\n")

for path in songList:
    try:
        audio = eyed3.load(path)
    except ValueError:
        print "Encoding problem with "+path
        continue

    try:
        band = audio.tag.artist
        if band in forbiddenArtists:
            continue #skip song if artist is in forbiddenArtists
            
        song = audio.tag.title
        tempBand = band
        tempSong = song
        band=band.lower().replace(' ','-') #for query purposes
        song=song.lower().replace(' ','-') #for query purposes
    except AttributeError:
        print 'Artist/Song information missing for '+path
        continue

    try:
        existingLyrics = audio.tag.lyrics[0]
        #print "Lyrics already exist for "+tempBand+" - "+tempSong
        continue

    except IndexError:
        #Lyrics don't exist. Hence finding it.
        lyrics=u""

        print "Getting lyrics for "+tempBand+" - "+tempSong

        #Google API + Metrolyrics
        if choice=='1':
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
                    print "Couldn't find lyrics for "+tempBand+" - "+tempSong+"\n"
                else:
                    lyrics = lyrics[:len(lyrics)-2]
                    audio.tag.lyrics.set(lyrics)
                    try:
                        audio.tag.save()
                        print "Found lyrics for "+tempBand+" - "+tempSong+"\n"
                    except NotImplementedError:
                        print "Error - ID3v2.2 for "+tempBand+" - "+tempSong+"\n"
                    
            else:
                print "Couldn't find lyrics for "+tempBand+" - "+tempSong+"\n"

        #AZLyrics
        elif choice=='2':
            searchUrl='http://search.azlyrics.com/search.php?q='+band+'+'+song
            searchPage = urllib.urlopen(searchUrl).read()
            searchSoup = BeautifulSoup(searchPage, 'html.parser')

            try:
                alltds = searchSoup.find_all('td')
                url = alltds[0].a['href'] #Will invoke Index Error if problem
                for td in alltds:
                    if td.has_attr('class'):
                        url = td.a['href']
                        break
            except IndexError:
                print "Couldn't find that song"
                continue

            mainPage = urllib.urlopen(url).read()
            soup = BeautifulSoup(mainPage, 'html.parser')

            #Finding div that contains the div that contains the lyrics
            for div in soup.find_all('div'):
                if div.has_attr('class'):
                    if [u'col-xs-12', u'col-lg-8', u'text-center'] == div['class']:
                        mainDiv = div
                        for div in mainDiv.find_all('div'):
                            if not div.has_attr('class'):
                                lyrics = div.text
                                for char in lyrics:
                                    if (char=='\n' or char=='\r'):
                                        lyrics=lyrics[1:]
                                    else:
                                        break
                        break

            #Saves lyrics in mp3 metadata
            audio.tag.lyrics.set(lyrics)
            try:
                audio.tag.save()
                print "Set lyrics for "+tempBand+" - "+tempSong+"\n"
            except NotImplementedError:
                print "Error - ID3v2.2 for "+tempBand+" - "+tempSong+"\n"
