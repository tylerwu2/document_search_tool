# import os
# from dotenv import load_dotenv
# import psycopg2
# from psycopg2.extras import register_vector 
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from embeddings import EmbeddingsGenerator

# load_dotenv()

# class VectorDB:

#     def __init__(self):
#             # establish database connection and embeddings model

#             self.conn = psycopg2.connect(
#                   database=os.getenv("DATABASE"),
#                   user=os.getenv("USER"),
#                   password=os.getenv("PASSWORD"),
#                   host=os.getenv("HOST"),
#                   port=os.getenv("PORT")
#             )
#             # register conn as a vector 
#             register_vector(self.conn)
#             self.cursor = self.conn.cursor() 
#             self.embeddings = EmbeddingsGenerator() 

    
#     def create_table(self, dimensions=384): 
#         # create table to store documents in postgresql

#         self.cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

#         sql_call = f"""
#                     CREATE TABLE IF NOT EXISTS documents (
#                     id SERIAL PRIMARY KEY,
#                     document TEXT,
#                     embedding VECTOR({dimensions})
#                     );  
#                     """

#         self.cursor.execute(sql_call)

#     def insert_document(self, text):
#         # insert document into vectordb using embeddings model 

#         embedding_vector = self.embeddings.embed_text(text)
        
#         sql_query = """
#                     INSERT INTO documents (document, embedding) VALUES (%s, %s);
#                     """
#         values = (text, embedding_vector.tolist())

#         self.cursor.execute(sql_query, values) 
#         self.conn.commit() 

#     def similarity_search(self, query, num_documents=5):
#         # search for most similar documents to return 

#         sql_query = """
#                     SELECT id, content, 1 - embedding <=> %s AS cosine_similarity
#                     FROM documents
#                     ORDER BY cosine_similarity DESC
#                     LIMIT %s; 
#                     """
        
#         values = (query.tolist(), num_documents)
        
#         self.cursor.execute(sql_query, values)
#         return self.cursor.fetchall()
    
#     # chunks document to place in vectordb 
#     def create_chunks(self, text):
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 10)
#         chunks = text_splitter.split_text(text)

#         for chunk in chunks:
#             self.insert_document(text) 

import chromadb 
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid 

class VectorDB:

    def __init__(self, collection_name="documents"):
        self.client = chromadb.Client()
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.embedding_function
            )

    def insert_document(self, text): 
        chunks = self.create_chunks(text)

        ids = [str(uuid.uuid4()) for _ in chunks]

        self.collection.add(documents=chunks, ids=ids)


    def create_chunks(self, text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 10)
        chunks = text_splitter.split_text(text)
        return chunks
    
    def similarity_search(self, query, num_documents=5):
        results = self.collection.query(query_texts=[query], n_results=num_documents)

        return results['documents'][0]