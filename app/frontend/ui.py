import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# Initialize logger
logger = get_logger(__name__)
logger.info("Logger initialized")

# Streamlit page setup
logger.info("Setting Streamlit page configuration")
st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent using Groq and Tavily New")
logger.info("Streamlit UI initialized")

# Collect user inputs
logger.info("Rendering system prompt text area")
system_prompt = st.text_area("Define your AI Agent:", height=70)
logger.info(f"System prompt input: {system_prompt}")

logger.info("Rendering model selection dropdown")
selected_model = st.selectbox("Select your AI model:", settings.ALLOWED_MODEL_NAMES)
logger.info(f"Selected model: {selected_model}")

logger.info("Rendering checkbox for web search")
allow_web_search = st.checkbox("Allow web search")
logger.info(f"Allow web search: {allow_web_search}")

logger.info("Rendering user query text area")
user_query = st.text_area("Enter your query:", height=150)
logger.info(f"User query input: {user_query}")

# API URL setup
API_URL = "http://127.0.0.1:9999/chat"
logger.info(f"API URL set to {API_URL}")

# Action button and API call
if st.button("Ask Agent") and user_query.strip():
    logger.info("Ask Agent button clicked and user query is not empty")

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    logger.info(f"Prepared payload: {payload}")

    try:
        logger.info("Sending POST request to backend")
        response = requests.post(API_URL, json=payload)
        logger.info(f"Received response with status code: {response.status_code}")

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")
            logger.debug(f"Agent response: {agent_response}")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
            logger.info("Displayed agent response to user")

        else:
            logger.error(f"Backend returned error with status code: {response.status_code}")
            st.error("Error with backend")

    except Exception as e:
        logger.exception("Exception occurred while sending request to backend")
        st.error(str(CustomException("Failed to communicate to backend")))
else:
    if not user_query.strip():
        logger.info("Ask Agent button clicked but user query is empty")
    else:
        logger.info("Ask Agent button not clicked")
