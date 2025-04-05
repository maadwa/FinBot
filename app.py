from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
import requests
import json
import re

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "finbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

def call_gemini_api(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error: No response")
    else:
        return f"Error: {response.text}"

def format_response(text):
    
    lines = text.split("\n")
    formatted_text = []
    counter = 1
    
    for line in lines:
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Remove bold (**text**)
        line = re.sub(r'\*(.*?)\*', r'\1', line)      # Remove italics (*text*)
        
        if line.strip().startswith(("-", "*")):
            formatted_text.append(f"{counter}. {line.strip('-* ')}")
            counter += 1
        else:
            formatted_text.append(line)
    
    return " ".join(formatted_text)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg
    print("User Input:", input_text)
    
    retrieved_docs = retriever.get_relevant_documents(input_text)
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    final_prompt = f"{context}\n\nQuestion: {input_text}"
    
    response = call_gemini_api(final_prompt)
    cleaned_response = format_response(response)
    
    print("Response:", cleaned_response)
    return str(cleaned_response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
