from db.queries import engine,Session
from sqlalchemy import text

def test_conn():
    with Session(engine) as session:
        stmt = session.execute(text("SELECT 1"))
        res = stmt.fetchone()

    assert res[0] == 1

