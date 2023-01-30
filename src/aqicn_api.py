import requests
import helper
import logging
config = helper.get_config()

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

    #Die Station ID's sortieren, falls meherere Stationen die gleiche Anzahl an Sensoren haben, wird aber die mit der kleinsten UID 
    all_station_ids = get_all_stations_from_city(cityname)
    all_station_ids.sort()    
    for station_id in all_station_ids:
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
    logging.info(f"Biggest station in: {cityname} - {station_id}")
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