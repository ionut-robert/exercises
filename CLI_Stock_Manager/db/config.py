from dotenv import load_dotenv
from os import getenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine

load_dotenv()

DB_DRIVER=getenv("DB_DRIVER")
SERVER =getenv("SERVER")
DB_DATABASE=getenv("DB_DATABASE")
DB_USER=getenv("DB_USER")
DB_PASSWORD=quote_plus(getenv("DB_PASSWORD"))

engine = create_engine(f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{SERVER}:1433/{DB_DATABASE}?{DB_DRIVER}&TrustServerCertificate=yes",echo=False)