from langchain_astradb import AstraDBVectorStore
import os
import pandas as pd
from dotenv import load_dotenv
from data_ingestion.data_transform import Data_converter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

ASTRA_DB_ENDPOINT = os.getenv('ASTRA_DB_ENDPOINT')
ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_DB_KEYSPACE = os.getenv('ASTRA_DB_KEYSPACE')

os.environ['ASTRA_DB_ENDPOINT']=ASTRA_DB_ENDPOINT
os.environ['ASTRA_DB_APPLICATION_TOKEN']=ASTRA_DB_APPLICATION_TOKEN
os.environ['ASTRA_DB_KEYSPACE']=ASTRA_DB_KEYSPACE
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')

class Ingest_data:
    def __init__(self):
        print("Data Ingestion class is initialised...")
        self.embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

    def data_ingestion(self,status):
        AstraDBVectorStore(
            collection_name="abc",
            api_endpoint=ASTRA_DB_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )
        storage = status

if __name__ =="__main__":
    data_ingest = Ingest_data()
    data_ingest.data_ingestion