import typer
from services.services import validate_create_customer,validate_stock_opretion,validate_create_product,validate_delete_product
from services.reports import all_products,find_product,low_stock,inventory_report
from db.models import StockActions

app = typer.Typer()

@app.command()
def add_product(name: str): #python main.py create-product (ProductName or 'Product Name')
    validate_create_product(name)

@app.command()
def delete_product(id: int):
    validate_delete_product(id)

@app.command()
def add_customer(name: str):
   validate_create_customer(name)

@app.command()
def add_order(prod_id: int,cust_id: int, qty : float):
    validate_stock_opretion(prod_id,qty,cust_id,StockActions.ORDER)

@app.command()
def stock_in(prod_id:int, qty: float):
    validate_stock_opretion(prod_id, qty,cust_id= None,Actions= StockActions.IN)

@app.command()
def stock_out(prod_id:int, qty: float):
    validate_stock_opretion(prod_id, qty,cust_id= None,Actions= StockActions.OUT)

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