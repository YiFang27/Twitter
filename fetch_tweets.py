import tweepy
import json
import os
import time


# Replace these with your Twitter API v2 credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANFFyAEAAAAAsCsyPAU699zyQozf8So0Rr1xtGE%3DAmnsJ60AD43mzlSMesvgGg5cwVJZM6KWdJPAUgZTre5oFmzgOk"

# Initialize the client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Search for recent tweets
query = "H1B"

# File to store the last fetched tweet ID
last_id_file = "last_tweet_id.txt"

def fetch_tweets():
    # Load the last tweet ID if it exists
    last_tweet_id = None
    if os.path.exists(last_id_file):
        with open(last_id_file, "r") as f:
            last_tweet_id = f.read().strip()

    # Fetch tweets
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=10,  # Fetch up to 10 tweets
            tweet_fields=["created_at", "text", "author_id"],
            expansions=["author_id"],
            since_id=last_tweet_id, # Fetch only tweets after the last fetched tweet
        )

        # Check if tweets are found
        if tweets.data:
            # Append new tweets to the existing JSON file
            with open("tweets.json", "a", encoding="utf-8") as file:
                for tweet in tweets.data:
                    # Prepare tweet data
                    tweet_data = {
                        "created_at": str(tweet.created_at),
                        "id": tweet.id,
                        "text": tweet.text,
                        "author_id": tweet.author_id,
                    }
                    # Save each tweet as a JSON object
                    json.dump(tweet_data, file)
                    file.write("\n")

            # Save the ID of the newest tweet
            last_tweet_id = tweets.data[0].id
            with open(last_id_file, "w") as f:
                f.write(str(last_tweet_id))

            print(f"Fetched and saved {len(tweets.data)} new tweets.")
        else:
            print("No new tweets found.")
    except tweepy.errors.TooManyRequests:
        print("Rate limit reached. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Refresh every 60 mins
while True:
    print("Fetching new tweets...")
    fetch_tweets()  # Run the fetch_tweets function directly

    # Optionally process tweets here
    os.system("python process_tweets.py")

    # Sleep for 60 minutes
    print("Waiting for 60 minutes...")
    time.sleep(60 * 60)


