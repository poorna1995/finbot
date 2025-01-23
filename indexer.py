import uuid
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from config import Doc
from langchain_openai import OpenAIEmbeddings
from config import ChromdbConfig,Template, Element
from typing import List, Dict
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.prompts import ChatPromptTemplate


class DocumentIndexer:
    """
    Manages document indexing using Chroma as the vector store.
    """

    def __init__(
        self,
        collection_name: str = ChromdbConfig.COLLECTION_NAME,
        embedding_model: str = ChromdbConfig.EMBEDDING_MODEL,
        persist_directory: str = ChromdbConfig.CHROMA_STORAGE
    ):
        self.collection_name = collection_name
        self.vectorstore = self._initialize_vectorstore(embedding_model, persist_directory)
        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=InMemoryStore(),
            id_key="doc_id"
        )

    def _initialize_vectorstore(self, embedding_model: str, persist_directory: str) -> Chroma:
        """Initialize the vector store."""
        embeddings = OpenAIEmbeddings(model=embedding_model)
        return Chroma(
            collection_name=self.collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        


    def _create_documents(self, table_list: List[Element], titles: List[str], summaries: List[str]) -> List[Doc]:
        """Create documents with unique IDs."""
        table_ids = [str(uuid.uuid4()) for _ in range(len(table_list))]
        summary_tables = [
            Document(page_content=s, metadata={"doc_id": table_ids[i], "title": titles[i]})
            for i, s in enumerate(summaries)
        ]
        return summary_tables
    
    
    # Document(metadata={'doc_id': '7b2d3e8b-54d2-4887-b7d5-3030fe4a51cf', 'title': 'Financial Document Structure and Analysis'}, page_content='The table contains a list of sections from a financial document,

    def index_documents(self,table_list: List[Element], titles: List[str], summaries:List[str]):
        """Index documents in the vector store and docstore."""
        documents = self._create_documents(table_list, titles, summaries)
        table_ids = [doc.metadata["doc_id"] for doc in documents]
        self.retriever.vectorstore.add_documents(documents)
        self.retriever.docstore.mset(zip(table_ids, table_list))
        



