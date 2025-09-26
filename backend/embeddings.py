from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingsGenerator:

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedder = HuggingFaceEmbeddings(model_name=model_name)

    def embed_text(self, text: str):
        return self.embedder.embed_query(text)

    def embed_documents(self, docs: list[str]):
        return self.embedder.embed_documents(docs)