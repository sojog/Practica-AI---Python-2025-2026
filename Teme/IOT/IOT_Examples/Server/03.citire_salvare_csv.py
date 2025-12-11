import paho.mqtt.client as mqtt
import json
import pandas as pd
import sqlite3
import random

# --- Configurare ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "curs/iot/temperatura_demo" 
CSV_FILE = "temperaturi_raw.csv"
DB_FILE = "iot_data.db"
TABLE_NAME = "senzori_temperatura"

# --- Funcții de Salvare ---
def save_to_csv(data):
    """Adaugă o nouă citire la un fișier CSV existent."""
    try:
        df_new = pd.DataFrame([data])
        # Verifică dacă fișierul există. Dacă nu, scrie cu header; dacă da, adaugă fără header.
        mode = 'a' if pd.io.common.file_exists(CSV_FILE) else 'w'
        header = not pd.io.common.file_exists(CSV_FILE)
        df_new.to_csv(CSV_FILE, mode=mode, header=header, index=False)
    except Exception as e:
        print(f"Eroare la salvarea în CSV: {e}")

def save_to_db(data):
    """Adaugă o nouă citire la baza de date SQLite."""
    try:
        conn = sqlite3.connect(DB_FILE)
        df_new = pd.DataFrame([data])
        # Adaugă datele. if_exists='append' este cheia.
        df_new.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
        conn.close()
    except Exception as e:
        print(f"Eroare la salvarea în DB: {e}")

# --- Funcții Callback MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Colector conectat cu succes la Broker.")
        client.subscribe(TOPIC)
        print(f"Abonat la Topic: {TOPIC}")
    else:
        print(f"Conexiune eșuată, cod de eroare: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        data = json.loads(payload_str)
        
        # Asigură-te că temperatura este un float pentru analiză
        data['temperatura'] = float(data['temperatura']) 
        
        print(f"[RECEPTIE] {data['timestamp']} | Temp: {data['temperatura']:.2f} C")
        
        # Salvare persistentă
        save_to_csv(data)
        save_to_db(data)
        
    except Exception as e:
        print(f"Eroare la procesarea/salvarea mesajului: {e}")

# --- Rulare Principală ---
client = mqtt.Client(client_id="Python_Collector_" + str(random.randint(1, 1000)))
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    print("Colectorul de date rulează. Apasă Ctrl+C pentru a opri.")
    client.loop_forever() # Ascultă constant mesaje

except KeyboardInterrupt:
    print("\nColector oprit de utilizator.")
    client.disconnect()
except Exception as e:
    print(f"Eroare critică: {e}")