from repository import *
from sqlalchemy.orm import Session
from dataclasses import dataclass

@dataclass
class RegisterData:
    products: list
    inventory: list

class Register():
    def get_data(self):
        with Session(engine) as session:
            products = session.query(Products).all()
            inventory = session.query(Inventory).all()
            return RegisterData(products=products,inventory=inventory)
        
register = Register()
global data
data = register.get_data()

def verify_create_product(name):
    create_product(name)

def verify_delete_product(id):
    delete_product(id)

def verify_create_customer(name):
    create_customer(name)

def verify_create_order(prod_id,cust_id,qty):
    create_order(prod_id,cust_id,qty)

def verify_stock_in(prod_id:int, qty: float):
    stock_in(prod_id, qty)

def verify_stock_out(prod_id : int, qty: float):
    stock_out(prod_id, qty)

