import sqlite3
import fastapi
import os
from pydantic import BaseModel

class Item(BaseModel):
    item_name: str
    cabinet_id: int
    absent: int

if not os.path.exists('db.sqlite'):
    # Create the db.sqlite since it does not exists
    open('db.sqlite', 'w').close()
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS items (item_name TEXT UNIQUE, cabinet_id INTEGER, absent INTEGER)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("salt", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("pepper", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("sugar", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("flour", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("rice", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("pasta", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("vinegar", 1, 0)')
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES ("olive oil", 1, 0)')
    con.commit()

# Connect to the database
con = sqlite3.connect('db.sqlite', check_same_thread=False)
cur = con.cursor()

app = fastapi.FastAPI()

@app.get("/items/")
def get_items():
    cur.execute('SELECT * FROM items')
    result = []
    items = cur.fetchall()
    
    for item in items:
        result.append({'item_name': item[0], 'cabinet_id': item[1], 'absent': item[2]})
    return result

@app.get('/items/{item_name}')
def get_item(item_name: str):
    cur.execute('SELECT * FROM items WHERE item_name = ?', (item_name,))
    
    item = cur.fetchone()
    print("Requested item: ", item)
    if item is None:
        return {'error': 'DOES_NOT_EXIST'}
    else:
        return {'item_name': item[0], 'cabinet_id': item[1], 'absent': item[2]}    

@app.post('/items/')
def create_item(item: Item):
    cur.execute('INSERT INTO items (item_name, cabinet_id, absent) VALUES (?, ?, ?)', (item.item_name, item.cabinet_id, item.absent))
    con.commit()
    return {'item_name': item.item_name, 'cabinet_id': item.cabinet_id, 'absent': item.absent}

@app.put('/items/{item_name}/remove')
def take_item(item_name: str):
    cur.execute('UPDATE items SET absent = 1 WHERE item_name = ?', (item_name,))
    con.commit()
    return {'item_name': item_name, 'absent': 1}

@app.put('/items/{item_name}/add')
def return_item(item_name: str):
    cur.execute('UPDATE items SET absent = 0 WHERE item_name = ?', (item_name,))
    con.commit()
    return {'item_name': item_name, 'absent': 0}


@app.put('/items/{item_name}/move')
def move_item(item_name: str, cabinet_id: int):
    cur.execute('UPDATE items SET cabinet_id = ? WHERE item_name = ?', (cabinet_id, item_name))
    con.commit()
    return {'item_name': item_name, 'cabinet_id': cabinet_id}