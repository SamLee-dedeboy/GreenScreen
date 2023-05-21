import json
import requests 
from pprint import pprint
from pytube import Channel
import re

def extract_channel_name(url: str) -> str:
    """Extract the ``channel_name`` or ``channel_id`` from a YouTube url.

    This function supports the following patterns:

    - :samp:`https://youtube.com/c/{channel_name}/*`
    - :samp:`https://youtube.com/channel/{channel_id}/*
    - :samp:`https://youtube.com/u/{channel_name}/*`
    - :samp:`https://youtube.com/user/{channel_id}/*
    - :samp:`https://youtube.com/@{channel_name}/*`

    :param str url:
        A YouTube url containing a channel name.
    :rtype: str
    :returns:
        YouTube channel name.
    """
    patterns = [
        r"(?:\/(c)\/([%\d\w_\-]+)(\/.*)?)",
        r"(?:\/(channel)\/([%\w\d_\-]+)(\/.*)?)",
        r"(?:\/(u)\/([%\d\w_\-]+)(\/.*)?)",
        r"(?:\/(user)\/([%\w\d_\-]+)(\/.*)?)",
        r"(?:(@[%\w\d_-]+)(.*)?)"
    ]
    for pattern in patterns:
        regex = re.compile(pattern)
        function_match = regex.search(url)
        if function_match:
            # logger.debug("finished regex search, matched: %s", pattern)
            uri_style = function_match.group(1)
            uri_identifier = function_match.group(2)
            return uri_style, uri_identifier
            # return f'{uri_style}{uri_identifier}'

    # raise RegexMatchError(
    #     caller="channel_name", pattern="patterns"
    # )

def get_channel_id(channel_url, API_KEY=None):
    print(channel_url)
    uri_style, channel_name = extract_channel_name(channel_url)
    print(uri_style, channel_name)
    if uri_style == 'channel':
        return channel_name
    elif uri_style.startswith('@'):
        channel_name = uri_style[1:]
    try:
        channel_url = f'https://www.youtube.com/c/{channel_name}'
        channel = Channel(channel_url)
        print(channel_url)
        print(channel.channel_id)
        return channel.channel_id
    except:
        payload = {
            'part': 'snippet', 
            'forUsername': channel_name,
            'key': API_KEY
        }
        r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/channels', params=payload).content)
        pprint(r)
        print(r['items'][0]['id'])
        return r['items'][0]['id']


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
            if 'nextPageToken' not in r: break
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
        try:
            chunk_viewCounts = list(map(lambda item: item['statistics']['viewCount'], r['items']))
        except KeyError:
            # sometimes viewCount is not included in statistics
            chunk_viewCounts = []
        durations += chunk_durations
        viewCounts += chunk_viewCounts
    return durations, viewCounts

def get_channel_video_data(channel_url, API_KEY):
    channel_id = get_channel_id(channel_url, API_KEY)
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
    for i in range(min(len(durations), len(viewCounts))):
        duration = toHours(durations[i]) # duration in hours
        viewCount = int(viewCounts[i])
        carbon += duration * viewCount * 36 / 1000
    return carbon

if __name__ == "__main__":
    API_KEY = 'AIzaSyBHOx6RgnF3QyQqzt094BTijDo7j2SzoYA'
    # channel_url = 'https://www.youtube.com/channel/UCOmHUn--16B90oW2L6FRR3A'
    channel_url = 'https://www.youtube.com/@Vox'
    carbon = calculate_carbon(channel_url, API_KEY)
    print(carbon)
