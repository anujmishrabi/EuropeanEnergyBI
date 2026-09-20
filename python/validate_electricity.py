import pandas as pd

input_file = "../data/processed/fact_electricity_generation.csv"

df = pd.read_csv(input_file)

print("========== BASIC INFORMATION ==========")

print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print("\n========== DATE RANGE ==========")

print("Minimum date:", df["date"].min())
print("Maximum date:", df["date"].max())

print("\n========== COUNTRIES ==========")

print("Number of countries:", df["geo"].nunique())
print(df["geo"].unique())

print("\n========== SIEC CODES ==========")

print("Number of SIEC codes:", df["siec"].nunique())
print(df["siec"].value_counts().sort_index())

print("\n========== UNITS ==========")

print(df["unit"].value_counts())

print("\n========== DUPLICATES ==========")

duplicates = df.duplicated(
    subset=[
        "freq",
        "siec",
        "unit",
        "geo",
        "date"
    ]
).sum()

print("Duplicate observations:", duplicates)

print("\n========== MISSING VALUES ==========")

print(df.isna().sum())

print("\n========== DATA TYPES ==========")

print(df.dtypes)