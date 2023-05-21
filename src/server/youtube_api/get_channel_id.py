import json
import requests 
from flask import jsonify
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
            return f'{uri_style}{uri_identifier}'

    # raise RegexMatchError(
    #     caller="channel_name", pattern="patterns"
    # )

def get_channel_id(channel_url, API_KEY=None):
    channel_name = extract_channel_name(channel_url)
    if channel_name.startswith('@'):
        channel_name = channel_name[1:]
        channel_url = f'https://www.youtube.com/c/{channel_name}'
    channel = Channel(channel_url)
    return channel.channel_id
    print(channel.channel_id)
    payload = {
        'part': 'snippet', 
        'forUsername': channel_name,
        'key': API_KEY
    }
    r = json.loads(requests.get('https://youtube.googleapis.com/youtube/v3/channels', params=payload).content)
    pprint(r)
    print(r['items'][0]['id'])

if __name__ == "__main__":
    API_KEY = 'AIzaSyBHOx6RgnF3QyQqzt094BTijDo7j2SzoYA'
    channel_url = 'https://www.youtube.com/@Vox'
    # channel_url = 'https://www.youtube.com/channel/UCW99xIi8vLoP9jTkXkVt2eA'
    print(get_channel_id(channel_url, API_KEY))
