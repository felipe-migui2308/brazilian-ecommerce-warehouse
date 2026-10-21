import pandas as pd

from src.pipeline import transform_data


def sample_data():
    return {
        "orders": pd.DataFrame({
            "order_id": ["order_1", "order_2"],
            "customer_id": ["customer_1", "customer_2"],
            "order_status": ["delivered", "canceled"],
            "order_purchase_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-11 11:00:00"
            ]
        }),
        "items": pd.DataFrame({
            "order_id": ["order_1", "order_2"],
            "order_item_id": [1, 1],
            "product_id": ["product_1", "product_2"],
            "price": [100.0, 200.0],
            "freight_value": [10.0, 20.0]
        }),
        "products": pd.DataFrame({
            "product_id": ["product_1", "product_2"],
            "product_category_name": ["beleza_saude", None]
        }),
        "customers": pd.DataFrame({
            "customer_id": ["customer_1", "customer_2"],
            "customer_city": ["Belo Horizonte", "São Paulo"],
            "customer_state": ["MG", "SP"]
        }),
        "categories": pd.DataFrame({
            "product_category_name": ["beleza_saude"],
            "product_category_name_english": ["health_beauty"]
        })
    }


def test_only_delivered_orders():
    tables = transform_data(sample_data())

    sales = tables["fact_sales"]

    assert len(sales) == 1
    assert sales.iloc[0]["order_id"] == "order_1"


def test_sales_values():
    tables = transform_data(sample_data())

    sales = tables["fact_sales"]

    assert sales["price"].sum() == 100.0
    assert sales["freight_value"].sum() == 10.0


def test_product_category_translation():
    tables = transform_data(sample_data())

    products = tables["dim_products"]

    category = products.loc[
        products["product_id"] == "product_1",
        "category"
    ].iloc[0]

    assert category == "health_beauty"


def test_unknown_product_category():
    tables = transform_data(sample_data())

    products = tables["dim_products"]

    category = products.loc[
        products["product_id"] == "product_2",
        "category"
    ].iloc[0]

    assert category == "unknown"


def test_date_dimension():
    tables = transform_data(sample_data())

    dates = tables["dim_dates"]

    assert len(dates) == 1
    assert dates.iloc[0]["year"] == 2018
    assert dates.iloc[0]["month"] == 1
    assert dates.iloc[0]["day"] == 10