import io
import asyncio
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# custom modules 
from vectordb import VectorDB
from response import Response, initialize_llm

#glboal instance of vector db, initialized in lifespan context manager
vectordb_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectordb_instance
    print("Application Startup...")
    try:
        print("Initializing Vector Database and Embeddings Model...")
        vectordb_instance = VectorDB()
        print("VectorDB initialized successfully.")
        print("Initializing LLM Pipeline... (may take a few minutes)")
        await asyncio.to_thread(initialize_llm)
        print("LLM Pipeline initialized successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to initialize Vector Database: {e}")
        raise RuntimeError(f"Application Startup Failed: {e}") from e
    yield
    print("Application Shutdown")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StatusResponse(BaseModel):
    status: str

class MessageResponse(BaseModel):
    message: str


def extract_text_from_pdf(pdf_bytes: bytes):
    import pdfplumber
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        # Handle potential pdfplumber errors (e.g., corrupted file)
        raise ValueError(f"Failed to process PDF file: {e}")

# API Endpoints 
# initialize app message
@app.get("/")
async def start_message():
    return {"message": "App Started!"}

# upload documents to vector db 
@app.post("/upload")
async def upload_documents(file: UploadFile = File(...)):
    if vectordb_instance is None:
        raise HTTPException(status_code=503, detail="VectorDB not initialized.")

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code = 400,
            detail = "Invalid file type. Please upload a PDF."
        )

    # add document to vectordb
    temp_file_path = f"temp_{file.filename}"
    try:
        # process file content and extract text
        file_content = await file.read()

        text = extract_text_from_pdf(file_content)

        if not text.strip():
            raise ValueError("PDF File appears to be empty.")
        
        # save to temp file for vectordb (which expects a file path)
        with open(temp_file_path, "wb") as f:
            f.write(file_content)

        await asyncio.to_thread(vectordb_instance.insert_document, temp_file_path, file.filename)
        return {"status": f"Document '{file.filename}' Uploaded Successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch-all for other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    finally: 
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# search and generate output based on query
@app.get("/response")
async def get_output(query: str):
    if vectordb_instance is None:
        raise HTTPException(status_code=503, detail="VectorDB not initialized.")

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty.")

    try:
        response = Response(query, vectordb_instance)
        result = await asyncio.to_thread(response.generate_response)
        return {"results": [result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")