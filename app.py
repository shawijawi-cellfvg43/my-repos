import streamlit as st
import requests
import time

# Configurations
API_KEY = "YOUR_API_KEY_HERE"  # Put your free TwitterAPI.io key here
HANDLES = ["MenchOsint", "A7_Mirza", "Suriyakmaps"]  # Put the 3 exact usernames here

st.set_page_config(page_title="Live Feed Dashboard", layout="wide")
st.title("🔴 Live Account Streams")
st.subheader("Updating in real-time")

# Add a forced manual/auto refresh mechanism for your friend
if st.button("🔄 Force Refresh Now"):
    st.rerun()

for handle in HANDLES:
    st.write(f"### @{handle}")
    url = f"https://twitterapi.io{handle}"
    headers = {"X-API-Key": API_KEY}
    
    try:
        response = requests.get(url, headers=headers).json()
        tweets = response.get("tweets", [])[:5] # Grabs the 5 most recent posts
        
        if not tweets:
            st.info("No recent posts found or account is private.")
            
        for tweet in tweets:
            with st.container():
                st.markdown(f"**Posted at:** {tweet.get('created_at', 'N/A')}")
                st.write(tweet.get("text", ""))
                st.markdown("---")
    except Exception as e:
        st.error(f"Could not load data for @{handle}")
