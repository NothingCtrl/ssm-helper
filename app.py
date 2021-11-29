from flask import Flask, jsonify, request
import os
import subprocess, platform
from dotenv import load_dotenv
import requests
import json

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return "OK"


# noinspection PyBroadException
@app.route('/ping', methods=['POST'])
def ping_check():
    data = request.get_json()
    if 'server_host' in data:
        try:
            subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', data['server_host']), shell=True)
        except Exception:
            return jsonify({'status': False, 'message': "PING failed!"})
        return jsonify({'status': True})
    return jsonify({'status': False, 'message': 'Payload incorrect!'})


# noinspection PyBroadException
@app.route('/http', methods=['POST'])
def http_check():
    data = request.get_json()
    if data and 'server_host' in data:
        try:
            rp = requests.get(data['server_host'])
            return jsonify({'status': rp.status_code in (200, 201, 202)})
        except Exception:
            ...
        return jsonify({'status': False, 'message': 'HTTP request failed!'})
    return jsonify({'status': False, 'message': 'Payload incorrect!'})


# noinspection PyBroadException
@app.route('/beat')
def send_beat():
    beat_host = os.getenv('BEAT_URL', '')
    if not beat_host:
        return jsonify({'status': False, 'message': "BEAT_URL is not valid!"})
    client_name = os.getenv('BEAT_CLIENT_NAME', 'ssm_client_helper')
    client_version = os.getenv('BEAT_CLIENT_VERSION', '1.0.0')
    status = False
    try:
        print(json.dumps({
                "client_name": client_name,
                "client_version": client_version
            }))
        rp = requests.post(beat_host, data={
            "json_data": json.dumps({
                "client_name": client_name,
                "client_version": client_version
            })
        })
        status = rp.status_code == 200
    except Exception:
        ...
    return jsonify({'status': status})

if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("APP_PORT", "8080")), debug=(os.getenv('DEBUG') and os.getenv('DEBUG') in ('true', 'True', '1')))