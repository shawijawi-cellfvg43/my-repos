import streamlit as st
import requests
from datetime import datetime, timedelta

# Configurations
API_KEY = "new1_401f3b69d503441389ca3a18ffe95440"  # Put your free TwitterAPI.io key here
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]  # Usernames synced from your dashboard

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Showing updates from the last 3 days")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

# Dynamically calculate the date threshold for 3 days ago (Format: YYYY-MM-DD)
three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

for handle in HANDLES:
    st.write(f"### @{handle}")
    
    # Using Advanced Search to target specific handles and dates without timeline caching errors
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {"X-API-Key": API_KEY}
    
    # Constructing search query payload to force history lookback
    params = {
        "query": f"from:{handle} since:{three_days_ago}",
        "queryType": "Latest"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Advanced search payloads store tweet arrays inside the 'tweets' root or 'data' block
            tweets = data.get("tweets", data.get("data", {}).get("tweets", []))
            
            if not tweets:
                st.info(f"No messages posted by @{handle} since {three_days_ago}.")
                
            for tweet in tweets:
                with st.container():
                    st.markdown(f"**Posted at:** {tweet.get('created_at', 'N/A')}")
                    st.write(tweet.get("text", ""))
                    st.markdown("---")
        else:
            st.error(f"API Error ({response.status_code}): Check your free credit balance at TwitterAPI.io.")
            
    except requests.exceptions.RequestException:
        st.error(f"Could not connect to service stream for @{handle}. Retrying...")
