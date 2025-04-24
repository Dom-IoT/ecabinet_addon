import os
import paho.mqtt.client as mqtt
import re
import requests
import json

MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")


def callback(client, userdata, msg):
    # Regex pour extraire l'ID et l'action
    match = re.match(r"cabinet/(\d+)/(add|remove)", msg.topic)
    if match:
        cabinet_id = match.group(1)
        action = match.group(2)
        item_id = msg.payload.decode()
        # Construire l'URL de la requête backend
        backend_url = f"http://0.0.0.0:8080/items/{cabinet_id}/{action}"

        # Envoyer la requête au backend (à adapter selon votre backend)
        try:
            item_data = {
                "item_id": str(item_id),
                "cabinet_id": cabinet_id,  # Assurez-vous que cette valeur correspond à celle dans l'URL
            }
            response = requests.put(backend_url, json=item_data)
            if response.status_code == 200:
                if(action == 'add'):
                    client.publish(f"cabinet/{cabinet_id}/status", 'OK')
            elif response.status_code == 201:
                client.publish(f"cabinet/{cabinet_id}/status", 'NOK')
                data = response.json()
                client.publish(f"cabinet/{data['good_cabinet']}/status", 'SIGNAL')
            else:
                print(f"Erreur lors de l'envoi de la requête à {backend_url} : Status Code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'envoi de la requête : {e}")
    else:
        print("Topic MQTT non reconnu")


client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = callback


def mqttloop():
    if (client.is_connected() != True):
        reconnect()
    client.loop()
        
def reconnect():
    if (client.connect(MQTT_HOST) == 0):
        print('connected')
        client.subscribe('cabinet/#') #listen all cabinet
    else:
        print('Error connecting mqtt broker')
# Exemple de publication
run = True
while run:
    mqttloop()

client.disconnect()