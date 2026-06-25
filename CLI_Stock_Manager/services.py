from repository import stock_in,stock_out,delete_product,get_customers,get_products_invetory,add_customer,add_order,add_product
from regex import fullmatch

def Reports(prod_name = None, show_qty = None, min_qty = None):#(2 ways?)

    global ids,names

    ids = []
    names = []
    qtys = []

    for id,name,qty in get_products_invetory():
        ids.append(id)
        names.append(name)
        qtys.append(qty)
    
    #Without qty
    if prod_name == None and show_qty == None and min_qty == None: 
        print(f"{'No':<6}{'Name':<20}")   
        for id,name in zip(ids,names):
            print(f"{id:<6}{name:<20}") 
        
    #With QTY
    else:
        print(f"{'No':<6}{'Name':<20}{'Qty':<5}")

        #search prod        
        if prod_name in names:
            indx = names.index(prod_name)
            print(f"{ids[indx]:<6}{names[indx]:<20}{qtys[indx]:<5}")
        
        else:
          for id,name,qty in zip(ids,names,qtys):
              #inventory
              if min_qty == None:
                  print(f"{id:<6}{name:<20}{qty:<5}")
              #qty alert
              elif qty < min_qty:
                  print(f"{id:<6}{name:<20}{qty:<5}1")
                


def verify_create_product(name):

    if len(name) < 50: 
        raise Exception('Product name > 50 char')
    
    elif bool(fullmatch(r"[A-Za-z0-9 -]+", name)) == True:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-" ') 
    
    else:
        add_product(name)


def verify_delete_product(id):
    delete_product(id)

def verify_create_customer(name):

    res = bool(fullmatch(r"[A-Za-z -]+", name))

    if len(name) < 50 and res == True:
        add_customer(name)
    
    #errs
    else:
        # name < 50
        if len(name) < 50:
            raise Exception('Product name must have < 50 char')
        
        #res have invalid char
        elif res == False:
            raise Exception(f'Just A-Z, a-z, [space], [tab], "-" ')

def verify_create_order(prod_id,cust_id,qty):
    add_order(prod_id,cust_id,qty)

def verify_stock_in(prod_id, qty):
    stock_in(prod_id, qty)

def verify_stock_out(prod_id, qty):
    stock_out(prod_id, qty)
