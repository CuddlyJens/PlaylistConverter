# PlaylistConverter

## First of all, change the .env File with your secrets
Go to https://developer.spotify.com then log in and go to your Dashboard
Create a new App, insert your App name, App description and Redirect URIs (i recomend http://localhost:3001 to not interfere with other local apps)

Go to Settings and ther you find your Client ID and your Client Secret

Place it like this in your .env file:
```
SPOTIPY_CLIENT_ID=1234567890
SPOTIPY_CLIENT_SECRET=asdfqwety5468jkluiop
SPOTIPY_REDIRECT_URI=http://localhost:3001
```

