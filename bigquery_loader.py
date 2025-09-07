import pandas as pd 
import json
from google.cloud import bigquery
from datetime import datetime as dt

with open("parameters.json", "r") as f:
    params = json.load(f)

cred = params["bigquery-credentials"]
client = bigquery.Client.from_service_account_json(cred)
tableid = "ifood-scraping.ifood_dataset.tb_orders"

df = pd.read_csv("marketorders.csv")
df['Dt_Leitura'] = dt.now()
print(df)

job_config = bigquery.LoadJobConfig(
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    write_disposition="WRITE_APPEND",
    #"WRITE_TRUNCATE",  #delete all data and load again
    autodetect=True     #autodetect column types
)

job = client.load_table_from_dataframe(df, tableid, job_config=job_config)
job.result()

