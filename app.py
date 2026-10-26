import streamlit as st
from ntscraper import Nitter
from datetime import datetime, timedelta

# Configurations - Put your 3 exact handles here (No @ symbol)
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Free monitoring (Last 3 days)")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

# Initialize the free scraper engine
scraper = Nitter(log_level=0)

# Calculate dynamic time cutoff for 3 days ago
three_days_ago = datetime.now() - timedelta(days=3)

for handle in HANDLES:
    st.write(f"### @{handle}")
    
    try:
        # Fetches the latest 20 tweets directly from public instances without an API key
        print(f"Fetching posts for {handle}...")
        data = scraper.get_tweets(handle, mode='user', number=20)
        tweets = data.get('tweets', [])
        
        valid_tweets_found = False
        
        for tweet in tweets:
            # Parse the tweet date string into a Python datetime object
            # Nitter format usually looks like: "Oct 24, 2026 · 5:23 PM UTC"
            try:
                tweet_date_str = tweet.get('date', '')
                # Clean up string formatting for parsing
                clean_date = tweet_date_str.split(' · ')[0]
                tweet_time = datetime.strptime(clean_date, "%b %d, %Y")
            except:
                # Fallback if date string structure changes slightly
                tweet_time = datetime.now() 
            
            # Filter block: Only render if it falls within the 3-day window
            if tweet_time >= three_days_ago:
                valid_tweets_found = True
                with st.container():
                    st.markdown(f"**Posted at:** {tweet.get('date', 'N/A')}")
                    st.write(tweet.get('text', ''))
                    
                    # Basic Link rendering if text contains links
                    if tweet.get('link'):
                        st.markdown(f"[View Original Post]({tweet.get('link')})")
                    st.markdown("---")
                    
        if not valid_tweets_found:
            st.info(f"No messages posted by @{handle} within the last 3 days.")
            
    except Exception as e:
        st.error(f"Could not load data stream for @{handle}. The public scraping node might be busy. Click refresh to retry.")
