from repository import *

def products_with_stock():
    return productXstock()

def verify_create_product(name):
    create_product(name)

def verify_delete_product(id):
    delete_product(id)

def verify_create_customer(name):
    create_customer(name)

def verify_create_order(prod_id,cust_id,qty):
    create_order(prod_id,cust_id,qty)

def verify_stock_in(prod_id, qty):
    stock_in(prod_id, qty)

def verify_stock_out(prod_id, qty):
    stock_out(prod_id, qty)

