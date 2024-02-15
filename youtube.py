from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
credentials_file = os.getenv('CREDENTIALS_FILE')

scopes = ['https://www.googleapis.com/auth/youtube']

flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
credentials = flow.run_local_server()

youtube = build('youtube', 'v3', developerKey=api_key, credentials=credentials)

search_api_keys_str = os.getenv('SEARCH_API_KEYS')
search_api_keys = search_api_keys_str.split(',')
max_retries = 5


def exponential_backoff(retries):
    delay = 2**retries
    time.sleep(delay)


def generate_keywords(song_name, artist):
    words = re.findall(r'\w+', song_name.lower()) + re.findall(r'\w+', artist.lower())

    common_words = ['the', 'and', 'feat', 'ft', 'featuring', 'with']
    keywords = [word for word in words if word not in common_words]

    return keywords if keywords else []


def get_playlist_items(playlist_url):
    playlist_id = parse_qs(urlparse(playlist_url).query)['list'][0]

    try:
        song_table = []
        next_page_token = None

        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                snippet = item['snippet']
                video_id = snippet['resourceId']['videoId']
                song_name = snippet['title']
                artist = snippet.get('videoOwnerChannelTitle', 'Unknown')
                video_details = youtube.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                if video_details['items'] and video_details['items'][0]['snippet']['title'] == song_name:
                    keywords = generate_keywords(song_name, artist)
                    song_table.append({
                        'song_name': song_name,
                        'artist': artist,
                        'keywords': keywords
                    })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return song_table

    except HttpError as e:
        print("An error occurred while accessing the YouTube API:", e)
        return []


def search_video_on_youtube(song_name, artist):
    random.shuffle(search_api_keys)

    for api_key in search_api_keys:
        retries = 0
        while retries < max_retries:
            try:
                youtube_search = build('youtube', 'v3', developerKey=api_key)
                query = f"{song_name} {artist}"
                request = youtube_search.search().list(
                    part="snippet",
                    q=query,
                    type="video",
                    maxResults=5
                )
                response = request.execute()

                if 'items' in response:
                    videos = response['items']
                    if videos:
                        video_id = videos[0]['id']['videoId']
                        return video_id

            except HttpError as e:
                error_code = e.resp.status
                if error_code == 403:
                    break
                elif error_code == 409:
                    exponential_backoff(retries)
                    retries += 1
                else:
                    print("An error occurred while searching for the video on YouTube:", e)
                    retries += 1

    return None


def create_new_youtube_playlist(playlist_name, song_table):
    try:
        # Erstellen Sie eine neue Playlist
        request = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": playlist_name,
                    "description": "My new playlist created with PlaylistConverter"
                }
            }
        )
        response = request.execute()

        playlist_id = response['id']

        # Fügen Sie die Songs zur Playlist hinzu
        for song_info in song_table:
            video_id = search_video_on_youtube(song_info['song_name'], song_info['artist'])
            if video_id:
                request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                )
                request.execute()
                print(f"Video '{song_info['song_name']}' by '{song_info['artist']}' added to the YouTube playlist.")

        print(f"The new YouTube playlist '{playlist_name}' was created successfully.")
        print()

    except HttpError as e:
        print("An error occurred while accessing the YouTube API:", e)
    except Exception as e:
        print("Error creating playlist:", e)
