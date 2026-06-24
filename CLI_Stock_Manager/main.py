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
    verify_stock_out(prod_id, qty)

@app.command()
def list_products():
    print(f"{'No':<6}{'Name':<20}")
    for id,name,qty in products_with_stock():
        print(f"{id:<6}{name:<20}")

@app.command()
def search_product(prod_name):
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}")
    for id,name,qty in products_with_stock():
        if name == prod_name:
            print(f"{id:<6}{name:<20}{qty:<5}")

@app.command()
def stock_alerts():
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}")
    for id,name,qty in products_with_stock():
        if qty < 10:
            print(f"{id:<6}{name:<20}{qty:<5}")

@app.command()
def inventory_report():
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}")
    for id,name,qty in products_with_stock():
            print(f"{id:<6}{name:<20}{qty:<5}")

if __name__ == "__main__":
    app()