import json
import math
import random
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
        pressure = {
            "value": np.cos(time.time()),
            "unit": "C",
            "timestamp": time.time() * 1000,
        }
        o2 = {
            "value": math.tan(time.time()),
            "unit": "C",
            "timestamp": time.time() * 1000,
        }

        if random.randint(1, 20) % 2 == 0:
            client.send(destination="/app/temperature", body=json.dumps(temperature))

        if random.randint(1, 30) % 2 == 0:
            client.send(destination="/app/pressure", body=json.dumps(pressure))

        if random.randint(1, 30) % 2 == 0:
            client.send(destination="/app/o2", body=json.dumps(o2))

        sleep(1)


if __name__ == "__main__":
    main()
