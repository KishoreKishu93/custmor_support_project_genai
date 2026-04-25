import os
from dotenv import load_dotenv
from typing import List
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from utils.config_loader import load_config
from utils.model_loader import ModelLoader


class Retriever:

    def __init__(self):
        self.model_loader = ModelLoader() #Automatic validation happens no need of def _load_env_variables(self)
        self.config = load_config()
        self.vstore = None
        self.retriever = None

    # def _load_env_variables(self):
         
    #     load_dotenv()
         
    #     required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        
    #     missing_vars = [var for var in required_vars if os.getenv(var) is None]
        
    #     if missing_vars:
    #         raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    #     self.google_api_key = os.getenv("GOOGLE_API_KEY")
    #     self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
    #     self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    #     self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")

    def load_retriever(self):

        if not self.vstore:
            collection_name = self.config["astra_db"]["collection_name"]

            self.vstore = AstraDBVectorStore(
                embedding = self.model_loader.load_embeddings(),
                collection_name=collection_name,
                api_endpoint=self.model_loader.db_api_endpoint,
                token = self.model_loader.db_application_token,
                namespace=self.model_loader.db_keyspace,
            )
            
        if not self.retriever:
            top_k=self.config['retriever']['top_k'] if 'retriever' in self.config else 3 #if no retriver, take default 3
            retriever = self.vstore.as_retriever(search_kwargs={'k':top_k})
            print("Retriever loaded successfully.")
            return retriever
        
    def call_retriever(self,query:str)->List[Document]:
        retriever = self.load_retriever()
        output = retriever.invoke(query)
        return output
    
if __name__=="__main__":
    retriever_obj =Retriever()
    query="Suggest me budget friendly earphones"
    response = retriever_obj.call_retriever(query)

    for idx,doc in enumerate(response,1):
        print(f"Result {idx}: {doc.page_content}\nMetadata: {doc.metadata}\n")






