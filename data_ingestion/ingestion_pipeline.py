import os
import pandas as pd
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from typing import List, Tuple
from utils.model_loader import ModelLoader
from utils.config_loader import load_config

class DataIngestion:
    """
    Class to handle data transformation and ingestion into AstraDB vector store.
    """

    def __init__(self):
        """
        Initialize environment variables, embedding model, and set CSV file path.
        """
        print("Initializing DataIngestion pipeline...")
        load_dotenv()
        self.model_loader = ModelLoader()
        self.config = load_config()
        self._load_env_variables()
        self.file_path = self._get_csv_path()
        self.product_data =self._load_csv()

    def _load_env_variables(self):
        """
        Load and validate required environment variables.
        """
        required_vars=["ASTRA_DB_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]   

        missing_vars = [var for var in required_vars if os.getenv(var) is None] 
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.db_api_endpoint = os.getenv('ASTRA_DB_ENDPOINT')
        self.db_application_token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
        self.db_keyspace = os.getenv('ASTRA_DB_KEYSPACE')

    def _get_csv_path(self):
        """
        Get path to the CSV file located inside 'data' folder.
        """   
        base_path = os.getenv('PROJECT_DATA_DIR')
        csv_path=os.path.join(base_path,"data","flipkart_product_review.csv")
        print("------csv_path------",csv_path)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        
        return csv_path
    
    def _load_csv(self):
        """
        Load product data from CSV.
        """
        df = pd.read_csv(self.file_path)
        expected_columns = {'product_title', 'rating', 'summary', 'review'}
        
        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"CSV must contain columns: {expected_columns}")

        return df

    def transform(self):
        """
        Transform product data into list of LangChain Document objects.
        """
        #required_columns = self.product_data.columns[1:]
        #Output: Index(['product_title', 'rating', 'summary', 'review'], dtype='object')

        documents =[]
        for index,row in self.product_data.iterrows():
            metadata ={
                'product_title':row['product_title'],
                'rating':row['rating'], 
                'summary':row['summary']
            }
            doc = Document(page_content=row['review'],metadata=metadata)
            documents.append(doc)
        print(f"Transformed {len(documents)} documents.") 
        return documents
    
    def store_in_vector_db(self, documents: List[Document]):
        """
        Store documents into AstraDB vector store.
        """
        collection_name = self.config['astra_db']['collection_name']
        vstore = AstraDBVectorStore(
            embedding= self.model_loader.load_embeddings(),
            collection_name=collection_name,
            api_endpoint=self.db_api_endpoint,
            token=self.db_application_token,
            namespace=self.db_keyspace,
        )

        inserted_ids = vstore.add_documents(documents)
        print(f"Successfully inserted {len(inserted_ids)} documents into AstraDB.")
        return vstore, inserted_ids

    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform data and store into vector DB.
        """
        documents = self.transform()   
        vstore,inserted_ids = self.store_in_vector_db(documents)

        # Optionally do a quick search
        query = "Can you tell me the low budget headphone"
        results = vstore.similarity_search(query)

        print(f"\nSample search results for query: {query}")
        for res in results:
            #print(res)
            print(f"Content:{res.page_content}\n metadata:{res.metadata}\n")

# Run if this file is executed directly
if __name__=='__main__':
    ingestion = DataIngestion()
    ingestion.run_pipeline()