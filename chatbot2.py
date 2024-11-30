import google.generativeai as genai
import streamlit as st

# i am ikram
# Google API key configuration
GOOGLE_API_KEY = 'AIzaSyBMsmccTM5AVuKUPSzGm0wyncHBafQb-uE'
genai.configure(api_key=GOOGLE_API_KEY)

# Model Initiate
model = genai.GenerativeModel("gemini-1.5-flash")

def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text

# Streamlit interface setup
st.set_page_config(page_title="Simple Chatbot", layout="centered")

st.title("⚜ Simple Chatbot ⚜")
st.write("Made by Ikram")

# Initialize chat history in session state if it doesn't exist
if "history" not in st.session_state:
    st.session_state["history"] = [] 

# User input form
with st.form(key="Chat Form", clear_on_submit=True):
    user_input = st.text_input("Enter your message:", max_chars=2000)
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input:
            response = get_chatbot_response(user_input)
            # Append the new user input and bot response to chat history
            st.session_state.history.append((user_input, response))
            # Set a flag to refresh the chat display
            st.session_state.refresh = True
        else:
            st.warning("Please enter a prompt")

# Display chat history
for user_message, bot_message in st.session_state.history:
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

    # Check if the response contains code and format it correctly
    if "```" in bot_message:  # Check if the response contains code
        # Split the code from the rest of the response and display it properly
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
                    <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #ffffff;"><b>Bot:</b> {block}</p> <!-- Updated to white -->
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
            <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #ffffff;"><b>Bot:</b> {bot_message}</p> <!-- Updated to white -->
        </div>
        """, unsafe_allow_html=True)

# Refresh the display if the flag is set
if 'refresh' in st.session_state:
    del st.session_state['refresh']  # Clear the flag to prevent endless refresh