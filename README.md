# Twitter Data Pipeline with Google Cloud Storage & BigQuery
## Overview
This project automates the process of fetching tweets from Twitter using the Twitter API, storing them in Google Cloud Storage (GCS), and loading them into BigQuery for further analysis. The pipeline ensures incremental data fetching, avoiding duplicates while allowing real-time updates.

## Features
Fetches tweets every 20 minutes using Twitter API v2.   

Stores tweet data in tweets.json and converts it to tweets.csv.  

Uploads tweets.csv to Google Cloud Storage.  
     
Loads data into Google BigQuery while avoiding duplicate entries.     

Automatically monitors the script and restarts fetch_tweets.py if it stops running.        

## Project Structure 
### 📂 Twitter
        │── fetch_tweets.py        # Fetches tweets from Twitter API
        │── process_tweets.py      # Converts and uploads data to GCS & BigQuery
        │── monitor.py             # Monitors and ensures scripts keep running
        │── last_tweet_id.txt      # Stores the last fetched tweet ID for incremental fetching
        │── tweets.json            # Raw tweet data in JSON format
        │── tweets.csv             # Processed tweet data in CSV format
        │── .gitignore             # Ignore unnecessary files (e.g., credentials)
        │── requirements.txt       # Python dependencies
        │── README.md              # Project documentation
## Setup Instructions
### 1. Clone the Repository
        git clone https://github.com/YiFang27/Twitter.git
        cd Twitter
### 2. Install Dependencies
#### Ensure you have Python 3.12+ installed. Then install the required libraries:
        pip install -r requirements.txt
### 3. Set Up Twitter API Credentials
Register a Twitter Developer account.   
Obtain **Bearer Token** from Twitter Developer Portal.   
Replace BEARER_TOKEN in fetch_tweets.py with your actual token.    
### 4. Set Up Google Cloud Credentials
Create a Google Cloud project and enable BigQuery & Cloud Storage.    
Download the service account JSON key.    
Set up the environment variable:     
        export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-service-key.json"
On Windows (PowerShell):     
        $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\your-path\your-service-key.json"
### 5. Run the Pipeline
Manually run the script     
To manually fetch and process tweets:     
        python fetch_tweets.py
        python process_tweets.py
Automate with Monitor Script     
To automatically check and restart the fetch script:        
        python monitor.py
This ensures fetch_tweets.py runs continuously, restarting if needed.     

## How It Works
### Fetching Tweets (fetch_tweets.py)
Queries Twitter API v2 for new tweets matching a keyword.     
Uses **since_id** to fetch only new tweets since the last run.     
Saves results to tweets.json.     
### Processing Tweets (process_tweets.py)
Reads tweets.json, removes duplicates, and cleans data.     
Saves the processed data into tweets.csv.    
Uploads tweets.csv to Google Cloud Storage.     
Loads data into a BigQuery table, ensuring incremental updates.     
### Monitoring & Automation (monitor.py)
Runs every 60 minutes to check if fetch_tweets.py is running.     
Restarts the script if it is not running.     
Ensures continuous tweet fetching.     
## Troubleshooting
### Common Errors & Fixes

| **Error**                          | **Cause**                          | **Solution**                                         |
|------------------------------------|------------------------------------|------------------------------------------------------|
| **Rate limit reached**             | Twitter API limit exceeded         | Reduce `max_results` or increase time between requests. |
| **Duplicate tweets in BigQuery**   | `since_id` not updating correctly  | Ensure `last_tweet_id.txt` is updated after each fetch. |
| **tweets.csv not updating**        | Script not running                 | Check logs or manually run `process_tweets.py`. |
| **GOOGLE_APPLICATION_CREDENTIALS not found** | Env variable not set            | Set it using `export` or `$env:` commands. |

## Future Improvements
Integrate with Google Cloud Functions for serverless automation.      
Implement Stream Processing with Pub/Sub for real-time updates.     
Improve data cleaning and enrichment (e.g., sentiment analysis, topic modeling).     
## License
This project is licensed under the MIT License.

## Contributors
Yi Fang – Developer & Data Engineer     
Contributions welcome! Feel free to submit a PR or open an issue.
## 🚀 Happy Coding!
If you found this project useful, give it a ⭐ on GitHub! 😊
