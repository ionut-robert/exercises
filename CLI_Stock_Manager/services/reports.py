from db.queries import get_products,get_invetory

def invetory_product():
    ids = []
    names = []
    qtys = []

    for prod,inv in zip(get_products(),get_invetory()):
        if prod[0] == inv[0]:
            ids.append(prod[0])
            names.append(prod[1])
            qtys.append(inv[1])

    return ids,names,qtys

def all_products():
    print(f"{'No':<6}{'Name':<20}") 

    for id,name in get_products():
        print(f"{id:<6}{name:<20}") 
    
def find_product(product_name):
    ids,names,qtys = invetory_product()

    print(f"{'No':<6}{'Name':<20}{'Qty':<5}") 

    if product_name not in names:
        raise Exception("Product not found")
    elif len(product_name) > 30:
        raise Exception("Max_len = 30")
    else:
        indx = names.index(product_name)
        print(f"{ids[indx]:<6}{names[indx]:<20}{qtys[indx]:<5}")

def low_stock(min_stock_qty):
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}") 

    for prod,inv in zip(get_products(),get_invetory()):
        if inv[1] < min_stock_qty and prod[0] == inv[0]:
            print(f"{prod[0]:<6}{prod[1]:<20}{inv[1]}")
        else:
            pass

def inventory_report():
    print(f"{'No':<6}{'Name':<20}{'Qty':<5}") 

    for prod,inv  in zip(get_products(),get_invetory()):
            if prod[0] == inv[0]:
                print(f"{prod[0]:<6}{prod[1]:<20}{inv[1]:<5}")