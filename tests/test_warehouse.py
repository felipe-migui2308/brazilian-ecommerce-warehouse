import sqlite3

import pytest

from src.pipeline import DATABASE_PATH


@pytest.fixture
def conn():
    if not DATABASE_PATH.exists():
        pytest.fail("Banco não encontrado. Execute python main.py primeiro.")

    connection = sqlite3.connect(DATABASE_PATH)
    yield connection
    connection.close()


def test_tables_exist(conn):
    tables = {
        row[0]
        for row in conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """)
    }

    expected = {
        "dim_customers",
        "dim_products",
        "dim_dates",
        "fact_sales"
    }

    assert expected.issubset(tables)


def test_fact_sales_not_empty(conn):
    count = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales
    """).fetchone()[0]

    assert count > 0


def test_no_duplicate_sales(conn):
    duplicates = conn.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT order_id, order_item_id
            FROM fact_sales
            GROUP BY order_id, order_item_id
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]

    assert duplicates == 0


def test_product_relationship(conn):
    missing = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales f
        LEFT JOIN dim_products p
            ON f.product_id = p.product_id
        WHERE p.product_id IS NULL
    """).fetchone()[0]

    assert missing == 0


def test_customer_relationship(conn):
    missing = conn.execute("""
        SELECT COUNT(*)
        FROM fact_sales f
        LEFT JOIN dim_customers c
            ON f.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """).fetchone()[0]

    assert missing == 0


def test_sales_value(conn):
    total = conn.execute("""
        SELECT SUM(price)
        FROM fact_sales
    """).fetchone()[0]

    assert total is not None
    assert total > 0