from initialize_db import vectordb
from langchain_community.document_loaders import UnstructuredDocumentPDFLoader

class Uploader:

    def __init__(self):
        pass

    # parse pdf into a document object
    def parse_document(self, file_path):
        loader = UnstructuredDocumentPDFLoader(file_path)

        documents = loader.load()

        if not documents:
            raise ValueError("No documents could be loaded from the PDF file.")

        return documents[0].page_content

    def upload_document(self, file_path):
        document = self.parse_document(file_path)

        vectordb.insert_document(document)