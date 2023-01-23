import os
import yaml
import datetime
import logging

#Directory paths ermitteln
src_path = str(os.path.dirname(__file__))
buffer_path = str(os.path.join(src_path, '../buffer'))
config_path = str(os.path.join(src_path, '../config.yaml'))
log_path = str(os.path.join(src_path, '../logs'))

def get_config():
    """
    Config einlesen und zurückgeben
    """ 
    config = yaml.safe_load(open(config_path, encoding='utf-8'))
    return config

def setup_login():
    """
    In dieser Funktion werden die logging einstellungen festgelegt
    """
    # Logging
    config = get_config()
    log_level = config['log_level']
    logging.basicConfig(
        filename=os.path.join(log_path, 'data-simulation.log'),
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d.%m.%y %H:%M:%S',
        encoding='utf-8',
        level=log_level,
        force=True
    )
    logging.info("Login wurde aufgesetzt")

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

def convert_time_from_iso8601_to_unix_milli_timestamp(iso_time):
    """
    Diese Methode bekommt eine Zeit im ISO 8601 Format übergeben und wandelt diese in einen UNIX Timestamp mit Millisekunden um
    """
    # Konvertiere Zeitstempel in ein datetime-Objekt
    time_obj = datetime.datetime.fromisoformat(iso_time)
    # Konvertiere Sie das datetime-Objekt in einen UNIX-Timestamp in Millisekunden
    unix_timestamp = int(time_obj.timestamp() * 1000)
    return unix_timestamp

def generate_seonsor_name(umweltstation_id, sensor):
    """
    Aus umweltstation_id und sensor Sensornamen generieren
    """
    return f'sensor_{umweltstation_id}_{sensor}'

def generate_response(id, time, value, city):
    """
    Erzeugt ein dicitionary aus: id, time, value, city 
    """
    #Response erzeugen
    response = {}
    response['id'] = id
    response['timestamp'] = time
    response['value'] = value
    response['city'] = city
    return response
