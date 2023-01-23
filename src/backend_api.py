import sys
import os
import logging
import yaml
import requests
import singelton
import json
import random
import aqicn_api
from stomp_ws.client import Client
sys.path.append('./')

#Directory paths ermitteln
src_path = str(os.path.dirname(__file__))
config_path = str(os.path.join(src_path, '../config.yaml'))

#config einlesen
config = yaml.safe_load(open(config_path, encoding='utf-8'))

# Api Base URL festlegen
API_BASE_URL = config['backend']['api_base_url']

# Singelton Klasse für das Backend
class BackendSingleton(metaclass=singelton.SingletonMeta):
    token = None
    client = None

    def __init__(self):
        self.token = self.get_keycloak_token()
        self.client = self.get_connected_client()

    
    # SETUP    
    def ws_error_callback(self):
        """
        Es kann sich nicht mehr mit dem Websocket verbunden werden -> Script stoppen
        """
        logging.critical("Fehler beim Websocket -> Abbruch")
        sys.exit(0)

    def get_connected_client(self):
        """
        Hier wird der Client mit dem Websocket verbunden und anschließend zurückgegeben
        """
        # open transport
        client = Client(config['backend']['api_ws_url'])
        client.errorCallback = self.ws_error_callback
        # connect to the endpoint
        client.connect()
        return client

    def get_keycloak_token(self):
        """
        Diese Methode fragt mit Hilfe von username und password, den Keycloak Token ab und gibt diesen anschließend zurück
        """
        # Daten aus Config einlesen
        url = config['backend']['keycloak_url']
        username = config['backend']['username']
        password = config['backend']['password']
        # Anfrage bauen
        payload = f"client_id=umweltrechner-backend&username={username}&password={password}&grant_type=password&client_secret=9ogIS2Mf9tcAuIDvkmzJ5KskixmAoKll"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # Anfrage abschicken
        response = requests.request("POST", url, data=payload, headers=headers)
        # Access Token zurückgeben
        return response.json()['access_token']


    # GET REQUESTS
    def get_all_citys_from_backend(self):
        """
        Brauche ich für die random citys. Es soll eine Liste zurückgebgen (aus dem be), welche alle 
        vertretenen Städte zurückgibt.
        SQL Kinda: "SELECT DISTICT city FROM tabelle;"
        """
        url = f"{API_BASE_URL}/sensor"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        response = requests.request("GET", url, headers=headers)
        all_citys = [value['location'] for value in response.json()]
        return all_citys
        
    def get_all_sensors_from_backend(self):
        """
        Diese Methode gibt alle Sensoren zurück, welche bereits in der Datenbank registriert sind
        api/sensors GET -> Liste von allen registrierten
        """
        #TODO optimieren im Backend
        url = f"{API_BASE_URL}/sensor"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        response = requests.request("GET", url, headers=headers)
        all_sensors = [value['name'] for value in response.json()]
        return all_sensors

    def get_number_of_valid_unused_citys(self, random_citys, anzahl_unterschiedlicher_städte):
        """
        Diese Funktion gibt aus einer Liste an Städten, eine gewisse Anzahl an Städten zurück, zu denen es 
        Daten gibt UND welche es noch nicht in unserer Datenbank gibt 
        """
        #valide Städte
        result_citys = []

        #List aller Städte, welche schon in der Datenbank vertreten sind
        db_city_list = self.get_all_citys_from_backend()

        #Mischen der Städte
        random.shuffle(random_citys)

        for city in random_citys:
            #Überprüfen, ob es zu dieser Stadt Daten gibt und wenn ja dem result hinzufügen
            if aqicn_api.city_avaiable(city) and city not in db_city_list:
                result_citys.append(city)

            # Ist die gewünschte Menge von unterschiedlichen Städten erfüllt, werden diese zurück gegeben
            if len(result_citys) == anzahl_unterschiedlicher_städte:
                logging.info(f"Zufällige Städte welche noch nicht benutzt wurden: {result_citys}")
                return result_citys
        return


    # POST REQUESTS
    def register_sensor(self, id, sensor, city):
        """
        Diese Methode registriert den Sensor in der Datenbank
        """
        print("Sensor: ", sensor, " der Stadt: ", city, " wurde neu registriert")
        url = f"{API_BASE_URL}/sensor"
        payload = {
            "name": id,
            "location": city,
            "unit": config['sensor_details'][sensor]['unit'],
            "description": config['sensor_details'][sensor]['description'],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        return

    def send_response_to_backend(self, response):
        """
        Diese Methode bekommt ein dict mit Sensordaten übergeben und sendet dieses an das Backend
        """
        # Pfad aus config einlesen    
        send_response_path = config['backend']['send_response_path']
        # Zielpfad vorbereiten
        dest = f"{send_response_path}{response['id']}"
        # Daten an das Backend senden
        self.client.send(destination=dest, body=json.dumps(response))
        #print("Response!!!!!:", response)
        logging.info(f"Folgende Response wird geschickt: {response}")
        return







