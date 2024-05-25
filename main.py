from google.cloud import bigquery
from flask import Flask
from flask import request
import os 

app = Flask(__name__)
client = bigquery.Client()

## this application when invoked by http url, will grab csv, update csv from gcs storage bucket and writes it to a table in bigquery called underscore states.happens everytime you invoke it using endpoint. file must be in gcs first 
# using GCP project ID. current one below is disco-alchemy-423417-u5
@app.route('/')
def main(big_query_client=client):
    # project id. dataset. table
    table_id = "disco-alchemy-423417-u5.test_schema.us_states"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        ### skips the header row of the csv file
        skip_leading_rows=1,
    )
    uri = "gs://sidd-ml-ops/us-states.csv"
    load_job = big_query_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

    load_job.result()  

    destination_table = big_query_client.get_table(table_id)
    return {"data": destination_table.num_rows}
## returns a json response of row numbers, which is 50 for this case of training video

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))