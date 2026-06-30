from db.queries import get_inventory_products

def all_products():
    print(f"{'No':<6}{'Name':<20}") 

    for id,name,_ in get_inventory_products():
        print(f"{id:<6}{name:<20}") 
    
def find_product(product_name):
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}") 

    if not any(product_name == name for _,name,_ in get_inventory_products()):
        raise Exception("Product not found")
    elif len(product_name) > 30:
        raise Exception("Max_len = 30")
    else:
        target = next((elem for elem in get_inventory_products() if elem[1] == product_name),None)
        id,name,qty = target
        print(f"{id:<6}{name:<20}{qty:<5}")

def low_stock(min_stock_qty):
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}") 

    for id,name,qty in get_inventory_products():
        if qty < min_stock_qty:
            print(f"{id:<6}{name:<20}{qty}")

def inventory_report():
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}") 

    for id,name,qty in get_inventory_products():
        print(f"{id:<6}{name:<20}{qty:<5}")