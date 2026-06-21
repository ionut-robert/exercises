from functions import add_product,del_product,Products,stock_in,stock_out,orders
if __name__ == '__main__':

    while True:
        menu = ['Menu','1.Add product','2.Delete product','3.Show Products','4.Search Product','5.Stock In','6.Stock Out','7.Orders','8.Stock Alerts','9.Invetory','10.Exit']

        for row in menu:
            print(row)

        Choice = int(input('\nSelect option number(1-8): '))

        if Choice == 1:
            product_name = input('Product Name:')
            add_product(product_name)

        elif Choice == 2:
            product_name = input('Product Name:')
            del_product(product_name)

        elif Choice == 3:
            print(f"{'Product Name':<21} {'Quantity':<8}")
            for row in Products():
                print(f'{row[0]:<21} {row[1]:<7}')

        elif Choice == 4:
            product_name = input('Product Name:')
            print(f"{'Product Name':<21} {'Quantity':<8}")
            for row in Products():
                if row[0].lower() == product_name.lower():
                    print(f'{row[0]:<21} {row[1]:<7}')

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
            orders(product_name,qtty,customer)

        elif Choice == 8:
            print(f"{'Product Name':<21} {'Quantity':<8}")
            for row in Products():
                if row[1] < 10:
                    print(f'{row[0]:<21} {row[1]:<7}')
        
        elif Choice == 9:
            print(f"{'Product Name':<21} {'Quantity':<8}")
            for row in Products():
                print(f'{row[0]:<21} {row[1]:<7}')

        elif Choice == 10:
            break

        else:
            print('\nInvalid command')
        input('Press any key to continue\n')

__name__ == '__main__'