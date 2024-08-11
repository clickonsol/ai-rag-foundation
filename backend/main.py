import chromadb
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from models import ChatMessage, ChatThread, Document, UserProfile
import openai
from user_manager import UserManager  # Import the UserManager class

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the OpenAI API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Ensure that the key is loaded correctly
if not openai_api_key:
    raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Initialize the FastAPI app
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Initialize ChromaDB client and collection
embedding_function = OpenAIEmbeddings()

# Corrected Chroma initialization
vector_store = Chroma(
    collection_name="documents",  # Name of the collection
    embedding_function=embedding_function,
    persist_directory="chroma_data"  # Optional: Directory to persist data
)

# Initialize UserManager
user_manager = UserManager()

# Function to generate response using GPT-4o-mini Chat API
def generate_response(input_text):
    # Call the OpenAI API using the chat completion method with your custom model
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant knowledgeable about Python code."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # Extract the assistant's reply from the response
    return response.choices[0].message.content.strip()

# In-memory storage for demonstration (replace with DB in production)
chat_history = []
documents = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the backend!"}

# Endpoint for chat interface using LangChain with GPT-4o-mini
@app.post("/chat/")
def post_message(message: ChatMessage):
    # Generate a response using the generate_response function
    response = generate_response(message.message)

    # Append to chat history (optional)
    message.timestamp = datetime.now()
    chat_history.append(message)

    return {"response": response}

# Endpoint to get chat history
@app.get("/chat/history/", response_model=List[ChatThread])
def get_chat_history():
    return chat_history

# Endpoint to get user profile
@app.get("/profile/", response_model=UserProfile)
def get_profile():
    return user_manager.get_user_profile()

# Endpoint to update user profile
@app.put("/profile/", response_model=UserProfile)
def update_profile(profile: UserProfile):
    return user_manager.update_user_profile(profile)

# Endpoint to upload documents and index in ChromaDB
@app.post("/documents/", response_model=Document)
def upload_document(document: Document):
    documents.append(document)
    
    # Add the document to ChromaDB via LangChain's Chroma vector store
    vector_store.add_texts(
        texts=[document.name],  # Assuming `document.name` is the text content, replace as needed
        metadatas=[{"name": document.name, "download_link": document.download_link}]
    )
    
    return document

# Endpoint to list documents
@app.get("/documents/", response_model=List[Document])
def list_documents():
    return documents
