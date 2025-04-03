import sqlite3
import fastapi
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class Item(BaseModel):
    item_id: str
    item_name: str
    cabinet_id: int
    absent: int

if not os.path.exists('db.sqlite'):
    # Create the db.sqlite since it does not exists
    open('db.sqlite', 'w').close()
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS items (item_id TEXT UNIQUE, item_name TEXT UNIQUE, cabinet_id INTEGER, absent INTEGER)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("a","salt", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("b","pepper", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("c","sugar", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("d","flour", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("e","rice", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("f","pasta", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("g","vinegar", 1, 0)')
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES ("o","olive oil", 1, 0)')
    con.commit()

# Connect to the database
con = sqlite3.connect('db.sqlite', check_same_thread=False)
cur = con.cursor()

app = fastapi.FastAPI()
origins = [
    "http://homeassistant.local:8123",  # Remplacez par l'URL de votre Home Assistant
    "http://localhost:8123", # a rajouter en cas de dev local.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items/")
def get_items():
    cur.execute('SELECT * FROM items')
    result = []
    items = cur.fetchall()
    for item in items:
        result.append({'item_id': item[0], 'item_name': item[1], 'cabinet_id': item[2], 'absent': item[3]})
    return result

@app.get('/items/{cabinet_id}/{item_name}')
def get_item(item_name: str, cabinet_id: int):
    cur.execute('SELECT * FROM items WHERE item_name = ? AND cabinet_id = ?', (item_name,cabinet_id))
    item = cur.fetchone()
    print("Requested item: ", item)
    if item is None:
        return {'error': 'DOES_NOT_EXIST'}
    else:
        return {'item_id': item[0], 'item_name': item[1], 'cabinet_id': item[2], 'absent': item[3]}    

@app.put('/items/{cabinet_id}/remove')
def return_item(cabinet_id: int, item: Item):
    cur.execute('UPDATE items SET absent = 1 WHERE item_nid = ? AND cabinet_id = ?', (item.item_id, cabinet_id))
    con.commit()
    return {'item_name': item.item_id, 'absent': 1}


@app.put('/items/{cabinet_id}/add')
def return_item(cabinet_id: int, item: Item):
    cur.execute('UPDATE items SET absent = 0 WHERE item_id = ? AND cabinet_id = ?', (item.item_id, cabinet_id))
    con.commit()
    return {'item_name': item.item_id, 'absent': 0}

#REST-Routes for vocal commands
@app.put('/items/{cabinet_id}/{item_name}/remove')
def take_item(item_name: str, cabinet_id: int):
    cur.execute('UPDATE items SET absent = 1 WHERE item_name = ? AND cabinet_id = ?', (item_name,cabinet_id))
    con.commit()
    return {'item_name': item_name, 'absent': 1}

@app.put('/items/{cabinet_id}/{item_name}/add')
def return_item(item_name: str, cabinet_id: int):
    cur.execute('UPDATE items SET absent = 0 WHERE item_name = ? AND cabinet_id = ?', (item_name,cabinet_id))
    con.commit()
    return {'item_name': item_name, 'absent': 0}


#Edit cabinet (add new items or change database info related to items)
@app.put('/items/{cabinet_id}/{item_name}/move')
def move_item(item_name: str, cabinet_id: int, new_cabinet_id: int):
    cur.execute('UPDATE items SET cabinet_id = ? WHERE item_name = ? AND cabinet_id = ?', (new_cabinet_id, item_name, cabinet_id))
    con.commit()
    return {'item_name': item_name, 'cabinet_id': new_cabinet_id}

@app.post('/items/')
def create_item(item: Item):
    cur.execute('INSERT INTO items (item_id, item_name, cabinet_id, absent) VALUES (?, ?, ?, ?)', (item.item_id, item.item_name, item.cabinet_id, item.absent))
    con.commit()
    return {'item_id': item.item_id,'item_name': item.item_name, 'cabinet_id': item.cabinet_id, 'absent': item.absent}
