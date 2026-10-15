
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

FACT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "fact_electricity_prices.csv"
)

COUNTRY_FILE = PROJECT_DIR / "data" / "dim_country.csv"

OUTPUT_FILE = PROJECT_DIR / "data" / "dim_price_country.csv"

prices = pd.read_csv(FACT_FILE, dtype={"geo": str})
existing_countries = pd.read_csv(COUNTRY_FILE, dtype=str)

# Reuse known country names wherever possible.
country_lookup = dict(
    zip(
        existing_countries["Geo_Code"],
        existing_countries["Country_Name"],
    )
)

# Add price-specific geographies not in the generation dimension.
country_lookup.update({
    "EA": "Euro area",
    "LI": "Liechtenstein",
})

geographies = sorted(prices["geo"].dropna().unique())

dim_price_country = pd.DataFrame({
    "Geo_Code": geographies,
    "Country_Name": [
        country_lookup.get(code, code)
        for code in geographies
    ],
})

dim_price_country.to_csv(OUTPUT_FILE, index=False)

print(f"Saved: {OUTPUT_FILE}")
print(f"Rows: {len(dim_price_country)}")
print("\nGeographies:")
print(dim_price_country.to_string(index=False))
