# Scan your music directory and remove any songs from songs.csv that are found in it
# Assumes the album is the anime title and the track number is the type and index (OP1, ED2, etc.) and matches based on that.
# Matching is case sensitive

import os
import re
from dataclasses import dataclass, asdict
from csv import DictReader, DictWriter
from mutagen.easyid3 import EasyID3
from rich.progress import track

TYPE_REGEX = re.compile(r'(\D*)(\d*)')
FIELD_NAMES = ['title', 'artist', 'anime', 'type', 'index']
DIRECTORY = r'DIRECTORY GOES HERE'

@dataclass
class Song():
    title: str
    artist: str
    anime: str
    type: str
    index: str


files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if f.endswith('.mp3')]
songs: list[Song] = []

with open('songs.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader = DictReader(csvfile)
    for row in reader:
        songs.append(Song(row['title'], row['artist'],
                     row['anime'], row['type'], row['index']))

initialCount = len(songs)

for f in track(files):
    audio = EasyID3(f)
    anime = audio['album'][0]
    if m := TYPE_REGEX.match(audio['tracknumber'][0]):
        songtype = m.group(1) if m.group(1) else ''
        index = m.group(2) if m.group(2) else ''
    else:
        songtype = ''
        index = ''

    songs = [s for s in songs if s.anime != anime or s.type != songtype or s.index != index]

print(f'Removed {initialCount - len(songs)} already present songs')

with open('songs.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = DictWriter(csvfile, fieldnames=FIELD_NAMES)
    writer.writeheader()
    test = [*map(asdict, songs)]
    writer.writerows(test)
