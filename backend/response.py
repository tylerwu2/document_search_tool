from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm_instance = None

def initialize_llm():
    global llm_instance
    if llm_instance is None:
        try:
            print("Loading LLM Pipeline...(may take a few minutes)")
            pipeline_instance = pipeline(
                task="text-generation",
                model="microsoft/Phi-3-mini-4k-instruct",
                return_full_text = False, 
                max_new_tokens=512
            )

            llm_instance = HuggingFacePipeline(pipeline=pipeline_instance)
            print("LLM Pipeline loaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM pipeline: {e}")
    return llm_instance

class Response:
    
    def __init__(self, query, vectordb_instance):
        self.query = query 
        self.vectordb = vectordb_instance
        # global LLM instance used 
        if llm_instance is None:
            raise RuntimeError("LLM pipeline not initialized. Please call initialize_llm() first.")
        self.llm = llm_instance


    def find_chunks(self):
        return self.vectordb.similarity_search(self.query)
    
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