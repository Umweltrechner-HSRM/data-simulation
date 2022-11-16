import signal
import sys
import os
import requests
import pprint 
import yaml
from threading import Thread
import time
import json
import random
from pathlib import Path
from datetime import datetime, timezone
import os


#Directory path ermitteln
buffer_path = str(os.path.join(os.path.dirname(__file__), '../buffer'))
config_path = str(os.path.join(os.path.dirname(__file__), '../config.yaml'))

#config einlesen
config = yaml.safe_load(open(config_path))

def get_station(query: str) -> str or None:
    #Doku https://aqicn.org/json-api/doc/
    response = requests.get(
        f"https://api.waqi.info/search/?token={config['aqicn_key']}&keyword={query}"
    )
    if (len(response.json()['data']) > 0):
        return response.json()['data'][0]['uid']
    return

def get_station_data(uid: str) -> dict or None:
    print(uid)
    response = requests.get(
        f"https://api.waqi.info/feed/@{uid}/?token={config['aqicn_key']}"
    )
    if response.json()['data'] == "Unknown station":
        return
    return response.json()['data']

def get_city_data(city_name: str) -> dict or None:
    #print(uid)
    response = requests.get(
        f"https://api.waqi.info/feed/{city_name}/?token={config['aqicn_key']}"
    )
    if response.json()['data'] == "Unknown station":
        return
    return response.json()['data']

def get_pm25(taktung, seed, city):
    #lungengängiger_feinstaub
    while True:
        data = get_city_data(city)
        print("lungengängiger_feinstaub data sent")
        with open(buffer_path+"/current_lungengängiger_feinstaub.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "lungengängiger_feinstaub": data['iaqi']['pm25']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_pm10(taktung, seed, city):
    #einatembarer_feinstaub
    while True:
        data = get_city_data(city)
        print("einatembarer_feinstaub data sent")
        with open(buffer_path+"/current_einatembarer_feinstaub.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "einatembarer_feinstaub": data['iaqi']['pm10']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_o3(taktung, seed, city):
    #Ozon
    while True:
        data = get_city_data(city)
        print("ozon data sent")
        with open(buffer_path+"/current_ozon.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "ozon": data['iaqi']['o3']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_no2(taktung, seed, city):
    #stickstoffdioxid
    while True:
        data = get_city_data(city)
        print("stickstoffdioxid data sent")
        with open(buffer_path+"/current_stickstoffdioxid.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "stickstoffdioxid": data['iaqi']['no2']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_so2(taktung, seed, city):
    #schwefeldioxid
    while True:
        data = get_city_data(city)
        print("Humidity data sent")
        with open(buffer_path+"/current_schwefeldioxid.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "schwefeldioxid": data['iaqi']['so2']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_co(taktung, seed, city):
    #Kohlenmonoxid
    while True:
        data = get_city_data(city)
        print("kohlenmonoxid data sent")
        with open(buffer_path+"/current_kohlenmonoxid.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "kohlenmonoxid": data['iaqi']['co']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_t(taktung, seed, city):
    #temperatur
    while True:
        data = get_city_data(city)
        print("temperature data sent")
        with open(buffer_path+"/current_temperature.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "temperature": data['iaqi']['t']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_p(taktung, seed, city):
    #pressure Luftdruck
    while True:
        data = get_city_data(city)
        print("pressure data sent")
        with open(buffer_path+"/current_pressure.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "pressure": data['iaqi']['p']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_h(taktung, seed, city):
    #Humidity / Feuchtigkeit
    while True:
        data = get_city_data(city)
        print("Humidity data sent")
        with open(buffer_path+"/current_humidity.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "humidity": data['iaqi']['h']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def get_w(taktung, seed, city):
    #wind
    while True:
        data = get_city_data(city)
        print("wind data sent")
        with open(buffer_path+"/current_wind.json", 'w', encoding="utf-8") as f:
            json.dump({"time": data['time']['iso'], "wind": data['iaqi']['w']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
        time.sleep(taktung)
    return

def random_sensor(id, taktung, lifetime):
    #zufälliger wert
    print("Sensor: ", id , "beginnt zu senden")
    t_end = time.time() + lifetime
    while time.time() < t_end:
        # get current datetime in UTC
        utc_dt = datetime.now(timezone.utc)
        # convert UTC time to ISO 8601 format
        iso_date = utc_dt.astimezone().isoformat()
        print("Sensor:", id ," data sent")
        with open(buffer_path+f"/current_Sensor{id}.json", 'w', encoding="utf-8") as f:
            json.dump({"time": iso_date, "value": random.randint(1, 100)}, f, ensure_ascii=False)
        time.sleep(taktung)
    print("Sensor: ", id , "hört auf zu senden")
    return
    

if __name__ == "__main__":
    #pprint.pprint(get_city_data("Wiesbaden"))
    print("path:", buffer_path)
    print("Sensoren werden gestartet")

    # Create new threads
    lungengängiger_feinstaub_thread = Thread(target=get_pm25, args=(config['pm25']['taktung'], config['pm25']['seed'], config['city']), daemon=True)
    einatembarer_feinstaub_thread = Thread(target=get_pm10, args=(config['pm10']['taktung'], config['pm10']['seed'], config['city']), daemon=True)
    ozon_thread = Thread(target=get_o3, args=(config['o3']['taktung'], config['o3']['seed'], config['city']), daemon=True)
    stickstoffdioxid_thread = Thread(target=get_no2, args=(config['no2']['taktung'], config['no2']['seed'], config['city']), daemon=True)
    schwefeldioxid_thread = Thread(target=get_so2, args=(config['so2']['taktung'], config['so2']['seed'], config['city']), daemon=True)
    kohlenmonoxid_thread = Thread(target=get_co, args=(config['co']['taktung'], config['co']['seed'], config['city']), daemon=True)
    temperatur_thread = Thread(target=get_t, args=(config['t']['taktung'], config['t']['seed'], config['city']), daemon=True)
    luftdruck_thread = Thread(target=get_p, args=(config['p']['taktung'], config['p']['seed'], config['city']), daemon=True)
    feuchtigkeit_thread = Thread(target=get_h, args=(config['h']['taktung'], config['h']['seed'], config['city']), daemon=True)
    wind_thread = Thread(target=get_w, args=(config['w']['taktung'], config['w']['seed'], config['city']), daemon=True)

    # Start new Threads
    lungengängiger_feinstaub_thread.start()
    einatembarer_feinstaub_thread.start()
    ozon_thread.start()
    stickstoffdioxid_thread.start()
    schwefeldioxid_thread.start()
    kohlenmonoxid_thread.start()
    temperatur_thread.start()
    luftdruck_thread.start()
    feuchtigkeit_thread.start()
    wind_thread.start()

    #Random sensoren erzeugen
    while True:
        for sensor_id in range(1, config['random_sensors']['anzahl_unterschiedlicher_sensoren']+1):
            random_thread = Thread(target=random_sensor, args=(sensor_id, config['random_sensors']['taktung'], config['random_sensors']['lifetime_pro_sensor']), daemon=True)
            random_thread.start()
            time.sleep(config['random_sensors']['zeitlicher_abstand_zwischen_den_starts'])
        