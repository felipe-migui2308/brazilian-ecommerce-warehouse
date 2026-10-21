import sqlite3
from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw")
DATABASE_PATH = Path("data/warehouse/ecommerce.db")


def extract_data():

    files = {
        "orders": "olist_orders_dataset.csv",
        "items": "olist_order_items_dataset.csv",
        "products": "olist_products_dataset.csv",
        "customers": "olist_customers_dataset.csv",
        "categories": "product_category_name_translation.csv"
    }

    data = {}

    for name, filename in files.items():

        path = RAW_PATH / filename

        data[name] = pd.read_csv(path)

        print(
            f"{name}: {len(data[name])} registros carregados"
        )

    return data
def transform_data(data):

    orders = data["orders"].copy()
    items = data["items"].copy()
    products = data["products"].copy()
    customers = data["customers"].copy()
    categories = data["categories"].copy()

    # Converter datas
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # Considerar somente pedidos entregues
    orders = orders[
        orders["order_status"] == "delivered"
    ].copy()

    # Dimensão clientes
    dim_customers = customers[
        [
            "customer_id",
            "customer_city",
            "customer_state"
        ]
    ].drop_duplicates(subset=["customer_id"])

    # Dimensão produtos
    dim_products = products[
        [
            "product_id",
            "product_category_name"
        ]
    ].merge(
        categories,
        on="product_category_name",
        how="left"
    )

    dim_products = dim_products[
        [
            "product_id",
            "product_category_name_english"
        ]
    ].drop_duplicates(subset=["product_id"])

    dim_products = dim_products.rename(
        columns={
            "product_category_name_english": "category"
        }
    )

    dim_products["category"] = (
        dim_products["category"].fillna("unknown")
    )

    # Tabela fato: cada registro é um item de pedido
    fact_sales = items.merge(
        orders[
            [
                "order_id",
                "customer_id",
                "order_purchase_timestamp"
            ]
        ],
        on="order_id",
        how="inner",
        validate="many_to_one"
    )

    fact_sales = fact_sales[
        [
            "order_id",
            "order_item_id",
            "customer_id",
            "product_id",
            "order_purchase_timestamp",
            "price",
            "freight_value"
        ]
    ].copy()

    fact_sales = fact_sales.rename(
        columns={
            "order_purchase_timestamp": "purchase_date"
        }
    )

    fact_sales["purchase_date"] = (
        fact_sales["purchase_date"].dt.strftime("%Y-%m-%d")
    )

    fact_sales = fact_sales.dropna(
        subset=[
            "order_id",
            "order_item_id",
            "customer_id",
            "product_id",
            "purchase_date",
            "price"
        ]
    )

    fact_sales = fact_sales.drop_duplicates(
        subset=["order_id", "order_item_id"]
    )

    # Dimensão de datas
    dates = pd.to_datetime(
        fact_sales["purchase_date"]
    ).drop_duplicates()

    dim_dates = pd.DataFrame({
        "date": dates.dt.strftime("%Y-%m-%d"),
        "year": dates.dt.year,
        "month": dates.dt.month,
        "day": dates.dt.day
    })

    return {
        "dim_customers": dim_customers,
        "dim_products": dim_products,
        "dim_dates": dim_dates,
        "fact_sales": fact_sales
    }
def load_data(tables):

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DATABASE_PATH) as conn:

        for table_name, df in tables.items():

            df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            print(
                f"{table_name}: {len(df)} registros salvos"
            )

        conn.commit()