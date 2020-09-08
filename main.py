from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    age: int
    namora: bool

listona = {
    'pedro' : {'age' :  5, 'namora' : True },
    'lucas' : {'age' :  6, 'namora' : True },
    'joão'  : {'age' : 80, 'namora' : False}
}

listona2 = [
    { 'id' : 0, 'name':'pedro', 'age' : 21, 'namora' : True  },
    { 'id' : 1, 'name':'lucas', 'age' : 21, 'namora' : True  },
    { 'id' : 2, 'name':'leo'  , 'age' : 21, 'namora' : False },
    { 'id' : 3, 'name':'manu' , 'age' : 48, 'namora' : True  }
]

@app.get("/") 
async def read_root():
    return listona

@app.get("/listona2") 
async def read_root():
    return listona2

@app.post("/addItems/")
async def create_item(item: Item):
    listona[item.name] = { 'age' : item.age, 'namora' : item.namora }
    return item

@app.post("/addItems2/")
async def create_item(item: Item):

    novo = { 
        'id'     : len(listona2), 
        'name'   : item.name, 
        'age'    : item.age, 
        'namora' : item.namora 
    }
    
    listona2.append(novo)
    return item

@app.get("/name/{item_name}")
async def read_allItem(item_name: str):
    return listona[item_name]

@app.get("/age/{item_name}")
async def read_age(item_name: str):
    return {'name' : item_name, 'age' : listona[item_name]['age']}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/{item_id}")
async def read_querry(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    if short:
        item.update(
            {"description": "blah"}
        )
    return item