import paho.mqtt.client as mqtt
import json
import random

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

def on_message(client, userdata, msg):
    """Se apelează de fiecare dată când se primește un mesaj pe Topic-ul abonat."""
    try:
        # Decodează payload-ul din bytes în șir de caractere (string)
        payload_str = msg.payload.decode()
        
        # Dacă este un JSON, îl poți parsa
        # data = json.loads(payload_str)
        
        print("\n--- DATE NOI PRIMITE ---")
        print(f"Topic: {msg.topic}")
        print(f"Calitatea serviciului (QoS): {msg.qos}")
        print(f"Mesaj (Payload): {payload_str}")
        
        # Ex: Afișare specifică a temperaturii
        # print(f"Temperatura raportată: {data['temperatura']} C")
        print("-------------------------")
        
    except Exception as e:
        print(f"Eroare la procesarea mesajului: {e}")


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