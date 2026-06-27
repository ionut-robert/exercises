from db.config import DB_USER,DB_PASSWORD,SERVER,DB_DATABASE,DB_DRIVER
from db.models import Products,Inventory,Customers,Orders,StockTransactions
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,select

engine = create_engine(f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{SERVER}:1433/{DB_DATABASE}?{DB_DRIVER}&TrustServerCertificate=yes",echo=False)

def add_product(name):
    with Session(engine) as session:
        stmt = Products(Product_Name = name)
        session.add(stmt)
        session.flush()

        inv = Inventory(Product_ID = stmt.Product_ID, Qty=0)
        session.add(inv)

        session.commit()

def delete_product(prod_id):
    with Session(engine) as session:
        inv_stmt = select(Inventory).where(Inventory.Product_ID==prod_id)
        prod_stmt = select(Products).where(Products.Product_ID == prod_id)

        inv = session.scalar(inv_stmt)
        prod = session.scalar(prod_stmt)

        session.delete(inv)
        session.delete(prod)

        session.commit()

def add_customer(name):
    with Session(engine) as session:
        cust = Customers(Customer_Name = name)
        session.add(cust)

        session.commit()

def add_order(prod_id, cust_id, qty):
    with Session(engine) as session:
        stmt = Orders(Customer_ID = cust_id, Product_ID = prod_id, Qty = qty, TransactionType_ID = 3)
        session.add(stmt)

        inv_stmt = select(Inventory).where(Inventory.Product_ID == prod_id)
        inv = session.scalar(inv_stmt)
        inv.Qty -= qty

        session.commit()

def stock_in(prod_id, qty):
    with Session(engine) as session:
        st = StockTransactions(Product_ID =prod_id, Qty = qty, TransactionType_ID = 1)
        session.add(st)

        inv_stmt = select(Inventory).where(Inventory.Product_ID == prod_id)
        inv = session.scalar(inv_stmt)
        inv.Qty += qty

        session.commit()

def stock_out(prod_id, qty):
    with Session(engine) as session:
        st = StockTransactions(Product_ID = prod_id, Qty = qty, TransactionType_ID = 2)
        session.add(st)

        inv_stmt = select(Inventory).where(Inventory.Product_ID == prod_id)
        inv = session.scalar(inv_stmt)
        inv.Qty -= qty

        session.commit()

def get_invetory():
    with Session(engine) as session:
        stmt = select(Inventory.Product_ID,Inventory.Qty)
        rows = session.execute(stmt).mappings().all()
    return [(row["Product_ID"],row["Qty"]) for row in rows]

def get_customers():
    with Session(engine) as session:
        stmt = select(Customers.Customer_ID,Customers.Customer_Name)
        rows = session.execute(stmt).mappings().all()
    return [(row["Customer_ID"],row["Customer_Name"]) for row in rows]

def get_products():
    with Session(engine) as session:
        stmt = select(Products.Product_ID,Products.Product_Name)
        rows = session.execute(stmt).mappings().all()
    return [(row["Product_ID"],row["Product_Name"]) for row in rows]

def get_stocktransactions():
    with Session(engine) as session:
        stmt = select(StockTransactions.Product_ID)
        rows = session.execute(stmt).mappings().all()
    return [set(row["Product_ID"]) for row in rows]#?
 

