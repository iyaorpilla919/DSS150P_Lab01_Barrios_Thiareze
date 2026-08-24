from pathlib import Path
import pandas as pd

RAW = Path("data/raw")

# LOAD SOURCE FILES
customers = pd.read_csv(RAW / "customers.csv")
orders = pd.read_json(RAW / "orders.json")
products = pd.read_parquet(RAW / "products.parquet")

sources = {
    "customers.csv": customers,
    "orders.json": orders,
    "products.parquet": products,
}

output_lines = []


def log(line=""):
    print(line)
    output_lines.append(str(line))


for name, df in sources.items():
    file_path = RAW / name
    file_size_kb = file_path.stat().st_size / 1024

    log(f"\n{'=' * 60}")
    log(f"=== {name} ===")
    log(f"{'=' * 60}")

    # FILE NAME/SIZE
    log(f"File size: {file_size_kb:.2f} KB")

    # ROWS/COLUMNS
    log(f"Shape (rows, columns): {df.shape}")

    # COLUMN NAMES IN OG ORDER
    log(f"Columns (in order): {list(df.columns)}")

    # DATA TYPES
    log("\nData types per column:")
    log(df.dtypes)

    # NULLS PER COLUMN
    log("\nMissing/null values per column:")
    log(df.isna().sum())

    # DUPLICATE ROWS (safe against unhashable types like nested dicts/lists)
    try:
        dup_count = df.duplicated().sum()
    except TypeError:
        dup_count = df.astype(str).duplicated().sum()
    log(f"\nNumber of fully duplicated rows: {dup_count}")

    # DISTINCT VAL PER COLUMN (safe against unhashable types)
    log("\nDistinct values per column:")
    for col in df.columns:
        try:
            log(f"  {col}: {df[col].nunique()} distinct values")
        except TypeError:
            distinct_count = df[col].astype(str).nunique()
            log(f"  {col}: {distinct_count} distinct values (counted as text, due to nested structure)")

    # First five records
    log("\nFirst 5 records:")
    log(df.head())

    # MIN/MAX NUM COLUMNS
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        log("\nMin/Max for numeric columns:")
        for col in numeric_cols:
            log(f"  {col}: min={df[col].min()}, max={df[col].max()}")
    else:
        log("\nNo numeric columns found.")

    # Earliest/latest for date-like columns
    log("\nDate/time column check:")
    found_date_col = False
    for col in df.columns:
        if df[col].dtype == "object" or "date" in col.lower() or "time" in col.lower():
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                if parsed.notna().sum() > 0:
                    found_date_col = True
                    log(f"  {col}: earliest={parsed.min()}, latest={parsed.max()}")
            except Exception:
                pass
    if not found_date_col:
        log("  No parseable date/time-like columns found.")


output_path = Path("data/evidence/profile_sources_output.txt")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"\n\nFull profiling output saved to {output_path}")