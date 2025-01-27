import os
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Any
from pydantic import BaseModel


class ChromdbConfig:
    QUERY_TRANSLATOR: str = "simple"
    CHROMA_STORAGE: str = "./db"
    COLLECTION_NAME: str = "sampleset_summaries"
    EMBEDDING_MODEL: str = "text-embedding-3-large"

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
        self.UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class Metadata(BaseModel):
    summary: str
    title: str
    keywords: str
    page_content: str


class TableMetaData(BaseModel):
    element_id:str
    page_number:int
    table_content:Any
    metadata:Metadata
class Document(BaseModel):
    id: str
    page_content: str
    metadata: Dict[str, Any]
    


class Template:
    GENERAL_PROMPT = """Answer the question based only on the following context, which can include text and tables:
        {context}
        Question: {question}
        """
    ENHANCED_PROMPT = """Answer the following question based on the provided context:
        {context}
        Question: {question}

        Provide a clear and concise answer with key points, supported by relevant examples from the context. If applicable, mention any important background or influencing factors.
        write it in pointer if needed, and provide the calculation if it needed it step by step
        """



class QueryPrompts:
    
    SIMPLE_TEMPLATE: str = (
        "You are a helpful assistant that enhances search queries related to: {question}. "
    )

    ENHANCER_TEMPLATE: str = (
        "You are a helpful assistant that enhances search queries related to: {question}. "
        "Your goal is to generate 2 alternative queries that are more specific, detailed, or paraphrased differently "
        "to improve the chances of retrieving relevant documents from a vector database.\n"
        "Output:\n"
    )




