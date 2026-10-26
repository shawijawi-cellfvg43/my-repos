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
st.subheader("Free monitoring (Last 3 days with Media)")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

async def fetch_twitter_data():
    client = Client('en-US')
    
    # Configure the active session using browser cookies
    client.set_cookies({
        'auth_token': AUTH_TOKEN,
        'ct0': CT0
    })

    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)

    # Split the browser screen width into 3 even columns side-by-side
    cols = st.columns(len(HANDLES))

    for i, handle in enumerate(HANDLES):
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
                        with st.container(border=True):
                            formatted_time = tweet_time.strftime("%b %d, %Y · %I:%M %p UTC")
                            st.caption(f"📅 {formatted_time}")
                            
                            # Use full_text to capture uncut posts
                            display_text = getattr(tweet, 'full_text', tweet.text)
                            
                            # Clean out internal short-links that point to attached media
                            if "https://t.co" in display_text:
                                words = display_text.split()
                                cleaned_words = [w for w in words if not w.startswith("https://t.co")]
                                display_text = " ".join(cleaned_words)
                                
                            st.write(display_text)
                            
                            # FIX: Access Twikit media object attributes directly using dot notation
                            if hasattr(tweet, 'media') and tweet.media:
                                for media_item in tweet.media:
                                    # Target attributes directly to fix the '.get()' argument breakdown
                                    media_type = getattr(media_item, 'type', None)
                                    image_url = getattr(media_item, 'media_url_https', None)
                                    
                                    if media_type == 'photo' and image_url:
                                        st.image(image_url, use_container_width=True)
                            
                if not valid_tweets_found:
                    st.info(f"No messages posted by @{handle} within the last 3 days.")
                    
            except Exception as api_error:
                st.error(f"Could not load data stream for @{handle}. Error Details: {api_error}")

# Run loop wrapper inside Streamlit's instance container
try:
    asyncio.run(fetch_twitter_data())
except Exception as loop_error:
    st.error(f"System initialization error: {loop_error}")
