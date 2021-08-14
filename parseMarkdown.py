import re, csv

indexPattern = re.compile(r'#R?\d*:?\s*')
episodesPattern = re.compile(r'\s*\(ep.*\)')
songPattern = re.compile(r'((?:"|“|”)*.*(?:"|“|”)*\s*(?:\(.*\))*)\s*[bB]y\s*(.*)')
quotePattern = re.compile(r'"|“|”')

fieldnames = ['title', 'artist', 'anime', 'type', 'index']

currentSong = {
    'title': '',
    'artist': '',
    'anime': '',
    'type': '',
    'index': 1
}

# Non-blank, non-separator, line generator
def getLines(f):
    for l in f:
        line = l.rstrip()
        if line and line != '---' and line != '# Anime Playist':
            yield line

# Parse line and take the appropriate action
def parseLine(line: str):
    if line.startswith('## '):
        currentSong['anime'] = line[3:]
    elif line == r'### Openings':
        currentSong['type'] = 'OP'
        currentSong['index'] = 1
    elif line == r'### Endings':
        currentSong['type'] = 'ED'
        currentSong['index'] = 1
    else:
        parseSong(line)

# Parse a song from a line
def parseSong(line: str):
    m = songPattern.search(stripLine(line))
    if m:
        currentSong['title'] = quotePattern.sub('', m.group(1)).strip()
        currentSong['artist'] = m.group(2)            
        writer.writerow(currentSong)
    else:
        print(f'Invalid Line: {line}')

    currentSong['index'] += 1

# Strip unneeded information from lines such as index and episodes
def stripLine(line: str):
    return indexPattern.sub('', episodesPattern.sub('', line))


if __name__ == '__main__':
    with open('songlist.md', 'r', encoding='utf-8') as file:
        lines = getLines(file)
        with open('songs.csv', 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')    
            writer.writeheader()
            for line in lines:
                parseLine(line)


