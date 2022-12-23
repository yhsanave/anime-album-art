import requests

userId = 156530 

query = '''
query ($id: Int, $date: FuzzyDateInt) {
  MediaListCollection(userId: $id, type: ANIME, status_in: [CURRENT, COMPLETED], startedAt_greater: $date) {
    lists {
      entries {
        media {
         	idMal
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

def getMalIds(date: int):
    variables['date'] = date
    response = requests.post(aniListUrl, json={'query': query, 'variables': variables})
    
    if response.status_code == 429:
        raise Exception("AniList API rate limit surpassed. Please try again later.")

    lists = response.json()["data"]["MediaListCollection"]["lists"]

    malIds = []

    for list in lists:
        for entry in list["entries"]:
            malIds.append(entry["media"]["idMal"])

    return [*set(malIds)]

