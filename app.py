import streamlit as st
from twikit import Client
from datetime import datetime, timedelta, timezone
import asyncio

# Configurations - Put your 3 exact handles here
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]

# Put your raw copied cookie string hashes here
AUTH_TOKEN = "ca9006ce457aca27df6ed7a39430510804ece86d"
CT0 = "7d90a0ba62e49984b64248b1a4daeef3ef91aa819b67085ae552ac0a0d8aa82533a745ac26062987a3a24552a324c726aff239226828169ddb5a22716d2c72a7e45d99e744c8b5e1d6fc8a8f3eaf3bec"

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Free monitoring (Last 3 days)")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

async def fetch_twitter_data():
    client = Client('en-US')
    
    # Manually configure the active session using your browser cookies
    client.set_cookies({
        'auth_token': AUTH_TOKEN,
        'ct0': CT0
    })

    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)

    # Automatically split the browser screen width into 3 even columns side-by-side
    cols = st.columns(len(HANDLES))

    for i, handle in enumerate(HANDLES):
        # Direct the content generation stream into its specific horizontal layout column node
        with cols[i]:
            st.markdown(f"### [@{handle}](https://x.com{handle})")
            st.markdown("---")
            
            try:
                user = await client.get_user_by_screen_name(handle)
                tweets = await user.get_tweets('Tweets', count=20)
                
                valid_tweets_found = False
                
                for tweet in tweets:
                    tweet_time = tweet.created_at_datetime
                    
                    if tweet_time >= three_days_ago:
                        valid_tweets_found = True
                        with st.container(border=True): # Wraps each message post block cleanly
                            formatted_time = tweet_time.strftime("%b %d, %Y · %I:%M %p UTC")
                            st.caption(f"📅 {formatted_time}")
                            st.write(tweet.text)
                            
                if not valid_tweets_found:
                    st.info(f"No messages posted by @{handle} within the last 3 days.")
                    
            except Exception as api_error:
                st.error(f"Could not load data stream for @{handle}. Error Details: {api_error}")

# Run loop wrapper inside Streamlit's instance container
try:
    asyncio.run(fetch_twitter_data())
except Exception as loop_error:
    st.error(f"System initialization error: {loop_error}")
