# Source Profile — Interpretation

## customers.csv

1. **Some contact info is missing.** When I profiled this file, I found that out of 250 rows, 3 customers don't have an email and 2 don't have a city listed. Since email could be used to reach customers or identify them, I'd treat these gaps as something that needs to be filled in or explicitly flagged before this data gets used for anything customer-facing, like marketing or support.

2. **A couple of duplicate rows slipped in.** I also found 2 fully identical rows in the file. Interestingly, this shows up alongside a smaller anomaly: there are 250 rows total but only 247 distinct customer_id values, which lines up almost exactly with the 2 duplicate rows I found plus one near-duplicate. Before loading this into a database, I'd want to deduplicate first, using customer_id as the check, otherwise something like a customer count in a report could end up slightly inflated.

## orders.json

1. **The shipping column isn't flat like the rest.** Instead of a simple value, shipping holds a small nested object with a region and a shipping method inside it (for example, {'region': 'Region VII', 'method': 'Standard'}). A regular relational table can't store that as-is without either flattening it into two separate columns (shipping_region, shipping_method) or storing it as raw JSON if the database engine supports a JSON column type, which PostgreSQL does.

2. **The data is clean, but highly unique by design.** I didn't find any missing values or duplicate rows anywhere in this file, which is a good sign for reliability. That said, columns like subtotal and total_amount have a nearly different value in almost every single row (250 distinct values out of 250 rows), which makes sense since they're calculated monetary amounts. That uniqueness is expected here and isn't a data-quality concern, it just means these columns are meant for calculations, not for grouping or acting as identifiers the way order_id can.

## products.parquet

1. **Looks clean overall, but prices vary a lot.** I didn't find any missing data or duplicates across all 200 rows. However, unit_price ranges from as low as ₱392.85 to as high as ₱84,796.84, which is a fairly wide spread for what looks like a single product catalog. I'd want to confirm with whoever owns this data that this range is intentional (different product tiers, for instance) rather than a data-entry mistake like a missing decimal point on some values.

2. **Some products show zero stock.** The stock_quantity column goes as low as 0, which I'd interpret as an item currently being out of stock rather than a data error, since Parquet's embedded schema already confirmed this column is a proper integer type with no nulls. Still, I wouldn't build any pipeline logic that assumes 0 always means "out of stock" without first confirming that interpretation with the source owner, since it could also represent something like a discontinued item.