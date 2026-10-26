import streamlit as st
from twikit import Client
from datetime import datetime, timedelta, timezone
import asyncio

# Configurations - Put your 3 exact handles here
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]

# Backend Dummy Account Login Credentials
X_USERNAME = "herberdagoat11"
X_EMAIL = "herbergabe@gmail.com"
X_PASSWORD = "GABEHERBERGFF(12"

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Free monitoring (Last 3 days)")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

async def fetch_twitter_data():
    client = Client('en-US')
    
    # Authenticate through async handler using exact keyword arguments
    try:
        await client.login(
            auth_info_1=X_USERNAME,
            auth_info_2=X_EMAIL,
            password=X_PASSWORD
        )
    except Exception as login_error:
        st.error(f"Authentication Failure: {login_error}")
        return

    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)

    for handle in HANDLES:
        st.write(f"### @{handle}")
        try:
            user = await client.get_user_by_screen_name(handle)
            tweets = await user.get_tweets('Tweets', count=20)
            
            valid_tweets_found = False
            
            for tweet in tweets:
                tweet_time = tweet.created_at_datetime
                
                if tweet_time >= three_days_ago:
                    valid_tweets_found = True
                    with st.container():
                        formatted_time = tweet_time.strftime("%b %d, %Y · %I:%M %p UTC")
                        st.markdown(f"**Posted at:** {formatted_time}")
                        st.write(tweet.text)
                        st.markdown("---")
                        
            if not valid_tweets_found:
                st.info(f"No messages posted by @{handle} within the last 3 days.")
                
        except Exception as api_error:
            st.error(f"Could not load data stream for @{handle}. Error: {api_error}")

# Execute the asynchronous pipeline safely within the synchronous framework
try:
    asyncio.run(fetch_twitter_data())
except Exception as loop_error:
    st.error(f"System initialization error: {loop_error}")
