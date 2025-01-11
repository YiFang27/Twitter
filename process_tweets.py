# Processing JSON into DataFrame
import pandas as pd
import json 

tweets_file = "tweets.json"
data = []

# Read JSON lines and convert to DataFrame
with open(tweets_file, "r", encoding="utf-8") as file:
    for line in file:
        data.append(json.loads(line))

df = pd.DataFrame(data)
print(df.head())

# Optional: Save DataFrame as CSV
df.to_csv("tweets.csv", index=False)

#Upload csv to buket
from google.cloud import storage
import pandas as pd

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