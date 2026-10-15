
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent

prices_file = (
    project_dir
    / "data"
    / "processed"
    / "fact_electricity_prices.csv"
)

countries_file = project_dir / "data" / "dim_country.csv"

prices = pd.read_csv(prices_file, dtype={"geo": str})
countries = pd.read_csv(countries_file, dtype=str)

price_geos = set(prices["geo"].dropna().unique())
known_geos = set(countries["Geo_Code"].dropna().unique())

print("Geographies in electricity prices:", len(price_geos))
print("Geographies in existing country dimension:", len(known_geos))

print("\nPrice geographies missing from dim_country:")
print(sorted(price_geos - known_geos))

print("\nExisting geographies absent from price data:")
print(sorted(known_geos - price_geos))
