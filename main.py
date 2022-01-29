from pprint import pprint
from time import sleep
import requests
from win10toast import ToastNotifier

SPOTIFY_ACCESS_TOKEN = "BQASfgMcSQuVGxZ8P5jXfbALNGYcDjLx2TezRRhMb8aYgogBfBzuHm0_Y4dJLHmqFLjydQm7LK7-dqNZmeHGiMUtEGJBed6qiKpB6BHeXjj3CQJ-aX1WuJSFaNk5wmj4Sg3TfCeTS3p43VQOK-cjvX40OnYiXTYsuKzNakA"
SPOTIFY_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"


def get_current_track(access_token):
    response = requests.get(SPOTIFY_CURRENT_TRACK_URL,
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
    )

    #convert response into JSON format
    resp_json = response.json()

    #find and store necessary info from JSON response
    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']
    artists = resp_json['item']['artists']
    track_artists = ', '.join([artist['name'] for artist in artists]) #Creates comma separated list of artists
    track_link = resp_json['item']['external_urls']['spotify']

    curr_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": track_artists,
        "link": track_link,
    }

    return curr_track_info

def create_toast_notification():
    curr_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)

    toast_notification = ToastNotifier()
    toast_notification.show_toast(
    curr_track_info['name'], 
    curr_track_info['artists'], 
    duration=3
    )

curr_track_name = "TEST" #keeps track of currently playing track
def main():
    curr_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)

    pprint(curr_track_info, indent=4)

    global curr_track_name
    curr_track_name = curr_track_info['name']
    #print(curr_track_name)

    

if __name__ == '__main__':
    last_track_name = ""
    while True:
        main()
        print(curr_track_name)
        
        #send notification if track changes
        if last_track_name != curr_track_name:
            print("TRACK CHANGE")
            create_toast_notification()
            last_track_name = curr_track_name
        
        sleep(2)