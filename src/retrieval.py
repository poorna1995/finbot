from indexer import VectorDB
from generator import QueryGenerator


class DocumentRetrieval:
    def __init__(self):
        self.vector_db = VectorDB()
        self.query_gen = QueryGenerator()

    def retrieve(self, query: str):
        result = self.vector_db.search(query)
        print(f"result : {result}")
        if result:
            context = result["content"]
            generated_response = self.query_gen.handle_query(context, query)
            return generated_response
        return None
