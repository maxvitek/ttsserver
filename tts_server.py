import os
import logging
import json

import soco
from speech import Speech  # this is taken from SoCo github #99

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap


TTS_SERVER_PORT = int(os.getenv('TTS_SERVER_PORT', default=os.getenv(
    'PORT0', default=5000)))

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def enter_phrase():
    zones = {zone.player_name: zone for zone in soco.discover()}
    zone_names = zones.keys()
    return render_template('index.html', zones=zone_names)

@app.route('/phrase', methods=['POST'])
def tts_phrase():
    zones = {zone.player_name: zone for zone in soco.discover()}
    data = request.get_data()
    if isinstance(data, str):  # handle jquery nonsense
        data = json.loads(data)
    zone = zones[data['zone']]
    text = data['text']
    speech = Speech(zone)
    speech.say(text)
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=TTS_SERVER_PORT)
