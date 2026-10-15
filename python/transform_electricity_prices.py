
import re
from pathlib import Path

import pandas as pd

# Resolve project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "data" / "raw" / "nrg_pc_204_raw.tsv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "fact_electricity_prices.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Reading raw electricity-price data...")

df = pd.read_csv(INPUT_FILE, sep="\t", dtype=str)

# Remove trailing/leading whitespace from column names
df.columns = df.columns.str.strip()

# Eurostat combines the dimension codes in the first column.
dimension_column = df.columns[0]

dimension_names = [
    "freq",
    "siec",
    "nrg_cons",
    "unit",
    "tax",
    "currency",
    "geo",
]

dimensions = df[dimension_column].str.split(",", expand=True)
dimensions.columns = dimension_names

df = pd.concat(
    [dimensions, df.drop(columns=[dimension_column])],
    axis=1,
)

# Convert the wide half-year columns into rows.
period_columns = [
    column
    for column in df.columns
    if re.fullmatch(r"\d{4}-S[12]", column)
]

if not period_columns:
    raise ValueError("No half-year period columns were found.")

fact = df.melt(
    id_vars=dimension_names,
    value_vars=period_columns,
    var_name="period",
    value_name="raw_value",
)

# Extract the numeric value and preserve any observation flag.
raw_value = fact["raw_value"].fillna("").str.strip()

fact["value"] = pd.to_numeric(
    raw_value.str.extract(
        r"^\s*(-?\d+(?:\.\d+)?)"
    )[0],
    errors="coerce",
)

fact["observation_flag"] = raw_value.str.extract(
    r"^\s*-?\d+(?:\.\d+)?\s+([A-Za-z]+)\s*$"
)[0]

# Eurostat periods: S1 starts in January, S2 starts in July.
fact["year"] = fact["period"].str[:4].astype(int)
fact["semester"] = fact["period"].str[-1].astype(int)

fact["date"] = pd.to_datetime(
    {
        "year": fact["year"],
        "month": fact["semester"].map({1: 1, 2: 7}),
        "day": 1,
    }
)


# Keep observations with actual numeric prices.
fact = fact.dropna(subset=["value"]).copy()

# Create the sort key before removing year and semester.
fact["period_sort"] = fact["year"] * 10 + fact["semester"]

# Keep the required output columns, including the sort key.
fact = fact[
    dimension_names
    + ["period", "period_sort", "date", "value", "observation_flag"]
]


fact = fact.sort_values(
    ["geo", "nrg_cons", "tax", "date"]
).reset_index(drop=True)


fact.to_csv(OUTPUT_FILE, index=False)

print("\nTransformation complete.")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(fact):,}")
print(f"Columns: {len(fact.columns)}")
print(f"Countries/geographies: {fact['geo'].nunique()}")
print(f"Periods: {fact['period'].nunique()}")
print(f"Date range: {fact['date'].min()} to {fact['date'].max()}")
print(f"Missing values in value: {fact['value'].isna().sum()}")

print("\nConsumption bands:")
print(fact["nrg_cons"].value_counts().head(10))

print("\nTax categories:")
print(fact["tax"].value_counts())

print("\nSample transformed rows:")
print(fact.head(10).to_string(index=False))
