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
import logging

# Globale Variablen anlegen

#Directory paths ermitteln
src_path = str(os.path.dirname(__file__))
buffer_path = str(os.path.join(src_path, '../buffer'))
config_path = str(os.path.join(src_path, '../config.yaml'))
log_path = str(os.path.join(src_path, '../logs'))

#config einlesen
config = yaml.safe_load(open(config_path, encoding='utf-8'))

#Logger anlegen
log_level = config['log_level']
logging.basicConfig(handlers=[logging.FileHandler(os.path.join(log_path, 'data-simulation.log'), 'w', 'utf-8')], level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

def generate_response(id, time, value, city):
    """
    Erzeugt ein dicitionary aus: id, time, value, city 
    """
    #Response vorbereiten
    response = {}
    response['id'] = id
    response['time'] = time
    response['value'] = value
    response['city'] = city
    return response

def get_number_of_valid_unused_citys(random_citys, anzahl_unterschiedlicher_städte):
    """
    Diese Funktion gibt aus einer Liste an Städten, eine gewisse Anzahl an Städten zurück, zu denen es 
    Daten gibt UND welche es noch nicht in unserer Datenbank gibt 
    """
    #valide Städte
    result_citys = []

    #List aller Städte, welche schon in der Datenbank vertreten sind
    db_city_list = get_all_citys_from_backend()
   
    #Mischen der Städte
    random.shuffle(random_citys)
    
    for city in random_citys:
        #Überprüfen, ob es zu dieser Stadt Daten gibt und wenn ja dem result hinzufügen
        if city_avaiable(city) and city not in db_city_list:
            result_citys.append(city)
        
        # Ist die gewünschte Menge von unterschiedlichen Städten erfüllt, werden diese zurück gegeben
        if len(result_citys) == anzahl_unterschiedlicher_städte:
            logging.info(f"Zufällige Städte welche noch nicht benutzt wurden: {result_citys}")
            return result_citys
    return


#Backend Kommunikation
def send_response_to_backend(response):
    """
    Diese Methode bekommt eine Json Datei übergeben und schickt diese an das Backend
    api/{sensorName} -> Websocket -> siehe mustercode "main.py" 
    s. discord chat
    """
    print(f"Folgende Daten wurden ans Backend versendet: {response}")

def get_all_citys_from_backend():
    """
    Brauche ich für die random citys. Es soll eine Liste zurückgebgen (aus dem be), welche alle 
    vertretenen Städte zurückgibt.
    SQL Kinda: "SELECT DISTICT city FROM tabelle;"
    """
    return ['Wiesbaden', 'Mainz']

def get_all_sensors_from_backend():
    """
    Diese Methode gibt alle Sensoren zurück, welche bereits in der Datenbank registriert sind
    api/sensors GET -> Liste von allen registrierten
    """
    #Das ist nur vorrübergehend
    return ['10036_pm25', '10036_pm10', '10036_o3', '10036_no2', '10036_so2', '10036_co', '10036_t', '10036_p', '10036_h', '10036_w']

def register_sensor(id, sensor, city):
    """
    Diese Methode registriert den Sensor in der Datenbank
    api/sensor PUT -> {
    "name" : "temp_1",
    "location": "Wiesbaden",
    "unit": "C",
    "description": "measures the temperature in Wiesbaden"
    }
    """
    print("Sensor: ", sensor, " der Stadt: ", city, " wurde neu registriert")

#AQICN-API Funktionen
def get_station_data(uid: str) -> dict or None:
    response = requests.get(
        f"https://api.waqi.info/feed/@{uid}/?token={config['aqicn_key']}"
    )
    if response.json()['data'] == "Unknown station":
        return
    return response.json()['data']


def get_all_stations_from_city(cityname):
    #Liste von allen Umweltstationen zu einer Stadt
    station_ids = []

    #Anfrage an API
    response = requests.get(
        f"https://api.waqi.info/search/?token={config['aqicn_key']}&keyword={cityname}"
    )
    if (len(response.json()['data']) > 0):
        for station in response.json()['data']:
            #Alle verfügbaren Station der Liste hinzufügen
            station_ids.append(station['uid'])
            #Liste zurückgeben
            return station_ids
    return

def get_biggest_station_of_city(cityname: str) -> str or None:
    """
    Sucht die Station einer Stadt mit den meisten Sensoren
    """
    #Doku https://aqicn.org/json-api/doc/

    biggest_station_with_sensor = {'uid': None, 'anzahl_sensors': 0}

    for station_id in get_all_stations_from_city(cityname):
        #Daten zur Station holen
        data = get_station_data(station_id)
        #Überprüfen, ob bereits ein Sensor existiert, wenn nicht wird der erste gespeichert
        if (biggest_station_with_sensor['uid'] is None):
            biggest_station_with_sensor['uid'] = station_id
            biggest_station_with_sensor['anzahl_sensors'] = data['iaqi']

        #überspeichern, wenn die station mehr sensoren hat
        if len(data['iaqi']) > len(biggest_station_with_sensor['anzahl_sensors']):
            biggest_station_with_sensor['uid'] = station_id
            biggest_station_with_sensor['anzahl_sensors'] = data['iaqi']

    #Rückgabe
    return biggest_station_with_sensor['uid']


def get_city_data(city_name: str) -> dict or None:
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
    if(get_biggest_station_of_city(city)):
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
    umweltstation_id = get_biggest_station_of_city(city)

    #Überprüfen, ob es den Sensor an der Wetterstation gibt
    if sensor not in get_station_sensors(umweltstation_id):
        raise Exception(f"ERROR: {umweltstation_id} Zu der Stadt: {city}, gibt es den Sensor: {sensor} nicht")

    #Überprüfen, ob der Sensor bereits in der Datenbank existiert, wenn nicht muss err angelegt werden
    id = f'{umweltstation_id}_{sensor}'
    if id in get_all_sensors_from_backend():
        #Registriere Sensor in der Datenbank
        register_sensor(id, sensor, city)

    #Sagen, dass die Stadt beginnt zu senden
    print("City: ", city, "mit Sensor", sensor, "beginnt zu senden")

    while True:
        #Daten der Umweltstation erfassen
        data = get_station_data(umweltstation_id)

        #Response vorbereiten
        response = generate_response(id, data['time']['iso'],  data['iaqi'][sensor]['v'], city)

        #Senden
        send_response_to_backend(response)
        with open(buffer_path+f"/{response['id']}.json", 'w', encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False)

        #Logging / Ausgabe
        # print(f"Der: {sensor} Sensor von der Station: {umweltstation_id}  aus der Stadt: {city} hat den Wert: {response['value']} am: {response['time']} versendet")
        # printTable([response, ])

        #Sensor pausieren bis zum nächsten Takt
        time.sleep(taktung)


def get_heger_spezial(taktung, intervall, max_value, min_value):
    """
    Hier solle eine Kurve mit harten Kanten simuliert werden so wie _TT_
    """
    #Startwerte festlegen
    current_value = max_value
    t_start = time.time()

    while True:
        #Hier schauen wir dass nach jedem Intervall zwischen dem min und max value gewechselt wird
        if (time.time() < t_start + intervall):
            if (current_value == max_value):
                current_value = min_value
                t_start = time.time()
            else:
                current_value = max_value
                t_start = time.time()

        #Zeit im richtigen Format errechnen
        utc_dt = datetime.now(timezone.utc).replace(microsecond=0)
        iso_date = utc_dt.astimezone().isoformat()

        #Response vorbereiten
        response = generate_response('HegerSpezial1', iso_date, current_value, 'imagination_Island')

        #Response versenden
        send_response_to_backend(response)
        with open(buffer_path+f"/{response['id']}.json", 'w', encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False)

        #Sensor pausieren bis zum nächsten Takt
        time.sleep(taktung)


def random_city_sensor(city, taktung, lifetime):
    #Sagen, dass die Stadt beginnt zu senden
    print("City: ", city, "beginnt zu senden")

    #Umweltstation zur Stadt finden
    umweltstation_id = get_biggest_station_of_city(city)

    t_end = time.time() + lifetime
    while time.time() < t_end:

        #Sensordaten erfassen
        data = get_station_data(umweltstation_id)

        for sensor in list(data['iaqi'].keys()):

            #Überprüfen, ob der Sensor bereits in der Datenbank existiert, wenn nicht muss err angelegt werden
            id = f'{umweltstation_id}_{sensor}'
            if id in get_all_sensors_from_backend():
                #Registriere Sensor in der Datenbank
                register_sensor(id, sensor, city)

            #Response vorbereiten
            response = generate_response(id, data['time']['iso'],  data['iaqi'][sensor]['v'], city)

            #Sensordaten versenden
            send_response_to_backend(response)

        #Taktung abwarten
        time.sleep(taktung)
    print("City: ", city , "hört auf zu senden")
    return

if __name__ == "__main__":
    logging.info("...")
    logging.info("AKTIVIERTE SENSOREN STARTEN")

    #Starte konfigurierte citys 
    if config['aktive_sensoren']['configured_citys']:
        for city in config['city_configuration']:
            current_city = list(city.keys())[0]
            for sensor in city[current_city]:
                sensor_thread = Thread(target=get_sensor_from_city, args=(sensor['sensor'], sensor['taktung'], sensor['seed'], current_city), daemon=True)
                sensor_thread.start()
                logging.info(f"Starte konfigurierten Sensor ARGS: - Stadt: {current_city} - Sensor: {sensor['sensor']} - Taktung: {sensor['taktung']} - Seed: {sensor['seed']}")
    
    #Start Heger Spezial
    if config['aktive_sensoren']['heger_spezial']:
        heger_thread = Thread(target=get_heger_spezial, args=(config['heger_spezial']['taktung'], config['heger_spezial']['intervall'], config['heger_spezial']['max_value'], config['heger_spezial']['min_value']), daemon=True)
        heger_thread.start()
        logging.info(f"Starte Heger Spezial ARGS: - Taktung: {config['heger_spezial']['taktung']} - Intervall: {config['heger_spezial']['intervall']} - Max Value: {config['heger_spezial']['max_value']}, - Min value: {config['heger_spezial']['min_value']}")

    # Random city_sensoren
    if config['aktive_sensoren']['random_citys']:
        random_citys = get_number_of_valid_unused_citys(config['random_citys'], config['random_citys_sensors']['anzahl_unterschiedlicher_citys'] )
        while True:
            for city in  random_citys:
                random_city_thread = Thread(target=random_city_sensor, args=(city, config['random_citys_sensors']['taktung'], config['random_citys_sensors']['lifetime_pro_city']), daemon=True)
                random_city_thread.start()
                logging.info(f"Starte zufällige Stadt: ARGS: - Stadt: {city} - Taktung: {config['random_citys_sensors']['taktung']} - City-Lifetime: {config['random_citys_sensors']['lifetime_pro_city']}")
                time.sleep(config['random_citys_sensors']['zeitlicher_abstand_zwischen_den_starts'])

    while True:
        time.sleep(1000000)
        