import typer
from services.services import verify_add_customer,verify_add_order,verify_add_product,verify_delete_product,verify_stock_in,verify_stock_out
from services.reports import all_products,find_product,low_stock,inventory_report

app = typer.Typer()

@app.command()
def add_product(name: str): #python main.py create-product (ProductName or 'Product Name')
    verify_add_product(name)

@app.command()
def delete_product(id: int):
    verify_delete_product(id)

@app.command()
def add_customer(name: str):
   verify_add_customer(name)

@app.command()
def add_order(prod_id: int,cust_id: int, qty : float):
    verify_add_order(prod_id,cust_id,qty)

@app.command()
def stock_in(prod_id:int, qty: float):
    verify_stock_in(prod_id, qty)

@app.command()
def stock_out(prod_id:int, qty: float):
    verify_stock_out(prod_id, qty)

@app.command()
def product_list():
    all_products()

@app.command()
def search_product(name : str):
    find_product(name)

@app.command()
def stock_alerts():
    min_stock_qty = 10
    low_stock(min_stock_qty)
    
@app.command()
def show_inventory():
    inventory_report()

if __name__ == "__main__":
    app()