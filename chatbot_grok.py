import streamlit as st
import os
import requests

# Get Grok API key from Streamlit secrets
GROK_API_KEY = os.getenv("GROK_API_KEY")

st.title("💬 Grok Chatbot")

# Keep chat history locally
if "history" not in st.session_state:
    st.session_state["history"] = []

# Display past messages
for role, content in st.session_state["history"]:
    st.chat_message(role).write(content)

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state["history"].append(("user", prompt))
    st.chat_message("user").write(prompt)

    # Grok API call
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-4.20-multi-agent-beta-0309",  # Actual Grok model name
        "input": prompt  # Grok expects 'input', not 'messages'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract reply (structure may vary slightly, check Grok docs)
        reply = data["output"][0]["content"]  # Grok returns 'output'
        st.session_state["history"].append(("assistant", reply))
        st.chat_message("assistant").write(reply)

    except requests.exceptions.RequestException as e:
        st.error(f"Grok API error: {e}")
