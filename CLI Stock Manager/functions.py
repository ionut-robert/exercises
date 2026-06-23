from database import engine,Products,Inventory,Customers,StockTransactions,Orders,TransactionType
from sqlalchemy.orm import Session
from sqlalchemy import select,update
from dataclasses import dataclass

@dataclass
class RegisterData:
    products: list
    customers: list
    inventory: list

class Register():
    def get_data(self):
        with Session(engine) as session:
            products = session.query(Products).all()
            customers = session.query(Customers).all()
            inventory = session.query(Inventory).all()
            return RegisterData(products=products,customers=customers,inventory=inventory)
        
register = Register()
data = register.get_data()

def add_product(name):
    if name not in (row.Product_Name for row in data.products):
        new_product = Products(Product_Name = name)
        with Session(engine) as session:
            session.add(new_product)
            session.flush()
            inventory_line = Inventory(Product_ID = new_product.Product_ID)
            session.add(inventory_line)
            session.commit()
        register.get_data()
    else:
        raise Exception('The product exists.')
    
def del_product(name):
        with Session(engine) as session:
            product = session.scalar(
                select(Products).join(StockTransactions, Products.Product_ID == StockTransactions.Product_ID).where(
                    Products.Product_Name == name, StockTransactions is None)
                )
            if product is not None :
                session.delete(product)
                session.commit()
            else:
                raise Exception('There are stock movements for this product.')
        register.get_data()

def add_customer(customer_name):
    with Session(engine) as session:
        add_customer = Customers(Customer_Name = customer_name)
        session.add(add_customer)
    register.get_data()

def add_order(product_name,qty,customer_name):
    customer_id = (c.Customer_ID for c in data.customers if c.Customer_Name == customer_name)
    product_id = (p.Product_ID for p in data.products if p.Product_Name == product_name)
    inventory_q = (q.Qty for q in data.inventory if q.Product_ID == product_id)

    with Session(engine) as session:
        new_order = Orders(Product_ID = product_id, Qty = qty, Customer_ID = customer_id,TransactionType_ID=3)
        inv_update = (update(Inventory).where(Inventory.Product_ID==product_id).values(Qty = inventory_q - qty))
        session.add(new_order)
        session.execute(inv_update)
        session.commit()

def stock_in(product_name,qty):
    product_id = (p.Product_ID for p in data.products if p.Product_Name == product_name)
    inventory_q = (q.Qty for q in data.inventory if q.Product_ID == product_id)

    with Session(engine) as session:
        stock_in = StockTransactions(Product_ID = product_id,Qty = qty, TransactionType_ID = 1)
        session.add(stock_in)
        stmt = (update(Inventory).where(Inventory.Product_ID==product_id).values(Qty = inventory_q + qty))
        session.execute(stmt)
        session.commit()

def stock_out(product_name,qty):
    product_id = (p.Product_ID for p in data.products if p.Product_Name == product_name)
    inventory_q = (q.Qty for q in data.inventory if q.Product_ID == product_id)

    with Session(engine) as session:
        stock_out = StockTransactions(Product_ID = product_id,Qty = qty, TransactionType_ID = 2)
        session.add(stock_out)
        stmt = (update(Inventory).where(Inventory.Product_ID==product_id).values(Qty = inventory_q - qty))
        session.execute(stmt)
        session.commit()


if __name__=='__main__':
    
    with Session(engine) as ses:
        for t in ('IN','OUT','ORDER'):
            transaction = TransactionType(TransactionType_Name = t)
            ses.add(transaction)
        ses.commit()
        
__name__ == '__main__'
