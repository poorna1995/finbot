import uuid
from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from config import Document

class DocumentIndexer:
    def __init__(self, collection_name: str, model: str, persist_directory: str):
        self.vectorstore = self.initialize_vectorstore(collection_name, model, persist_directory)
        self.store = InMemoryStore()
        self.id_key = "doc_id"
        self.retriever = MultiVectorRetriever(vectorstore=self.vectorstore, docstore=self.store, id_key=self.id_key)
        
    def initialize_vectorstore(self, collection_name: str, model: str, persist_directory: str):
        """Initialize the vector store for indexing."""
        return Chroma(
            collection_name=collection_name,
            embedding_function=OllamaEmbeddings(model=model),
            persist_directory=persist_directory,
        )
    
    def generate_unique_ids(self, table_data: List(Element)) -> List(str):
        """Generate unique UUIDs."""
        return [str(uuid.uuid4()) for _ in table_data]

    def create_documents(self, summaries: List[str], titles:List[str]) -> List[Document]:
        """Create Document objects from summaries and titles."""
        table_ids = self.generate_unique_ids(len(summaries))
        summary_table = [
            Document(page_content=summaries[i], metadata={self.id_key: table_ids[i], "title": titles[i]})
            for i in range(len(summaries))
        ]
        return summary_table
        def store_documents(self, table_data: List[Element]):
            """Store documents in the retriever's docstore."""
            table_ids = self.generate_unique_ids(len(summaries))
            self.retriever.vectorstore.add_documents(summary_tables)
            self.retriever.docstore.mset(list(zip(table_ids, table_data)))
            
        def index_documents(self, summaries: List[str], titles: List[str]):
            """Main method to index documents."""
            documents = self.create_documents(summaries, titles)
            self.store_documents(documents)