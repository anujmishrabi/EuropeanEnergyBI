import pandas as pd


# ---------------------------------------------------------
# 1. Read fact table
# ---------------------------------------------------------

input_file = "../data/processed/fact_electricity_generation.csv"

fact = pd.read_csv(input_file)

fact["date"] = pd.to_datetime(fact["date"])


# ---------------------------------------------------------
# 2. Determine date range
# ---------------------------------------------------------

min_date = fact["date"].min()
max_date = fact["date"].max()

print("Minimum date:", min_date)
print("Maximum date:", max_date)


# ---------------------------------------------------------
# 3. Create monthly date dimension
# ---------------------------------------------------------

dates = pd.date_range(
    start=min_date,
    end=max_date,
    freq="MS"
)

dim_date = pd.DataFrame({
    "Date": dates
})


# ---------------------------------------------------------
# 4. Add useful calendar attributes
# ---------------------------------------------------------

dim_date["Year"] = dim_date["Date"].dt.year

dim_date["Month_Number"] = dim_date["Date"].dt.month

dim_date["Month_Name"] = dim_date["Date"].dt.strftime("%B")

dim_date["Month_Short"] = dim_date["Date"].dt.strftime("%b")

dim_date["Quarter"] = (
    "Q" + dim_date["Date"].dt.quarter.astype(str)
)

dim_date["Year_Month"] = (
    dim_date["Date"].dt.strftime("%Y-%m")
)


# ---------------------------------------------------------
# 5. Save
# ---------------------------------------------------------

output_file = "../data/dim_date.csv"

dim_date.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print("\nCreated:", output_file)
print("Rows:", len(dim_date))

print("\nFirst 10 rows:")
print(dim_date.head(10).to_string(index=False))