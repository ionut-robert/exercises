from db.config import engine
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from db.models import Products,Inventory,Customers,Orders,StockTransactions,Base,TransactionType,StockActions

Base.metadata.create_all(engine)

with Session(engine) as ses:
    if not ses.execute(text("SELECT 1 FROM TransactionType")).first():
        ses.add_all([
            TransactionType(TransactionType_Name = StockActions.IN.name),
            TransactionType(TransactionType_Name = StockActions.OUT.name),
            TransactionType(TransactionType_Name = StockActions.ORDER.name)
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

def update_inventory_qty(prod_id,qty):
    with Session(engine) as session:
        stmt = select(Inventory).where(Inventory.Product_ID == prod_id)
        inv = session.scalar(stmt)
        inv.Qty = qty
        session.commit()

def create_stock_transaction(prod_id, qty, Actions):
    with Session(engine) as session:
        st = StockTransactions(Product_ID =prod_id, Qty = qty, TransactionType_ID = Actions)
        session.add(st)
        session.commit()

def create_order(prod_id,qty,Actions,cust_id):
    with Session(engine) as session:
        ord = Orders(Customer_ID = cust_id, Product_ID = prod_id, Qty = qty, TransactionType_ID = Actions)
        session.add(ord)
        session.commit()

def get_customers():
    with Session(engine) as session:
        stmt = select(Customers.Customer_ID,Customers.Customer_Name)
        rows = session.execute(stmt).mappings().all()
    return rows

def get_stocktransactions_orders():
    ids = set()
    with Session(engine) as session:
        st_stmt = select(StockTransactions.Product_ID)
        st_rows = session.execute(st_stmt).mappings().all()

        o_stmt = select(Orders.Product_ID)
        o_rows = session.execute(o_stmt).mappings().all()

        ids.update(row["Product_ID"] for row in st_rows)
        ids.update(row["Product_ID"] for row in o_rows)

    return ids

def get_inventory_products():
    with Session(engine) as session:
        stmt = select(Products.Product_ID,Products.Product_Name,Inventory.Qty).join(Inventory, Inventory.Product_ID == Products.Product_ID)

        rows = session.execute(stmt).fetchall()
        return rows