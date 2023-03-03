import os
import requests
import yaml
import json
import os

#Directory path ermitteln
config_path = str(os.path.join(os.path.dirname(__file__), '../config.yaml'))
city_sensor_path = str(os.path.join(os.path.dirname(__file__), '../data/city_sensor_map.json'))
#config einlesen
config = yaml.safe_load(open(config_path))

def get_city_data(city_name: str) -> dict or None:
    """
    Bezieht Daten einer Stadt
    """
    response = requests.get(
        f"https://api.waqi.info/feed/{city_name}/?token={config['aqicn_key']}"
    )
    if response.json()['data'] == "Unknown station":
        return
    return response.json()['data']

def generate_city_sensor_map(city_list):
    """
    Bekommt eine Liste an Städten gegeben und speichert alle Städte zu denen es Sensordaten gibt.
    Des weiteren könnte ein dict erzeugt werden, welches Sensoren einer Stadt zuordnet.
    Dies befindet sich in result wird aber nicht gespeichert.
    """
    result = []
    result2 = []
    with open(city_list, encoding='utf-8') as json_file:
        data = json.load(json_file) 
        for city in data:
            city_data = get_city_data(city)
            print("City:", city)
            if city_data is None:
                continue
            if city_data['iaqi'] is not None:
                result2.append(city)
                result.append({'city': city, 'sensors': list(city_data['iaqi'].keys())})

    with open(city_sensor_path, "w", encoding='utf-8') as jsonfile:
        json.dump(result2,jsonfile,ensure_ascii=False)

if __name__ == "__main__":
    city_list = str(os.path.join(os.path.dirname(__file__), '../data/liste_aller_städte.json'))
    generate_city_sensor_map(city_list)
    