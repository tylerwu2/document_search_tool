import io
import asyncio
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# custom modules 
from vectordb import vectordb
from response import Response

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup...")
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
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code = 400,
            detail = "Invalid file type. Please upload a PDF."
        )

    # add document to vectordb
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        await asyncio.to_thread(vectordb.insert_document, text)
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
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty.")

    try:
        response = Response(query)
        result = await asyncio.to_thread(response.generate_response)
        return {"results": [result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")