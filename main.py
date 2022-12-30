from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel
from app_database import Database

app = FastAPI()

#Database
DATABASE_PATH = r"./items.db"

#Models

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Union[bool, None] = None

# class Items(BaseModel):
#     list()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}",response_model=Item)
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.get("/items/{item_id}",response_model=ItemResponse)
def read_item(item_id: int):
    db_conn = Database(DATABASE_PATH)
    item = db_conn.get_item(item_id)
    return item

@app.get("/allitems/",response_model=List[ItemResponse])
def get_all_items():
    db_conn = Database(DATABASE_PATH)
    items = db_conn.all_items()
    return items

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    db_conn = Database(DATABASE_PATH)
    success = db_conn.create_item({
        'id': item_id,
        'name':item.name,
        'price': item.price,
        'is_offer' : 'TRUE' if item.is_offer else 'FALSE'
    })
    print(success)
    return {"name": item.name, "id": item_id, 'price' : item.price,'is_offer': item.is_offer}

@app.post("/items/additem", response_model=ItemResponse)
def add_item(item: Item):
    db_conn = Database(DATABASE_PATH)
    print('ITEM',item.price,item.is_offer)
    #success= 1
    success = db_conn.add_item({
        'name':item.name,
        'price': item.price,
        'is_offer' : 'TRUE' if item.is_offer else 'FALSE'
    })
    print(success)
    return {"id": success, "name": item.name,'price' : item.price,'is_offer': item.is_offer}