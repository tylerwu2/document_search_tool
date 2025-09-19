from fastAPI import APIRouter
from initialize_db import vectordb
from langchain import langchain_huggingface, langchain_core, langchain_text_splitters
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveChracterTextSplitter

class Response:
    
    def __init__(self, query):
        self.query = query
        self.pipeline = HuggingFacePipeline(
            model_id="gpt2", 
            task = "text-generation"
        )


    def find_chunks(self):
        chunks = vectordb.similarity_search(self.query)
        return chunks
    
    # include chunks within llm query so response only draws from context of the chunks and not outside sources
    def generate_response(self):
        template = """Question: {query}
        
        Use the provided context and information to generate a response, do not bring in outside context or information. 
        Context: {context}
        """ 
        
        prompt = PromptTemplate.from_template(template)
        chain = self.pipeline(prompt)
        output_chunks = self.find_chunks()
        return(chain.invoke({"query":self.query, "context":output_chunks}))