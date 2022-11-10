from time import sleep

import json
import time
import requests

import numpy as np
from stomp_ws.client import Client


def on_message(message):
    print(message)


def print_frame(frame):
    print(json.loads(frame.body))

def getToken():
    body = {
        'client_id': 'umweltrechner-backend',
        'username': 'cem',
        'password': 'cem',
        'grant_type': 'password',
        'client_secret': 'mEPtfyx0vf1RQsgFMyHMIK7i0EYNtOLa',
    }
    head = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = requests.post('http://localhost:8084/auth/realms/Umweltrechner-keycloak/protocol/openid-connect/token', headers=head, data=body)
    token = req.json()["access_token"]
    print(token)

def main():

    # open transport
    client = Client("ws://127.0.0.1:8230/api/looping?token={}".format(getToken()))

    # connect to the endpoint
    client.connect()

    # subscribe channel
    client.subscribe("/topic/temperature", callback=print_frame)

    while True:
        temperature = {
            "value": np.sin(time.time()),
            "unit": "C",
            "timestamp": time.time(),
        }
        client.send(destination="/app/temperature", body=json.dumps(temperature))
        sleep(0.1)


if __name__ == "__main__":
    main()
