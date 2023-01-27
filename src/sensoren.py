import time
import random
import helper
import aqicn_api
import backend_api

# Globale Variablen
config = helper.get_config()

# Backend objekt
backend = backend_api.BackendSingleton()

#Sensorsimulationsmethoden (für die Threads)
def get_sensor_from_city(sensor, taktung, seed, city):
    """
    Hier bekommt man die Sensorwerte für eine Stadt
    """
    #Überprüfen, ob es zu der Stadt Sensordaten gibt
    if not aqicn_api.city_avaiable(city):
        raise Exception(f"ERROR: Zu der Stadt: {city}, gibt es keine Sensoren")
    #Umweltstation zur Stadt finden
    umweltstation_id = aqicn_api.get_biggest_station_of_city(city)
    #Überprüfen, ob es den Sensor an der Wetterstation gibt
    if sensor not in aqicn_api.get_station_sensors(umweltstation_id):
        raise Exception(f"ERROR: {umweltstation_id} Zu der Stadt: {city}, gibt es den Sensor: {sensor} nicht")
    #Überprüfen, ob der Sensor bereits in der Datenbank existiert, wenn nicht muss err angelegt werden
    id = helper.generate_seonsor_name(umweltstation_id, sensor, city)
    if id not in backend.get_all_sensors_from_backend():
        #Registriere Sensor in der Datenbank
        backend.register_sensor(id, sensor, city)
    #Sagen, dass die Stadt beginnt zu senden
    print("City: ", city, "mit Sensor", sensor, "beginnt zu senden")

    while True:
        #Daten der Umweltstation erfassen
        data = aqicn_api.get_station_data(umweltstation_id)
        # Zeit umrechnern
        #timestamp = convert_time_from_iso8601_to_unix_milli_timestamp(data['time']['iso'])
        timestamp = time.time() * 1000      
        print("Random Range:", random.uniform(-seed, seed)) 
        data_value = float(data['iaqi'][sensor]['v']) + random.uniform(-seed, seed)
        #Response vorbereiten        
        response = helper.generate_response(id, timestamp, data_value, city)
        #Senden
        backend.send_response_to_backend(response)
        #Logging / Ausgabe
        #Sensor pausieren bis zum nächsten Takt
        time.sleep(taktung)


def get_heger_spezial(taktung, max_value, min_value):
    """
    Hier solle eine Kurve mit harten Kanten simuliert werden so wie _TT_
    """
    #Wurde der Sensor bereits registriert?
    if config['heger_spezial']['id'] not in backend.get_all_sensors_from_backend():
        backend.register_sensor(config['heger_spezial']['id'], config['heger_spezial']['sensor_art'], config['heger_spezial']['city'])
    # Variable zum speichern des aktuellen Sensorwerts
    current_value = max_value
    while True:
        #Zeit messen
        timestamp = round(time.time()*1000)
        #Response vorbereiten
        response = helper.generate_response(config['heger_spezial']['id'], timestamp, current_value, config['heger_spezial']['city'])
        #Response versenden
        backend.send_response_to_backend(response)
        #Jetzt muss direkt der nächste Sensordatensatz verschickt werden, um den harten Übergang zu erzeugen
        # Zu sendenden Sensorwert wechseln
        current_value = min_value if current_value == max_value else max_value
        # Zeit um eine Millisekunde verschieben
        timestamp = timestamp + 1
        # Zweite Response vorbereiten
        response = helper.generate_response(config['heger_spezial']['id'], timestamp, current_value, config['heger_spezial']['city'])
        # Zweite Response versenden
        backend.send_response_to_backend(response)
        # Warten bis zum nächsten Senden
        time.sleep(taktung)

def random_city_sensor(city, taktung, lifetime):
    #Sagen, dass die Stadt beginnt zu senden
    print("Random_City: ", city, "beginnt zu senden")
    #Umweltstation zur Stadt finden
    umweltstation_id = aqicn_api.get_biggest_station_of_city(city)
    t_end = time.time() + lifetime
    while time.time() < t_end:
        #Sensordaten erfassen
        data = aqicn_api.get_station_data(umweltstation_id)
        for sensor in list(data['iaqi'].keys()):
            #Überprüfen, ob der Sensor bereits in der Datenbank existiert, wenn nicht muss err angelegt werden
            id = helper.generate_seonsor_name(umweltstation_id, sensor, city)
            if id not in backend.get_all_sensors_from_backend():
                #Registriere Sensor in der Datenbank
                backend.register_sensor(id, sensor, city)
            # Zeit umrechnen
            timestamp = helper.convert_time_from_iso8601_to_unix_milli_timestamp(data['time']['iso'])
            #Response vorbereiten
            response = helper.generate_response(id, timestamp, data['iaqi'][sensor]['v'], city)
            #Sensordaten versenden
            backend.send_response_to_backend(response)
        #Taktung abwarten
        time.sleep(taktung)
    print("City: ", city , "hört auf zu senden")
    return