#!/usr/bin/with-contenv bashio

MQTT_HOST=$(bashio::services mqtt 'host')
MQTT_USER=$(bashio::services mqtt 'username')
MQTT_PASSWORD=$(bashio::services mqtt 'password')


export MQTT_HOST MQTT_USER MQTT_PASSWORD

python automations.py & uvicorn main:app --host 0.0.0.0 --port 8080
