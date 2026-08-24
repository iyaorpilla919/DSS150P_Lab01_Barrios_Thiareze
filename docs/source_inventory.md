# Source Inventory

## 1. customers.csv

| Field | Value |
|---|---|
| Source name | customers.csv |
| Source-system type | Flat file |
| Data format | CSV |
| Structured / semi-structured / unstructured | Structured |
| Expected update pattern | Batch (manual/periodic drop) |
| Likely acquisition method | Downloaded/copied into data/raw/ |
| Schema location or schema owner | No formal schema; inferred from file headers |
| Possible primary/business key | customer_id |
| Potential schema-evolution risk | New columns added or renamed without notice |
| Potential data-quality risk | Missing values, duplicate rows |

*I confirmed customer_id as a usable key after profiling, though it isn't perfectly unique: I found 250 rows but only 247 distinct customer_id values, along with 2 fully duplicated rows and 3 missing emails and 2 missing city values. This means I'd need a deduplication step before treating customer_id as a strict primary key in production.*

## 2. orders.json

| Field | Value |
|---|---|
| Source name | orders.json |
| Source-system type | Flat file (semi-structured) |
| Data format | JSON |
| Structured / semi-structured / unstructured | Semi-structured |
| Expected update pattern | Batch (manual/periodic drop) |
| Likely acquisition method | Downloaded/copied into data/raw/ |
| Schema location or schema owner | No formal schema; inferred from JSON structure |
| Possible primary/business key | order_id |
| Potential schema-evolution risk | Nested fields added/removed, inconsistent structure |
| Potential data-quality risk | Nested/missing fields, inconsistent data types |

*When I profiled this file, order_id turned out to be fully unique across all 250 rows with zero duplicates and zero nulls in any column, which makes it a reliable key. The shipping field is nested (region and method inside a dictionary), so I'd need to flatten it into separate columns before loading it into a relational table.*

## 3. products.parquet

| Field | Value |
|---|---|
| Source name | products.parquet |
| Source-system type | Flat file (columnar) |
| Data format | Parquet |
| Structured / semi-structured / unstructured | Structured |
| Expected update pattern | Batch (manual/periodic drop) |
| Likely acquisition method | Downloaded/copied into data/raw/ |
| Schema location or schema owner | Embedded schema within the Parquet file itself |
| Possible primary/business key | product_id |
| Potential schema-evolution risk | Column type or name changes between file versions |
| Potential data-quality risk | Type mismatches, missing values |

*Profiling showed product_id was fully unique across all 200 rows with no nulls and no duplicate rows, so it's a solid primary key candidate. Since Parquet stores its schema internally, I didn't need to infer data types manually the way I did with the CSV and JSON files, they came through as proper numeric types (unit_price, stock_quantity, weight_kg) automatically.*

## 4. REST API

| Field | Value |
|---|---|
| Source name | REST API — https://jsonplaceholder.typicode.com/posts |
| Source-system type | Web API |
| Data format | JSON |
| Structured / semi-structured / unstructured | Semi-structured |
| Expected update pattern | Batch / On-demand API retrieval |
| Likely acquisition method | HTTP GET request via requests library |
| Schema location or schema owner | Owned by API provider; no local schema file |
| Possible primary/business key | id |
| Potential schema-evolution risk | API provider changes response structure without notice |
| Potential data-quality risk | Timeouts, malformed responses, unexpected nulls |

*When I called this endpoint, it returned a status 200 with a top-level list of exactly 100 records, each with userId, id, title, and body fields. Since this is a public third-party API I don't control, I have no guarantee this structure or record count will stay the same the next time I call it.*

## 5. PostgreSQL table (inventory_snapshot)

| Field | Value |
|---|---|
| Source name | inventory_snapshot |
| Source-system type | Relational database table |
| Data format | SQL table (PostgreSQL) |
| Structured / semi-structured / unstructured | Structured |
| Expected update pattern | Periodic batch snapshot |
| Likely acquisition method | SQL SELECT query via SQLAlchemy/psycopg2 |
| Schema location or schema owner | Defined in PostgreSQL information_schema (public schema) |
| Possible primary/business key | item_id (PRIMARY KEY) |
| Potential schema-evolution risk | Column added/dropped/altered in the database without notice |
| Potential data-quality risk | Null values in optional fields (category, last_updated) |

*I inspected this table directly through information_schema.columns rather than a file, which is a fundamentally different acquisition pattern from the other four sources: there's no download step, just a live query against a running database that could change between the moment I query it and the moment a pipeline actually loads from it.*

## Retrieval Timestamps

* **REST API:** `retrieved_at_utc: 2026-08-24T14:30:04.708269+00:00`
* **PostgreSQL:** `retrieved_at_utc: 2026-08-24T15:07:55.561364+00:00`