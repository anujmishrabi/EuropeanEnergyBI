import requests
import pandas as pd
import gzip
from io import BytesIO

url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nrg_cb_pem?format=TSV&compressed=true"

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Download failed: {response.status_code}")

print("Download successful")
print("Compressed size:", len(response.content), "bytes")

# Decompress the gzip response
decompressed_data = gzip.decompress(response.content)

print("Decompressed size:", len(decompressed_data), "bytes")

# Read the TSV data
df = pd.read_csv(
    BytesIO(decompressed_data),
    sep="\t"
)

print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

# Save raw data
output_file = "../data/nrg_cb_pem_raw.tsv"

df.to_csv(
    output_file,
    sep="\t",
    index=False
)

print(f"\nSaved to: {output_file}")