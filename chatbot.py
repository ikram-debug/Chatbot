import google.generativeai as genai
import streamlit as st

# Google API key configuration
GOOGLE_API_KEY = 'AIzaSyBMsmccTM5AVuKUPSzGm0wyncHBafQb-uE'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text

# Streamlit interface setup
st.set_page_config(page_title="⚜ Simple Chatbot ⚜", layout="centered")

# Custom CSS to fix the input form at the bottom
st.markdown("""
    <style>
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        padding: 10px 20px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }
    .chat-container {
        margin-bottom: 80px; /* To prevent overlap with the fixed input form */
        max-height: 80vh;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚜ Simple Chatbot ⚜")
st.write("Made by Ikram")

# Initialize chat history in session state if it doesn't exist
if "history" not in st.session_state:
    st.session_state["history"] = []

# Create a container for chat history
chat_container = st.container()

with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    # Reverse the chat history so that the latest input appears at the top
    reversed_history = st.session_state.history[::-1]
    
    for user_message, bot_message in reversed_history:
        # User message
        st.markdown(f"""
        <div style="
              background-color: #d1d3e0;
              border-radius: 15px;
              padding: 10px 15px;
              margin: 5px 0;
              max-width: 70%;
              text-align: left;
              display: inline-block;">
            <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #000000;"><b>You:</b> {user_message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bot response
        if "```" in bot_message:  # Check if the response contains code
            code_blocks = bot_message.split("```")
            for i, block in enumerate(code_blocks):
                if i % 2 == 0:  # Text outside code block
                    st.markdown(f"""
                    <div style="
                          background-color: #000000;
                          border-radius: 15px;
                          padding: 10px 15px;
                          margin: 5px 0;
                          max-width: 70%;
                          text-align: left;
                          display: inline-block;">
                        <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #ffffff;"><b>Bot:</b> {block}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # Code block
                    st.code(block.strip(), language="cpp")  # Adjust language as needed
        else:
            st.markdown(f"""
            <div style="
                  background-color: #000000;
                  border-radius: 15px;
                  padding: 10px 15px;
                  margin: 5px 0;
                  max-width: 70%;
                  text-align: left;
                  display: inline-block;">
                <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #ffffff;"><b>Bot:</b> {bot_message}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Fixed input form at the bottom
st.markdown("<div class='fixed-bottom'>", unsafe_allow_html=True)
with st.form(key="Chat Form", clear_on_submit=True):
    user_input = st.text_input("Enter your message:", max_chars=2000, key="input")
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input:
            response = get_chatbot_response(user_input)
            # Append the new user input and bot response to chat history
            st.session_state.history.append((user_input, response))
            # Optionally, you can scroll to the top of the chat history
            # using JavaScript, but Streamlit doesn't support it directly
        else:
            st.warning("Please enter a prompt")
st.markdown("</div>", unsafe_allow_html=True)
