from langchain_astradb import AstraDBVectorStore
import os
import pandas as pd
from dotenv import load_dotenv
from data_ingestion.data_transform import Data_converter


class Ingest_data:
    def __init__(self):
        print("Data Ingestion class is initialised...")

    def data_ingestion(self):
        pass

if __name__ =="__main__":
    data_ingest = Ingest_data()
    data_ingest.data_ingestion