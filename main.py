from time import sleep

import json
import time

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

    val = 0.0
    toggle = 1

    while True:
        temperature = {
            "value": "%.2f" % val,
            "unit": "C",
            "timestamp": time.time(),
        }
        client.send(destination="/app/temperature", body=json.dumps(temperature))
        val = val + 0.01 * toggle
        if val <= -1 or val >= 1:
            toggle = toggle * -1
        sleep(0.1)


if __name__ == "__main__":
    main()
