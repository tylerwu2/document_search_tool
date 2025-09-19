from initialize_db import vectordb
from langchain_community.document_loaders import UnstructuredDocumentPDFLoader

class Uploader:

    def __init__(self):
        pass

    # parse pdf into a document object
    def parse_document(self, file_path):
        loader = UnstructuredDOcumentPDFLoader(file_path)

        documents = loader.load()

        return documents[0].page_content

    def upload_document(self, file_path):
        document = self.parse_document(file_path)

        vector_db.insert_document(document)