from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

CHROMA_PATH = "chroma_db"

class VectorDB:

    def __init__(self, collection_name="documents"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.vectordb = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.embeddings
        )

    def insert_document(self, doc_path, filename): 
        try:
            loader = PyPDFLoader(doc_path)
            document = loader.load() 

            if not document:
                raise ValueError(f"Failed to load document from {doc_path}")
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
            chunks = text_splitter.split_documents(document)

            if not chunks:
                raise ValueError(f"No text chunks could be generated from {doc_path}")

            for doc in chunks:
                doc.metadata={"source":filename}

            self.vectordb.add_documents(chunks)
        except Exception as e:
            raise ValueError(f"Error processing document {filename}: {e}")

    def similarity_search(self, query, num_documents=5):
        try:
            return self.vectordb.similarity_search(query, k=num_documents)
        except Exception as e:
            raise RuntimeError(f"Error during similarity search: {e}")

vectordb = VectorDB()