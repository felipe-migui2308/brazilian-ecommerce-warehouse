from src.pipeline import (
    extract_data,
    transform_data,
    load_data
)


def main():

    print("\nIniciando E-commerce Data Warehouse...\n")

    data = extract_data()

    print("\nTransformando dados...\n")

    tables = transform_data(data)

    print("\nCarregando Data Warehouse...\n")

    load_data(tables)

    print("\nData Warehouse criado com sucesso!")


if __name__ == "__main__":
    main()