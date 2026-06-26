from repository import stock_in,stock_out,delete_product,get_customers,get_products_invetory,add_customer,add_order,add_product,get_products,get_stocktransactions
from regex import fullmatch

class Report():
    def __init__(self): 
        self.ids = []
        self.names = []
        self.qtys = []

        for id,name,qty in get_products_invetory():
            self.ids.append(id)
            self.names.append(name)
            self.qtys.append(qty)
    
    def all_products(self):
        print(f"{'No':<6}{'Name':<20}")   
        for id,name in zip(self.ids,self.names):
            print(f"{id:<6}{name:<20}") 
        
    def find_product(self,product_name):
        print(f"{'No':<6}{'Name':<20}{'Qty':<5}")    
        if product_name in self.names:
            indx = self.names.index(product_name)
            print(f"{self.ids[indx]:<6}{self.names[indx]:<20}{self.qtys[indx]:<5}")
        else:
            raise Exception("Product not found")

    def low_stock(self,min_stock_qty):
        for id,name,qty in zip(self.ids,self.names,self.qtys):
            if qty < min_stock_qty:
                print(f"{id:<6}{name:<20}{qty:<5}")
            else:
                pass

    def inventory_report(self):
        for id,name,qty in zip(self.ids,self.names,self.qtys):
                print(f"{id:<6}{name:<20}{qty:<5}")

class CheckRules:
    def __init__(self):
        self.product_ids = []
        self.product_names = []

        for id,name in get_products():
            self.product_ids.append(id)
            self.product_names.append(name)
    
    def verify_add_product(self,prod_name):
        if bool(fullmatch(r"[A-Za-z0-9 -.]+", prod_name)) == False:
            raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-", "." ') 
        elif len(prod_name) > 30:
            raise Exception("max_len = 30 ")
        elif prod_name in self.product_names:
            raise Exception("Duplicate product name ")
        else:
            add_product(prod_name)
            print('Product added successfully')

    def verify_delete_product(self,prod_id):
        if prod_id not in self.product_ids:
            raise Exception("Product id not found")
        elif prod_id in stockT_data():
            raise Exception("Product have stock movements")
        else:
            delete_product(prod_id)

    def verify_add_order(self,prod_id,cust_id,qty):
        if prod_id not in self.product_ids:
            raise Exception("Product not exists")
        elif cust_id not in customers_data()[0]:
            raise Exception("Customer not exists")
        elif qty < 0:
            raise Exception("Qty cannot be negative")
        else:
            add_order(prod_id,cust_id,qty)

    def verify_stock_in(self,prod_id, qty):
        if prod_id not in self.product_ids:
            raise Exception("Product id not found")
        elif qty < 0:
            raise Exception("Qty cant be negative")
        else:
            stock_in(prod_id, qty)

    def verify_stock_out(self,prod_id, qty):
        if prod_id not in self.product_ids:
            raise Exception("Product id not found")
        elif qty < 0:
            raise Exception("Qty cant be negative")
        else:
            stock_out(prod_id, qty)

def stockT_data():
    PstockT_ids = set()

    for ids in get_stocktransactions():
        PstockT_ids.add(ids[0])
    
    return PstockT_ids

def customers_data():
    customer_ids = []
    customer_names = []

    for id,name in get_customers():
        customer_ids.append(id)
        customer_names.append(name)

    return customer_ids,customer_names

def verify_add_customer(cust_name):
    if bool(fullmatch(r"[A-Za-z0-9 -]+", cust_name)) == False:
        raise Exception(f'Just A-Z, a-z, 0-9, [space], [tab], "-"') 
    elif len(cust_name) > 30:
        raise Exception("max_len = 30 ")
    elif cust_name in customers_data()[1]:
        raise Exception("Duplicate customer name")
    else:
        add_customer(cust_name)