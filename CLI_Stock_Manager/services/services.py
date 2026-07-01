from db.queries import get_inventory_products,initialize_product,get_stocktransactions_orders,remove_product,get_customers,create_customer,create_stock_transaction,create_order,update_inventory_qty
from regex import fullmatch
from db.models import StockActions

def validate_stock_opretion(prod_id,qty,cust_id = None, Actions = None):
    if not any(prod_id == product_id for product_id,_,_ in get_inventory_products()):
        raise Exception("Product id not found")
    elif qty < 0:
        raise Exception("Qty cannot be negative")
    elif any(prod_id == product_id and Qty < qty for product_id,_,Qty in get_inventory_products()):
        raise Exception("Insufficient quantity")
    else:
        c_qty = next((Qty for product_id,_,Qty in get_inventory_products() if product_id == prod_id),None)

        if Actions == StockActions.IN:
            create_stock_transaction(prod_id, qty,Actions)
            c_qty += qty
            update_inventory_qty(prod_id,c_qty)
        elif Actions == StockActions.OUT:
            create_stock_transaction(prod_id, qty,Actions)
            c_qty -= qty
            update_inventory_qty(prod_id,c_qty)
        else:
            if not any(cust_id == id for id,_ in get_customers()) and Actions == StockActions.ORDER:
                raise Exception("Customer not exists")
            else:
                create_order(prod_id,qty,Actions,cust_id)
                c_qty -= qty
                update_inventory_qty(prod_id,c_qty)
        
def validate_create_product(name):
    if bool(fullmatch(r"[A-Za-z0-9 -.]+", name)) == False:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-", "." ') 
    elif len(name) > 30:
        raise Exception("max_len = 30")
    elif any(name == product_name for _,product_name,_ in get_inventory_products()):
        raise Exception("Duplicate product name ")
    else:
        initialize_product(name)
        return print('Product added successfully')

def validate_delete_product(prod_id):
    if not any(prod_id == product_id for product_id,_,_ in get_inventory_products()):
        raise Exception("Product id not found")
    elif any(prod_id == id for id in get_stocktransactions_orders()):
        raise Exception("Product has stock movements")
    else:
        remove_product(prod_id)

def validate_create_customer(cust_name):
    if bool(fullmatch(r"[A-Za-z0-9 -]+", cust_name)) == False:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-"') 
    elif len(cust_name) > 30:
        raise Exception("max_len = 30 ")
    elif any(cust_name == customer_name for _,customer_name in get_customers()):
        raise Exception("Duplicate customer name")
    else:
        create_customer(cust_name)