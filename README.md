# Dokumentation - Datensimulation

## Anwender Dokumentation

### Allgemein

Im Folgenden wird die Datensimulation beschrieben. Diese kann unter anderem Wetterdaten aus verschiedenen Städten ausgeben. Das Programm lässt sich sowohl über eine GUI, als auch über das Terminal ausführen. Hier werden beide Methoden genau beschrieben. Da die Konfiguration über die GUI einfacher ist, dient diese als Leitfaden.

### Setup

Um die Datensimulation starten zu können, muss das Projekt zuerst aufgesetzt werden. Dafür geht man folgendermaßen vor:

1. [Python Version 11](https://www.python.org/downloads/) installieren
2. Das Repository von Github clonen
`git clone https://github.com/Umweltrechner-HSRM/data-simulation.git`
3. Die Datei `config.yaml.dist` in `config.yaml` umbenennen
4. Alle benötigten Module installieren. Hierfür muss man sich im Ordner `data-simulation` befinden und dort
`pip install -r requirements.txt` ausführen

### GUI starten

Um die grafische Oberfläche zu starten, muss lediglich die Datei `konfiguration_gui.py` aufgerufen werden, welche sich im `src` Ordner befindet. Dies geht mit folgendem Befehl `python ./src/konfiguration_gui.py`

### Control Panel

Das Control Panel lässt sich über den Reiter `Control Panel` erreichen und hat die Aufgabe, die Anwendung zentral zu steuern.

![Control Panel](./pictures/ControlPanel.png)

### Anwendung starten / stoppen

GUI:

> Unter der Überschrift `Datensimulation status` lässt sich die Anwendung starten / stoppen, indem man den Knopf `Anwendung starten` / `Anwendung stoppen` drückt.

Terminal:

> Hier muss die `main.py` ausgeführt werden, welche sich im `src` Ordner befindet. Der Befehl dazu lautet: `python ./src/main.py`. Die Anwendung läuft jetzt so lange weiter, bis ein Keyboard Interrupt ausgelöst wird, welches die Anwendung stoppt. Dies funktioniert in Windows mit der Tastenkombination `Strg + C`.

### Sensoren zentral aktivieren und deaktivieren

Es gibt drei unterschiedliche Sensorarten (Stadt-Sensoren, Zufällige Städte, Heger Sensor). Diese können zentral deaktiviert / aktiviert werden.

GUI:

> Unter der Überschrift `Aktivierte Sensoren` muss ein Haken in alle Felder gesetzt werden, die aktiv sein sollen. Danach muss auf Speichern geklickt werden, damit die Veränderungen übernommen werden (Dies ist bei allen weiteren Einstellungen ebenfalls der Fall und wird nicht noch einmal erwähnt)

Terminal:

> In der `config.yaml` kann man unter `aktive_sensoren` die einzelnen Sensorwerte auf true / false setzen.

### Logging

Wichtige Events, wie versendete Daten oder neu registrierte Sensordaten werden geloggt.

GUI:

> Unter `Datensimulation Logs` sollten die Logs angezeigt werden, sobald die Anwendung gestartet ist.

Terminal:

> Im Ordner `logs` befindet sich (nachdem das Programm gestartet wurde) eine Datei namens `data-simulation.log`, welche die logs des Programmdurchlaufs enthält.

### Stadt Sensoren

Die Stadt Sensoren lassen sich mit dem Reiter `Stadt-Sensoren` erreichen. Hier kann man explizit gewünschte Städte und ihre Sensoren festlegen, deren Daten empfangen werden sollen. Diese einzelnen Sensoren lassen sich weiter konfigurieren. Zum einen kann angegeben werden, in was für einem Sekundentakt Daten versendet werden sollen. Zum anderen besteht die Möglichkeit, einen Seed anzugeben, welcher künstliche Schwankungen bei den Werten erzeugt, indem eine Zahl in der Range -seed zu +seed gewählt und mit dem echten Wert verrechnet wird.

![stadt-sensoren](./pictures/stadt-sensoren.png)

### Stadt Sensor aktivieren / deaktivieren

Hier lässt sich der Sensor aktivieren und deaktivieren. Die Funktionsweise ist hierbei identisch mit dem vorherigen Block [Sensoren zentral aktivieren und deaktivieren](#sensoren-zentral-aktivieren-und-deaktivieren).

### Stadt mit Sensoren hinzufügen

GUI:

> Unter der Überschrift “Stadt-Sensoren Konfiguration” kann man in Json Syntax mehrere Städte einfügen. Die Stadt enthält dann eine Liste mit allen Sensoren, die später gesendet werden sollen. Dies wird an einem Beispiel ersichtlich:

```json
[
 {
   "Wiesbaden": [
   {
    "seed": 1,
    "sensor": "pm10",
    "taktung": 5,
   },
   {
    "seed": 3,
    "sensor": "t",
    "taktung": 10,
   }
  ]
 },
   "Mainz": [
   {
    "seed": 1,
    "sensor": "t",
    "taktung": 5,
   }
  ]
 }
]
```

> Hier senden nun die Städte Wiesbaden und Mainz. In  Mainz sendet der Sensor t (Temperatur) und in Wiesbaden sendet der Sensor pm10 (einatembarer Feinstaub) und t. Hierbei ist zu beachten, dass der Sensor auf welchen verwiesen wird (in dem Beispiel wären das `pm10` und `t`) auch in der `Sensor Information Map` hinterlegt sein muss. Darauf wird bei den Einstellungen unter dem Punkt `Sensor Information Map` eingegangen.`

Terminal:

> In der `config.yaml` muss der Punkt `city_configuration` bearbeitet werden. Das Prinzip ist das gleiche, allerdings muss statt der Json Syntax eine yaml Syntax verwendet werden.

### Sensoren der Stadt konfigurieren (Seed und Taktung)

Die Sensoren einer Stadt können entkoppelt und individuell konfiguriert werden. Was Seed und Taktung machen, wurde bereits erklärt und wird nicht noch einmal erwähnt.

GUI:

> Hier müssen (wie im vorherigen Beispiel gezeigt) in Json die Attribute `seed` und `taktung` bearbeitet werden. Im vorherigen Beispiel hätte Wiesbaden einen t sensor, welcher alle 10 Sekunden Daten versendet und den versendeten Wert mit einem Seed von 3. Zusätzlich hat Wiesbaden den `pm10` Sensor, welcher alle 5 Sekunden Daten mit einem Seed von 1 versendet.

Terminal:

> Hier gilt dasselbe wie beim Punkt `Stadt mit Sensoren hinzufügen`.

### Zufällige Städte

Dieser Sensor lässt sich unter dem Reiter ‘Zufällige Städte’ erreichen. Der Sensor hat die Aufgabe, zufällig neue Städte zu finden und die Sensordaten der Stadt an das Backend zu schicken. Die Städte werden  hierbei aus einer Liste ausgewählt. Auch hier gibt es wieder Konfigurationsmöglichkeiten.

![Zufällige Städte1](./pictures/Zuf%C3%A4lligeSt%C3%A4dte1.png)
![Zufällige Städte2](./pictures/Zuf%C3%A4lligeSt%C3%A4dte2.png)

### Zufällige Städte aktivieren / deaktivieren

Hier lässt sich der Sensor aktivieren und deaktivieren. Die Funktionsweise ist hierbei identisch mit dem vorherigen Block `Sensoren zentral aktivieren und deaktivieren`.

### Zufällige Städte konfigurieren

Hier gibt es folgende Konfigurationsmöglichkeiten:

1. `Taktung`: wurde bereits zuvor erklärt
2. `Anzahl unterschiedlicher Städte`: sagt aus wie viele neue zufällige Städte erzeugt werden sollen
3. `Abstand zwischen den Starts der Städte`: Der Name spricht für sich
4. `Lebenszeit einer Stadt`: Die Stadt soll nach einem gewissen Zeitraum das versenden von Nachrichten beenden

GUI:

Alle eben genannte Attribute können unter dem Punkt `Zufällige Städte Konfiguration` angepasst werden.

Terminal:

In der `config.yaml` kann man den Punkt `random_citys_sensors` bearbeiten. Auch hier kann wieder das gleiche Prinzip angewandt werden. Die Attribute heißen zwar ein bisschen anders, werden aber aus dem Kontext ersichtlich.

### Neue potentielle zufällige Stadt hinzufügen

Aus dieser Liste werden neue Städte gewählt, die noch nicht im Backend registriert wurden. Diese Liste kann man folgendermaßen erweitern.

GUI:

> Unter dem Punkt: `Liste aller zufälligen Städte`wird die Stadt in die Liste eingefügt. Es kann sein, dass zu einer Stadt keine Sensordaten vorliegen. In diesem Fall kann die Stadt nicht aufgerufen werden.

Terminal:

> In der `config.yaml` kann man unter dem Punkt `random_citys` neue Städte in die Liste einfügen.

### Heger Sensor

Der Heger Sensor lässt sich unter dem Reiter `Heger Sensor` finden. Dieser soll sehr schnell wechselnde Sensordaten modellieren, um einen nahezu eckigen Graphen zu erzeugen. Auch hier lassen sich Konfigurationen vornehmen.

![Heger Sensor](./pictures/HegerSensor.png)

### Heger Sensor aktivieren / deaktivieren

Hier lässt sich der Sensor aktivieren und deaktivieren. Die Funktionsweise ist hierbei identisch mit dem vorherigen Block `Sensoren zentral aktivieren und deaktivieren`.

### Heger Sensor konfigurieren

Der Heger Sensor lässt sich folgendermaßen konfigurieren. Es muss ein min und max Wert angegeben werden, der gesendet wird. Über die Taktung (in Sekunden) wird die Intervalllänge festgelegt. Des Weiteren werden dem Sensor unter `Sensorname` ein Name und unter `Stadt` eine Stadt zugeteilt. Unter `Sensor-Art` muss auf einen Sensor verwiesen werden, welcher auch in der Sensor Information Map zu finden ist.

GUI:

> Alle oben genannten Werte können in der GUI unter dem Punkt `Heger Konfiguration` angepasst werden.

Terminal:

> In der `config.yaml` können die gleichen Konfigurationen unter dem Punkt `heger_spezial` verwendet werden. Die Namen sind nicht deckungsgleich, jedoch aus dem Kontext ersichtlich.

### Einstellungen

Hier können Einstellungen vorgenommen werden, welche die allgemeine Anwendung und nicht die Sensoren betreffen.

![Einstellungen1](./pictures/Einstellungen1.png)
![Einstellungen2](./pictures/Einstellungen2.png)

### AQICN API Konfiguration

Hier wird der Token zu der Wetter Schnittstelle von Aqicn abgelegt.

GUI:

> Unter `AQICN API Konfiguration` einen validen Token einfügen.

Terminal:

> In der `config.yaml` den Wert bei ‘aqicn_key’ anpassen.

### Backend Konfiguration

Hier wird die Konfiguration zum Backend geregelt. Es gibt folgende Attribute:

1. `Username`: Benutzername für Verifizierung
2. `Passwort`: Passwort für Verifizierung
3. `Keycloak Url`: Nötig zur Authentifizierung
4. `API base Url`: Basis Url, aus welcher später andere Url’s abgeleitet werden
5. `API ws Url`: Url zu dem Websocket an den gesendet wird
6. `Send response path`: Pfad an den Werte geschickt werden sollen

GUI:

> Alle diese Attribute lassen sich unter dem Punkt `Backend Konfiguration` anpassen.

Terminal:

> Die gleichen Konfigurationen lassen sich auch in der `config.yaml` unter dem Punkt `backend` vornehmen. Auch hier sind die Attributnamen nicht deckungsgleich, aber aus dem Kontext ersichtlich.

### Logging

Hier kann das Loglevel ausgewählt werden. Es gibt folgende Auswahlmöglichkeiten:

- `DEBUG`: Diese Ebene wird verwendet, um detaillierte Informationen über die internen Vorgänge der Anwendung bereitzustellen. Dies wird in der Regel zu Debugging-Zwecken verwendet.
- `INFO`: Diese Ebene wird verwendet, um Informationen über den normalen Betrieb der Anwendung bereitzustellen. Dies könnte Nachrichten umfassen, die anzeigen, dass eine bestimmte Funktion aufgerufen wurde oder ein bestimmter Codeabschnitt erreicht wurde.
- `WARNING`: Diese Ebene wird verwendet, um ein mögliches Problem anzuzeigen. Dies könnte Situationen umfassen, in denen eine Anwendung weiterhin ausgeführt wird, aber etwas Unerwartetes passiert ist.
- `ERROR`: Diese Ebene wird verwendet, um ein ernstes Problem anzuzeigen, das aufgetreten ist. Dies könnte Situationen umfassen, in denen die Anwendung eine bestimmte Operation nicht ausführen kann oder in denen eine Ausnahme ausgelöst wurde.
- `CRITICAL`: Diese Ebene wird verwendet, um ein kritisches Problem anzuzeigen, das aufgetreten ist. Dies könnte Situationen umfassen, in denen die Anwendung nicht mehr verwendbar ist oder in denen Daten verloren gegangen sind.

GUI:

> Unter dem Punkt `Logging` beim Dropdown das gewünschte Loglevel auswählen.

Terminal:

> In der `config.yaml` muss unter dem Punkt `log_level` das gewünschte Log-Level als String gesetzt werden.

### Sensor Information Map

In der Anwendung wird nicht mit vollständigen Sensornamen gearbeitet, stattdessen werden Abkürzungen verwendet. Diese verweisen auf die `Sensor Information Map`, welche hier genauer beschrieben wird.

GUI:

> Unter dem Punkt  `Sensor Information Map` lassen sich Einstellungen vornehmen. Dies wird am besten anhand eines Beispiels erklärt:

```json
{
  "co2": {   
    "description": "Informationen über Kohlenstoffmonoxidgehalt",
    "name": "kohlenmonoxid",
    "unit": "µg/m3"
 },
 "t": {   
    "description": "Informationen über die Temperatur",
    "name": "temperatur",
    "unit": "°C"
 }
}
```

> In diesem Beispiel wird die Abkürzung `co2`, genauer definiert. `description` wäre hierbei eine ausführliche Beschreibung `name`, der ausgeschriebene Name der Sensorart und `unit` die Messeinheit. Unter Beibehaltung der Syntax lassen sich so neue Sensoren hinzufügen und bestehende verändern.

Terminal:

> In der `config.yaml` kann man die gleichen Konfigurationen unter dem Punkt ‘sensor_details’ vornehmen. Allerdings ist hier wieder zu beachten, dass eine yaml statt einer json syntax verwendet werden muss.

## Technische Dokumentation

### Sensor Namen

Die Namen der verwendeten Daten haben folgenden Aufbau: <Stadt_Sensorart_UmweltstationID> 
 z.B 'Wiesbaden_temperatur_10869'

![Architektur](./pictures/datensimulation_architektur.png)

Bild