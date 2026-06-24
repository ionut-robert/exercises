from config import *
from sqlalchemy import ForeignKey,String,create_engine,delete,select,update
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

def create_product(name):
    with Session(engine) as session:
        stmt = Products(Product_Name = name)
        session.add(stmt)
        session.flush()

        inv_stmt = Inventory(Product_ID = stmt.Product_ID, Qty=0)
        session.add(inv_stmt)

        session.commit()

def delete_product(prod_id: int):
    with Session(engine) as session:
        prod = select(Products).where(Product_ID = prod_id)
        session.delete(prod)
        session.commit()

def create_customer(name: str):
    with Session(engine) as session:
        stmt = Customers(Customer_Name = name)
        session.add(stmt)

        session.commit()

def create_order(prod_id : int, cust_id: int, qty : float):
    with Session(engine) as session:
        stmt = Orders(Customer_ID = cust_id, Product_ID = prod_id, Qty = qty, TransactionType_ID = 3)
        session.add(stmt)

        inv_stmt = select(Inventory).where(Product_ID = prod_id) #stmt
        inv_stmt.Qty -= qty

        session.commit()

def stock_in(prod_id:int, qty: float):
    with Session(engine) as session:
        stmt = StockTransactions(Product_ID =prod_id, Qty = qty, TransactionType_ID = 1)
        session.add(stmt)

        inv_stmt = select(Inventory).where(Inventory.Product_ID == prod_id) #stmt
        inv_stmt.Qty += qty

        session.commit()

def stock_out(prod_id : int, qty: float):
    with Session(engine) as session:
        stmt = StockTransactions(Product_ID =prod_id, Qty = qty, TransactionType_ID = 2)
        session.add(stmt)

        inv_stmt = select(Inventory).where(Inventory.Product_ID == prod_id) #stmt
        inv_stmt.Qty -= qty

        session.commit()

if __name__ == '__main__':

    Database.metadata.create_all(engine)
    
    with Session(engine) as ses:
        for t in ('IN','OUT','ORDER'):
            transaction = TransactionType(TransactionType_Name = t)
            ses.add(transaction)
        ses.commit()

__name__=='__main__'
