import typer
from services import *
app = typer.Typer()


@app.command()
def create_product(name: str): #python main.py create-product NameProduct (!Name Product)
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
    stock_out(prod_id, qty)

@app.command()
def list_products():
    pass

@app.command()
def search_product():
    pass

@app.command()
def stock_alerts():
    pass

@app.command()
def inventory_report():
    pass

if __name__ == "__main__":
    app()