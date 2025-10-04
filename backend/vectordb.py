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
        loader = PyPDFLoader(doc_path)
        document = loader.load() 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        chunks = text_splitter.split_documents(document)

        for doc in chunks:
            doc.metadata={"source":filename}

        self.vectordb.add_documents(chunks)

    def similarity_search(self, query, num_documents=5):
        return self.vectordb.similarity_search(query, k=num_documents)

vectordb = VectorDB()