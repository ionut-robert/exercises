from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class Products(Base):
    __tablename__ = 'Products'

    Product_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_Name: Mapped[str] = mapped_column(String(50),nullable=False)

class Inventory(Base):
    __tablename__ = 'Inventory'

    Inventory_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_ID: Mapped[int] = mapped_column(ForeignKey(Products.Product_ID))
    Qty : Mapped[float] = mapped_column(default=0,nullable=False)

class TransactionType(Base):
    __tablename__ = 'TransactionType'

    TransactionType_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    TransactionType_Name: Mapped[str] = mapped_column(String(15), nullable=False)

class StockTransactions(Base):
    __tablename__ = 'StockTransactions'

    StockTransactions_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_ID: Mapped[int] = mapped_column(ForeignKey(Products.Product_ID))
    Qty: Mapped[float] = mapped_column(nullable=False)
    TransactionType_ID: Mapped[int] = mapped_column(ForeignKey(TransactionType.TransactionType_ID))

class Customers(Base):
    __tablename__ = 'Customers'

    Customer_ID: Mapped[int] = mapped_column(primary_key=True)
    Customer_Name: Mapped[str] = mapped_column(String(50))

class Orders(Base):
    __tablename__ = 'Orders'

    Order_ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Product_ID: Mapped[int] = mapped_column(ForeignKey(Products.Product_ID))
    Qty: Mapped[float] = mapped_column(nullable=False)
    Customer_ID: Mapped[int] = mapped_column(ForeignKey(Customers.Customer_ID))
    TransactionType_ID: Mapped[int] = mapped_column(ForeignKey(TransactionType.TransactionType_ID))