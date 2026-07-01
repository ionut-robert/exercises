from fastapi import FastAPI
from services.services import validate_create_product
from services.reports import all_products
from pydantic import BaseModel

class Item(BaseModel):
    id : int
    name : str

app = FastAPI()

@app.put("/product")
def add_product(name : str):
    validate_create_product(name)
    
@app.get("/reports")
def product_list():
    return all_products()
