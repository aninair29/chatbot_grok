import streamlit as st
import os
import requests

GROK_API_KEY = os.getenv("GROK_API_KEY")

st.title("💬 Grok Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-4.20-beta-0309-reasoning",
        "messages": st.session_state["messages"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        reply = data["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except requests.exceptions.HTTPError as e:
        # Show a friendly message instead of raw JSON
        if response.status_code == 403:
            st.error("⚠️ Service unavailable — please try again later.")
        else:
            st.error(f"Grok API error: {e}")
            # Optional: log raw response for debugging
            st.write("Error response body:", response.text)
    except Exception as e:
        st.error(f"Unexpected error: {e}")
