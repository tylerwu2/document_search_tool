from fastAPI import APIRouter
from initialize_db import vectordb
from langchain import langchain_huggingface, langchain_core, langchain.text_splitter
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.text-splitter import RecursiveChracterTextSplitter

class Response:
    
    def __init__(self, query):
        self.query = query
        self.pipeline = HuggingFacePipeline(
            model_id="gpt2, 
            task = "text-generation"
        )


    def find_chunks(self):
        chunks = vectordb.similarity_search(self.query)
        return chunks
    
    # include chunks within llm query so response only draws from context of the chunks and not outside sources
    def generate_response(self):
        template = """Question: {self.query}
        
        """ 
        
        prompt = PromptTemplate.from_template(template)
        chain = pipeline(prompt)
        output_chunks = self.find_chunks()
        return(chain.invoke({"query":self.query}))