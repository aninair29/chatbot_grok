import streamlit as st
import os
import requests

# Get Grok API key from Streamlit secrets
GROK_API_KEY = os.getenv("GROK_API_KEY")

st.title("💬 Grok Chatbot")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display past messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Grok API call
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-4.20-multi-agent-beta-0309",
        "messages": st.session_state["messages"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Debug: show raw response
        st.write("Raw Grok response:", data)

        # Extract reply from choices
        reply = data["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except requests.exceptions.RequestException as e:
        st.error(f"Grok API error: {e}")
