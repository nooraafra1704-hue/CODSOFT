import streamlit as st
from chatbot import get_chatbot_response

# 1. Page Configuration for a premium look
st.set_page_config(
    page_title="Aegis - Rule-Based Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for rich aesthetics (fonts, gradients, margins)
st.markdown("""
<style>
    /* Google Font Imports */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;800&display=swap');

    /* Global Body Fonts */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Main Title Styling with Linear Gradient */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #00C6FF, #0072FF, #9b5DE5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0px;
        padding-bottom: 0px;
        letter-spacing: -0.5px;
    }
    
    /* Subtitle Styling */
    .sub-title {
        text-align: center;
        font-family: 'Inter', sans-serif;
        color: #888888;
        font-size: 1.15rem;
        margin-top: 8px;
        margin-bottom: 35px;
        font-weight: 400;
        line-height: 1.5;
    }

    /* Interactive elements styling */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.2);
    }
    
    /* Sidebar header styling */
    .sidebar-header {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #0072FF;
        font-size: 1.6rem;
        text-align: center;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Session State Variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 I'm **Aegis**, your friendly rule-based chatbot. I can talk about Python 🐍, Artificial Intelligence 🤖, the CodSoft Internship 💼, or tell you the current date/time 📅. How can I help you today? 😊"
        }
    ]

if "chat_active" not in st.session_state:
    st.session_state.chat_active = True

# Helper function to clear and restart chat
def reset_chat_session():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 I'm **Aegis**, your friendly rule-based chatbot. I can talk about Python 🐍, Artificial Intelligence 🤖, the CodSoft Internship 💼, or tell you the current date/time 📅. How can I help you today? 😊"
        }
    ]
    st.session_state.chat_active = True

# 4. Sidebar Content (Project Specs & controls)
with st.sidebar:
    st.markdown("<div class='sidebar-header'>🤖 Aegis Control Panel</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    ### ⚙️ How It Works
    This chatbot is built completely using **Python** & **Streamlit** for **Task 1** of the **CodSoft Artificial Intelligence Internship**.
    
    It relies entirely on:
    1. **Predefined Rules & Dictionaries**
    2. **Regular Expression Pattern Matching**
    
    *No LLMs or Machine Learning models are used.* 🚫🧠
    """)
    st.markdown("---")
    
    # Clear Chat Button in Sidebar
    if st.button("🧹 Clear Chat History", use_container_width=True):
        reset_chat_session()
        st.rerun()
        
    st.markdown("---")
    st.markdown("""
    ### 💡 Example Commands
    Try asking:
    - *What is Python?*
    - *Tell me about Artificial Intelligence.*
    - *What is CodSoft?*
    - *Who created you?*
    - *What is the time?*
    - *Help*
    - *Bye / Quit / Exit*
    """)
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.85rem;'>CodSoft AI Internship - Task 1</div>", unsafe_allow_html=True)

# 5. Main UI Headers
st.markdown("<h1 class='main-title'>🤖 Aegis Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>A modern, responsive, and friendly rule-based chatbot application</p>", unsafe_allow_html=True)

# 6. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Chat Input and Response Processing
if st.session_state.chat_active:
    # Display the chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Render User Message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Append User Message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate chatbot response and check if exit intent was triggered
        response, is_exit = get_chatbot_response(user_input)
        
        # Render Assistant Response
        with st.chat_message("assistant"):
            st.markdown(response)
            
        # Append Assistant Response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # If exit intent is triggered, disable further interaction
        if is_exit:
            st.session_state.chat_active = False
            st.rerun()

else:
    # When the chat is inactive (after goodbye/exit)
    st.warning("🔒 **The conversation has ended.** You can restart the chat to talk to Aegis again!")
    if st.button("🔄 Restart Chat", type="primary", use_container_width=True):
        reset_chat_session()
        st.rerun()
