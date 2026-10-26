import streamlit as st
import requests

# Configurations
API_KEY = "YOUR_API_KEY_HERE"  # Put your free TwitterAPI.io key here
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]  # Put the exact usernames here (No @ symbol)

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Updating in real-time")

if st.button("🔄 Force Refresh Now"):
    st.rerun()

for handle in HANDLES:
    st.write(f"### @{handle}")
    url = "https://twitterapi.io"
    headers = {"X-API-Key": API_KEY}
    # Fix 1: TwitterAPI.io requires camelCase parameter "userName"
    params = {"userName": handle}
    
    try:
        response = requests.get(url, headers=headers, params=params).json()
        # Fix 2: The tweets array lives inside the "data" parent key
        tweets = response.get("data", {}).get("tweets", [])[:5]
        
        if not tweets:
            st.info(f"No recent posts found for @{handle} or key limits reached.")
            
        for tweet in tweets:
            with st.container():
                st.markdown(f"**Posted at:** {tweet.get('created_at', 'N/A')}")
                st.write(tweet.get("text", ""))
                st.markdown("---")
    except Exception as e:
        st.error(f"Network error loading data for @{handle}")
