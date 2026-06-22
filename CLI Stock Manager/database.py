import pyodbc
from config import DB_DRIVER,SERVER,DB_DATABASE,DB_USER,DB_PASSWORD

def get_connection():
    conn = pyodbc.connect(DB_DRIVER, host=SERVER, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, TrustServerCertificate='yes')
    return conn

create =  False
if create == True:
    cnxn = get_connection()
    cursor = cnxn.cursor()

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables)
    BEGIN
    CREATE TABLE Products (
        Product_ID INT IDENTITY(1,1) PRIMARY KEY,
        Product_Name VARCHAR(50) NOT NULL
    )

    CREATE TABLE Inventory(
        Product_ID INT,
        Qtty FLOAT DEFAULT(0)

        FOREIGN KEY (Product_ID)
        REFERENCES Products(Product_ID)
    )
    CREATE TABLE TransactionType(
        TransactionType_ID INT IDENTITY(1,1) PRIMARY KEY,
        TransactionType_Name VARCHAR(20)
    )

    CREATE TABLE Orders (
        Order_ID INT IDENTITY(1,1) PRIMARY KEY,
        StockTransaction_ID INT,
        Product_ID INT,
        Qtty FLOAT,
        Customer_Name VARCHAR(50),
        TransactionType_ID INT DEFAULT(3)

        FOREIGN KEY (Product_ID)
        REFERENCES Products(Product_ID),
        FOREIGN KEY (TransactionType_ID)
        REFERENCES TransactionType(TransactionType_ID)
    )

    CREATE TABLE StockTransactions(
        StockTransaction_ID INT IDENTITY(1,1) PRIMARY KEY,
        Product_ID INT,
        Qtty FLOAT,
        TransactionType_ID INT

        FOREIGN KEY (Product_ID)
        REFERENCES Products(Product_ID),
        FOREIGN KEY (TransactionType_ID)
        REFERENCES TransactionType(TransactionType_ID)
    )
    END ''')

    cursor.execute('''CREATE TRIGGER trg_inventory_insert
        ON Products
        AFTER INSERT
    AS 
    BEGIN
        INSERT INTO Inventory 
        SELECT TOP 1 Product_ID,0
        FROM Products
        ORDER BY Product_ID DESC
    END
                   
    INSERT INTO TransactionType(TransactionType_Name) VALUES ('IN','OUT','ORDER')''')
    
    cnxn.commit()
    cursor.close()
    cnxn.close()
