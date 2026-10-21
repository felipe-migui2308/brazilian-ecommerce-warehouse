import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("data/warehouse/ecommerce.db")
SQL_PATH = Path("sql/analytics.sql")


def main():

    sql_content = SQL_PATH.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    with sqlite3.connect(DATABASE_PATH) as conn:

        for index, query in enumerate(queries, start=1):

            print(f"\n{'=' * 60}")
            print(f"CONSULTA {index}")
            print("=" * 60)

            result = pd.read_sql_query(query, conn)

            print(result.to_string(index=False))


if __name__ == "__main__":
    main()