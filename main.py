from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Union
app = FastAPI()
# items = ["ao" , "quan" , "mu" , "giay"]
class Item(BaseModel):
    name: str
    price: float
    description: Union[str, None] = None

@app.post("/items/")
def create_item(item: Item):
    print(f"deta touroku: {item.name}, {item.price}, {item.description}")
    return item