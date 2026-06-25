from config import *
from sqlalchemy import ForeignKey,String,create_engine,select
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session

engine = create_engine(f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{SERVER}:1433/{DB_DATABASE}?{DB_DRIVER}&TrustServerCertificate=yes",echo=False)

class Database(DeclarativeBase):
    pass

class Products(Database):
    __tablename__ = 'Products'

    Product_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_Name: Mapped[str] = mapped_column(String(50),nullable=False)

class Inventory(Database):
    __tablename__ = 'Inventory'

    Inventory_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_ID: Mapped[int] = mapped_column(ForeignKey(Products.Product_ID))
    Qty : Mapped[float] = mapped_column(default=0,nullable=False)

class TransactionType(Database):
    __tablename__ = 'TransactionType'

    TransactionType_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    TransactionType_Name: Mapped[str] = mapped_column(String(15), nullable=False)

class StockTransactions(Database):
    __tablename__ = 'StockTransactions'

    StockTransactions_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_ID: Mapped[int] = mapped_column(ForeignKey(Products.Product_ID))
    Qty: Mapped[float] = mapped_column(nullable=False)
    TransactionType_ID: Mapped[int] = mapped_column(ForeignKey(TransactionType.TransactionType_ID))

class Customers(Database):
    __tablename__ = 'Customers'

    Customer_ID: Mapped[int] = mapped_column(primary_key=True)
    Customer_Name: Mapped[str] = mapped_column(String(50))

class Orders(Database):
    __tablename__ = 'Orders'

    Order_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_ID: Mapped[int] = mapped_column(ForeignKey(Products.Product_ID))
    Qty: Mapped[float] = mapped_column(nullable=False)
    Customer_ID: Mapped[int] = mapped_column(ForeignKey(Customers.Customer_ID))
    TransactionType_ID: Mapped[int] = mapped_column(ForeignKey(TransactionType.TransactionType_ID))

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

def get_products_invetory():
    with Session(engine) as session:
        stmt = select(Products.Product_ID ,Products.Product_Name,Inventory.Qty).where(Inventory.Product_ID==Products.Product_ID)
        products = session.execute(stmt).all()
    return products

def get_customers():
    with Session(engine) as session:
        stmt = select(Customers.Customer_ID,Customers.Customer_Name)
        customers = session.execute(stmt).all()
    return customers
'''
    Database.metadata.create_all(engine)
    
    with Session(engine) as ses:
        for t in ('IN','OUT','ORDER'):
            transaction = TransactionType(TransactionType_Name = t)
            ses.add(transaction)
        ses.commit()
'''
