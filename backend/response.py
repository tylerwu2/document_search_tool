from initialize_db import vectordb
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Response:
    
    def __init__(self, query):
        self.query = query 
        self.pipeline = pipeline(
            task="text-generation",
            model="gpt2",
            return_full_text = False, 
            max_new_tokens=150
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipeline)


    def find_chunks(self):
        return vectordb.similarity_search(self.query)
    
    # include chunks within llm query so response only draws from context of the chunks and not outside sources
    def generate_response(self):
        template = """
        Answer the following question using only the provided context.

        Context {context}

        Question: {query}

        Answer:
        """ 
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        context_chunks = self.find_chunks()
        context_string = "\n\n".join([doc.page_content for doc in context_chunks])
        response = (chain.invoke({"query":self.query, "context": context_string}))
        return response