import os
import subprocess
import logging
import yaml
import requests
import json

import soco
from speech import Speech  # this is taken from SoCo github #99

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

BIND_IP = os.getenv('TTSSONOS_BIND_IP', '0.0.0.0:5000')

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
    try:
        data = request.get_data()
        if isinstance(data, str):  # handle jquery nonsense
            data = json.loads(data)
        zone = zones[data['zone']]
        text = data['text']
        speech = Speech(zone)
        speech.say(text) 
        return 'success'
    except Exception as e:
        logger.exception(e, exc_info=True)


if __name__ == '__main__':
    host, port = BIND_IP.split(':')
    app.run(host=host, port=int(port))
