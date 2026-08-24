# Source Profile — Interpretation

## customers.csv
1. **Some contact info is missing.** Out of 250 rows, 3 customers don't have an email and 2 don't have a city listed. Since email could be used to reach customers or identify them, these gaps would need to be filled in or flagged before this data is used for anything important.
2. **A couple of duplicate rows slipped in.** The file has 2 fully identical rows. Before loading this into a database, we'd want to remove duplicates first (probably using `customer_id` as the check), otherwise things like customer counts in reports could end up slightly inflated.

## orders.json
1. **The `shipping` column isn't flat like the rest.** Instead of a simple value, `shipping` holds a small object with a region and a shipping method inside it (e.g., `{'region': 'Region VII', 'method': 'Standard'}`). A regular database table can't store that as-is, so it would need to be split into two separate columns, or saved as raw JSON if the database supports it.
2. **Data is clean, but very unique.** There are no missing values and no duplicate rows here, which is a good sign. That said, columns like `subtotal` and `total_amount` have a different value in almost every row, which makes sense since they're money amounts — they're meant for calculations, not for grouping or acting as identifiers.

## products.parquet
1. **Looks clean overall, but prices vary a lot.** No missing data and no duplicates in any of the 200 rows. However, `unit_price` ranges from as low as ₱392.85 to as high as ₱84,796.84, which is a pretty big spread. It's worth double-checking with whoever owns this data to confirm those aren't typos (like a missing decimal point).
2. **Some products show zero stock.** The `stock_quantity` column goes as low as 0, which most likely just means an item is currently out of stock rather than a mistake in the data. Still, this should be confirmed with the source owner before any logic assumes 0 stock is always an error.