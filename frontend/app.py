import requests
import streamlit as st


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Business Idea Assistant",
    page_icon="💡",
    layout="centered"
)


# -----------------------------
# Page Header
# -----------------------------
st.title("💡 Business Idea Assistant")
st.caption(
    "Describe your interests, skills, budget, or problem — "
    "I'll help you explore business ideas."
)


# -----------------------------
# Backend URL
# -----------------------------
BACKEND_URL = "http://127.0.0.1:8000/chat/"


# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat Input
# -----------------------------
user_input = st.chat_input(
    "Describe your business idea or tell me what you're looking for..."
)


if user_input:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)


    # Send message to backend
    try:

        response = requests.post(
        BACKEND_URL,
        json={"messages": st.session_state.messages}
    
    ) 
        response.raise_for_status()

        data = response.json()

        assistant_response = data["message"]


    except requests.exceptions.RequestException as e:

        assistant_response = (
            f"Sorry, I couldn't connect to the backend. "
            f"Error: {e}"
        )


    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )


    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)