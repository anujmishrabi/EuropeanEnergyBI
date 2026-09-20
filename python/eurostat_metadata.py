import requests
import xml.etree.ElementTree as ET

url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/SIEC/1.0"

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Request failed: {response.status_code}")

root = ET.fromstring(response.content)

namespaces = {
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
}

print("SIEC CODE LIST")
print("=" * 70)

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

    print(f"{code_id:<15} -> {english_name}")