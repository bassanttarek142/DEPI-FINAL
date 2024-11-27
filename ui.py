import streamlit as st
import requests

# Base URL of your FastAPI app (assumes it's running locally)
FASTAPI_URL = "http://127.0.0.1:8000"

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to display the chat messages
def display_chat():
    for chat in st.session_state.chat_history:
        if chat['sender'] == 'user':
            st.write(f"**You**: {chat['message']}")
        else:
            st.write(f"**Assistant**: {chat['message']}")

# Upload PDF
st.title("Upload PDF and Chat with It")

# Step 1: Upload PDF
st.header("Step 1: Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # If the file is uploaded, show a button to process it
    if st.button("Upload and Process PDF"):
        files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
        
        # Send the PDF file to FastAPI upload endpoint
        upload_response = requests.post(f"{FASTAPI_URL}/upload_pdf/", files=files)

        if upload_response.status_code == 200:
            st.success("PDF uploaded and processed successfully!")
        else:
            st.error(f"Failed to upload PDF: {upload_response.content.decode()}")

# Step 2: Chat with the uploaded PDF
st.header("Step 2: Chat with the PDF")

# Display previous chat messages
display_chat()

# Input for user query
user_query = st.text_input("Enter your question")

# Ask Question Button
if st.button("Ask Question"):
    if user_query:
        # Add user message to chat history
        st.session_state.chat_history.append({"sender": "user", "message": user_query})
        
        # Send the chat query to FastAPI chat endpoint
        response = requests.get(f"{FASTAPI_URL}/chat", params={"query_request": user_query})

        if response.status_code == 200:
            assistant_response = response.json().get('response').get('response')

            # Add assistant response to chat history
            st.session_state.chat_history.append({"sender": "assistant", "message": assistant_response})

            # Refresh the chat display
            display_chat()
        else:
            st.error(f"Error: {response.content.decode()}")
    else:
        st.warning("Please enter a question before clicking 'Ask Question'.")
