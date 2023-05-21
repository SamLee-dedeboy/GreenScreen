from flask import Flask
from flask_cors import CORS
import json
from youtube_api.channel import calculate_carbon

app = Flask(__name__)
CORS(app)

API_KEY = open(r'youtube_api/credentials', 'r').read()
print(API_KEY)
@app.route("/channel/<channel_url>")
def get_channel_carbon(channel_url):
    return json.dumps({'carbon': calculate_carbon(channel_url, API_KEY)})

