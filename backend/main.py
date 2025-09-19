from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.response import JSONResponse
from initialize_db import vectordb
import pdfplumber
import io
import upload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(pdf_bytes: bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


@app.on_event("startup")
def startup():
    vectordb.create_table()

# initialize app message
@app.get("/")
async def start_message():
    return {"message": "App Started!"}

# upload documents to vector db 
@app.post("/upload")
async def upload_documents(file: UploadFile = File(...)):
        # add document to vectordb
    try:
        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)
        vectordb.insert_document(text)
        return {"status": "Document Uploaded"}
    except Exception as e:
        return JSONResponse(status_code = 500, content = {"error": str(e)})

# search and generate output based on query
@app.get("/response")
async def get_output(query: str):
    response = Response(query)
    return response.generate_response()