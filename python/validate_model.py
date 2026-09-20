import pandas as pd

fact_file = "../data/processed/fact_electricity_generation.csv"
country_file = "../data/dim_country.csv"
energy_file = "../data/dim_energy_source.csv"
date_file = "../data/dim_date.csv"
unit_file = "../data/dim_unit.csv"

fact = pd.read_csv(fact_file)
country = pd.read_csv(country_file)
energy = pd.read_csv(energy_file)
date = pd.read_csv(date_file)
unit = pd.read_csv(unit_file)

print("=" * 60)
print("EUROPEAN ENERGY BI - MODEL VALIDATION")
print("=" * 60)

# --------------------------------------------------
# FACT TABLE
# --------------------------------------------------

print("\nFACT TABLE")
print("-" * 40)

print("Rows:", len(fact))
print("Columns:", fact.columns.tolist())
print("Duplicate rows:", fact.duplicated().sum())

print("\nMissing values:")
print(fact.isna().sum())

print("\nDate range:")
print("Minimum:", fact["date"].min())
print("Maximum:", fact["date"].max())

print("\nUnits:")
print(fact["unit"].value_counts().to_string())

# --------------------------------------------------
# DIMENSIONS
# --------------------------------------------------

print("\nDIMENSIONS")
print("-" * 40)

print("DimCountry:", len(country), "rows")
print("DimEnergySource:", len(energy), "rows")
print("DimDate:", len(date), "rows")
print("DimUnit:", len(unit), "rows")

print("\nDimCountry columns:")
print(country.columns.tolist())

print("\nDimEnergySource columns:")
print(energy.columns.tolist())

print("\nDimDate columns:")
print(date.columns.tolist())

print("\nDimUnit columns:")
print(unit.columns.tolist())

# --------------------------------------------------
# KEY COVERAGE
# --------------------------------------------------

print("\nKEY COVERAGE")
print("-" * 40)

# Country / geography
fact_countries = set(fact["geo"].dropna().unique())

country_code_column = "Geo_Code"

dim_countries = set(
    country[country_code_column].dropna().unique()
)

missing_countries = fact_countries - dim_countries

print("Geographies in fact:", len(fact_countries))
print("Missing from DimCountry:", missing_countries)

# Energy source
fact_siec = set(fact["siec"].dropna().unique())

dim_siec = set(
    energy["SIEC_Code"].dropna().unique()
)

missing_siec = fact_siec - dim_siec

print("SIEC codes in fact:", len(fact_siec))
print("Missing from DimEnergySource:", missing_siec)

# Units
fact_units = set(fact["unit"].dropna().unique())

dim_units = set(
    unit["unit"].dropna().unique()
)

missing_units = fact_units - dim_units

print("Units in fact:", fact_units)
print("Missing from DimUnit:", missing_units)

# --------------------------------------------------
# DATE COVERAGE
# --------------------------------------------------

fact_dates = pd.to_datetime(fact["date"])
dim_dates = pd.to_datetime(date["Date"])

missing_dates = set(
    fact_dates.unique()
) - set(
    dim_dates.unique()
)

print("\nDate values in fact:", len(fact_dates.unique()))
print("Dates in DimDate:", len(dim_dates.unique()))
print("Missing dates from DimDate:", len(missing_dates))

# --------------------------------------------------
# FINAL VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)

if (
    fact.duplicated().sum() == 0
    and fact.isna().sum().sum() == 0
    and len(missing_countries) == 0
    and len(missing_siec) == 0
    and len(missing_units) == 0
    and len(missing_dates) == 0
):
    print("STATUS: PASS")
else:
    print("STATUS: CHECK REQUIRED")