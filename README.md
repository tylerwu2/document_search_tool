#  Document Search Tool

A full-stack application that allows users to summarize and query uploaded documents. Built with **Next.js** and **React** for the frontend, and **FastAPI** for the backend.

##  Features

-  Upload documents and generate summaries
-  Query documents using natural language
-  Retrieval-Augmented Generation (RAG) system for semantic search
-  Vector database storage with **ChromaDB** and embeddings via **LangChain**

##  Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js, React |
| Backend | FastAPI, Python |
| Search / Embeddings | LangChain, ChromaDB |
| Database | Vector database for semantic search |

##  Getting Started

### Prerequisites

Make sure you have the following installed:

```bash
# Node.js
node -v

# Python 3.x
python --version

# Yarn (optional)
yarn -v
```

## Install
1. Clone the repository:
```bash
git clone https://github.com/tylerwu2/document_search_tool.git
cd document_search_tool
```
2. Install frontend dependencies:
```bash
npm install
# or
yarn install
```
3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

## Development
```bash
npm run dev
# or
yarn dev
```
