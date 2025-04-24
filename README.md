# DomIoT - eCabinet
eCabinet is a smart cabinet system that allows you to control and monitor your cabinet's contents remotely.
### Requirements
You need to have the Mosquitto broker add-on and the MQTT integration install on your system. This will create the mqtt broker which will be used by the cabinets to communicate with HomeAssistant.
### UserInterface
To add user interface for adding new items in the cabinet and showing the number of items copy these lines into configuration.yaml : 
```yaml
input_text:
  item_id:
    name: "Item ID"
    icon: mdi:identifier
  item_name:
    name: "Item Name"
  cabinet_id:
    name: "Cabinet ID"
    icon: mdi:inbox

rest_command:
  ecabinet_post_item:
    url: "http://localhost:8001/items"
    method: "POST"
    headers:
      Content-Type: "application/json"
    payload: >
      {
        "item_id": "{{ states('input_text.item_id') }}",
        "item_name": "{{ states('input_text.item_name') }}",
        "cabinet_id": {{ states('input_text.cabinet_id') }},
        "absent": 0
      }
rest:
  - resource: http://localhost:8001/items/
    method: "GET"
    scan_interval: 60  # Mise à jour toutes les 60 secondes (ajustez selon vos besoins)
    sensor:
      - name: Item List
        json_attributes: ""
        value_template: "{{ value_json | count }}" # 
```
then in the configuration editor of your dashboard add : 
```yaml
views:
  - name: Example
    cards:
      - type: entities
        entities:
          - type: button
            tap_action:
              action: call-service
              service: rest_command.ecabinet_post_item
            name: Ajouter un élément au placard connecté
          - input_text.item_id
          - input_text.item_name
          - input_text.cabinet_id
      - graph: none
        type: sensor
        entity: sensor.item_list
        detail: 1
        name: Nombre d'items dans les placards
    title: Aidant

```