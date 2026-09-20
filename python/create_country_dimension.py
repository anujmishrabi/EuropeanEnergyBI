import requests
import xml.etree.ElementTree as ET
import pandas as pd

geo_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/GEO/1.0"
fact_file = "../data/processed/fact_electricity_generation.csv"
output_file = "../data/dim_country.csv"

# --------------------------------------------------
# Read geographies actually used by the fact table
# --------------------------------------------------

fact = pd.read_csv(fact_file)

used_geos = sorted(fact["geo"].dropna().unique())

print("Geographies used in fact table:", len(used_geos))
print(used_geos)

# --------------------------------------------------
# Download Eurostat GEO metadata
# --------------------------------------------------

response = requests.get(geo_url)

if response.status_code != 200:
    raise Exception(f"Download failed: {response.status_code}")

root = ET.fromstring(response.content)

namespaces = {
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
}

records = []

for code in root.findall(".//s:Code", namespaces):

    geo_code = code.attrib.get("id")

    if geo_code not in used_geos:
        continue

    english_name = ""

    for name in code.findall("c:Name", namespaces):

        language = name.attrib.get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

        if language == "en":
            english_name = name.text
            break

    records.append({
        "Geo_Code": geo_code,
        "Country_Name": english_name
    })

# --------------------------------------------------
# Create dimension
# --------------------------------------------------

df = pd.DataFrame(records)

df = df.sort_values("Geo_Code").reset_index(drop=True)

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print("\nCreated:", output_file)
print("Rows:", len(df))

print("\nDimension:")
print(df.to_string(index=False))