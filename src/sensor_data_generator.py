import os
import requests
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
city_sensor_path = str(os.path.join(os.path.dirname(__file__), '../config.yaml'))

#config einlesen
config = yaml.safe_load(open(config_path))

#Hilfsfunktionen
def printTable(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList: print(formatStr.format(*item))
   print("")

#Backend Kommunikation
def send_response_to_backend(response):
    """
    Diese Methode bekommt eine Json Datei übergeben und schickt diese an das Backend
    api/{sensorName} -> Websocket -> siehe mustercode "main.py" 
    s. discord chat
    """
    print(f"Folgende Daten wurden ans Backend versendet: {response}")

def get_all_sensors_from_backend():
    """
    Diese Methode gibt alle Sensoren zurück, welche bereits in der Datenbank registriert sind
    api/sensors GET -> Liste von allen registrierten
    """
    #Das ist nur vorrübergehend
    return ['10036_pm25', '10036_pm10', '10036_o3', '10036_no2', '10036_so2', '10036_co', '10036_t', '10036_p', '10036_h', '10036_w']

def register_sensor():
    """
    Diese Methode registriert den Sensor in der Datenbank
    api/sensor PUT -> {
    "name" : "temp_1",
    "location": "Wiesbaden",
    "unit": "C",
    "description": "measures the temperature in Wiesbaden"
    }
    """

#AQICN-API Funktionen
def get_station(query: str) -> str or None:
    #Doku https://aqicn.org/json-api/doc/
    response = requests.get(
        f"https://api.waqi.info/search/?token={config['aqicn_key']}&keyword={query}"
    )
    if (len(response.json()['data']) > 0):
        return response.json()['data'][0]['uid']
    return

def get_station_data(uid: str) -> dict or None:
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

def city_avaiable(city):
    """
    Testet, ob es für die Stadt Wetterdaten gibt
    """
    if(get_station(city)):
        return True
    return False

def get_station_sensors(uid):
    """
    Gibt eine Liste über alle Sensoren zurück, über die eine Wetterstation verfügt
    """
    station_data = get_station_data(str(uid))
    return list(station_data['iaqi'].keys())

#Sensorsimulationsmethoden (für die Threads)
def get_sensor_from_city(sensor, taktung, seed, city):
    """
    Hier bekommt man die Sensorwerte für eine Stadt
    """
    #Überprüfen, ob es zu der Stadt Sensordaten gibt
    if not city_avaiable(city):
        raise Exception(f"ERROR: Zu der Stadt: {city}, gibt es keine Sensoren") 

    #Umweltstation zur Stadt finden
    umweltstation_id = get_station(city)

    #Überprüfen, ob es den Sensor an der Wetterstation gibt
    if umweltstation_id not in get_station_sensors(umweltstation_id):
        raise Exception(f"ERROR: Zu der Stadt: {city}, gibt es den Sensor: {sensor} nicht")

    #Überprüfen, ob der Sensor bereits in der Datenbank existiert, wenn nicht muss err angelegt werden
    id = f'{umweltstation_id}_{sensor}'
    if id in get_all_sensors_from_backend():
        #Registriere Sensor in der Datenbank
        register_sensor()

    while True:
        #Daten der Umweltstation erfassen
        data = get_station_data(umweltstation_id)

        #Response vorbereiten
        response = {}
        response['id'] = id
        response['time'] = data['time']['iso']
        response['value'] = data['iaqi'][sensor]['v']+random.randint(-seed, seed)
        response['city'] = city

        #Senden
        send_response_to_backend(response)
        with open(buffer_path+f"/{response['id']}.json", 'w', encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False)

        #Logging / Ausgabe
        # print(f"Der: {sensor} Sensor von der Station: {umweltstation_id}  aus der Stadt: {city} hat den Wert: {response['value']} am: {response['time']} versendet")
        printTable([response, ])

        #Sensor pausieren bis zum nächsten Takt
        time.sleep(taktung)

# def get_heger_spezial(taktung, intervall, max_value, min_value):
#     """
#     Hier solle eine Kurve mit harten Kanten simuliert werden so wie _TT_
#     """
#     #Startwerte festlegen
#     current_value = max_value
#     t_start = time.time()

#     while True:
#         #Hier schauen wir dass nach jedem Intervall zwischen dem min und max value gewechselt wird
#         if (time.time() < t_start + intervall):
#             if (current_value == max_value):
#                 current_value = min_value
#                 t_start = time.time()
#             else:
#                 current_value = max_value
#                 t_start = time.time()

#         #Zeit im richtigen Format errechnen
#         utc_dt = datetime.now(timezone.utc).replace(microsecond=0)
#         iso_date = utc_dt.astimezone().isoformat()

#         #Response vorbereiten
#         response = {}
#         response['id'] = 'HegerSpezial1'
#         response['time'] = iso_date
#         response['value'] = current_value
#         response['city'] = ''

#         #Response versenden
#         send_response_to_backend(response)
#         with open(buffer_path+f"/{response['id']}.json", 'w', encoding="utf-8") as f:
#             json.dump(response, f, ensure_ascii=False)

#         #Sensor pausieren bis zum nächsten Takt
#         time.sleep(taktung)

# def random_city_sensor(city_sensors, taktung, lifetime):
#     #zufälliger wert
#     print("City: ", city_sensors['city'] , "beginnt zu senden")
#     t_end = time.time() + lifetime
#     while time.time() < t_end:
#         data = get_city_data(city_sensors['city'])
#         for sensor in list(data['iaqi'].keys()):

#             #Response vorbereiten
#             response = {}
#             response['id'] = 'HegerSpezial1'
#             response['time'] = iso_date
#             response['value'] = current_value
#             response['city'] = ''

#             #Hier weiter machen
#         with open(buffer_path+"/current_wind.json", 'w', encoding="utf-8") as f:
#             json.dump({"time": data['time']['iso'], "wind": data['iaqi']['w']['v']+random.randint(-seed, seed)}, f, ensure_ascii=False)
#         time.sleep(taktung)

#         time.sleep(taktung)
#     print("Sensor: ", city_sensors['city'] , "hört auf zu senden")
#     return
    

if __name__ == "__main__":
    print("Sensoren werden gestartet")

    for city in config['city_configuration']:
        current_city = list(city.keys())[0]
        for sensor in city[current_city]:
            sensor_thread = Thread(target=get_sensor_from_city, args=(sensor['sensor'], sensor['taktung'], sensor['seed'], current_city), daemon=True)
            sensor_thread.start()
    
    # Random city_sensoren
    # citys with their sensors
    # with open(city_sensor_path, encoding='utf-8') as json_file:
    #     city_sensors = json.load(json_file)
    # random_citys = random.sample(city_sensors, config['random_citys_sensors']['anzahl_unterschiedlicher_städte'])
    # while True:
    #     for city_with_sensors in  random_citys:
    #         random_city_thread = Thread(target=random_city_sensor, args=(city_with_sensors, config['random_citys_sensors']['taktung'], config['random_citys_sensors']['lifetime_pro_city']), daemon=True)
    #         random_city_thread.start()
    #         time.sleep(config['random_citys_sensors']['zeitlicher_abstand_zwischen_den_starts'])

    while True:
        time.sleep(1000000)
        