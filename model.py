import os
import chromadb
from chromadb.utils import embedding_functions
from llama_index.core import StorageContext, VectorStoreIndex, PromptTemplate
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole

# Initialize constants
pdf_file_path = 'constitution.pdf'
openai_key = "sk-vc0c33AUVXu6WqRjfiba8Rum1c-aIdfv7uDdCn0wieT3BlbkFJUsQ7x3FKbBlc4Nwg1zLh2CJ7MycA4WBAjGBy5p-jsA"
collection_name = os.path.splitext(os.path.basename(pdf_file_path))[
    0]  # Use the file name without extension

# Function to set up the database and collection


def setup_chroma_collection():
    """Initialize ChromaDB client and create a collection."""
    # Create an OpenAI embedding function
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small"
    )

    # Initialize ChromaDB client and create a collection
    db = chromadb.PersistentClient(path="./new_chroma_db")
    return db.get_or_create_collection(collection_name, embedding_function=openai_ef)

# Function to create the vector store and index


def create_vector_store_and_index(chroma_collection):
    """Create vector store and storage context."""
    # Create an embedding model
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    # Initialize vector store and storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create the index
    index = VectorStoreIndex.from_documents(
        documents=[], storage_context=storage_context, embed_model=embed_model)

    return index

# Function to set up the chat engine


def setup_chat_engine(index):
    """Initialize the chat engine."""
    llm = OpenAI(model="gpt-4o-mini")
    query_engine = index.as_query_engine(llm=llm)

    custom_prompt = PromptTemplate(
        """\
بناءً على محادثة حول الدستور المصري ورسالة متابعة من المستخدم، \
قم بإعادة صياغة الرسالة لتكون سؤالًا مستقلاً يتضمن جميع السياقات المهمة من المحادثة.

<سجل المحادثة>
{chat_history}

<رسالة المتابعة>
{question}

<السؤال المستقل>
"""
    )

    chat_history = []

    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=custom_prompt,
        chat_history=chat_history,
        verbose=True
    )

    return chat_engine, chat_history

# Function to handle chat queries


def chat_with_memory(chat_engine, chat_history, user_query):
    """Process the user's query and update chat history."""
    chat_history.append(ChatMessage(role=MessageRole.USER, content=user_query))
    response = chat_engine.chat(user_query)
    chat_history.append(ChatMessage(
        role=MessageRole.ASSISTANT, content=response))
    return response
