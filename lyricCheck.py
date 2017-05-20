import os, eyed3
dict={}
eyed3.log.setLevel("ERROR") #only print errors, not wornings
for subdir, dir, files in os.walk(os.getcwd()):
    for fileName in files:
        if fileName.endswith(".mp3"):
            try:
                audio = eyed3.load(subdir+'/'+fileName)
                band = audio.tag.artist
                song = audio.tag.title
                existingLyrics = audio.tag.lyrics[0]
                if band in dict.keys():
                    dict[band].append(song)
                else:
                    dict[band]=[song]
            except ValueError:
                continue
            except AttributeError:
                continue
            except IndexError:
                continue

artists = dict.keys()
artists.sort()

for item in artists:
    print item,' : '
    for song in dict[item]:
        print '\t',song
    print
