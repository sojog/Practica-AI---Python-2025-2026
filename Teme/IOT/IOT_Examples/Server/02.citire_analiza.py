import paho.mqtt.client as mqtt
import json
import random
import pandas as pd
import json
import sqlite3

# --- Configurarea Brokerului Public ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "curs/iot/temperatura_demo" # ATENȚIE: Trebuie să fie același Topic ca la Publicator

# --- Funcții Callback ---

def on_connect(client, userdata, flags, rc):
    """Se apelează la conectarea la broker."""
    if rc == 0:
        print("Aplicația (Abonat) s-a conectat cu succes la Broker.")
        client.subscribe(TOPIC) # Abonează-te imediat după conectare
        print(f"Abonat la Topic: {TOPIC}")
    else:
        print(f"Conexiune eșuată, cod de eroare: {rc}")


def perform_analysis():
    """Funcție pentru a folosi datele colectate în Pandas."""
    global received_data
    
    # 1. Crearea DataFrame-ului
    df = pd.DataFrame(received_data)
    
    print("\n" + "="*50)
    print("ANALIZA DATELOR CU PANDAS")
    print("="*50)
    print("DataFrame-ul complet:")
    print(df)
    
    # 2. Analiză de bază
    temp_medie = df['temperatura'].mean()
    temp_max = df['temperatura'].max()
    
    print(f"\nTemperatura Medie: {temp_medie:.2f} C")
    print(f"Temperatura Maximă: {temp_max:.2f} C")
    print("="*50)


    # 3. Salvarea Datelor în Baza de Date SQLite
    try:
        # Creează/Conectează la baza de date (va crea fișierul 'iot_demo.db')
        conn = sqlite3.connect('iot_demo.db') 
        
        # Salvează DataFrame-ul într-un tabel numit 'senzori_temp'
        df.to_sql('senzori_temp', conn, if_exists='replace', index=False)
        
        # Verifică salvarea (Opțional)
        print("\nVerificarea datelor din baza de date:")
        query = pd.read_sql("SELECT * FROM senzori_temp", conn)
        print(query)
        
        conn.close()
        print("Datele au fost salvate cu succes în 'iot_demo.db'.")
        
    except Exception as e:
        print(f"Eroare la salvarea în SQLite: {e}")


# Stocarea datelor:
received_data = []
DATA_LIMIT = 5 # Stochează primele 5 mesaje pentru analiză

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        data = json.loads(payload_str) # Parsarea JSON-ului
        
        # 1. Stocarea datelor în listă
        received_data.append(data)
        print(f"Mesaj adăugat: {data['temperatura']} C. Total: {len(received_data)}")
        
        # 2. Dacă s-a atins limita, oprește ascultarea și începe analiza
        if len(received_data) >= DATA_LIMIT:
            client.loop_stop()
            client.disconnect()
            
            # Apelarea funcției de analiză
            perform_analysis()
            
    except Exception as e:
        print(f"Eroare la procesarea mesajului: {e}")


# def on_message(client, userdata, msg):
#     """Se apelează de fiecare dată când se primește un mesaj pe Topic-ul abonat."""
#     try:
#         # Decodează payload-ul din bytes în șir de caractere (string)
#         payload_str = msg.payload.decode()
        
#         # Dacă este un JSON, îl poți parsa
#         # data = json.loads(payload_str)
        
#         print("\n--- DATE NOI PRIMITE ---")
#         print(f"Topic: {msg.topic}")
#         print(f"Calitatea serviciului (QoS): {msg.qos}")
#         print(f"Mesaj (Payload): {payload_str}")
        
#         # Ex: Afișare specifică a temperaturii
#         # print(f"Temperatura raportată: {data['temperatura']} C")
#         print("-------------------------")
        
#     except Exception as e:
#         print(f"Eroare la procesarea mesajului: {e}")


# --- Setare Client ---
client = mqtt.Client(client_id="Python_Abonat_" + str(random.randint(1, 1000)))
client.on_connect = on_connect
client.on_message = on_message

# --- Logica Principală ---
try:
    client.connect(BROKER, PORT, 60)
    
    # Rulează o buclă infinită pentru a asculta permanent mesaje noi
    client.loop_forever() 

except KeyboardInterrupt:
    print("\nAplicația oprită de utilizator.")
    client.disconnect()
except Exception as e:
    print(f"A apărut o eroare: {e}")