import pandas as pd
from langchain_core.documents import Document

class Data_converter:

    def __init__(self):
       print("Data Convertion has been initialised...")
       self.product_data = pd.read_csv(r'..\data\flipkart_product_review.csv')
       #print(self.product_data.head())

    def data_transformation(self):
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
        #print(documents[0])    
        return documents
        


if __name__ =="__main__":
    data = Data_converter()
    data.data_transformation()
    

