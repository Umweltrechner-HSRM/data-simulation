from time import sleep

import json
import time

import numpy as np
from stomp_ws.client import Client


def on_message(message):
    print(message)


def print_frame(frame):
    print(json.loads(frame.body))


def main():
    # open transport
    client = Client("ws://127.0.0.1:8230/api/looping")

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
