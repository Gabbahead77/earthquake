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
