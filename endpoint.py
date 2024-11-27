from fastapi import FastAPI, File, UploadFile, HTTPException
from model import setup_chat_engine , create_vector_store_and_index, setup_chroma_collection, chat_with_memory
from ingest import create_collection_from_pdf
from fastapi.responses import JSONResponse

import os

app = FastAPI()



@app.get("/chat")
async def chat_with_pdf(query_request: str):
    try:
        chroma_collection = setup_chroma_collection()
        index = create_vector_store_and_index(chroma_collection)
        chat_engine, chat_history = setup_chat_engine(index)

        response = chat_with_memory(chat_engine, chat_history, query_request)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded PDF file to a temporary location
    pdf_file_path = f"./temp/{file.filename}"  # Save it in a temp folder
    try:
        os.makedirs("./temp", exist_ok=True)  # Ensure temp folder exists
        with open(pdf_file_path, "wb") as f:
            f.write(await file.read())
        
        # Process the PDF file and create a collection
        create_collection_from_pdf(pdf_file_path)

        # Clean up the temporary file after processing
        os.remove(pdf_file_path)

        return JSONResponse(content={"message": f"Collection created from '{file.filename}' successfully."}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Ensure the file is removed in case of an error
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
# To run the FastAPI app, use the command:
# uvicorn filename:app --reload
