from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_DRIVER=getenv("DB_DRIVER")
SERVER =getenv("SERVER")
DB_DATABASE=getenv("DB_DATABASE")
DB_USER=getenv("DB_USER")
DB_PASSWORD=getenv("DB_PASSWORD")