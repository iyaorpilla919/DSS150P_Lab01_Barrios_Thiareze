# DSS150P Lab 01 — Data Source Assessment

**Student Name:** Thiareze Orpilla Barrios

**Student Number:** 2024100899

## Purpose
In this laboratory, I set up a reproducible local data-engineering environment and performed a first-pass technical assessment of multiple source systems (CSV, JSON, Parquet, REST API, and PostgreSQL) to prepare for future pipeline development.

## Software Requirements
- Python 3.x
- Git
- Docker Desktop (with Docker Compose)
- Visual Studio Code

## Steps I Followed to Reproduce the Environment

1. I cloned this repository:
```
git clone https://github.com/iyaorpilla919/DSS150P_Lab01_Barrios_Thiareze.git
cd DSS150P_Lab01_Barrios_Thiareze
```
2. I created a virtual environment:
```
python -m venv .venv
```
3. I activated the virtual environment:
```
.\.venv\Scripts\Activate.ps1
```
4. I installed the dependencies:
```
pip install -r requirements.txt
```

## Starting and Stopping PostgreSQL

To start the database, I ran:
```
docker compose up -d
```

To confirm it was running, I ran:
```
docker ps
```

To stop the database, I ran:
```
docker compose down
```

## How I Ran Each Python Script

To verify the PostgreSQL connection, I ran:
```
python src/verify_environment.py
```

To profile the CSV, JSON, and Parquet source files, I ran:
```
python src/profile_sources.py
```

To retrieve and inspect the REST API, I ran:
```
python src/inspect_api.py
```

## Description of Each Source

- **customers.csv** — A flat, structured file containing customer records (customer_id, first_name, last_name, email, city, signup_date, customer_segment).
- **orders.json** — A semi-structured JSON file containing order records.
- **products.parquet** — A structured, columnar file containing product catalog data.
- **REST API** (`https://jsonplaceholder.typicode.com/posts`) — An external JSON API returning a list of post/order-style records, which I used to simulate a live data source.
- **PostgreSQL** — A relational database source running in Docker. I inspected it using `information_schema` to document its table structure, and used it to store the formalized `lab.customers` schema I created in Task 3.2.

## AI Usage
**Tool Used:** Claude

**What I asked it to help with:** 

- I asked it to help me understand some terms that I don't quite understand at first.
- Helped me navigate how to view the code table I built into a real digital table, which was resolved and it was the "Open as Preview" button.
- I asked it to guide me resolve errors that occured.

**What I changed/verified myself**
-  Helped me cross-check if I have done everything right accordingly to the instructions for this task.
- Helped me understand to accomplish the task step-by-step and letting me do the work.


## Known Limitations / Unresolved Questions

- I could not confirm a data owner for any of the sources used in this lab; I marked ownership as "unknown - requires source owner confirmation" in the data contract.
- I don't know the freshness/update expectations for customers.csv — this would require confirmation from a real source owner in a production setting.
- My professor's GitHub collaborator invite may still show as "Pending" until it's accepted on their end.
- I did not load bulk data into PostgreSQL beyond schema definition, per the lab instructions (the focus was schema definition and validation, not full data loading).
- The data contract in Task 3.3 revealed that the actual customers.csv file contains separate first_name and last_name columns, while the PostgreSQL schema built in Task 3.2 used a single full_name column instead. This discrepancy was identified during review but the Task 3.2 schema was intentionally left unchanged to preserve the original implementation and avoid introducing new untested changes late in the lab.