
import os
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Any
from pydantic import BaseModel




@dataclass
class ChromdbConfig:
    QUERY_TRANSLATOR: str = "simple"
    CHROMA_STORAGE: str = "./chroma_data"
    COLLECTION_NAME: str = "sampleset_summaries"
    EMBEDDING_MODEL: str = "text-embedding-3-large"

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
        self.UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class Template:
    PROMPT_TEMPLATE : str = (
        """
        Given the following document containing tables, perform the following tasks:
        1. Analyze the data in the tables and generate a comprehensive summary that highlights the key insights, trends, or patterns present in the data. Ensure the summary is concise, informative, and easy to understand.
        2. From the generated summary, extract and provide a meaningful and descriptive title that encapsulates the core findings.

        The output should follow this format:
        - Summary: <Provide the summary here>
        - Title: <Provide the title here>
        
        Document: \n {doc}
        """
    )


class Element(BaseModel):
    type: str
    title: str
    page_content: Any
    

class Doc(BaseModel):
    metadata: Dict[str, Any]
    page_content: str



class Model:
    model="gpt-3.5-turbo"

@dataclass
class Document(BaseModel):
    metadata: Dict[str, Any]  
    page_content: str



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

