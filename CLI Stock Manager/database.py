import pyodbc
from config import DB_DRIVER,SERVER,DB_DATABASE,DB_USER,DB_PASSWORD

def get_connection():
    conn = pyodbc.connect(DB_DRIVER, host=SERVER, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, TrustServerCertificate='yes')
    return conn


cnxn = get_connection()
cursor = cnxn.cursor()

cursor.execute('''IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Products') BEGIN CREATE TABLE Products(Product_Id INT IDENTITY(1,1) PRIMARY KEY, Product_Name VARCHAR(255)) END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Invetory') BEGIN CREATE TABLE Invetory(Product_Id INT, Qtty FLOAT, FOREIGN KEY (Product_Id) REFERENCES Products(Product_Id)) END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'TransactionsType') BEGIN CREATE TABLE TransactionsType(TransactionType_Id INT IDENTITY(1,1) PRIMARY KEY, TransactionType_Name VARCHAR(255)) END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'StockTransactions') BEGIN CREATE TABLE StockTransactions(Transaction_Id INT IDENTITY(1,1) PRIMARY KEY,Product_Id INT, Qtty FLOAT, Transaction_Type INT, FOREIGN KEY (Product_Id) REFERENCES Products(Product_Id),FOREIGN KEY (Transaction_Type) REFERENCES TransactionsType(TransactionType_Id)) END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Orders') BEGIN CREATE TABLE Orders(Order_Id INT IDENTITY(1,1) PRIMARY KEY, TransactionType_Id INT, Qtty FLOAT, Product_Id INT,Customer_Name varchar(255), FOREIGN KEY(TransactionType_Id) REFERENCES TransactionsType(TransactionType_Id),FOREIGN KEY(Product_Id) REFERENCES Products(Product_Id)) END
               
IF (SELECT COUNT(TransactionType_Name) FROM TransactionsType WHERE TransactionType_Name IN ('IN','OUT','Order')) = 0 BEGIN INSERT INTO TransactionsType(TransactionType_Name) VALUES ('Orders'),('IN'),('OUT') END''')

cursor.commit()
cnxn.close()