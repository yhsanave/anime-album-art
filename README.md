# anime-playlist

A tool to help you manage your anime playlist

## Setup

0. You will need both an AniList and a MyAnimeList account. Only the AniList account needs to have your list, the MAL account is only used to generate an api key. 
You will also need [python](https://www.python.org/) and `requests` (`pip install requests`) in order to run the program.

1. Go to https://myanimelist.net/apiconfig (login if needed) and click `Create ID`

2. Choose `web` for your app type and fill in the other boxes with whatever you want, none of it matters except the type.

3. Click `Submit` then `Back to list` and `Edit` on the new client in the list

4. Copy the `Client ID` and `Client Secret` into their respective places in `client.py`, replacing the existing text. Be sure to put both of them in quotation marks.

5. Login to AniList and navigate to your profile. Press F12 to open DevTools, select the `Network` tab and refresh the page. 

6. Enter `graphql` in the filter bar in DevTools, click the second result, and open the `Response` tab. 

7. You should see your user id in the response data, copy that and replace the value of `userId` in `anilist.py` with it. Do not put this one in quotes.

8. Save both files, you are now ready to run the program.

## Usage

1. Open `animePlaylist.bat` and copy the link into your browser (hightlight it and press enter, ctrl+c will kill the program)

2. Click `Authorize` and you will be redirected to whatever page you put in the redirect url when you made the MAL client.

3. There will be a long authorization code in the address bar, copy everything after `code=`, paste it into the program (ctrl+v), and press enter.

4. Now just wait for it to finish getting the data from MAL. You can stop the program early by closing the window or pressing ctrl+c

5. Once the program finishes, it will save your song list to `songlist.md`

6. If you want the list as a `.csv`, run `parseMarkdown.py`
