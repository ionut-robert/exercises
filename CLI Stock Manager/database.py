from config import *
from sqlalchemy import ForeignKey,String,create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

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

if __name__ == '__main__':

    Database.metadata.create_all(engine)
    
__name__=='__main__'
