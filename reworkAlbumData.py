# I initially save the anime name and index (eg. OP1, ED1, etc) as the album in the mp3 metadata, but later decided to change it so the album is just the anime and the index is the track #
# This is the script to automate that, you probably don't need it

from mutagen.easyid3 import EasyID3
import os

directory = r'DIRECTORY GOES HERE'
files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
for file in files:
    audio = EasyID3(file)
    album = audio['album'][0]
    audio['album'] = ' '.join(album.split()[:-1])
    audio['tracknumber'] = album.split()[-1]
    audio.save()
    print(audio)