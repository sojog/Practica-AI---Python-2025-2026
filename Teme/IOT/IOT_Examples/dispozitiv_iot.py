import paho.mqtt.client as mqtt
import time
import random


# --- Configurarea Brokerului Public ---
BROKER = "broker.hivemq.com"  # Un broker public de încredere
PORT = 1883
TOPIC = "curs/iot/temperatura_demo" # Alege un topic unic

# --- Funcții Callback (Opțional, dar bun pentru debug) ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Dispozitivul (Publicator) s-a conectat cu succes la Broker.")
    else:
        print(f"Conexiune eșuată, cod de eroare: {rc}")






# --- Setare Client ---
client = mqtt.Client(client_id="Python_Publicator_" + str(random.randint(1, 1000)))
client.on_connect = on_connect

# --- Logica Principală ---
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # Rulează în fundal pentru a menține conexiunea

    while True:
        # 1. Generează Date Simulate
        temperatura = round(random.uniform(20.0, 30.0), 2)
        
        # 2. Creează Payload (format JSON simplu)
        payload = f'{{"timestamp": "{time.strftime("%Y-%m-%d %H:%M:%S")}", "temperatura": {temperatura}}}'
        
        # 3. Publică Mesajul
        client.publish(TOPIC, payload, qos=1)
        print(f"[TRIMIS] Topic: {TOPIC} | Payload: {payload}")
        
        time.sleep(5) # Așteaptă 5 secunde înainte de a trimite următorul mesaj

except KeyboardInterrupt:
    print("\nSimularea dispozitivului oprită de utilizator.")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"A apărut o eroare: {e}")