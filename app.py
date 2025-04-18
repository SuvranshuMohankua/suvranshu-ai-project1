import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Set up the Streamlit page - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Science Tutor Chatbot",
    page_icon="🔬",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file. Please add your API key to the .env file.")
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"❌ Error configuring Gemini API: {str(e)}")
    st.stop()

# Set up the model
try:
    model = genai.GenerativeModel('gemini-1.5-pro')
    # Test the model with a simple prompt
    test_response = model.generate_content("Hello")
    st.success("✅ Successfully connected to Gemini API!")
except Exception as e:
    st.error(f"❌ Error initializing Gemini model: {str(e)}")
    st.info("Note: Make sure you have access to the Gemini 1.5 Pro model. If not, try using 'gemini-pro' instead.")
    st.stop()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e6f3ff;
    }
    .assistant-message {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔬 Science Tutor Chatbot")
st.markdown("""
    Welcome to your personal Science Tutor! I can help you understand various scientific concepts,
    solve problems, and answer your questions about physics, chemistry, biology, and more.
    Feel free to ask any science-related questions!
""")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your science question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                response_text = response.text
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                st.info("If you're seeing this error, it might be because:")
                st.markdown("""
                - The API key is invalid or has expired
                - You don't have access to the Gemini 1.5 Pro model
                - There's an issue with the API service
                - The prompt might be too long or contain inappropriate content
                """)

# Sidebar with instructions
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. Type your science-related question in the chat input
    2. Wait for the AI tutor to respond
    3. Ask follow-up questions to dive deeper into topics
    4. The chat history is maintained during your session
    """)
    
    st.header("About")
    st.markdown("""
    This Science Tutor Chatbot is powered by Google's Gemini 1.5 Pro model.
    It can help you with:
    - Physics concepts and problems
    - Chemistry equations and reactions
    - Biology topics and processes
    - Scientific explanations
    - Problem-solving strategies
    """)
    
    st.header("Debug Info")
    st.code(f"API Key Status: {'✅ Present' if GOOGLE_API_KEY else '❌ Missing'}")
    st.code(f"Model: gemini-1.5-pro") 