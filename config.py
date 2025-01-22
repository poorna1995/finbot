
import os
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Any
from pydantic import BaseModel


@dataclass
class Element(BaseModel):
    type: str
    page_content: Any
    title : str


class Model:
    model="llama3:latest"

@dataclass
class Document(BaseModel):
    metadata: Dict[str, Any]  
    page_content: str




class Config:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
        self.UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")



@dataclass
class SingleQuery:
    query          : str 
    is_modified    : Optional[bool] = None 
    updated_query  : Optional[str] = None

@dataclass
class MultiQuery:
    query : str
    querylist : List[str]

@dataclass
class UserQuery:
    query : SingleQuery | MultiQuery



@dataclass
class Chromdb : 
    QUERY_TRANSLATOR = "simple"
    CHROMA_STORAGE   = "../db_data/chorma_langchain_db"
    COLLECTION_NAME  = "sampleset_summaries"
    EMBEDDING_MODEL  = "text-embedding-3-large"
    

@dataclass
class QueryPrompts:

    SIMPLE_TEMPLATE: str = (
        "You are a helpful assistant that enhances search queries related to: {question}. "
    )

    ENHANCER_TEMPLATE: str = (
        "You are a helpful assistant that enhances search queries related to: {question}. "
        "Your goal is to generate multiple alternative queries that are more specific, detailed, or phrased differently "
        "to improve the chances of retrieving relevant documents from a vector database. "
        "Provide these alternative questions in a paragaraph Original question:  question: {question}" 
        "Output:" 
    )

    DECOMPOSITION_TEMPLATE: str = (
        "You are a helpful assistant that generates multiple sub-questions related to an input question. "
        "The goal is to break down the input into a set of sub-problems / sub-questions that can be answered in isolation. "
        "Generate multiple search queries related to: {question} \n"
        "Output (5 queries):"
    )




prompt = ChatPromptTemplate.from_template(
    """
    1. Generate a summary for the following tables given: \n {doc}
    2. Provide a title for the from the summary
    """
)