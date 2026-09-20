import requests
import xml.etree.ElementTree as ET
import pandas as pd

url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/SIEC/1.0"

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Request failed: {response.status_code}")

root = ET.fromstring(response.content)

namespaces = {
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
}

records = []

for code in root.findall(".//s:Code", namespaces):

    code_id = code.attrib.get("id")
    english_name = ""

    for name in code.findall("c:Name", namespaces):
        language = name.attrib.get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

        if language == "en":
            english_name = name.text
            break

    records.append({
        "SIEC_Code": code_id,
        "SIEC_Description": english_name
    })

df = pd.DataFrame(records)

output_file = "../data/dim_energy_source.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print("Created:", output_file)
print("Rows:", len(df))
print("\nFirst 20 rows:")
print(df.head(20).to_string(index=False))