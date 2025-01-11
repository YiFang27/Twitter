from google.cloud import storage

# Initialize the client
client = storage.Client()

# List buckets in your GCP project
try:
    buckets = list(client.list_buckets())
    print("Buckets in your project:")
    for bucket in buckets:
        print(bucket.name)
except Exception as e:
    print(f"Error: {e}")