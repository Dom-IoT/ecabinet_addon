# DomIoT - eCabinet
eCabinet is a smart cabinet system that allows you to control and monitor your cabinet's contents remotely.
### UserInterface
To add user interface for adding new items in the cabinet copy these lines into configuration.yaml : 
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
  envoyer_item:
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
```