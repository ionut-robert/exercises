import typer
from services import *

app = typer.Typer()

@app.command()
def create_product(name: str): #python main.py create-product (ProductName or 'Product Name')
    verify_create_product(name)

@app.command()
def delete_product(id: int):
    verify_delete_product(id)

@app.command()
def create_customer(name: str):
    verify_create_customer(name)

@app.command()
def create_order(prod_id: int,cust_id: int, qty : float):
    verify_create_order(prod_id,cust_id,qty)

@app.command()
def stock_in(prod_id:int, qty: float):
    verify_stock_in(prod_id, qty)

@app.command()
def stock_out(prod_id:int, qty: float):
    verify_stock_out(prod_id, qty)

@app.command()
def product_list():
    Reports()

@app.command()
def search_product(name : str):
    req_qty = True
    Reports(prod_name = name, show_qty = req_qty)

@app.command()
def stock_alerts():
    req_qty = True
    min_stock_qty = 10
    Reports(show_qty = req_qty, min_qty = min_stock_qty)
    

@app.command()
def inventory_report():
    req_qty = True
    Reports(show_qty = req_qty)


if __name__ == "__main__":
    app()