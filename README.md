# Brazilian E-commerce Data Warehouse

## Visão geral

Este projeto implementa um Data Warehouse para consolidar e analisar
dados históricos de vendas de um e-commerce brasileiro.

A solução utiliza dados públicos da Olist, referentes principalmente
ao período de 2016 a 2018, para transformar informações distribuídas
em arquivos CSV em um modelo dimensional preparado para consultas SQL.

## Problema de negócio

Plataformas de comércio eletrônico armazenam informações de pedidos,
produtos e clientes em diferentes estruturas de dados.

Essa fragmentação dificulta a obtenção de indicadores consolidados,
como volume de vendas, ticket médio, desempenho por categoria
e distribuição geográfica dos pedidos.

## Solução desenvolvida

Foi implementado um pipeline ETL em Python que:

1. Extrai dados de cinco arquivos CSV.
2. Filtra pedidos com status de entrega concluída.
3. Realiza transformações e relacionamentos com Pandas.
4. Organiza os dados em tabelas fato e dimensão.
5. Armazena as informações em SQLite.
6. Disponibiliza consultas SQL para análise comercial.
7. Executa verificações de qualidade e testes automatizados.

## Arquitetura

```text
       Olist Public Dataset
                |
                v
          CSV Files
                |
                v
       Python + Pandas
                |
                v
       ETL Transformation
                |
                v
        SQLite Warehouse
                |
        +-------+-------+
        |               |
        v               v
    Dimensions       Fact Sales
        |               |
        +-------+-------+
                |
                v
         SQL Analytics
```

## Tecnologias

- Python 3.13
- Pandas
- SQLite
- SQL
- Pytest
- Git

## Modelagem dimensional

O Data Warehouse utiliza uma estrutura inspirada no modelo estrela.

### Tabela fato

`fact_sales`

Cada registro representa um item de pedido entregue.

Campos principais:

- order_id
- order_item_id
- customer_id
- product_id
- purchase_date
- price
- freight_value

### Dimensões

`dim_customers`: informações geográficas dos clientes.

`dim_products`: produtos e categorias.

`dim_dates`: datas, anos, meses e dias.

A granularidade da tabela fato é definida pela combinação
de `order_id` e `order_item_id`.

## Resultados

A execução do pipeline produziu:

| Indicador | Resultado |
|---|---:|
| Pedidos entregues | 96.478 |
| Itens de pedidos entregues | 110.197 |
| Valor total dos produtos | R$ 13.221.498,11 |
| Ticket médio por pedido | R$ 137,04 |
| Testes automatizados | 6 aprovados |

Os valores representam os preços dos itens de pedidos entregues,
sem incluir frete. Não representam necessariamente a receita
contábil ou o faturamento líquido da empresa.

## Análises disponíveis

O arquivo `sql/analytics.sql` contém consultas para:

- Valor total dos produtos vendidos.
- Evolução mensal das vendas.
- Categorias com maior valor vendido.
- Estados com maior valor vendido.
- Ticket médio por pedido.

## Qualidade dos dados

O projeto implementa verificações para identificar:

- Duplicatas na tabela fato.
- Produtos sem correspondência na dimensão.
- Clientes sem correspondência na dimensão.

Os testes automatizados verificam a existência das tabelas,
a presença de registros, a ausência de duplicatas e
a integridade dos relacionamentos analisados.

## Estrutura

```text
brazilian-ecommerce-warehouse/
├── data/
│   ├── raw/
│   └── warehouse/
├── src/
│   ├── __init__.py
│   └── pipeline.py
├── sql/
│   └── analytics.sql
├── tests/
│   └── test_warehouse.py
├── main.py
├── queries.py
├── validate.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/felipe-migui2308/brazilian-ecommerce-warehouse.git
cd brazilian-ecommerce-warehouse
```

### 2. Baixar o dataset

Fonte:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Baixe os dados e coloque os seguintes arquivos em `data/raw/`:

- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_products_dataset.csv
- olist_customers_dataset.csv
- product_category_name_translation.csv

### 3. Criar ambiente virtual

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Executar o pipeline

```bash
python main.py
```

### 6. Executar análises SQL

```bash
python queries.py
```

### 7. Validar os dados

```bash
python validate.py
```

### 8. Executar testes

```bash
python -m pytest -v
```

## Decisões técnicas

### Granularidade

A tabela fato utiliza um registro por item de pedido.

Essa escolha permite analisar valores por produto e categoria
sem confundir quantidade de itens com quantidade de pedidos.

### Pedidos entregues

A análise considera apenas pedidos com status `delivered`.

Pedidos cancelados ou com outros status não entram
nos indicadores de vendas deste projeto.

### Estratégia de carregamento

O pipeline utiliza carga completa, substituindo as tabelas
a cada execução.

Essa abordagem foi escolhida porque a fonte utilizada
é um conjunto histórico de dados estáticos.

### Limitações

- O banco não possui restrições formais de chaves estrangeiras.
- O pipeline ainda não implementa carga incremental.
- As consultas financeiras não consideram descontos ou ajustes.
- Os testes dependem de um banco previamente gerado.

## Evoluções futuras

- Implementação de carga incremental.
- Migração para PostgreSQL.
- Criação de restrições de integridade no banco.
- Orquestração com Apache Airflow.
- Integração com ferramentas de BI.
- Análise de atrasos nas entregas.

## Fonte dos dados

Brazilian E-Commerce Public Dataset by Olist.

Dataset público disponibilizado no Kaggle.