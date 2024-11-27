import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb.utils import embedding_functions
from utils import clean_text_arabic


def create_collection_from_pdf(pdf_file_path):
    # Load documents from the PDF

    reader = SimpleDirectoryReader(input_files=[pdf_file_path])
    documents = reader.load_data()

    # Clean the text in the documents
    for document in documents:
        document.text = clean_text_arabic(document.text)

    # Get OpenAI API key from environment variable
    openai_key = "sk-vc0c33AUVXu6WqRjfiba8Rum1c-aIdfv7uDdCn0wieT3BlbkFJUsQ7x3FKbBlc4Nwg1zLh2CJ7MycA4WBAjGBy5p-jsA"
    # Create an OpenAI embedding function
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small"
    )

    # Initialize ChromaDB client and create a collection
    db = chromadb.PersistentClient(path="./new_chroma_db")
    collection_name = os.path.splitext(os.path.basename(pdf_file_path))[
        0]  # Use the file name without extension
    chroma_collection = db.get_or_create_collection(
        collection_name, embedding_function=openai_ef)

    # Create an embedding model
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    # Initialize vector store and storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create a VectorStoreIndex from the documents
    VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model)

    print(
        f"Collection '{collection_name}' created successfully with {len(documents)} documents.")

# Usage
# create_collection_from_pdf('constitution.pdf')
