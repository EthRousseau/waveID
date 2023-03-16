import os
from time import sleep

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

try:
    import config
except:
    with open("config.py", 'w') as config_file:
        config_file.write("SPOTIPY_CLIENT_ID = 'CLIENT_ID'\nSPOTIPY_CLIENT_SECRET = 'CLIENT_SECRET'")
    print("Please identify your client in the config.py file")
    exit(0)


class waveID():
    def __init__(self):
        os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
        os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
        os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8085'
        self.spotifyOAuth = self.getOAuthObject()
        self.currentState = {}

    def getOAuthObject(self):
        scope = "user-read-playback-state"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        return sp

    def getState(self):
        res = self.spotifyOAuth.current_playback()
        try:
            artists = [x['name'] for x in res['item']['album']['artists']]
            return res['is_playing'], res['item']['name'], artists, res['item']['album']['images'][0]['url']
        except:
            return False, None, None, None

    def updateState(self):
        isPlaying, songTitle, artistName, albumArtUrl = wave.getState()
        if self.currentState.get('isPlaying') != isPlaying and isPlaying != None:
            wave.setPlay(isPlaying)
        if songTitle and songTitle != self.currentState.get('songTitle'):
            self.currentState['songTitle'] = songTitle
            wave.writeTitle(songTitle)
        if artistName and artistName != self.currentState.get('artistName'):
            self.currentState['artistName'] = artistName
            wave.writeArtist(artistName)
        if albumArtUrl and albumArtUrl != self.currentState.get('albumArtUrl'):
            self.currentState['albumArtUrl'] = albumArtUrl
            wave.writeArtwork(albumArtUrl)

    def writeTitle(self, title):
        with open("title.txt", 'w') as title_file:
            if '(' in title:
                title = title[:title.find('(')]
            if len(title) >= 23:
                title = f"{title[:20]}..."
            print(f"Changing title to {title}")
            title_file.write(title)

    def writeArtist(self, artists):
        artist_string = ""
        for artist in artists:
            artist_string += f"{artist}, "
        artist_string = artist_string[:-2]
        if len(artist_string) >= 40:
            artist_string = f"{artist_string[:37]}..."
        with open("artist.txt", 'w') as artist_file:
            print(f"Changing artist to {artist_string}")
            artist_file.write(artist_string)

    def setPlay(self, play=False):
        with open("playbutton.png", "wb") as main_file:
            if play == True:
                print("Making Play")
                self.currentState['isPlaying'] = True
                main_file.write(open("Play.png", "rb").read())
            else:
                print("Making Paused")
                self.currentState['isPlaying'] = False
                main_file.write(open("Pause.png", "rb").read())

    def writeArtwork(self, url):
        imageData = requests.get(url).content
        print("Writing artwork image file")
        with open("coverart.jpg", "wb") as coverart:
            coverart.write(imageData)


wave = waveID()
while True:
    wave.updateState()
    sleep(1)
