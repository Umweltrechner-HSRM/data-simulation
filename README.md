# Datensimulator
Todo:
- Testing
- Logging
- Doku

### Was macht das Skript?
Dieses Skript ermittelt die echten und aktuellen Air Quality Daten einer Stadt und legt diese dann im Buffer ab.

### Welche Werte könne ermittet werden?
Je nachdem welche Stadt angeben wird kann die Vielfalt der Sensoren schwanken. So gibt es in Mainz z.B relativ wenig Daten, während man in Wiesbaden folgende erhält:

- PM25 (lungengängiger Feinstaub)
- PM10 (einatembarer Feinstaub)
- O3 (Ozon)
- NO2 (Stickstoffdioxid)
- SO2 (Schwefeldioxid)
- CO (Kohlenstoffmonoxid)
- t (Temperatur)
- p (Pressure/Luftdruck)
- h (humidity/Feuchtigkeit)
- w (Wind)

### Wie starte ich das Skript?
Zu erst müssen alle Module heruntergeladen werden. Die Liste aller Module befindet sich in `python_requirements.txt` Jetzt muss man nur noch den Befehl usführen:
```
pip install -r python_requirements.txt
``` 
Dann lässt sich der Datensimulator mit folgendem Befehl starten, wenn man sich im Hauptverzeichnis befindet
```
python ./src/sensor_data_generator.py

```
Wird das Skript gestartet, bleibt es so lange am Laufen, bis es mit Strg+C abgebrochen wird. In dieser Zeit werden ständig Daten erzeugt.

### Wo finde ich die Daten?
Die Daten liegen im Verzeichnis `buffer` als Json-Dateien vor. Später sollen diese Daten direkt verschickt werden

### Wie kann ich das Skript konfigurieren?
Im Hauptverzeichnis liegt eine Datei `config.yaml` vor. (Ganz unten kannst du dir einen Ausschnitt der config auch anschauen). Mit dieser lässt sich das Skript weiter konfigurieren. Dabei lässt sich:
1. Die Stadt verändern, aus der Daten bezogen werden. Dies findet man unter dem Punkt `city`
2. Zu jedem Sensor kann angegeben werde, wie oft die Daten abgefragt und versendet werden soll. Dies findet man unter dem Punkt `taktung`. Die Angabe erfolgt in Sekunden
3. Zu jedem Sensor kann man auch noch einen `seed` hinzufügen. Das ist vorallem zu Testzwecken interessant. Falls z.B die Temperatur über einen längeren Zeitraum gleich bleibt, können so künstlich sichtbare Schwankungen erzeugt werden. Der seed ist default mäßif auf 0, sprich es ändert sich nichts am Wert.

Des weiteren gibt es noch die zufälligen Sensoren, welche man auch konfigurieren kann. Diese kommen im Betrieb neu hinzu. Konfigurieren kann man diese unter `random_sensors` folgend:
1. `taktung` Zeitabstände in denen der Sensor Daten schickt
2. `anzahl_unterschiedlicher_sensoren` Anzahl von Sensoren die maximal simuliert werden
3. `zeitlicher_abstand_zwischen_den_starts` Abstand in dem die Sensoren starten (damit nicht alle sensoren direkt online sind)
4. `lifetime_pro_sensor` Wie lange ein Sensor insgesamt sendet

### Wie funktinoiert das Skript unter der Haube?
Es wird diese [API](https://aqicn.org/map/wiesbaden/de/) verwendet, welche alle Sensordaten einer Stadt liefert. Da unser Skript jeder Sensor einzeln simulieren soll, werden diese Werte aufgespalten. Um die unterschiedliche Taktung (Sendezyklus) am besten simulieren zu können, arbeitet das Skript mit mehreren Threads, welche dann jeweils einen Sensor simulieren. Die Daten die diese Threads dann "erzeugen", werden als Json File im Buffer gespeichert

### Wie sieht ein erzeugtes json File aus?
```
{
    "time": "2022-11-04T15:00:00+01:00",
    "temperature": 11.3
}
```

### Wie sieht die config.yaml aus?
```
---
city: 'Wiesbaden'     #Aus welcher Stadt sollen die Daten stammen?

pm25:                 # lungengängiger_feinstaub
  taktung: 1          # Wiederholungsrate in s
  seed: 0             # Zum Testen sinnvoll 
pm10:                 # einatembarer_feinstaub
  taktung: 1
  seed: 0
o3:                   #ozon
  taktung: 2
  seed: 0
no2:                  #stickstoffdioxid
  taktung: 3
  seed: 0
so2:                  #schwefeldioxid     
  taktung: 4
  seed: 0
...
...
...
random_sensors:
  taktung: 5
  anzahl_unterschiedlicher_sensoren: 50
  zeitlicher_abstand_zwischen_den_starts: 1
  lifetime_pro_sensor: 40
```


# Fehler die abzufangen sind
- Sensoren die es nicht gibt
- Städte, die es nicht gibt
- stadt gibt es nicht aber sensor
- Testen
- logging
