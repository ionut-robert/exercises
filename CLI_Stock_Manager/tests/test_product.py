from services.services import verify_add_product,verify_delete_product
from pytest import raises
from db.queries import engine,Session
from db.models import Products
from sqlalchemy import text

def test_err_special_char_add_prod():
    with raises(Exception):
        verify_add_product("Pr@#!")

def test_add_product():
    verify_add_product("Product")
    with Session(engine) as session:
        result = session.query(Products).all()
        assert len(result) == 1

def test_err_duplicate_add_prod():
    with raises(Exception):
        verify_add_product("Product")

def test_err_id_nf_delete_prod():
    with raises(Exception):
        verify_delete_product(2)

def test_delete_product():
    with Session(engine) as session:
        verify_delete_product(1)
        result = session.query(Products).all()

        assert len(result) == 0

        session.rollback()

def test_drop_table(): #!!!!!!!!!!
    with Session(engine) as session:
        session.execute(text("DROP TABLE StockTransactions,Orders,Customers,Inventory,Products,TransactionType"))
        session.commit()