import tweepy
import json

# Replace these with your Twitter API v2 credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANFFyAEAAAAAsCsyPAU699zyQozf8So0Rr1xtGE%3DAmnsJ60AD43mzlSMesvgGg5cwVJZM6KWdJPAUgZTre5oFmzgOk"

# Initialize the client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Search for recent tweets
query = "Trump"

# Save fetched tweets
with open("tweets.json", "w", encoding="utf-8") as file:
    try:
        # Fetch tweets
        tweets = client.search_recent_tweets(
            query=query,
            max_results=10,  # Fetch up to 10 tweets
            tweet_fields=["created_at", "text", "author_id"]
        )
        
        # Check if tweets are found
        if tweets.data:
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
            print("Tweets saved to tweets.json")
        else:
            print("No tweets found.")
    except tweepy.errors.TooManyRequests:
        print("Rate limit reached. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {e}")