# PlaylistConverter

## First of all, change the .env File with your secrets
Go to https://developer.spotify.com then log in and go to your Dashboard

Create a new App -> insert your App name, App description and Redirect URIs (i recomend http://localhost:3001 to not interfere with other local apps) -> Go to Settings and ther you find your Client ID and your Client Secret

Place it like this in your .env file:
```
SPOTIPY_CLIENT_ID=1234567890
SPOTIPY_CLIENT_SECRET=asdfqwety5468jkluiop
SPOTIPY_REDIRECT_URI=http://localhost:3001
```

Go to https://console.cloud.google.com/ to get your Google Secrets

Create a new Project -> Insert Projectname and Click "Create" -> Go to APIs and Services -> Select your Project -> Credentials -> + Create Credentials -> API-Key -> Wait a bit and then you get your API Key

OAuth consent screen -> if not configure set it to External -> Insert your App name and email -> Save and Continue and go forward to get back to dashbord -> back to Credentials -> + Create Credentials -> OAutch client ID -> Application type "Desktop app" -> Create

DOWNLOAD JSON FILE and rename it to "credentials_file.json" then place it to your Folder

Place the Google API-Key in your .env file like this for GOOGLE_API_KEY and SEARCH_API_KEYS:
```
GOOGLE_API_KEY=RdfkjieAduadkjfeNadfjieDadfjhueuafUadfjkeMasdfe
SEARCH_API_KEYS=RdfkjieAduadkjfeNadfjieDadfjhueuafUadfjkeMasdfe
```

## Reminder: each search, playlist creation and insert cost Queries where you have a value of 10k each day. If you need more, create a new project and API-Key and place it behind the SEARCH_API_KEYS 

For example:
```
SEARCH_API_KEYS=RdfkjieAduadkjfeNadfjieDadfjhueuafUadfjkeMasdfe,RdfkjieAduadkjfeNadfjieDadfjhueuafUadfjkeMasdfe
```
