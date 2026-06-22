from database import get_connection

def Products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT p.Product_Name, i.Qtty FROM Products p LEFT JOIN Inventory i ON p.Product_ID = i.Product_ID''')
    products = cursor.fetchall()
    conn.commit()
    
    cursor.close()
    conn.close()
    return products

def add_product(product_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''IF NOT EXISTS (SELECT 1 FROM Products WHERE LOWER(Product_Name) = LOWER(?)) BEGIN INSERT INTO Products(Product_Name) VALUES (?) END''',(product_name),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def del_product(product_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''IF NOT EXISTS (SELECT 1 FROM StockTransactions st, Products p WHERE st.Product_ID = p.Product_ID AND LOWER(p.Product_Name) = LOWER(?)) BEGIN DELETE FROM Inventory WHERE Product_ID = (SELECT Product_ID FROM Products WHERE LOWER(Product_Name) = LOWER(?)) DELETE FROM Products WHERE Product_Name = ? END''', (product_name),(product_name),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def stock_in(product_name,Qtty):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO StockTransactions (Product_ID,Qtty,TransactionType_ID) (SELECT Product_ID, ?,(SELECT TransactionType_ID FROM TransactionType WHERE TransactionType_ID = 1) FROM Products WHERE LOWER(Product_Name) = LOWER(?)) UPDATE Inventory SET Qtty = Qtty + ? WHERE Product_ID = (SELECT Product_ID FROM Products WHERE LOWER(Product_Name) = LOWER(?))''',(Qtty),(product_name),(Qtty),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def stock_out(product_name,Qtty):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO StockTransactions (Product_ID,Qtty,TransactionType_ID) SELECT p.Product_ID, ?, (SELECT TransactionType_ID FROM TransactionType WHERE TransactionType_ID = 2) FROM Products p WHERE LOWER(p.Product_Name) = LOWER(?) UPDATE Inventory SET Qtty = Qtty - ? WHERE Product_ID = (SELECT Product_ID FROM Products WHERE LOWER(Product_Name) = LOWER(?))''',(Qtty),(product_name),(Qtty),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def orders(product_name,Qtty,Customer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Orders (Product_ID,TransactionType_ID,Qtty,Customer_Name) SELECT p.Product_ID,(SELECT TransactionType_ID FROM TransactionType WHERE TransactionType_ID = 3),?,? FROM Products p WHERE LOWER(p.Product_Name) = LOWER(?) UPDATE Inventory SET Qtty = Qtty - ? WHERE Product_ID = (SELECT Product_ID FROM Products WHERE LOWER(Product_Name) = LOWER(?))''',(Qtty),(Customer),(product_name),(Qtty),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def catalog_products():
    print(f"{'Product Name':<21} {'Quantity':<8}")
    for row in Products():
        print(f'{row[0]:<21} {row[1]:<7}')
