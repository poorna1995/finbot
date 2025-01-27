from client import DocumentClient
from indexer import VectorDB
from query import QueryHandler
from utilities import save_metadata, save_csv
from config import TableMetaData, Document
import uuid
from retrieval import DocumentRetrieval
from generator import QueryGenerator
from preprocessing import DataPreprocessing

class DocumentProcessor:
    def __init__(self, pdf_path):
        # Initialize document processing only once
        self.pdf_path = pdf_path
        self.document_processor = DocumentClient()
        self.elements = self.document_processor.partition(pdf_path)
        self.data_preprocessor = DataPreprocessing()
        self.structured_data = self.data_preprocessor.structure_data(self.elements)
        self.metadata_list = self.data_preprocessor.link_metadata(self.structured_data)
        self.document_list = self.data_preprocessor.create_documents(self.structured_data, self.metadata_list)
        
        # Set up vector database once
        self.vector_db = VectorDB()
        self.vector_db.add_documents(self.document_list)
    
    def process_query(self, query: str):
        # Use the preprocessed vector database to search for query results
        result = self.vector_db.search(query)
        if result:
            context = result["content"]
            reference = result['metadata']
            query_gen = QueryGenerator()
            generated_response = query_gen.handle_query(context, query, reference)
            return generated_response
        else:
            return "No results found for the query."
        



# # Initialize the document processor once with the given PDF path
# document_processor = DocumentProcessor("statement.pdf")

# def main(pdf_path, user_query):
#     pdf_path = "statement.pdf"
#     # Call the process_query method of the pre-initialized DocumentProcessor
#     response = document_processor.process_query(user_query)
    
#     print("Generated Response:", response)
#     return response
