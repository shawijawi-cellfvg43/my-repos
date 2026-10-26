import streamlit as st
from twikit import Client
from datetime import datetime, timedelta, timezone

# Configurations - Put your 3 exact handles here
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]

# Backend Dummy Account Login Credentials (The script logs in silently)
X_USERNAME = "herberdagoat11"
X_EMAIL = "herbergabe@gmail.com"
X_PASSWORD = "GABEHERBERGFF(12"

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Free monitoring (Last 3 days)")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

@st.cache_resource
def get_twitter_client():
    client = Client('en-US')
    try:
        client.login(auth_info=X_USERNAME, password=X_PASSWORD, email=X_EMAIL)
        return client
    except Exception as e:
        st.error("Failed to authenticate background engine. Check your dummy credentials.")
        return None

client = get_twitter_client()

if client:
    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)

    for handle in HANDLES:
        st.write(f"### @{handle}")
        try:
            # Fetch the user profile and their raw timeline posts
            user = client.get_user_by_screen_name(handle)
            tweets = user.get_tweets('Tweets', count=20)
            
            valid_tweets_found = False
            
            for tweet in tweets:
                # Twikit returns a standard datetime object natively
                tweet_time = tweet.created_at_datetime
                
                if tweet_time >= three_days_ago:
                    valid_tweets_found = True
                    with st.container():
                        # Format timestamp nicely
                        formatted_time = tweet_time.strftime("%b %d, %Y · %I:%M %p UTC")
                        st.markdown(f"**Posted at:** {formatted_time}")
                        st.write(tweet.text)
                        st.markdown("---")
                        
            if not valid_tweets_found:
                st.info(f"No messages posted by @{handle} within the last 3 days.")
                
        except Exception as e:
            st.error(f"Could not load data stream for @{handle}. X rate limit hit, wait a few minutes.")
