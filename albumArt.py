# Download cover images and save them to art/ to be used as album art

import requests
import shutil
from time import sleep
from pathvalidate import sanitize_filename
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn


class Show:
    title = ''
    imageURL = ''

    def __init__(self, titles, imageURL) -> None:
        self.title = titles['english'] if titles['english'] else titles['romaji']
        self.imageURL = imageURL


userId = 156530

query = '''
query ($id: Int) {
  MediaListCollection(userId: $id, type: ANIME, status_in: [CURRENT, COMPLETED]) {
    lists {
      entries {
        media {
         	title {
                english
                romaji
            }
            coverImage {
                extraLarge
            }
        }
      }
    }
  }
}
'''

variables = {
    'id': userId
}

aniListUrl = 'https://graphql.anilist.co'

response = requests.post(
    aniListUrl, json={'query': query, 'variables': variables})
lists = response.json()["data"]["MediaListCollection"]["lists"]
shows: list[Show] = []

for list in lists:
    for entry in list['entries']:
        show = Show(entry['media']['title'], entry['media']
                    ['coverImage']['extraLarge'])
        if not [s for s in shows if s.title == show.title]:
            shows.append(show)


with Progress(TextColumn('Getting cover art: {task.fields[title]}'), BarColumn(), MofNCompleteColumn(), TimeRemainingColumn(), transient=True) as prog:
    task = prog.add_task(description='Getting cover art',
                         total=len(shows), title='')

    for show in shows:
        prog.update(task, title=f'{show.title:30.30}{"..." if len(show.title) > 30 else "   "}', advance=1)
        image_url = show.imageURL
        filename = f'art\\{sanitize_filename(show.title)}.{image_url.split(".")[-1]}'

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print(f'Image couldn\'t be retreived for show: {show.title}')
