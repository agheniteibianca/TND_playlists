from googleapiclient.discovery import build
import json
import youtube_dl
import requests
import re 
"""
#requirements
pip install youtube-dl
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

class CreatePlaylist:

    

    def __init__(self):
        #get api key from Google Developers Console  https://console.developers.google.com/
        self.api_key = 'AIzaSyCFdYWIMgGl4r2-xQZ4MdO6uqR5RkdbjmQ'
        self.youtube=build('youtube', 'v3', developerKey=self.api_key)

        #get token from https://developer.spotify.com/console/get-recommendations/ (scroll all the way to the bottom and click on the ‘Get Token’ button)
        self.spotify_token = 'BQAXQTUFC7vpu2y_7jhkUPn_7wYJFs7tNvBCdirHyLigjpXU5UnE65o4l6y-mlxDSps_H_EWvECL2xi0t7I7dwb_YTA0BmHK0EuIPEeR4BU7V3CaRPJO64vWUvabJbgeCweKR8-La4CgLYJyKX1oNLEoWXGJYJBnW2NQkz2LXdhZK0LbpqBO8P4VtDqDX8GNE1z9EDKQKm7pqi_iF7jwv3lakg_cL8FyGIcL7bV-0G9EtUYRCvU8vd4kp1BRlWdbrNdP8l-m93a1RFl-qVX5LHFdiB4s0GE-7kh3zWB-'

        #self.get_description()
        #self.get_song_data()
        print (self.create_playlist("bilu", "not good"))
        self.add_song_to_playlist()
        #self.get_song_data()

    """
    def get_playlists(self):
        request = self.youtube.channels().list(
            part='statistics',
            forUsername='theneedledrop'
        )
        response = request.execute()
        print(response)
    """

    #melon channel id: UCt7fwAhXDy3oNFTAzF2o8Pw 
    #weekly roundup playlist id: PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c
    
    def parse_urls(self):
        myString = self.get_description()
        url = re.search("(?P<url>https?://www.youtube.com/[^\s]+)", myString).group("url")
        return url

    #extracts all the descriptions of every video in given playlist
    def get_description(self):
        pl_request = self.youtube.playlistItems().list(
            part= 'snippet',
            playlistId='PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c'
        )
        pl_response = pl_request.execute()
    

        item = pl_response['items'][1]
        description = item['snippet']['description']
        print(description)
        return description

    
    #gets song name and artist from given url
    def get_song_data(self):
        url = self.parse_urls()
        video = youtube_dl.YoutubeDL({}).extract_info(url, download=False)
        song_name = video["track"]
        artist = video["artist"]
        print(song_name, "by", artist)
    

    #create an empty playlist
    def create_playlist(self,title,description):

        request_body = json.dumps({
            "name": title,
            "description": description,
            "public": True
        })
        
        query_body = "https://api.spotify.com/v1/users/22qxhpskugtktr5sxkrxhbhsq/playlists"
        headers_body = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.post(query_body, data=request_body, headers=headers_body)
        response_json = response.json()
        #print(response_json)
        return response_json['id']


    #add song to playlsit by uri
    def add_song_to_playlist(self):
        #song uri: 7oDFvnqXkXuiZa1sACXobj
        #playlist uri: 4vtOe4IJOxkBOKTW28bVXf

        track_uris = ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M"]
        request_data = json.dumps(track_uris)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format('4vtOe4IJOxkBOKTW28bVXf')

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format('BQAXQTUFC7vpu2y_7jhkUPn_7wYJFs7tNvBCdirHyLigjpXU5UnE65o4l6y-mlxDSps_H_EWvECL2xi0t7I7dwb_YTA0BmHK0EuIPEeR4BU7V3CaRPJO64vWUvabJbgeCweKR8-La4CgLYJyKX1oNLEoWXGJYJBnW2NQkz2LXdhZK0LbpqBO8P4VtDqDX8GNE1z9EDKQKm7pqi_iF7jwv3lakg_cL8FyGIcL7bV-0G9EtUYRCvU8vd4kp1BRlWdbrNdP8l-m93a1RFl-qVX5LHFdiB4s0GE-7kh3zWB-')
            }
        )
        print(query)
        print(response)




if __name__ == '__main__':
    CreatePlaylist()
