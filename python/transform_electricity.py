import pandas as pd


# ---------------------------------------------------------
# 1. File locations
# ---------------------------------------------------------

input_file = "../data/raw/nrg_cb_pem_raw.tsv"
output_file = "../data/processed/fact_electricity_generation.csv"


# ---------------------------------------------------------
# 2. Read raw Eurostat data
# ---------------------------------------------------------

print("Reading raw Eurostat data...")

df = pd.read_csv(
    input_file,
    sep="\t"
)

print("Raw shape:", df.shape)


# ---------------------------------------------------------
# 3. Split the first column
# ---------------------------------------------------------

first_column = df.columns[0]

dimensions = df[first_column].str.split(",", expand=True)

dimensions.columns = [
    "freq",
    "siec",
    "unit",
    "geo"
]

df = pd.concat(
    [
        dimensions,
        df.iloc[:, 1:]
    ],
    axis=1
)


# ---------------------------------------------------------
# 4. Unpivot the monthly columns
# ---------------------------------------------------------

print("Unpivoting monthly observations...")

fact = df.melt(
    id_vars=[
        "freq",
        "siec",
        "unit",
        "geo"
    ],
    var_name="date",
    value_name="value"
)


# ---------------------------------------------------------
# 5. Clean date
# ---------------------------------------------------------

fact["date"] = fact["date"].str.strip()

fact["date"] = pd.to_datetime(
    fact["date"],
    format="%Y-%m",
    errors="coerce"
)


# ---------------------------------------------------------
# 6. Convert Eurostat missing values
# ---------------------------------------------------------

fact["value"] = fact["value"].replace(
    [":", ": ", ""],
    pd.NA
)


# ---------------------------------------------------------
# 7. Convert values to numeric
# ---------------------------------------------------------

fact["value"] = pd.to_numeric(
    fact["value"],
    errors="coerce"
)


# ---------------------------------------------------------
# 8. Remove completely empty observations
# ---------------------------------------------------------

before = len(fact)

fact = fact.dropna(
    subset=["value"]
)

after = len(fact)

print("Rows before removing missing values:", before)
print("Rows after removing missing values:", after)


# ---------------------------------------------------------
# 9. Sort
# ---------------------------------------------------------

fact = fact.sort_values(
    [
        "geo",
        "siec",
        "unit",
        "date"
    ]
)


# ---------------------------------------------------------
# 10. Save
# ---------------------------------------------------------

fact.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)


# ---------------------------------------------------------
# 11. Summary
# ---------------------------------------------------------

print("\nTransformation complete!")

print("Final shape:", fact.shape)

print("\nColumns:")
print(fact.columns.tolist())

print("\nSample:")
print(
    fact.head(10).to_string(index=False)
)

print(f"\nSaved to: {output_file}")