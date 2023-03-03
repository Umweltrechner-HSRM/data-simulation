import PySimpleGUI as sg
import os
import yaml
import subprocess as sp
import json
import ast

# VORBEREITUNG
# Directory paths ermitteln
src_path = str(os.path.dirname(__file__))
config_path = str(os.path.join(src_path, '../config.yaml'))
log_path = str(os.path.join(src_path, '../logs'))

# config einlesen
with open(config_path, 'r', encoding='utf-8') as file:
    # Load the YAML data into a Python dictionary
    config = yaml.load(file, Loader=yaml.FullLoader)

# Theme festlegen
sg.theme('DarkTeal9')

# SPALTEN-LAYOUT
# statisches Menü
menue_column = [
    [sg.Text('Data-Simulation\nDashboard', font=( '',12))],
    [sg.HorizontalSeparator()],

    [sg.Button('Control Panel', size=(12),  key='-CONTROL_PANEL-')],
    [sg.Button('Stadt-Sensoren', size=(12), key='-STADT-SENSOREN-')],
    [sg.Button('Zufällige Städte', size=(12), key='-ZUFÄLLIGE_STÄDTE-')],
    [sg.Button('Heger Sensor', size=(12), key='-HEGER_SENSOR-')],    
    [sg.Button('Einstellungen', size=(12), key='-EINSTELLUNGEN-')],    
]

# Control Panel
control_panel_column = [
    [sg.Text('CONTROL PANEL', font=( '',16))],

    [sg.Text('Aktivierte Sensoren: ', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Checkbox('Stadt-Sensoren', key=('-STADT-SENSOREN_STATUS-'))],
    [sg.Checkbox('Zufällige Städte', key=('-ZUFÄLLIGE_STÄDTE_STATUS-'))],
    [sg.Checkbox('Heger Sensor', key=('-HEGER_SENDER_STATUS-'))],

    [sg.Text('Datensimulation status: ', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Button('Datensimulation starten', button_color='green' ,key='-DATENSIMULATION_START_STOP-')], 

    [sg.Text('Datensimulation Logs: ', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Multiline(size=(130, 5),auto_refresh=True, autoscroll=True, key='-DATENSIMULATION_LOGS-')],

    [sg.HorizontalSeparator()],
    [sg.Button('SPEICHERN', font=('', 12), key='-SPEICHERN_CONTROL_PANEL-')],
]

# Stadt-Sensoren
stadt_sensoren_column = [
    [sg.Text('STADT-SENSOREN', font=( '',16))],

    [sg.Text('Aktivierungsstatus Zufällige Städte: ', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Checkbox('Stadt-Sensoren', key=('-STADT-SENSOREN_STATUS2-'))],

    [sg.Text('Stadt-Sensoren Konfiguration', font=( '',12), pad=((0,0),(10,0)))],    
    [sg.Text("""* Bitte beachte, dass bei der Eingabe eine korrekte JSON Schreibweise verwendet werden muss und dass der Sensor dann ebenfalls unter:
     Einstellungen -> 'Sensor Information Map' genau definiert sein muss. Eine Fehlerüberprüfung findet hier nicht statt.""")],
    [sg.Multiline(size=(30, 20), key='-STADT_SENSOREN_MULTILINE-')],

    [sg.HorizontalSeparator()],
    [sg.Button('SPEICHERN', font=('', 12), key='-SPEICHERN_STADT-SENSOREN-')],
]

# Zufällige Städte
zufällige_städte_column = [
    [sg.Text('ZUFÄLLIGE STÄDTE', font=( '',16))],

    [sg.Text('Aktivierungsstatus Stadt-Sensoren: ', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Checkbox('Zufällige Städte', key=('-ZUFÄLLIGE_STÄDTE_STATUS2-'))],

    [sg.Text('Zufällige Städte Konfiguration:', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Text('Taktung: ')],
    [sg.Spin(values=list(range(0, 1000)), initial_value=5, key='-ZUFALL-TAKTUNG-')],
    [sg.Text('Anzahl unterschiedlicher Städte: ')],
    [sg.Spin(values=list(range(0, 1000)), initial_value=2, key='-ZUFALL-UNTERSCHIEDLICHE_STÄDTE-')],
    [sg.Text('Abstand zwischen den Starts der Städte: ')],
    [sg.Spin(values=list(range(0, 1000)), initial_value=15, key='-ZUFALL-START_ABSTAND-')],
    [sg.Text('Lebenszeit einer Stadt: ')],
    [sg.Spin(values=list(range(0, 1000)), initial_value=60, key='-ZUFALL-LEBENSZEIT-')],


    [sg.Text('Liste aller zufälligen Städte', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Text("""* Bitte beachte, dass bei der Eingabe eine korrekte JSON Schreibweise verwendet werden muss und dass es
    nicht dafür garantiert werden kann, dass es für jede Stadt Sensordaten gibt""")],
    [sg.Multiline(default_text='', size=(30, 20), key='-ZUFÄLLIGE_STÄDTE_MULTILINE-')],

    [sg.HorizontalSeparator()],
    [sg.Button('SPEICHERN', font=('', 12), key='-SPEICHERN_ZUFÄLLIGE_STÄDTE-')],
]

# Heger Sensor
heger_sensor_column = [
    [sg.Text('HEGER SENSOR', font=( '',16))],

    [sg.Text('Aktivierungsstatus Heger Sensoren: ', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Checkbox('Heger Sensor: ', key=('-HEGER_SENDER_STATUS2-'))],

    [sg.Text('Heger Konfiguration:', font=('',12), pad=((0,0),(10,0)))],
    [sg.Text('Sensorname: ')],
    [sg.Input(default_text='', key='-HEGER_SENSORNAME-')],
    [sg.Text('Sensor-Art: ')],
    [sg.Input(default_text='', key='-HEGER_SENSORART-')],
    [sg.Text('Stadt: ')],
    [sg.Input(default_text='', key='-HEGER_STADT-')],

    [sg.Text('Taktung: ')],
    [sg.Spin(values=list(range(0, 1000)), initial_value=5, enable_events=True, key='-HEGER-TAKTUNG-')],    
    [sg.Text('Maximaler Wert: ')],
    [sg.Input(default_text='', key='-HEGER_MAX_WERT-')],
    [sg.Text('Minimaler Wert: ')],
    [sg.Input(default_text='', key='-HEGER_MIN_WERT-')],

    [sg.HorizontalSeparator()],
    [sg.Button('SPEICHERN', font=('', 12), key='-SPEICHERN_HEGER_SENSOR-')],
]

# Einstellungen
einstellungen_column = [
    [sg.Text('EINSTELLUNGEN', font=( '',16))],

    [sg.Text('AQICN API Konfiguration', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Text('API KEY: '), sg.Input(default_text='', key='-AQICN_API_KEY-')],

    [sg.Text('Backend Konfiguration', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Text('Username: ')],
    [sg.Input(default_text='', key='-BACKEND_USERNAME-')],
    [sg.Text('Passwort: ')],
    [sg.Input(default_text='', key='-BACKEND_PASSWORT-')],
    [sg.Text('Keycloak Url: ')],
    [sg.Input(default_text='', key='-BACKEND_KEYCLOAK-')],
    [sg.Text('API base Url: ')],
    [sg.Input(default_text='', key='-BACKEND_API_BASE-')],
    [sg.Text('API ws Url: ')],
    [sg.Input(default_text='', key='-BACKEND_API_WS-')],
    [sg.Text('Send response path: ')],
    [sg.Input(default_text='', key='-BACKEND_SEND_RESPONSE_PATH-')],

    [sg.Text('Logging', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Text('Logging Art wählen'), sg.Drop(values=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), key='-BACKEND_LOGGING-')],

    [sg.Text('Sensor Information Map', font=( '',12), pad=((0,0),(10,0)))],
    [sg.Text("""* Bitte beachte, dass bei der Eingabe eine korrekte JSON Schreibweise verwendet werden muss und dass der Sensor dann ebenfalls unter:
     Einstellungen -> 'Sensor Information Map' genau definiert sein muss. Eine Fehlerüberprüfung findet hier nicht statt.""")],    
    [sg.Multiline(default_text='', size=(30, 20), key='-INFORMATION_MAP-')],

    [sg.HorizontalSeparator()],
    [sg.Button('SPEICHERN', font=('', 12), key='-SPEICHERN_EINSTELLUNGEN-')],
]

# LAYOUT ANLEGEN
layout = [
    [sg.Column(layout = menue_column, vertical_alignment='top'),
     sg.VSeperator(),
     sg.Column(layout = control_panel_column, visible=True, key='-DYNAMIC_COLUMN1-'), sg.Column(layout = stadt_sensoren_column, visible=False, key='-DYNAMIC_COLUMN2-'),
     sg.Column(layout = zufällige_städte_column, scrollable=True, vertical_scroll_only=True, visible=False, key='-DYNAMIC_COLUMN3-'), sg.Column(layout = heger_sensor_column, visible=False, key='-DYNAMIC_COLUMN4-'),
     sg.Column(layout = einstellungen_column, scrollable=True, vertical_scroll_only=True, visible=False, key='-DYNAMIC_COLUMN5-'),
    ]
]
window = sg.Window('Data-simulation', layout, finalize=True)


# HILFSFUNKTIONEN
def save_yaml():
    """
    speichern der config
    """
    #speichere änderungen an der yaml
    with open(config_path, 'w', encoding='utf-8') as file:
        # Load the YAML data into a Python dictionary
        yaml.dump(config, file, default_flow_style=False, encoding='utf-8', allow_unicode=True, Dumper=yaml.SafeDumper)

def yaml_to_json(yaml_element):
    """
    Hier konvertiert man yaml zu Json, da man nur dieses schön in der GUI anzeigen kann
    """
    return json.dumps(yaml_element, indent=2, ensure_ascii=False)  

def json_to_yaml(json_string):
    """
    Hier wird json in yaml konvertiert
    """  
    return json.loads(json_string)  

def activate_column(column_name):
    """
    Diese Funktion bekommt eine Column via Name übergeben und muss diese aktivieren
    """
    # Alle Columns deaktivieren
    for col in dynamic_layout_keys:
        window[col].update(visible=False)
    #Neue Column aktivieren
    window[column_name].update(visible=True)


# SPALTEN-DATEN LADEN
def load_control_panel():
    """
    Laden der Daten, welche auf dem Control Panel angezeigt werden
    """
    window['-STADT-SENSOREN_STATUS-'].update(value=config['aktive_sensoren']['configured_citys'])
    window['-HEGER_SENDER_STATUS-'].update(value=config['aktive_sensoren']['heger_spezial'])
    window['-ZUFÄLLIGE_STÄDTE_STATUS-'].update(value=config['aktive_sensoren']['random_citys'])

def load_stadt_sensoren():
    """
    Laden der Daten, welche bei den Stadt-Sensoren angezeigt werden
    """
    window['-STADT-SENSOREN_STATUS2-'].update(value=config['aktive_sensoren']['configured_citys'])
    window['-STADT_SENSOREN_MULTILINE-'].update(value=yaml_to_json(config['city_configuration']))

def load_zufällige_städte():
    """
    Laden der Daten, welche bei den zufälligen Städten angezeigt werden
    """
    window['-ZUFÄLLIGE_STÄDTE_STATUS2-'].update(value=config['aktive_sensoren']['random_citys'])
    window['-ZUFALL-TAKTUNG-'].update(value=config['random_citys_sensors']['taktung'])
    window['-ZUFALL-UNTERSCHIEDLICHE_STÄDTE-'].update(value=config['random_citys_sensors']['anzahl_unterschiedlicher_citys'])
    window['-ZUFALL-START_ABSTAND-'].update(value=config['random_citys_sensors']['zeitlicher_abstand_zwischen_den_starts'])
    window['-ZUFALL-LEBENSZEIT-'].update(value=config['random_citys_sensors']['lifetime_pro_city'])
    window['-ZUFÄLLIGE_STÄDTE_MULTILINE-'].update(value=config['random_citys'])

def load_heger_sensor():
    """
    Laden der Daten, welche bei Heger Sensor angezeigt werden
    """
    window['-HEGER_SENDER_STATUS2-'].update(value=config['aktive_sensoren']['heger_spezial'])
    window['-HEGER_SENSORNAME-'].update(value=config['heger_spezial']['id'])
    window['-HEGER_SENSORART-'].update(value=config['heger_spezial']['sensor_art'])
    window['-HEGER_STADT-'].update(value=config['heger_spezial']['city'])
    window['-HEGER-TAKTUNG-'].update(value=config['heger_spezial']['taktung'])
    window['-HEGER_MAX_WERT-'].update(value=config['heger_spezial']['max_value'])
    window['-HEGER_MIN_WERT-'].update(value=config['heger_spezial']['min_value'])

def load_einstellungen():    
    """
    Laden der Daten, welche bei den Einstellungen angezeigt werden
    """
    window['-AQICN_API_KEY-'].update(value=config['aqicn_key'])
    window['-BACKEND_USERNAME-'].update(value=config['backend']['username'])
    window['-BACKEND_PASSWORT-'].update(value=config['backend']['password'])
    window['-BACKEND_KEYCLOAK-'].update(value=config['backend']['keycloak_url'])
    window['-BACKEND_API_BASE-'].update(value=config['backend']['api_base_url'])
    window['-BACKEND_API_WS-'].update(value=config['backend']['api_ws_url'])
    window['-BACKEND_LOGGING-'].update(value=config['log_level'])
    window['-BACKEND_SEND_RESPONSE_PATH-'].update(value=config['backend']['send_response_path'])
    window['-INFORMATION_MAP-'].update(value=yaml_to_json(config['sensor_details']))    


# HILFSVARIABLEN
# speichert den Programm status
programm_running = False
# speichert den Prozess
process = ''
# speichert die letzten logs
last_logs = ''
# liste vona allen Columns
dynamic_layout_keys = ['-DYNAMIC_COLUMN1-', '-DYNAMIC_COLUMN2-', '-DYNAMIC_COLUMN3-', '-DYNAMIC_COLUMN4-', '-DYNAMIC_COLUMN5-']

# VORABFUNKTIONEN
# Erste Column laden
load_control_panel()

# EVENT LOOP
while True:    
    event, values = window.read(timeout=100, timeout_key='-TIMEOUT-')        

    # UI schließen
    if event == sg.WIN_CLOSED:        
        break

    # MENÜ
    if event == '-CONTROL_PANEL-':
        activate_column('-DYNAMIC_COLUMN1-') 
        load_control_panel()

    if event == '-STADT-SENSOREN-':
        load_stadt_sensoren() 
        activate_column('-DYNAMIC_COLUMN2-')

    if event == '-ZUFÄLLIGE_STÄDTE-':
        activate_column('-DYNAMIC_COLUMN3-') 
        load_zufällige_städte()

    if event == '-HEGER_SENSOR-':
        activate_column('-DYNAMIC_COLUMN4-')
        load_heger_sensor()

    if event == '-EINSTELLUNGEN-':
        activate_column('-DYNAMIC_COLUMN5-') 
        load_einstellungen()
    
    # CONTROL PANEL SPEICHERN UND FUNKTIONALITÄT
    if event == '-SPEICHERN_CONTROL_PANEL-':
        config['aktive_sensoren']['configured_citys'] = values['-STADT-SENSOREN_STATUS-']
        config['aktive_sensoren']['random_citys'] = values['-ZUFÄLLIGE_STÄDTE_STATUS-']
        config['aktive_sensoren']['heger_spezial'] = values['-HEGER_SENDER_STATUS-']
        save_yaml()
        load_control_panel()
    
    if event == '-DATENSIMULATION_START_STOP-':
        # Startet und stoppt das Programm
        if programm_running == False:
            process = sp.Popen(['python', os.path.join(src_path, 'main.py') ])
            programm_running = True
            window['-DATENSIMULATION_START_STOP-'].update('Datensimulation stoppen', button_color='red')
        else:            
            process.terminate()
            programm_running = False
            window['-DATENSIMULATION_START_STOP-'].update('Datensimulation starten', button_color='green')

    if event == '-TIMEOUT-':
        # Einlesen des Logfiles und updaten
        try:
            file_object = open(os.path.join(log_path, 'data-simulation.log'), 'r', encoding='utf-8')
            log = file_object.read()[-2000:]
            file_object.close()
        except IOError:
            continue
        
        if log != last_logs and programm_running == True:
            window['-DATENSIMULATION_LOGS-'].update(log)
            last_logs = log

    # STADT-SENSOR SPEICHERN
    if event == '-SPEICHERN_STADT-SENSOREN-':
        config['aktive_sensoren']['configured_citys'] = values['-STADT-SENSOREN_STATUS2-']
        config['city_configuration'] = json_to_yaml(values['-STADT_SENSOREN_MULTILINE-'])
        save_yaml()
        load_control_panel()        

    # ZUFÄLLIGE STÄDTE SPEICHERN
    if event == '-SPEICHERN_ZUFÄLLIGE_STÄDTE-':
        config['aktive_sensoren']['random_citys'] = values['-ZUFÄLLIGE_STÄDTE_STATUS2-']
        config['random_citys_sensors']['taktung'] = values['-ZUFALL-TAKTUNG-']
        config['random_citys_sensors']['anzahl_unterschiedlicher_citys'] = values['-ZUFALL-UNTERSCHIEDLICHE_STÄDTE-']
        config['random_citys_sensors']['zeitlicher_abstand_zwischen_den_starts'] = values['-ZUFALL-START_ABSTAND-']
        config['random_citys_sensors']['lifetime_pro_city'] = values['-ZUFALL-LEBENSZEIT-']
        config['random_citys'] = ast.literal_eval(values['-ZUFÄLLIGE_STÄDTE_MULTILINE-'])
        save_yaml()
        load_control_panel()

    # HEGER SPEZIAL SPEICHERN
    if event == '-SPEICHERN_HEGER_SENSOR-':
        config['aktive_sensoren']['heger_spezial'] = values['-HEGER_SENDER_STATUS2-']
        config['heger_spezial']['id'] = values['-HEGER_SENSORNAME-']
        config['heger_spezial']['sensor_art'] = values['-HEGER_SENSORART-']
        config['heger_spezial']['city'] = values['-HEGER_STADT-']
        config['heger_spezial']['taktung'] = values['-HEGER-TAKTUNG-']
        config['heger_spezial']['max_value'] = int(values['-HEGER_MAX_WERT-'])
        config['heger_spezial']['min_value'] = int(values['-HEGER_MIN_WERT-'])
        save_yaml()
        load_heger_sensor()

    # EINSTELLUNGEN SPEICHERN
    if event == '-SPEICHERN_EINSTELLUNGEN-':
        config['aqicn_key'] = values['-AQICN_API_KEY-']
        config['backend']['username'] = values['-BACKEND_USERNAME-']
        config['backend']['password'] = values['-BACKEND_PASSWORT-']
        config['backend']['keycloak_url'] = values['-BACKEND_KEYCLOAK-']
        config['backend']['api_base_url'] = values['-BACKEND_API_BASE-']
        config['backend']['api_ws_url'] = values['-BACKEND_API_WS-']
        config['backend']['send_response_path'] = values['-BACKEND_SEND_RESPONSE_PATH-']
        config['log_level'] = values['-BACKEND_LOGGING-']
        config['sensor_details'] = json_to_yaml(values['-INFORMATION_MAP-'])
        save_yaml()
        load_heger_sensor()

window.close()