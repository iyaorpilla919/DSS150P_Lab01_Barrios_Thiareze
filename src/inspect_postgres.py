from sqlalchemy import create_engine, text
from pathlib import Path
from datetime import datetime, timezone
import json

engine = create_engine(
    "postgresql+psycopg2://dss150p:dss150p_lab@localhost:5432/dss150p_lab"
)

output_lines = []


def log(line=""):
    print(line)
    output_lines.append(str(line))


with engine.connect() as conn:
    # LIST TABLES
    log("=== Available tables ===")
    tables = conn.execute(text("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
    """)).fetchall()
    for schema, table in tables:
        log(f"  {schema}.{table}")

    table_name = "inventory_snapshot"

    # COLUMNS/DATA TYPES/NULLABILITY
    log(f"\n=== Columns for '{table_name}' ===")
    columns = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position;
    """), {"table_name": table_name}).fetchall()

    for col_name, data_type, is_nullable in columns:
        log(f"  {col_name} | {data_type} | nullable={is_nullable}")

    # CONSTRAINTS/KEYS
    log(f"\n=== Constraints for '{table_name}' ===")
    constraints = conn.execute(text("""
        SELECT tc.constraint_type, kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_name = :table_name;
    """), {"table_name": table_name}).fetchall()

    if constraints:
        for constraint_type, column_name in constraints:
            log(f"  {constraint_type} on {column_name}")
    else:
        log("  No constraints found.")

    # ROWS COUNT
    log(f"\n=== Row count for '{table_name}' ===")
    row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).scalar()
    log(f"  {row_count} rows")

    # SAMPLE ROWS
    log(f"\n=== Sample rows (first 5) from '{table_name}' ===")
    sample_rows = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5;")).fetchall()
    for row in sample_rows:
        log(f"  {row}")


output_path = Path("data/evidence/postgres_inspection_output.txt")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

retrieved_at_utc = datetime.now(timezone.utc).isoformat()
print(f"\nSaved output to: {output_path}")
print(f"retrieved_at_utc: {retrieved_at_utc}")
