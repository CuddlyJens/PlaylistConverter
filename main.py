from urllib.parse import urlparse
import importlib
from spotify import create_new_spotify_playlist
from youtube import create_new_youtube_playlist


def detect_service(playlist_url):
    parsed_url = urlparse(playlist_url)
    if "spotify.com" in parsed_url.netloc:
        return "spotify"
    elif "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
        return "youtube"
    else:
        return None


def main():
    playlist_url = input("Enter the playlist URL: ")

    service = detect_service(playlist_url)

    if service == "spotify" or service == "youtube":
        song_table = []
        if service == "spotify":
            spotify_script = importlib.import_module("spotify")
            song_table = spotify_script.get_playlist_items(playlist_url)
        elif service == "youtube":
            youtube_script = importlib.import_module("youtube")
            song_table = youtube_script.get_playlist_items(playlist_url)

        service_choice = input(
            "Would you like to create a YouTube playlist or a Spotify playlist? (youtube/spotify/exit): ")

        if service_choice.lower() == "exit":
            return
        elif service_choice.lower() not in ["youtube", "spotify"]:
            print("Invalid input. Please choose 'youtube', 'spotify', or 'exit'.")
            return

        if service_choice.lower() == "youtube":
            playlist_name = input("Enter the name of the new YouTube playlist: ")
            create_new_youtube_playlist(playlist_name, song_table)
        elif service_choice.lower() == "spotify":
            playlist_name = input("Enter the name of the new Spotify playlist: ")
            create_new_spotify_playlist(playlist_name, song_table)
    else:
        print("Unknown playlist URL or unsupported service.")


if __name__ == "__main__":
    main()
