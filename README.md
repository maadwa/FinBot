# FinBot: AI Powered Financial Assistant 🤖💰

FinBot is an intelligent chatbot designed to answer queries related to finance and investment. It is trained using the renowned book **"Financial and Investment Management" by Sudhindra Bhat**, ensuring high-quality, reliable responses rooted in established academic content.

📚 Overview

FinBot leverages the power of **NLP**, **embedding models**, and **vector databases** to provide accurate answers to user queries. It utilizes **Gemini 2.0 Flash** from Google for content generation and **Pinecone** for vector storage and retrieval, delivering context-aware responses with speed and precision.

🚀 Features

- 💬 **Conversational Chatbot** interface built with Flask
- 📖 **Domain-specific training** using PDF content
- 🧠 **Semantic search** using Sentence Transformers
- 📌 **Vector database integration** with Pinecone
- 🤖 **AI responses** powered by Google's Gemini 2.0 Flash
- 🌐 Environment configuration using `.env`

🛠️ Tech Stack

- **Frontend/Backend**: Flask
- **AI & Embedding**: LangChain, Sentence Transformers
- **Vector DB**: Pinecone (gRPC)
- **PDF Parsing**: PyPDF
- **LLM**: Google Gemini 2.0 Flash API

📥 Data Used

- **Training Material**: _"Financial and Investment Management"_ by Sudhindra Bhat (PDF)
- Uploaded and parsed using PyPDF for embedding and retrieval.

💡 How It Works

1. PDF content is parsed and embedded using Sentence Transformers.
2. Embeddings are stored in Pinecone for fast vector search.
3. When a user asks a question:
   - The query is converted into an embedding.
   - Relevant sections are retrieved from Pinecone.
   - Gemini 2.0 Flash generates a contextual response using retrieved data.

🎬 Live Preview

Here's a quick look at FinBot in action:

![FinBot Demo](asset/demo.gif)

## 📜 License

This project is for educational purposes only. All rights to the book content belong to the original author and publisher.
