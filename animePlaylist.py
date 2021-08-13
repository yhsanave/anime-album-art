import json
import requests
import secrets
import anilist
from time import sleep
from sys import stdout
from client import CLIENT_ID, CLIENT_SECRET

# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorise your application by clicking here: {url}\n')


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the requests contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        })
    
    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")

def getAnimeById(id: int, access_token: str):
    url = f'https://api.myanimelist.net/v2/anime/{id}'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        }, params= {
            ('fields', 'title,opening_themes,ending_themes')
        })

    response.raise_for_status()
    anime = response.json()
    response.close()

    return anime

def makeList(malIds, token: str):
    print(f"{len(malIds)} anime to collect. Lowest ID: {malIds[-1:]}")
    animelist = []

    for id in malIds:
        sleep(.5)
        stdout.write(f"\rGetting anime from MAL with ID: {id}")
        stdout.flush()
        animelist.append(getAnimeById(id, token))

    return animelist

def sortFunc(anime):
    return anime["title"]

def writeToFile(animelist):
    with open("songlist.md", "w", encoding="utf-8") as file:
        file.write("# Anime Playist\n\n")
        
        for anime in animelist:
            file.write(f'## {anime["title"]}\n\n')

            if 'opening_themes' in anime:
                file.write("### Openings\n\n")
                for opening in anime["opening_themes"]:
                    file.write(f"{opening['text']}\n\n")

            if 'ending_themes' in anime:
                file.write("### Endings\n\n")
                for ending in anime["ending_themes"]:
                    file.write(f"{ending['text']}\n\n")

            file.write("---\n\n")

if __name__ == '__main__':
    if CLIENT_ID == "YOUR_CLIENT_ID" or CLIENT_SECRET == "YOUR_CLIENT_SECRET":
        print("You must register a MAL application and save the client ID and secret in client.py!")
        print("Follow step 0 here: https://myanimelist.net/blog.php?eid=835707")
        exit()

    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorisation_url(code_challenge)

    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    token = generate_new_token(authorisation_code, code_verifier)

    animelist = makeList(anilist.getMalIds(), token['access_token'])
    animelist.sort(key=sortFunc)

    writeToFile(animelist)

