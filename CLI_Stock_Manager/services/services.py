from db.queries import get_products,add_product,get_stocktransactions,delete_product,get_customers,stock_in,stock_out,add_customer,add_order
from regex import fullmatch

def verify_add_product(prod_name):
    if bool(fullmatch(r"[A-Za-z0-9 -.]+", prod_name)) == False:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-", "." ') 
    elif len(prod_name) > 30:
        raise Exception("max_len = 30 ")
    elif prod_name in [names for id,names in get_products()]:
        raise Exception("Duplicate product name ")
    else:
        add_product(prod_name)
        print('Product added successfully')

def verify_delete_product(prod_id):
    if prod_id not in get_products()[0]:
        raise Exception("Product id not found")
    elif prod_id in get_stocktransactions():
        raise Exception("Product has stock movements")
    else:
        delete_product(prod_id)

def verify_add_order(prod_id,cust_id,qty):
    if prod_id not in get_products()[0]:
        raise Exception("Product not exists")
    elif cust_id not in get_customers()[0]:
        raise Exception("Customer not exists")
    elif qty < 0:
        raise Exception("Qty cannot be negative")
    else:
        add_order(prod_id,cust_id,qty)

def verify_stock_in(prod_id, qty):
    if prod_id not in get_products()[0]:
        raise Exception("Product id not found")
    elif qty < 0:
        raise Exception("Qty cannot be negative")
    else:
        stock_in(prod_id, qty)

def verify_stock_out(prod_id, qty):
    if prod_id not in get_products()[0]:
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
    elif cust_name in get_customers()[1]:
        raise Exception("Duplicate customer name")
    else:
        add_customer(cust_name)