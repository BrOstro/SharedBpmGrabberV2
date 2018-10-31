Grabs a given playlist from a given user and finds each song's BPM and danceability rating and stores it in a database.

Requirements:
1) Python 3
2) Spotipy (https://github.com/plamere/spotipy). You can install this by running "pip install -r requirements.txt"
3) A Spotify client ID and client secret. You can get both of these from https://developer.spotify.com/dashboard/applications and clicking "Create a Client ID" after logging in with your Spotify account.  

How to Use:  
1) Insert your client ID and client secret into the SharedBpm.py file on lines 8 and 9.
2) Run the script with the following format: "./SharedBpm.py \<PlaylistURL\>".  
	You can get a playlist URL by right clicking the URL, hovering over the "Share" menu option, and clicking "Copy Playlist Link". Please note that the playlist must be marked as PUBLIC.
3) After the script is finished, all of the data will be saved in a file called "songs.db". You can view the contents in a couple of ways:  
	My preferred method is a desktop program called "SQLite Browser". You can get it here: https://sqlitebrowser.org/  
	Otherwise, you can view the contents online by Googling "Online database viewer" and trying out different results by uploading the songs.db file.
