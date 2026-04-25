import os
from dotenv import load_dotenv
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from utils.config_loader import load_config


class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config=load_config()

    def _validate_env(self):
        """
        Validate necessary environment variables.
        """
        required_vars = ["HF_TOKEN","GROQ_API_KEY","ASTRA_DB_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        # Force clear old key if cached
        # if "GROQ_API_KEY" in os.environ:
        #     del os.environ["GROQ_API_KEY"]
        
        missing_vars = [var for var in required_vars if os.getenv(var) is None] 
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}") 

        self.groq_api_key=os.getenv("GROQ_API_KEY")
        self.hugging_face_toke=os.getenv("HF_TOKEN")
        
        self.db_api_endpoint = os.getenv('ASTRA_DB_ENDPOINT')
        self.db_application_token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
        self.db_keyspace = os.getenv('ASTRA_DB_KEYSPACE')


    def load_embeddings(self):
        """
        Load and return the embedding model.
        """
        print("Loading Embedding model")
        model_name=self.config["embeddings_model"]["model_name"]
        return HuggingFaceEmbeddings(model=model_name)

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        model_name=self.config["llm"]["model_name"]
        print(self.groq_api_key)
        groq_model=ChatGroq(model=model_name,api_key=self.groq_api_key)
        #gemini_model=ChatGoogleGenerativeAI(model=model_name)
        
        return groq_model  # Placeholder for future LLM loading