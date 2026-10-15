
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "fact_electricity_prices.csv"

df = pd.read_csv(INPUT_FILE, parse_dates=["date"])

print("ELECTRICITY PRICE DATA VALIDATION")
print("=" * 45)

print(f"Total rows: {len(df):,}")
print(f"Columns: {list(df.columns)}")
print(f"Geographies: {df['geo'].nunique()}")
print(f"Periods: {df['period'].nunique()}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

print("\nMissing values:")
print(df.isna().sum().to_string())

key_columns = [
    "freq", "siec", "nrg_cons", "unit",
    "tax", "currency", "geo", "period"
]

duplicates = df.duplicated(subset=key_columns).sum()
print(f"\nDuplicate observations: {duplicates}")

print("\nCurrencies:")
print(df["currency"].value_counts().to_string())

print("\nTax categories:")
print(df["tax"].value_counts().to_string())

print("\nConsumption bands:")
print(df["nrg_cons"].value_counts().to_string())

# Profile the proposed dashboard selection.
dashboard = df[
    (df["currency"] == "EUR")
    & (df["nrg_cons"] == "KWH2500-4999")
    & (df["tax"] == "I_TAX")
].copy()

print("\nPROPOSED DASHBOARD SCOPE")
print("=" * 45)
print("Currency: EUR")
print("Consumption band: KWH2500-4999")
print("Tax category: I_TAX")
print(f"Rows: {len(dashboard):,}")
print(f"Geographies: {dashboard['geo'].nunique()}")
print(f"Periods: {dashboard['period'].nunique()}")
print(
    f"Date range: {dashboard['date'].min()} "
    f"to {dashboard['date'].max()}"
)

print("\nSample prices:")
print(
    dashboard[
        ["geo", "period", "tax", "currency", "value"]
    ].head(10).to_string(index=False)
)

print("\nSTATUS")
if duplicates == 0 and df["value"].notna().all():
    print("PASS: No duplicate observations or missing prices.")
else:
    print("CHECK REQUIRED: Review duplicates or missing prices.")
