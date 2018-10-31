import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import math
import re
import sys

client_id = ''  # Your client ID here
client_secret = ''  # Your client secret here

conn = sqlite3.connect('songs.db')  # Connect to database, or create it if it doesn't exist
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS songs (`song` VARCHAR(255),`bpm` FLOAT(10),`danceRating` FLOAT(10));')  # Create a new table if it doesn't yet exist in the database
c.execute('DELETE FROM songs;')  # Delete all existing data in the table
conn.commit()

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

url = str(sys.argv[1])

user = re.search('/user/(.*)/playlist/', url).group(1)  # Extract username ID from playlist URL
playlist = re.search('/playlist/(.*)\?si=', url).group(1)  # Extract playlist ID from playlist URL

if url is None:
    print("You must specify a playlist url. Usage is ./SharedBpm.py <PlaylistUrl>")
    exit()


def get_iterations(x):  # Because Spotify only return 100 tracks per API call, we must break it up into multiple API calls
    return int(math.ceil(x / 100.0))


results = sp.user_playlist(user, playlist, fields='tracks(total)')  # Gets the number of tracks in playlist
count = results['tracks']['total']  # Gets the number of tracks in playlist
iterations = get_iterations(count)  # Number of API calls we'll have to make due to each call only returning 100 tracks
for i in range(0, iterations):
    tracks = sp.user_playlist_tracks(user, playlist, fields='items(track)', offset= i*100)  # Get all the tracks in the given playlist with an offset
    tracks = tracks['items'];
    trackFeatures = []
    trackNames = []
    for track in tracks:  # Add necessary track information to two arrays for later use
        track = track['track']
        trackFeatures.append(track['id'])
        trackNames.append(track['artists'][0]['name'] + " - " + track['name'])
    trackFeatures = sp.audio_features(trackFeatures)  # Store all information  (that contains BPM and danceability)
    for j in range(0, len(trackNames)):  # For each track in the two arrays, insert the data into the database
        name = trackNames[j]
        bpm = trackFeatures[j]['tempo']
        dance = trackFeatures[j]['danceability']
        c.execute('INSERT OR IGNORE INTO songs (song, bpm, danceRating) VALUES (?, ?, ?)', (name, bpm, dance))

conn.commit()  # Commit all SQL changes to the database file
conn.close()  # Close the SQL connection
