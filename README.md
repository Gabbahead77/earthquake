# Earthquake & Volcano Warning App

Dieses Projekt ist ein Frühwarnsystem für Erdbeben und Vulkanausbrüche. Es lädt RSS-Feeds (für Griechenland und Italien) und sendet bei Überschreitung eines definierten Magnitudenschwellwerts Warnmeldungen per E-Mail und Telegram. Gleichzeitig wird eine Weboberfläche mit einer interaktiven Karte (via Folium) und einer Tabelle der letzten Ereignisse bereitgestellt.

---

## Funktionen

- **RSS-Feed-Abfrage:**  
  Das System lädt und parst RSS-Feeds aus Griechenland und Italien.

- **Alarmierung:**  
  Automatische Warnmeldungen werden per E-Mail und Telegram versendet, wenn ein Ereignis einen bestimmten Magnitudenschwellwert überschreitet.

- **Weboberfläche:**  
  Eine interaktive Karte und eine Tabelle zeigen die letzten Ereignisse an.

- **Konfigurierbar:**  
  Alle Einstellungen (z. B. Update-Interval, E-Mail- und Telegram-Einstellungen, RSS-Feed-URLs, Kartenkonfiguration) werden über die `config.ini` gesteuert. Nutzer können diese Parameter individuell anpassen, um das Warnsystem ihren Bedürfnissen anzupassen.

---

## Einrichtung

### 1. Voraussetzungen

- **Python 3**
- Die benötigten Pakete (siehe `requirements.txt`), z. B.:
  - Flask
  - requests
  - folium
  - python-telegram-bot
  - Weitere Pakete, die in `requirements.txt` aufgelistet sind.

### 2. Konfiguration

Alle Konfigurationseinstellungen werden in der Datei `config.ini` vorgenommen. Wichtige Punkte:

- **Allgemein:**  
  Legt Update-Intervall, maximale Anzahl an anzuzeigenden Einträgen (Tabelle & Karte) sowie den Magnitudenschwellwert fest.

- **E-Mail:**  
  Trage hier deinen SMTP-Server, Port, Absender- und Empfängeradressen sowie das Passwort ein.

- **Telegram:**  
  Füge deinen Telegram-Bot-Token und die Chat-ID ein (siehe unten).

- **RSS:**  
  Hier werden die URLs der RSS-Feeds für Griechenland und Italien eingetragen.

- **Karte:**  
  Definiert den Mittelpunkt und den Zoom-Level der Karte.

- **Regionen (optional):**  
  Koordinaten, die für individuelle Marker genutzt werden können.

### 3. Telegram-Bot erstellen

Um Warnmeldungen per Telegram zu versenden, benötigst du einen Telegram-Bot:

1. **Öffne Telegram** und suche nach **@BotFather**.
2. **Starte einen Chat** mit BotFather und sende den Befehl `/newbot`.
3. **Folge den Anweisungen:**  
   Du wirst nach einem Namen und einem Benutzernamen für deinen Bot gefragt.
4. **Erhalte den Token:**  
   BotFather sendet dir einen Bot-Token. Füge diesen in der `config.ini` unter `bot_token` ein.
5. **Ermittle deine Chat-ID:**  
   Um deine Chat-ID zu erhalten, kannst du beispielsweise [@userinfobot](https://telegram.me/userinfobot) verwenden oder den Bot so programmieren, dass er dir beim ersten Kontakt die Chat-ID zurückliefert.

### 4. Anwendung starten

- **Unter Windows:**  
  Nutze die bereitgestellte `start.bat`:
  ```bat
  @echo off
  REM Starte das Python-Skript in einem neuen Fenster
  start "" python earthquake_warning_app.py
  REM Warte 5 Sekunden, damit der Server hochfährt
  timeout /t 5
  REM Öffne den Browser mit der lokalen Weboberfläche
  start http://127.0.0.1:5000
  
- **Alternativ:**
Starte die Anwendung direkt via:
bash
Kopieren
python earthquake_warning_app.py


### English Version ###

# Earthquake & Volcano Early Warning System

This project is an early warning system for earthquakes and volcanic eruptions. It fetches RSS feeds (from Greece and Italy) in parallel and sends alerts via email and Telegram when a configured magnitude threshold is exceeded. Additionally, it launches a web interface displaying an interactive map (using Folium) and a table of recent events.

---

### Features

- **RSS Feed Parsing:**  
  The system fetches and parses RSS feeds from Greece and Italy.

- **Alerting:**  
  Automatically sends alerts via email and Telegram when an event exceeds the specified magnitude threshold.

- **Web Interface:**  
  Provides an interactive map and a table showing the latest events.

- **Configuration:**  
  All settings (e.g., update intervals, email and Telegram configurations, RSS feed URLs, map settings, etc.) are managed via the `config.ini` file. Users can customize these parameters to suit their needs.

---

## Setup

### 1. Requirements

- **Python 3**
- The required packages (see `requirements.txt`), for example:
  - Flask
  - requests
  - folium
  - python-telegram-bot
  - (and others listed in `requirements.txt`)

### 2. Configuration

All configuration settings are specified in the `config.ini` file. Key points include:

- **General:**  
  Sets the update interval, maximum number of items for the table and map, and the magnitude threshold.

- **Email:**  
  Provide your SMTP server details, port, sender and receiver emails, and password.

- **Telegram:**  
  Enter your Telegram Bot token and chat ID (see instructions below).

- **RSS:**  
  Enter the URLs of the RSS feeds for Greece and Italy.

- **Map:**  
  Defines the center and zoom level of the map.

- **Regions (optional):**  
  Coordinates that can be used for individual markers.

### 3. Creating a Telegram Bot

To send alerts via Telegram, you need a Telegram Bot. Here’s how to create one:

1. **Open Telegram** and search for **@BotFather**.
2. **Start a chat** with BotFather and send the command `/newbot`.
3. **Follow the instructions:**  
   You will be asked for a name and username for your bot.
4. **Obtain the token:**  
   BotFather will send you a bot token. Insert this token into `config.ini` under `bot_token`.
5. **Get your Chat ID:**  
   To obtain your Chat ID, you can use a bot (e.g., [@userinfobot](https://telegram.me/userinfobot)) or implement a simple script to retrieve it.

### 4. Running the Application

- **On Windows:**  
  Use the provided `start.bat` file:
  ```bat
  @echo off
  REM Start the Python script in a new window
  start "" python earthquake_warning_app.py
  REM Wait 5 seconds for the server to start
  timeout /t 5
  REM Open the browser with the local web interface
  start http://127.0.0.1:5000  
  
- **Alternatively:**  
	Run the application directly:
	python earthquake_warning_app.py
	Then open your browser at http://127.0.0.1:5000.
