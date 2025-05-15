import streamlit as st
import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from agent import root_agent  # Make sure your agent.py defines root_agent

# Constants
APP_NAME = "code_pipeline_app"
USER_ID = "user_123"
SESSION_ID = "session_001"

# Initialize session service
session_service = InMemorySessionService()

# Create session if not already exists
try:
    session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
except Exception:
    pass  # Avoid crashing if session already exists

# Setup runner
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# Streamlit UI
st.title("🛠️ Sequential Code Pipeline Agent")
spec = st.text_area("Enter a code specification:", placeholder="e.g. Write a Python function to check for palindrome")

if st.button("Run Agent Pipeline"):
    if not spec.strip():
        st.warning("Please enter a specification.")
    else:
        async def run_pipeline():
            # Set up the user message
            msg = types.Content(role="user", parts=[types.Part(text=spec)])
            output = ""

            # Run the agent pipeline
            async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=msg):
                if event.is_final_response() and event.content and event.content.parts:
                    output = event.content.parts[0].text
            return output

        # Display spinner while processing
        with st.spinner("Running code generation, review, and refactor..."):
            result = asyncio.run(run_pipeline())
            st.subheader("✅ Refactored Code")
            st.code(result, language="python")
