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
| Possible primary/business key | customer_id (to confirm after profiling) |
| Potential schema-evolution risk | New columns added or renamed without notice |
| Potential data-quality risk | Missing values, duplicate rows |

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
| Possible primary/business key | order_id (to confirm after profiling) |
| Potential schema-evolution risk | Nested fields added/removed, inconsistent structure |
| Potential data-quality risk | Nested/missing fields, inconsistent data types |

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
| Possible primary/business key | product_id (to confirm after profiling) |
| Potential schema-evolution risk | Column type or name changes between file versions |
| Potential data-quality risk | Type mismatches, missing values |

## 4. REST API

| Field | Value |
|---|---|
| Source name | REST API (instructor-provided endpoint) |
| Source-system type | Web API |
| Data format | JSON |
| Structured / semi-structured / unstructured | Semi-structured |
| Expected update pattern | Unknown - requires confirmation (likely near real-time or on-demand) |
| Likely acquisition method | HTTP GET request via requests library |
| Schema location or schema owner | Owned by API provider; no local schema file |
| Possible primary/business key | Unknown until response is inspected |
| Potential schema-evolution risk | API provider changes response structure without notice |
| Potential data-quality risk | Timeouts, malformed responses, unexpected nulls |

## 5. PostgreSQL table (inventory_snapshot)

| Field | Value |
|---|---|
| Source name | inventory_snapshot |
| Source-system type | Relational database table |
| Data format | SQL table (Postgres) |
| Structured / semi-structured / unstructured | Structured |
| Expected update pattern | Unknown - requires confirmation (likely batch snapshot) |
| Likely acquisition method | SQL SELECT query via SQLAlchemy/psycopg2 |
| Schema location or schema owner | Defined in PostgreSQL information_schema |
| Possible primary/business key | To confirm via information_schema.columns constraints |
| Potential schema-evolution risk | Column added/dropped/altered in the database without notice |
| Potential data-quality risk | Stale snapshot data, null values in optional columns |

## Retrieval Timestamp (REST API)

retrieved_at_utc: <fill in after running inspect_api.py, e.g. 2026-08-24T10:15:00+00:00>