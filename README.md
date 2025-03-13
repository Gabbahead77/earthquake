# Earthquake & Volcano Warning App

Dieses Projekt ist ein Frühwarnsystem für Erdbeben und Vulkanausbrüche. Es lädt RSS-Feeds (für Griechenland und Italien) und sendet bei Überschreitung eines definierten Magnitudenschwellwerts Warnmeldungen per E-Mail und Telegram. Gleichzeitig wird eine Weboberfläche mit einer Karte (via Folium) und einer Tabelle der letzten Ereignisse bereitgestellt.

## Features

- **RSS-Feed-Abfrage:**  
  Lädt und parst RSS-Feeds aus Griechenland und Italien.

- **Alarmierung:**  
  Versendet automatische Warnungen per E-Mail und Telegram, wenn ein Ereignis einen bestimmten Schwellenwert überschreitet.

- **Weboberfläche:**  
  Zeigt eine interaktive Karte und eine Tabelle mit den letzten Ereignissen an.

- **Konfigurierbar:**  
  Alle Einstellungen (z. B. Update-Interval, E-Mail- und Telegram-Einstellungen, RSS-Feed-URLs, Kartenkonfiguration) werden über die `config.ini` gesteuert.
  
## Englisch Version   

# Earthquake & Volcano Early Warning System

This project is an early warning system for earthquakes and volcanic eruptions. It fetches RSS feeds (from Greece and Italy) in parallel and sends alerts via email and Telegram when a configured magnitude threshold is exceeded. Additionally, it launches a web interface displaying a map and a table of recent events.

## Features

- **RSS Feed Parsing:**  
  Fetches and parses RSS feeds from Greece and Italy.

- **Alerting:**  
  Automatically sends alerts via email and Telegram when an event exceeds the specified magnitude threshold.

- **Web Interface:**  
  Provides an interactive map (using Folium) and a table of recent events.

- **Configuration:**  
  All settings (update intervals, email and Telegram configurations, RSS feed URLs, map settings, etc.) are managed via `config.ini`.


