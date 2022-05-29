import requests
import base64 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import random

class Song:
    def __init__(self, title, artist, rating1, rating2, album):
        self.title = title
        self.artist = artist
        self.rating1 = rating1
        self.rating2 = rating2
        self.album =album
    def __str__(self):
        return f"--NextSong--\n Name: {self.title}\n Artist: {self.artist}\n Rating: {self.rating1}\n\t {self.rating2}\n Album: {self.album}\n"

    def __repr__(self):
        return self.__str__()

def nextRandom():
    playlistID = "37i9dQZF1DXcBWIGoYBM5M?si=9db18609dade4867"
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
    clientID = "5506e77102234c37ae00119d3d14bebe"
    clientSecret = "bd034b7c09bc45d5beeda3afe2759542"  
    token = getAccessToken(clientID,clientSecret)    
    GetPlaylistTracks(token, playlistEndPoint)
    tracklistjson = GetPlaylistTracks(token,playlistEndPoint)
    tracklist = []
   
    for track in tracklistjson['tracks']['items']:
        tracklist.append(Song(
            track['track']['name'].replace("(","").replace(")",""),
            track['track']['artists'][0]['name'], 
            "Popularity: "+str(track['track']['popularity']),
            "World market: "+str(len(track['track']['available_markets'])),
            track['track']['album']['name']
            ))
    return random.choice(tracklist)
    
def nextHighestTrack():
    
    website = "https://musicboard.app/tracks?view=detailed&order_by=week&genre=132"
    path = '/Users/mihaelafetcu/Downloads/chromedriver'
    driver = webdriver.Chrome(service=Service(path))
    driver.get(website)
    sleep(3)
    first_track= driver.find_element_by_css_selector('a.link-overlay')
    title= driver.find_element_by_css_selector('h6').get_attribute('innerText')
    rating1= driver.find_element_by_css_selector('p.black').get_attribute('innerText')
    driver.get(first_track.get_attribute('href'))
    sleep(3)
    album = driver.find_element_by_css_selector('h1').get_attribute('innerText')
    artist = driver.find_element_by_css_selector('.flex-row.margin-top-16>:nth-child(2) p').get_attribute('innerText')
    rating2 = driver.find_elements_by_css_selector('h3.black')[1].get_attribute('innerText')
    driver.quit()
    tracklist = []
    tracklist.append(Song(title,artist, "Popularity: "+rating1,"Album rating: "+rating2,album))
    return tracklist[0]
    
def nextKeyWord(keyword):
    playlistEndPoint = f"https://api.spotify.com/v1/search?include_external=audio&q=name:{keyword}%20genre:pop&type=track"
    clientID = "5506e77102234c37ae00119d3d14bebe"
    clientSecret = "bd034b7c09bc45d5beeda3afe2759542"  
    token = getAccessToken(clientID,clientSecret)    
    GetPlaylistTracks(token,playlistEndPoint)
    tracklistjson = GetPlaylistTracks(token,playlistEndPoint)
    tracklist = []

    for track in tracklistjson['tracks']['items']:
        tracklist.append(Song(
                        track['name'],  
                        track['artists'][0]['name'],  
                        "Popularity: "+str(track['popularity']),
                        "World market: "+str(len(track['album']['available_markets'])),
                    track['album']['name'] 
         ))
    return tracklist[0]
  

def getAccessToken(clientID,clientSecret):
        authURL = "https://accounts.spotify.com/api/token"
        authHeader ={}
        authData = {}
        message = f"{clientID}:{clientSecret}"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        authHeader['Authorization'] = "Basic " + base64_message
        authData['grant_type'] = "client_credentials"
        res = requests.post(authURL, headers=authHeader, data=authData)
        responseObject = res.json()
        accessToken = responseObject['access_token']
        return accessToken       
    
def GetPlaylistTracks(token,playlistEndPoint):
        getHeader = {
            "Authorization": "Bearer " + token
        }
        res = requests.get(playlistEndPoint,headers=getHeader)
        playlistObject = res.json()
        return playlistObject
    

    

       