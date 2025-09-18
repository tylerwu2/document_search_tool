from fastapi import FastAPI, APIRouter
from initialize_db import vectordb

app = FastAPI()
router = APIRouter() 

# initialize app message
@app.get("/")
async def start_message():
    # initialize vectordb if not created already
    vectordb.create_table() 
    return {"message": "App Started!"}

# upload documents to vector db 
@app.post("/upload")
async def upload_documents(document):
    # add document to vectordb
    vectordb.insert_document(document)
    return {"status": "Document Uploaded", "document": document}

# search and generate output based on query
@app.get("/search")
async def search_output(query):
    return vectordb.similarity_search(query)