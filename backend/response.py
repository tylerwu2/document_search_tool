from vectordb import vectordb
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Response:
    
    def __init__(self, query):
        self.query = query 
        # error handling for LLM pipeline
        try:
            self.pipeline = pipeline(
                task="text-generation",
                model="gmistralai/Mistral-7B-Instruct-v0.2",
                return_full_text = False, 
                max_new_tokens=512
            )
            self.llm = HuggingFacePipeline(pipeline=self.pipeline)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM pipeline: {e}")


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

        # handle empty search results
        if not context_chunks:
            return {"content": "No relevant documents found in the database. Please upload documents first."}

        context_string = "\n\n".join([doc.page_content for doc in context_chunks])

        try:
            response = (chain.invoke({"query": self.query, "context": context_string}))
            if isinstance(response, dict) and "content" in response:
                return response["content"]
            elif hasattr(response, "content"):
                return response.content
            else:
                return str(response)
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}")