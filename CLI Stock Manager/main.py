from functions import data,add_customer,add_order,add_product,stock_in,stock_out,del_product

if __name__ == '__main__':
    while True:
        menu = ['Menu','1.Add product','2.Delete product','3.All Products','4.Search Product','5.Stock In','6.Stock Out','7.Orders','8.Low Stock Alerts','9.Inventory','10.Exit']

        for row in menu:
            print(row)

        Choice = int(input('\nSelect option number(1-10): '))

        
        if Choice == 1:
            product_name = input('Product Name:')

            try:
                add_product(product_name)
            except Exception as e:
                print('\n',e)
          
        elif Choice == 2:
            product_name = input('Product Name:')

            try:
                del_product(product_name)
            except Exception as e:
                print('\n',e)

        elif Choice == 3:
            print(f"{'No.':<12} {'Product Name':<21}")
            for row in data.products:
                print(f'{row.Product_ID:<12} {row.Product_Name:<7}')

        elif Choice == 4:
            product_name = input('Product Name:')

            print(f"{'No.':<12} {'Product Name':<21}")
            for row in data.products:
                if row[0] == product_name:
                    print(f'{row.Product_ID:<12} {row.Product_Name:<7}')

        elif Choice == 5:
            product_name = input('Product Name: ')
            qtty = float(input('Quantity: '))

            stock_in(product_name,qtty)

        elif Choice == 6:
            product_name = input('Product Name: ')
            qtty = float(input('Quantity: '))

            stock_out(product_name,qtty)

        elif Choice == 7:
            product_name = input('Product Name: ')
            qtty = float(input('Quantity: '))
            customer = input('Customer Name: ')

            add_order(product_name,qtty,customer)

        elif Choice == 8:
            print(f"{'No.':<10}{'Product Name':<21} {'Quantity':<8}")
            for row in data.products:
                if row.Qty < 10:
                    print(f'{row:<21} {row[1]:<7}')
        
        elif Choice == 9:
            for x in zip(data.inventory,data.products):
                print(x[0].Inventory_ID,x[0].Product_ID,x[0].Qty,x[1].Product_ID,x[1].Product_Name)


        elif Choice == 10:
            customer_name = input('Name customer: ')
            add_customer(customer_name)

        elif Choice == 11:
            break

        else:
            print('\nInvalid command')
        input('Press any key to continue\n')


__name__ == '__main__'
