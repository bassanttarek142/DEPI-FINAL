# Constitution Study Chatbot

This project is part of the **Digital Pioneer of Egypt** initiative. It is a chatbot designed specifically for law students who want to study the Egyptian Constitution.

## Team Members
- **Abdelrhman Mohamed Ali**
- **Kenzy Mohamed**
- **Mohamed Tarek**
- **Abdelrhman Mohamed Mahmoud**
- **Marwan Tamer Mahmoud**
- **Bassant Tarek**

### Under the Supervision of:
- **Mohamed Agoor**

## Project Overview

The chatbot allows users to upload a PDF version of the Constitution and then interact with it by asking questions. The system works by creating a **vector database** from the content of the uploaded PDF, using **ChromaDB** for storage. 

The chatbot uses **LlamaIndex** to query the vector database, enabling users to get accurate and relevant responses from the Constitution text.

## Key Components

1. **Vector Database**: The Constitution PDF is processed, and a vector database is created using **ChromaDB**.
2. **Querying the Database**: The **LlamaIndex** is used to query the vector database and retrieve relevant information based on user questions.
3. **FastAPI Endpoints**: Two FastAPI endpoints are provided:
   - `/upload_pdf`: For uploading the Constitution PDF.
   - `/chat`: For interacting with the uploaded PDF and querying it with questions.
   
## How to Run

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
    ```

2. Start the FastAPI server: bash Copy code
   ```bash
   uvicorn endpoint:app --reload
    ``` 
3. Run the Streamlit UI: bash Copy code 
   ```bash
   streamlit run ui.py
    ``` 


