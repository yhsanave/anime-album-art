# Prune duplicates from songs.csv
# Duplicates typically occur for shows where the OP is first played at the end of episode 1 and MAL lists it as both an OP and ED
# If a song is both an OP and an ED, it will only be listed as an OP and all following EDs will have their index updated to reflect its removal

import csv

songs = []
current_anime = ''
fieldnames = ['title', 'artist', 'anime', 'type', 'index']
op_offset = 0
ed_offset = 0
count = 0

with open('songs.csv', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel')

    for song in reader:
        if song['anime'] != current_anime:
            current_anime = song['anime']
            op_offset = 0
            ed_offset = 0

        check = [s for s in songs if s['title'] == song['title']
                 and s['artist'] == song['artist'] and s['anime'] == song['anime']]
        if len(check):
            op_offset = len([c for c in check if c['type'] == 'ED'])
            ed_offset = len([c for c in check if c['type'] == 'OP'])
            count += 1
        else:
            songs.append({
                'title': song['title'],
                'artist': song['artist'],
                'anime': song['anime'],
                'type': song['type'],
                'index': int(song['index']) - ed_offset if song['type'] == 'ED' else int(song['index']) - op_offset
            })

with open('songs.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    writer.writeheader()
    writer.writerows(songs)

print(f'Pruned {count} duplicate songs')
