import sqlite3

DATABASE = "data/warehouse/ecommerce.db"


def main():

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        # Verificar duplicatas na tabela fato
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT order_id, order_item_id
                FROM fact_sales
                GROUP BY order_id, order_item_id
                HAVING COUNT(*) > 1
            )
        """)

        duplicates = cursor.fetchone()[0]

        # Verificar produtos sem correspondência
        cursor.execute("""
            SELECT COUNT(*)
            FROM fact_sales f
            LEFT JOIN dim_products p
                ON f.product_id = p.product_id
            WHERE p.product_id IS NULL
        """)

        missing_products = cursor.fetchone()[0]

        # Verificar clientes sem correspondência
        cursor.execute("""
            SELECT COUNT(*)
            FROM fact_sales f
            LEFT JOIN dim_customers c
                ON f.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """)

        missing_customers = cursor.fetchone()[0]

        print("\n=== DATA QUALITY REPORT ===")

        print(f"Duplicatas: {duplicates}")
        print(f"Produtos sem correspondência: {missing_products}")
        print(f"Clientes sem correspondência: {missing_customers}")

        assert duplicates == 0, "Foram encontradas duplicatas!"
        assert missing_products == 0, "Existem produtos sem correspondência!"
        assert missing_customers == 0, "Existem clientes sem correspondência!"

        print("\nValidação concluída com sucesso!")


if __name__ == "__main__":
    main()