from db.queries import get_inventory_products,initialize_product,get_stocktransactions,remove_product,get_customers,create_order,stock_in,stock_out,create_customer
from regex import fullmatch

def verify_create_product(name):
    if bool(fullmatch(r"[A-Za-z0-9 -.]+", name)) == False:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-", "." ') 
    elif len(name) > 30:
        raise Exception("max_len = 30 ")
    elif any(name == product_name for _,product_name,_ in get_inventory_products()):
        raise Exception("Duplicate product name ")
    else:
        initialize_product(name)
        return print('Product added successfully')

def verify_delete_product(prod_id):
    if not any(prod_id == product_id for product_id,_,_ in get_inventory_products()):
        raise Exception("Product id not found")
    elif any(prod_id == id for id,_,_ in get_stocktransactions()):
        raise Exception("Product has stock movements")
    else:
        remove_product(prod_id)

def verify_add_order(prod_id,cust_id,qty):
    if not any(prod_id == product_id for product_id,_,_ in get_inventory_products()):
        raise Exception("Product not exists")
    elif not any(cust_id == id for id,_ in get_customers()):
        raise Exception("Customer not exists")
    elif qty < 0:
        raise Exception("Qty cannot be negative")
    else:
        create_order(prod_id,cust_id,qty)

def verify_stock_in(prod_id, qty):
    if not any(prod_id == product_id for product_id,_,_ in get_inventory_products()):
        raise Exception("Product id not found")
    elif qty < 0:
        raise Exception("Qty cannot be negative")
    else:
        stock_in(prod_id, qty)

def verify_stock_out(prod_id, qty):
    if not any(prod_id == product_id for product_id,_,_ in get_inventory_products()):
        raise Exception("Product id not found")
    elif qty < 0:
        raise Exception("Qty cannot be negative")
    else:
        stock_out(prod_id, qty)

def verify_add_customer(cust_name):
    if bool(fullmatch(r"[A-Za-z0-9 -]+", cust_name)) == False:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-"') 
    elif len(cust_name) > 30:
        raise Exception("max_len = 30 ")
    elif any(cust_name == customer_name for _,customer_name in get_customers()):
        raise Exception("Duplicate customer name")
    else:
        create_customer(cust_name)