import pandas as pd

input_file = "../data/processed/fact_electricity_generation.csv"

fact = pd.read_csv(input_file)

units = fact[["unit"]].drop_duplicates().sort_values("unit")

unit_mapping = {
    "GWH": "Gigawatt-hours",
    "PC": "Percentage"
}

units["Unit_Description"] = units["unit"].map(unit_mapping)

output_file = "../data/dim_unit.csv"

units.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print("Created:", output_file)
print("\nUnit dimension:")
print(units.to_string(index=False))