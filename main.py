import json
import time
from time import sleep

import numpy as np

from stomp_ws.client import Client


def on_message(message):
    print(message)


def print_frame(frame):
    print(json.loads(frame.body))


def main():
    # open transport
    client = Client("wss://api.sensorguard.systems/api/looping")

    # connect to the endpoint
    client.connect()

    # subscribe channel
    client.subscribe("/topic/temperature", callback=print_frame)

    while True:
        temperature = {
            "value": np.sin(time.time())*2,
            "unit": "C",
            "timestamp": time.time() * 1000,
        }
        client.send(destination="/app/temperature", body=json.dumps(temperature))
        client.send(destination="/app/pressure", body=json.dumps(temperature))
        client.send(destination="/app/o2", body=json.dumps(temperature))
        sleep(1)


if __name__ == "__main__":
    main()
