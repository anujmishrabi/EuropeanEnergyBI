\# European Energy Intelligence Dashboard



An end-to-end data engineering and business intelligence project analysing electricity generation and household electricity prices across European countries using public Eurostat data.



\## Project Overview



This project combines Python-based data extraction and transformation with Power BI dashboards to explore electricity generation trends, renewable energy production, energy-source composition, and household electricity prices.



\## Dashboard Pages



\### 1. Executive Overview

\- Total electricity generation

\- Renewable electricity generation and renewable share

\- Selected fossil-fuel generation categories

\- Annual generation trends

\- Latest electricity generation by energy source



\### 2. Country Explorer

\- Country-level electricity generation analysis

\- Annual generation trends

\- Renewable share over time

\- Renewable versus selected fossil generation



\### 3. Electricity Prices

\- Latest household electricity price

\- Historical electricity price trends

\- Comparison of the ten highest-priced countries

\- Country-level price table

\- Year-over-year price change analysis



\## Data Sources



The project uses public datasets from Eurostat:



\- \*\*Electricity generation:\*\* `nrg\_cb\_pem`

\- \*\*Household electricity prices:\*\* `nrg\_pc\_204`



Data availability and reporting periods vary by country.



\## Technology Stack



\- \*\*Python:\*\* data extraction, transformation, and validation

\- \*\*Pandas:\*\* data reshaping and processing

\- \*\*Power BI:\*\* data modelling, DAX measures, and interactive dashboards

\- \*\*CSV:\*\* processed data and dimension tables

\- \*\*Git and GitHub:\*\* source control and project versioning



\## Data Pipeline



1\. Download public Eurostat datasets.

2\. Transform raw observations into structured fact tables.

3\. Validate records, dimensions, periods, and duplicate observations.

4\. Load processed data and dimension tables into Power BI.

5\. Build interactive dashboards using a dimensional data model.



\## Project Structure



```text

EuropeanEnergyBI/

├── data/

│   ├── raw/

│   ├── processed/

│   ├── dim\_country.csv

│   ├── dim\_date.csv

│   ├── dim\_energy\_source.csv

│   ├── dim\_unit.csv

│   └── dim\_price\_country.csv

├── python/

│   ├── download\_eurostat.py

│   ├── transform\_electricity.py

│   ├── validate\_electricity.py

│   ├── download\_electricity\_prices.py

│   ├── transform\_electricity\_prices.py

│   ├── validate\_electricity\_prices.py

│   ├── inspect\_price\_geographies.py

│   └── create\_price\_country\_dimension.py

├── powerbi/

│   └── EuropeanEnergyBI.pbix

└── README.md

```



\## Analytical Considerations



\- Electricity generation measures are filtered to the relevant reporting unit.

\- The fossil-generation measure currently represents selected fuel categories, not the complete Eurostat fossil-generation aggregate.

\- Electricity prices are compared using a consistent currency, household consumption band, and tax category.

\- Historical price comparisons use semester-level reporting periods where applicable.

\- Latest observations may differ between countries.



\## Running the Python Pipeline



Run commands from the project root.



Download electricity-price data:



```powershell

python python/download\_electricity\_prices.py

```



Transform the downloaded data:



```powershell

python python/transform\_electricity\_prices.py

```



Validate the processed output:



```powershell

python python/validate\_electricity\_prices.py

```



The generation pipeline has corresponding download, transformation, and validation scripts.



\## Future Enhancements



\- Expand energy-market indicators and analytical measures.

\- Improve automated data-quality checks.

\- Explore scalable data processing with Databricks.

\- Add further public energy datasets where useful.



\## Purpose



This project demonstrates practical skills in data engineering, dimensional modelling, Python data processing, DAX, Power BI dashboard development, and source control using publicly available data.



