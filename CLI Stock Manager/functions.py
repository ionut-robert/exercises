from database import get_connection

def Products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT p.Product_Name, ISNULL(i.Qtty,0) FROM Products p LEFT JOIN Invetory i ON p.Product_Id = i.Product_Id''')
    products = cursor.fetchall()
    conn.commit()
    
    cursor.close()
    conn.close()
    return products

def add_product(product_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''IF NOT EXISTS (SELECT 1 FROM Products WHERE LOWER(Product_Name) = LOWER(?)) BEGIN INSERT INTO Products(Product_Name) VALUES (?) INSERT INTO Invetory (Product_Id,Qtty) SELECT p.Product_Id, 0 FROM Products p WHERE LOWER(p.Product_Name) = LOWER(?) END''',(product_name),(product_name),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def del_product(product_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''IF NOT EXISTS (SELECT 1 FROM StockTransactions st, Products p WHERE st.Product_Id = p.Product_Id AND LOWER(p.Product_Name) = LOWER(?)) BEGIN DELETE FROM Invetory WHERE Product_Id = (SELECT Product_Id FROM Products WHERE LOWER(Product_Name) = LOWER(?)) DELETE FROM Products WHERE Product_Name = ? END''', (product_name),(product_name),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def stock_in(product_name,Qtty):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO StockTransactions (Product_Id,Qtty,Transaction_Type) SELECT p.Product_Id, ?, (SELECT TransactionType_Id FROM TransactionsType WHERE TransactionType_Id = 1) FROM Products p WHERE LOWER(p.Product_Name) = LOWER(?) UPDATE Invetory SET Qtty = Qtty + ? WHERE Product_Id = (SELECT Product_Id FROM Products WHERE LOWER(Product_Name) = LOWER(?))''',(Qtty),(product_name),(Qtty),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def stock_out(product_name,Qtty):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO StockTransactions (Product_Id,Qtty,Transaction_Type) SELECT p.Product_Id, ?, (SELECT TransactionType_Id FROM TransactionsType WHERE TransactionType_Id = 2) FROM Products p WHERE LOWER(p.Product_Name) = LOWER(?) UPDATE Invetory SET Qtty = Qtty - ? WHERE Product_Id = (SELECT Product_Id FROM Products WHERE LOWER(Product_Name) = LOWER(?))''',(Qtty),(product_name),(Qtty),(product_name))
    conn.commit()

    cursor.close()
    conn.close()

def orders(product_name,Qtty,Customer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Orders (Product_Id,TransactionType_Id,Qtty,Customer_Name) SELECT p.Product_Id,(SELECT TransactionType_Id FROM TransactionsType WHERE TransactionType_Id = 3),?,? FROM Products p WHERE LOWER(p.Product_Name) = LOWER(?) UPDATE Invetory SET Qtty = Qtty - ? WHERE Product_Id = (SELECT Product_Id FROM Products WHERE LOWER(Product_Name) = LOWER(?))''',(Qtty),(Customer),(product_name),(Qtty),(product_name))
    conn.commit()

    cursor.close()
    conn.close()