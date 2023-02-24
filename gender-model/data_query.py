from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../gender-model/gender-model-006f0132749e.json"

client = bigquery.Client()

query = f"""
    SELECT name, gender
    FROM `bigquery-public-data.usa_names.usa_1910_current` 
"""

query_job = client.query(query)
results = query_job.result()

i = 0;
for row in results:
    print(row)
    i = i+1;
    if i > 50: 
        break