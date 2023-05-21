import json
import requests 
from pprint import pprint
from get_channel_id import get_channel_id

def get_channel_playlists(channel_id, API_KEY):
    payload = {
        'channelId': channel_id,
        'maxResults': '50',
        'key': API_KEY
    }
    r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/playlists', params=payload).content)
    playlist_ids = list(map(lambda item: item['id'], r['items']))
    total_results = r['pageInfo']['totalResults']
    results_per_page = r['pageInfo']['resultsPerPage']
    if total_results > results_per_page:
        nextPageToken = r['nextPageToken']
        while nextPageToken:
            payload['pageToken'] = nextPageToken
            r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/playlists', params=payload).content)
            playlist_ids += list(map(lambda item: item['id'], r['items']))
            nextPageToken = r['nextPageToken']

    return playlist_ids

def get_playlist_items(playlist_id, API_KEY):
    payload = {
        'part': 'contentDetails', 
        'maxResults': '50',
        'playlistId': playlist_id,
        'key': API_KEY
    }
    r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems', params=payload).content)
    video_ids = list(map(lambda item: item['contentDetails']['videoId'], r['items']))
    total_results = r['pageInfo']['totalResults']
    results_per_page = r['pageInfo']['resultsPerPage']
    if total_results > results_per_page:
        nextPageToken = r['nextPageToken']
        while nextPageToken:
            payload['pageToken'] = nextPageToken
            r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems', params=payload).content)
            video_ids += list(map(lambda item: item['contentDetails']['videoId'], r['items']))
            if 'nextPageToken' not in r: break
            nextPageToken = r['nextPageToken']
    return video_ids

def get_video_data(video_ids, API_KEY):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    video_id_chunks = chunks(video_ids, 50)
    durations = []
    viewCounts = []
    for chunk_video_ids in video_id_chunks:
        payload = {
            'part': 'contentDetails,statistics', 
            'maxResults': '50',
            'id': ','.join(chunk_video_ids),
            'key': API_KEY
        }
        r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/videos', params=payload).content)
        chunk_durations = list(map(lambda item: item['contentDetails']['duration'], r['items']))
        chunk_viewCounts = list(map(lambda item: item['statistics']['viewCount'], r['items']))
        durations += chunk_durations
        viewCounts += chunk_viewCounts
    return durations, viewCounts

def get_channel_video_data(channel_url, API_KEY):
    channel_id = get_channel_id(channel_url)
    print(channel_id)
    playlist_ids = get_channel_playlists(channel_id, API_KEY)
    print("playlists: ", len(playlist_ids))
    video_ids = []
    for playlist_id in playlist_ids:
        video_ids += get_playlist_items(playlist_id, API_KEY)
    print("total videos: ", len(video_ids))
    durations, viewCounts = get_video_data(video_ids, API_KEY)
    print(len(durations), len(viewCounts))
    return durations, viewCounts


def calculate_carbon(channel_url, API_KEY):
    """
        returns carbon of a channel in kg
    """
    def toHours(PT):
        print(PT, PT.split('M')[0].split('T')[1])
        try:
            minutes = int(PT.split('M')[0].split('T')[1])
            return minutes/60
        except:
            return 0

    durations, viewCounts = get_channel_video_data(channel_url, API_KEY)
    carbon = 0
    for i in range(len(durations)):
        duration = toHours(durations[i]) # duration in hours
        viewCount = int(viewCounts[i])
        carbon += duration * viewCount * 36 / 1000
    return carbon

if __name__ == "__main__":
    API_KEY = 'AIzaSyBHOx6RgnF3QyQqzt094BTijDo7j2SzoYA'
    channel_url = 'https://www.youtube.com/@Fireship'
    carbon = calculate_carbon(channel_url, API_KEY)
    print(carbon)
