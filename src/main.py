import sys
from threading import Thread
import sensoren
import time
import backend_api
import helper
import logging

#Initalize Logging
helper.setup_logging()

#config einlesen
config = helper.get_config()

#Verbinden mit Backend
backend = backend_api.BackendSingleton()
client = backend.client

def starte_stadt_sensoren():
    #Starte konfigurierte citys
    for city in config['city_configuration']:
            current_city = list(city.keys())[0]
            for sensor in city[current_city]:
                sensor_thread = Thread(target=sensoren.get_sensor_from_city, args=(sensor['sensor'], sensor['taktung'], sensor['seed'], current_city), daemon=True)
                sensor_thread.start()
                logging.info(f"Starte konfigurierten Sensor ARGS: - Stadt: {current_city} - Sensor: {sensor['sensor']} - Taktung: {sensor['taktung']} - Seed: {sensor['seed']}")

def starte_random_sensoren():
    # Random city_sensoren
    random_citys = backend.get_number_of_valid_unused_citys(config['random_citys'], config['random_citys_sensors']['anzahl_unterschiedlicher_citys'] )
    print("Random_citys:list: ", random_citys)        
    for city in  random_citys:
        random_city_thread = Thread(target=sensoren.random_city_sensor, args=(city, config['random_citys_sensors']['taktung'], config['random_citys_sensors']['lifetime_pro_city']), daemon=True)
        random_city_thread.start()
        logging.info(f"Starte zufällige Stadt: ARGS: - Stadt: {city} - Taktung: {config['random_citys_sensors']['taktung']} - City-Lifetime: {config['random_citys_sensors']['lifetime_pro_city']}")
        time.sleep(config['random_citys_sensors']['zeitlicher_abstand_zwischen_den_starts'])

def starte_heger_spezial():
    #Start Heger Spezial
    heger_thread = Thread(target=sensoren.get_heger_spezial, args=(config['heger_spezial']['taktung'], config['heger_spezial']['max_value'], config['heger_spezial']['min_value']), daemon=True)
    heger_thread.start()
    logging.info(f"Starte Heger Spezial ARGS: - Taktung: {config['heger_spezial']['taktung']} - Max Value: {config['heger_spezial']['max_value']}, - Min value: {config['heger_spezial']['min_value']}")


def starte_sensoren():
    """
    Hier werden die aktiven Sensorthreads gestartet
    """
    logging.info("AKTIVIERTE SENSOREN STARTEN")    
    print("Akitvierte Sensoren gestartet")    
    if config['aktive_sensoren']['configured_citys']:
        starte_stadt_sensoren()        

    if config['aktive_sensoren']['heger_spezial']:
        starte_heger_spezial()

    if config['aktive_sensoren']['random_citys']:
        starte_random_sensoren()


if __name__ == "__main__":
    starte_sensoren()

    #Solange der Websocket verbunden ist, werden Daten gesendet
    while True:        
        # Websocketverbindung ist abgebrochen
        if client.connected == False:
            # Versuchen erneut zu verbinden
            client.connect()
            if client.connected == False:
                #Es kann sich nicht mehr mit dem Websocket verbunden werden -> Script stoppen
                logging.critical("Keine Verbindung zum Websocket möglich -> Abbruch")
                sys.exit(0)
        time.sleep(1)