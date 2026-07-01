from services.services import verify_create_product,verify_delete_product
from pytest import raises
from db.queries import engine,Session
from db.models import Products
from sqlalchemy import text

def test_err_empty_name_create_product():
    with raises(Exception) as e:
        verify_create_product('')

    assert "Just" in str(e.value)

def test_err_max_len_create_product():
    with raises(Exception) as e:
        verify_create_product('i' * 31)

    assert "max_len" in str(e.value)

def test_err_special_char_create_prod():
    with raises(Exception):
        verify_create_product("Pr@#!")

def test_add_product():
    verify_create_product("Product")
    with Session(engine) as session:
        result = session.query(Products).all()
        assert len(result) == 1

def test_err_duplicate_add_prod():
    with raises(Exception) as e:
        verify_create_product("Product")
    assert "Duplicate" in str(e.value)

def test_err_id_nf_delete_prod():
    with Session(engine) as session:
        product = session.execute(text("SELECT * FROM Products")).mappings().one()
    with raises(Exception):
        verify_delete_product(product.Product_ID)

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