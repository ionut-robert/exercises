from db.config import engine
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from db.models import Products,Inventory,Customers,Orders,StockTransactions,Base,TransactionType
from enum import Enum

class StockActions(Enum):
    IN = 1
    OUT = 2
    ORDER = 3

Base.metadata.create_all(engine)

with Session(engine) as ses:
    if not ses.execute(text("SELECT 1 FROM TransactionType")).first():
        ses.add_all([
            TransactionType(TransactionType_Name = 'IN'),
            TransactionType(TransactionType_Name = 'OUT'),
            TransactionType(TransactionType_Name = 'ORDER')
        ])
    ses.commit()

def initialize_product(name):
    with Session(engine) as session:
        product = Products(Product_Name = name)
        session.add(product)
        session.flush()

        inv = Inventory(Product_ID = product.Product_ID)
        session.add(inv)

        session.commit()

def remove_product(prod_id):
    with Session(engine) as session:
        inv_stmt = select(Inventory).where(Inventory.Product_ID == prod_id)
        prod_stmt = select(Products).where(Products.Product_ID == prod_id)

        inv = session.scalar(inv_stmt)
        prod = session.scalar(prod_stmt)

        session.delete(inv)
        session.delete(prod)

        session.commit()

def create_customer(name):
    with Session(engine) as session:
        cust = Customers(Customer_Name = name)
        session.add(cust)

        session.commit()

def create_order(prod_id, cust_id, qty):
    with Session(engine) as session:
        stmt = Orders(Customer_ID = cust_id, Product_ID = prod_id, Qty = qty, TransactionType_ID = StockActions.ORDER)
        session.add(stmt)

        session.commit()

def invetory_update(prod_id,qty):
    with Session(engine) as session:
        stmt = select(Inventory).where(Inventory.Product_ID == prod_id)

        inv = session.scalar(stmt)
        inv.Qty = qty
        session.commit()


def stock_in(prod_id, qty):
    with Session(engine) as session:
        st = StockTransactions(Product_ID =prod_id, Qty = qty, TransactionType_ID = StockActions.IN)
        session.add(st)

        session.commit()

def stock_out(prod_id, qty):
    with Session(engine) as session:
        st = StockTransactions(Product_ID = prod_id, Qty = qty, TransactionType_ID = StockActions.OUT)
        session.add(st)

        session.commit()

def get_customers():
    with Session(engine) as session:
        stmt = select(Customers.Customer_ID,Customers.Customer_Name)
        rows = session.execute(stmt).mappings().all()
    return rows

def get_stocktransactions():
    with Session(engine) as session:
        stmt = select(StockTransactions.Product_ID)
        rows = session.execute(stmt).mappings().all()
    return rows

def get_orders():
    with Session(engine) as session:
        stmt = select(Orders.Product_ID,Orders.Customer_ID)
        rows = session.execute(stmt).mappings().all()
    return rows

def get_inventory_products():
    with Session(engine) as session:
        stmt = select(Products.Product_ID,Products.Product_Name,Inventory.Qty).join(Inventory, Inventory.Product_ID == Products.Product_ID)

        rows = session.execute(stmt).fetchall()
        return rows