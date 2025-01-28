from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from config import Config,Document,ChromdbConfig
from typing import List,Dict,Any
from translator import QueryTranslator
import logging




# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


    
class VectorDB:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=ChromdbConfig.EMBEDDING_MODEL)
        self.collection_name = ChromdbConfig.COLLECTION_NAME
        self.vector_store = Chroma(collection_name=self.collection_name, embedding_function=self.embeddings, persist_directory=ChromdbConfig.CHROMA_STORAGE)
        self.query_translator = QueryTranslator()
        self.initialize_db()
        
    def initialize_db(self):
        """Check if the database is initialized properly."""
        try:
            collections = self.vector_store._client.list_collections()
            logger.info(f"Available Collections: {collections}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def add_documents(self, documents: List[Document]):
        if documents:
            self.vector_store.add_documents(documents)
            print(self.vector_store._client.list_collections())
            self.vector_store.persist()  # Ensure data is saved to disk
            logger.info(f"Added {len(documents)} documents to the vector store.")
        else:
            logger.warning("No documents provided to add.")
        
        # self.vector_store.add_documents(documents)

    def select_best_query(self, queries: List[str], k: int = 3) -> str:
        query_scores = {}
        for query in queries:
            results_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
            if results_with_scores:
                top_score = max(results_with_scores, key=lambda x: x[1])[1]
                query_scores[query] = top_score
        
        best_query = max(query_scores, key=query_scores.get) if query_scores else ""
        print(f"Best Query Selected: {best_query}")  
        return best_query

    def search(self, query: str, k: int = 3) -> Dict[str, Any]:

        enhanced_queries = self.query_translator.translate(query)
        print(f"Original Query: {query}")
        print(f"Enhanced Queries: {enhanced_queries}")

        best_query = self.select_best_query(enhanced_queries, k=k)

        search_results_with_scores = self.vector_store.similarity_search_with_score(best_query, k=k)
        print(f"search_results_with_scores: {search_results_with_scores}")
        
        if search_results_with_scores:
            first_result = search_results_with_scores[0]
            print(f"Content: {first_result[0].metadata['page_content']}, Score: {first_result[1]}")
            formatted_result = {
                "content": first_result[0].metadata['page_content'],
                "metadata": first_result[0].metadata.get('csv_path', 'N/A'),
            }
            return formatted_result
        
        return None
