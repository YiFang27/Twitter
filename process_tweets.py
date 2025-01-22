# Processing JSON into DataFrame
import pandas as pd
import json 

tweets_file = "C:/Users/fy199/Twitter/tweets.json"
data = []

# Read JSON lines and convert to DataFrame
with open(tweets_file, "r", encoding="utf-8") as file:
    for line in file:
        data.append(json.loads(line))

df = pd.DataFrame(data)
print(df.head())

# Clean text to handle problematic quotes and newlines
def clean_text(text):
    if isinstance(text, str):
        text = text.replace('"', '""')  # Escape quotes for CSV compatibility
        text = text.replace('\n', ' ')  # Replace newlines with spaces
    return text


# Apply cleaning to the 'text' column
df['text'] = df['text'].apply(clean_text)

# Save the cleaned DataFrame to CSV
df.to_csv("tweets.csv", index=False, quoting=1)  # quoting=1 uses `csv.QUOTE_NONNUMERIC`

# Upload csv to buket
from google.cloud import storage

# Initialize the GCS client
client = storage.Client()

# Define bucket and file details
bucket_name = "my-twitter-data-bucket"  # Replace with your bucket name
source_file_name = "tweets.csv"         # Local file to upload
destination_blob_name = "tweets.csv"    # File name in the bucket

# Get the bucket and blob
bucket = client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

# Upload the file to GCS
blob.upload_from_filename(source_file_name)
print(f"File {source_file_name} uploaded to {bucket_name} as {destination_blob_name}.")



# Load to BigQuery
from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client()

# Define dataset and table
dataset_id = "twitter_data"  # Dataset name
table_id = "tweets"          # Table name
project_id = "elegant-racer-435515-f4"  # Replace with your project ID
uri = "gs://my-twitter-data-bucket/tweets.csv"  # GCS file path

# Configure the load job to append data
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    write_disposition="WRITE_APPEND",
    max_bad_records=10,  # Allow up to 5 bad rows
    ignore_unknown_values=True,  # Ignore extra values not in the schema
)


# Load the data into BigQuery
load_job = client.load_table_from_uri(
    uri,
    f"{client.project}.{dataset_id}.{table_id}",
    job_config=job_config,
)
load_job.result()  # Waiting for finishing the loading
print(f"Appended data to {dataset_id}.{table_id}.")
blob.upload_from_filename("tweets.csv")

