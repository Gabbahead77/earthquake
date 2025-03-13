# -*- coding: utf-8 -*-
"""
Earthquake/Volcano Early Warning Script (Enhanced with Configuration File)

This script loads configuration from config.ini, fetches two RSS feeds (Greece & Italy) in parallel,
and sends alerts via email and Telegram when a threshold is exceeded.
It also launches a web interface with a map and a table displaying recent events.
"""

############################################
# 1) IMPORT SECTION
############################################
import configparser
import requests  # For HTTP requests
import xml.etree.ElementTree as ET  # For XML parsing
import smtplib  # For sending emails
from email.mime.text import MIMEText  # For creating email messages
import telegram  # Telegram Bot (pip install python-telegram-bot)
from flask import Flask, render_template_string  # For the web server
import time
import threading
import folium  # For maps
import datetime

############################################
# 2) LOAD CONFIGURATION FROM config.ini
############################################
config = configparser.ConfigParser()
config.read('config_en.ini')

# General settings
UPDATE_INTERVAL = int(config['General']['update_interval'])
MAX_LIST_ITEMS = int(config['General']['max_list_items'])
MAX_MAP_ITEMS = int(config['General']['max_map_items'])
MAG_THRESHOLD = float(config['General']['mag_threshold'])

# Email settings
SMTP_SERVER = config['Email']['smtp_server']
SMTP_PORT = int(config['Email']['smtp_port'])
SENDER_EMAIL = config['Email']['sender_email']
SENDER_PASSWORD = config['Email']['sender_password']
RECEIVER_EMAIL = config['Email']['receiver_email']
EMAIL_INTERVAL = int(config['Email']['email_interval'])

# Telegram settings
TELEGRAM_BOT_TOKEN = config['Telegram']['bot_token']
TELEGRAM_CHAT_ID = config['Telegram']['chat_id']
TELEGRAM_INTERVAL = int(config['Telegram']['telegram_interval'])

# RSS feeds
RSS_FEED_URL_GREECE = config['RSS']['feed_greece']
RSS_FEED_URL_ITALY  = config['RSS']['feed_italy']

# Map settings
map_center_str = config['Map']['map_center']
MAP_CENTER = [float(x.strip()) for x in map_center_str.split(',')]
MAP_ZOOM_START = int(config['Map']['map_zoom_start'])

# Optional: Regional coordinates (for individual markers, if needed)
if 'Regions' in config:
    REGION_COORDS_GREECE = [float(x.strip()) for x in config['Regions']['greece_coords'].split(',')]
    REGION_COORDS_ITALY  = [float(x.strip()) for x in config['Regions']['italy_coords'].split(',')]
else:
    REGION_COORDS_GREECE = REGION_COORDS_ITALY = None

############################################
# 3) FETCH AND PARSE RSS FEED DATA
############################################
def fetch_quake_data(rss_url, feed_name):
    """
    Fetches the RSS feed from rss_url, parses the fields,
    and adds a 'feed' key indicating the source.
    Returns a list of dictionaries.
    """
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to fetch ({feed_name}): {e}")
        return []

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"[ERROR] XML parsing error ({feed_name}): {e}")
        return []

    channel = root.find('channel')
    if channel is None:
        print(f"[WARN] No <channel> tag in feed {feed_name}.")
        return []

    items = channel.findall('item')
    if not items:
        print(f"[INFO] No <item> tags in feed {feed_name}.")
        return []

    quake_list = []
    for it in items:
        title = it.findtext('title', "")
        link = it.findtext('link', "")
        description = it.findtext('description', "")
        pubDate = it.findtext('pubDate', "")

        magnitude = 0.0
        lat = 0.0
        lon = 0.0
        depth = 0.0
        region = ""
        time_utc = ""

        parts = description.split('<br>')
        clean_parts = [p.strip() for p in parts if p.strip()]

        for p in clean_parts:
            p_lower = p.lower()
            if p_lower.startswith('m '):
                try:
                    magnitude = float(p.split()[1])
                except:
                    pass
            elif 'latitude:' in p_lower:
                lat_str = p.split(':')[1].strip().replace('N','').replace('S','-')
                try:
                    lat = float(lat_str)
                except:
                    pass
            elif 'longitude:' in p_lower:
                lon_str = p.split(':')[1].strip().replace('E','').replace('W','-')
                try:
                    lon = float(lon_str)
                except:
                    pass
            elif 'depth:' in p_lower:
                d_str = p.split(':')[1].strip().replace('km','')
                try:
                    depth = float(d_str)
                except:
                    pass
            elif 'time:' in p_lower:
                time_utc = p.replace('Time:', '').strip()
            elif 'km' in p_lower:
                region = p

        quake_dict = {
            'title': title,
            'link': link,
            'description': description,
            'pubDate': pubDate,
            'magnitude': magnitude,
            'lat': lat,
            'lon': lon,
            'depth': depth,
            'region': region,
            'time_utc': time_utc,
            'feed': feed_name  # Source identifier
        }
        quake_list.append(quake_dict)

    return quake_list

############################################
# 4) EMAIL ALERT SENDING
############################################
def send_email_alert(quake):
    subject = f"Alert ({quake.get('feed','Unknown')}): M{quake['magnitude']:.1f}"
    body = (f"Location: {quake['region']}\n"
            f"Magnitude: {quake['magnitude']}\n"
            f"Depth: {quake['depth']} km\n"
            f"Coordinates: {quake['lat']}, {quake['lon']}\n"
            f"Time (UTC): {quake['time_utc']}\n"
            f"Link: {quake['link']}\n")
    
    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print(f"[INFO] Email alert sent to {RECEIVER_EMAIL} ({quake.get('feed')})")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

############################################
# 5) TELEGRAM BOT ALERT SENDING
############################################
def send_telegram_alert(quake):
    message = (f"Alert ({quake.get('feed','Unknown')})!\n"
               f"Magnitude: {quake['magnitude']}\n"
               f"Depth: {quake['depth']} km\n"
               f"Location: {quake['region']}\n"
               f"Coordinates: {quake['lat']}, {quake['lon']}\n"
               f"Time (UTC): {quake['time_utc']}\n"
               f"Link: {quake['link']}")
    
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"[INFO] Telegram alert sent to Chat {TELEGRAM_CHAT_ID} ({quake.get('feed')})")
    except Exception as e:
        print(f"[ERROR] Failed to send Telegram alert: {e}")

############################################
# 6) WEB INTERFACE WITH FLASK
############################################
app = Flask(__name__)
quake_data = []  # Global list for display

@app.route('/')
def index():
    # Sort events by time (newest first)
    sorted_quakes = sorted(quake_data, key=lambda q: q['time_utc'], reverse=True)
    table_quakes = sorted_quakes[:MAX_LIST_ITEMS]
    map_quakes = sorted_quakes[:MAX_MAP_ITEMS]

    m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM_START)
    for q in map_quakes:
        if q['lat'] == 0.0 and q['lon'] == 0.0:
            continue
        popup_text = (f"Mag: {q['magnitude']}\n"
                      f"Time: {q['time_utc']}\n"
                      f"Location: {q['region']}\n"
                      f"Feed: {q.get('feed','')}")
        color = 'red' if q['magnitude'] >= MAG_THRESHOLD else 'blue'
        folium.Marker(
            location=[q['lat'], q['lon']],
            popup=popup_text,
            icon=folium.Icon(color=color)
        ).add_to(m)

    map_html = m._repr_html_()

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Earthquake/Volcano View</title>
        <style>
          .container {
            display: flex;
            flex-direction: row;
          }
          .table-container {
            flex: 1;
            max-width: 500px;
            overflow-y: auto;
            height: 80vh;
            border: 1px solid #ccc;
            margin-right: 1rem;
          }
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th, td {
            border: 1px solid #ccc;
            padding: 4px 8px;
          }
          .map-container {
            flex: 1;
            height: 80vh;
          }
          .map-container iframe {
            width: 100%;
            height: 100%;
          }
        </style>
    </head>
    <body>
      <h1>Earthquakes & Volcanoes in Greece and Italy</h1>
      <div class="container">
        <div class="table-container">
          <h2>Recent Events (max. {{max_list}})</h2>
          <table>
            <tr>
              <th>UTC Time</th>
              <th>Magnitude</th>
              <th>Location</th>
              <th>Feed</th>
            </tr>
            {% for q in table_quakes %}
            <tr>
              <td>{{ q.time_utc }}</td>
              <td>{{ q.magnitude }}</td>
              <td>{{ q.region }}</td>
              <td>{{ q.feed }}</td>
            </tr>
            {% endfor %}
          </table>
        </div>
        <div class="map-container">
          {{ map_html|safe }}
        </div>
      </div>
    </body>
    </html>
    """
    return render_template_string(
        html_template,
        table_quakes=table_quakes,
        max_list=MAX_LIST_ITEMS,
        map_html=map_html
    )

############################################
# 7) PROCESSING FEEDS IN PARALLEL
############################################
latest_time_utc = {"greece": None, "italy": None}
last_email_time = {"greece": 0, "italy": 0}
last_telegram_time = {"greece": 0, "italy": 0}

def process_feed(feed_name, rss_url):
    global quake_data, latest_time_utc, last_email_time, last_telegram_time
    dt_format = "%d-%b-%Y %H:%M:%S"

    while True:
        print(f"[INFO] Fetching new data for {feed_name} ...")
        quakes = fetch_quake_data(rss_url, feed_name)
        
        if quakes:
            # Process only the first event in the feed
            top = quakes[0]
            time_str = top['time_utc'].replace('(UTC)', '').strip()
            try:
                dt_obj = datetime.datetime.strptime(time_str, dt_format)
            except ValueError:
                dt_obj = None

            if dt_obj:
                if (latest_time_utc[feed_name] is None) or (dt_obj > latest_time_utc[feed_name]):
                    print(f"[INFO] NEW event found for {feed_name}.")
                    if top['magnitude'] >= MAG_THRESHOLD:
                        now = time.time()
                        send_email_alert(top)
                        last_email_time[feed_name] = now
                        send_telegram_alert(top)
                        last_telegram_time[feed_name] = now
                    latest_time_utc[feed_name] = dt_obj

                elif dt_obj == latest_time_utc[feed_name]:
                    if top['magnitude'] >= MAG_THRESHOLD:
                        now = time.time()
                        if (now - last_email_time[feed_name]) > EMAIL_INTERVAL:
                            print(f"[INFO] Repeated email alert for {feed_name}")
                            send_email_alert(top)
                            last_email_time[feed_name] = now
                        if (now - last_telegram_time[feed_name]) > TELEGRAM_INTERVAL:
                            print(f"[INFO] Repeated Telegram alert for {feed_name}")
                            send_telegram_alert(top)
                            last_telegram_time[feed_name] = now
                    else:
                        print(f"[INFO] Same event for {feed_name}, but below threshold.")
                else:
                    print(f"[INFO] Top event for {feed_name} is older than the last known timestamp.")
            else:
                print(f"[WARN] Could not parse timestamp for {feed_name}.")
        else:
            print(f"[INFO] No data received for {feed_name}.")

        # Add new events to the global list (simple duplicate check)
        for q in quakes:
            if q not in quake_data:
                quake_data.append(q)

        time.sleep(UPDATE_INTERVAL)

############################################
# 8) START MAIN PROGRAM / THREADS
############################################
def start_flask_app():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    greece_thread = threading.Thread(target=process_feed, args=("greece", RSS_FEED_URL_GREECE))
    italy_thread  = threading.Thread(target=process_feed, args=("italy", RSS_FEED_URL_ITALY))
    greece_thread.daemon = True
    italy_thread.daemon = True
    greece_thread.start()
    italy_thread.start()

    while True:
        time.sleep(1)
