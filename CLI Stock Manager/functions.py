from database import engine,Products,Inventory,Customers,StockTransactions,Orders
from sqlalchemy.orm import Session
from sqlalchemy import select,update
from dataclasses import dataclass

@dataclass
class RegisterData:
    products: list
    customers: list
    inventory: list
    orders: list
    stoc_t: list

class Register():
    def get_data(self):
        with Session(engine) as session:
            products = session.query(Products).all()
            customers = session.query(Customers).all()
            inventory = session.query(Inventory).all()
            orders = session.query(Orders).all()
            stoc_t = session.query(StockTransactions).all()
            return RegisterData(products=products,customers=customers,inventory=inventory,orders=orders,stoc_t = stoc_t)
        
register = Register()
data = register.get_data()

def add_product(name):
    if name not in (row.Product_Name for row in data.products):
        last_row_id = data.products[-1].Product_ID + 1
        last_inventory_id = data.inventory[-1].Inventory_ID + 1 

        data.products.append(Products(Product_ID = last_row_id,Product_Name = name))
        data.inventory.append(Inventory(Inventory_ID = last_inventory_id, Product_ID = last_row_id, Qty = 0))
    else:
        raise Exception('The product found.')

def del_product(name):
    if name in (row.Product_Name for row in data.products):
        prod = next(row for row in data.products if row.Product_Name == name)
        inv = next(row for row in data.inventory if row.Product_ID == prod.Product_ID)
        
        data.products.remove(prod)
        data.inventory.remove(inv)
    else:
        raise Exception('Product not found.')

def add_customer(customer_name):
    if customer_name not in (row.Customer_Name for row in data.customers):
        data.customers.append(Customers(Customer_Name = customer_name))
    else:
        raise Exception('Duplicate customer')

def add_order(product_name,qty,customer_name):
    customer = next(c for c in data.customers if c.Customer_Name == customer_name)
    product = next(p for p in data.products if p.Product_Name == product_name)
    inventory = next(q for q in data.inventory if q.Product_ID == product.Product_ID)
    order_id = (data.orders[-1].Order_ID + 1)
    
    if customer.Customer_ID in (row.Customer_ID for row in data.customers):
        data.orders.append(Orders(Order_ID = order_id, Product_ID = product.Product_ID , Qty = qty, Customer_ID = customer.Customer_ID,TransactionType_ID=3))
        inventory.Qty -= qty
    else:
        raise Exception('Customer not found')

def stock_in(product_name,qty):
    product = next(p for p in data.products if p.Product_Name == product_name)
    inventory = next(q for q in data.inventory if q.Product_ID == product.Product_ID)
    st_id = data.stoc_t[-1].StockTransactions_ID or 0 + 1

    data.stoc_t.append(StockTransactions(StockTransactions_ID = st_id, Product_ID = product.Product_ID, Qty = qty, TransactionType_ID = 0))
    inventory.Qty += qty

def stock_out(product_name,qty):
    product = next(p for p in data.products if p.Product_Name == product_name)
    inventory = next(q for q in data.inventory if q.Product_ID == product.Product_ID)
    st_id = data.stoc_t[-1].StockTransactions_ID or 0 + 1

    data.stoc_t.append(StockTransactions(StockTransactions_ID = st_id, Product_ID = product.Product_ID, Qty = qty, TransactionType_ID = 1))
    inventory.Qty -= qty
'''
    
    with Session(engine) as ses:
        for t in ('IN','OUT','ORDER'):
            transaction = TransactionType(TransactionType_Name = t)
            ses.add(transaction)
        ses.commit()
        
'''
