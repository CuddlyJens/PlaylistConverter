import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-read-private playlist-modify-private'))


def generate_keywords(song_name, artist):
    words = re.findall(r'\w+', song_name.lower()) + re.findall(r'\w+', artist.lower())
    common_words = ['the', 'and', 'feat', 'ft', 'featuring', 'with']
    keywords = [word for word in words if word not in common_words]

    return keywords if keywords else []


def get_playlist_items(playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    if not playlist_id:
        print("Error: Unable to extract the playlist ID from the URL.")
        return []

    try:
        offset = 0
        limit = 100

        while True:
            results = sp.playlist_items(playlist_id, offset=offset, limit=limit)
            tracks = results.get('items', [])
            total_tracks = results.get('total', 0)

            song_table = []
            for item in tracks:
                track = item.get('track')
                if track:
                    artist = ", ".join([artist['name'] for artist in track.get('artists', [])])
                    song_name = track.get('name')
                    keywords = generate_keywords(song_name, artist)
                    song_table.append({
                        'song_name': song_name,
                        'artist': artist,
                        'keywords': keywords
                    })
            print(f"Es wurden {total_tracks} Songs in der Spotify-Playlist gefunden.")
            print()

            return song_table

    except spotipy.exceptions.SpotifyException as e:
        print("Error getting playlist. Make sure the URL is correct and the playlist is publicly accessible.", e)


def create_new_spotify_playlist(playlist_name, song_table):
    try:
        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        playlist_id = playlist['id']

        for song_info in song_table:
            title, artist, keywords = song_info['song_name'], song_info['artist'], song_info['keywords']

            query = f"{title} {artist} {' '.join(keywords)}"

            results = sp.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.playlist_add_items(playlist_id, [track_uri])

                print(f"Song '{title}' by '{artist}' added to the Spotify playlist.")

        print(f"The new Spotify playlist '{playlist_name}' was created successfully.")
        print()

    except spotipy.exceptions.SpotifyException as e:
        print(
            "Error creating playlist. Make sure you have the 'playlist-modify-private' scope and the songs are valid.",
            e)
    except Exception as e:
        print("Error searching for track:", e)
