
import gzip
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests

url = (
    "https://ec.europa.eu/eurostat/api/"
    "dissemination/sdmx/2.1/data/nrg_pc_204"
    "?format=TSV&compressed=true"
)

project_dir = Path(__file__).resolve().parent.parent
output_dir = project_dir / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "nrg_pc_204_raw.tsv"

print("Downloading Eurostat household electricity prices...")

response = requests.get(url, timeout=120)
response.raise_for_status()

data = gzip.decompress(response.content)

df = pd.read_csv(BytesIO(data), sep="\t")

df.to_csv(output_file, sep="\t", index=False)

print(f"Saved: {output_file}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")
print("\nFirst five rows:")
print(df.head())
