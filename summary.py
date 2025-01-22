from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 
from config import Config, Element
import logging
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from typing import List
from config import Element

class ExtractData:
    def __init__(self, model: str = "llama3:latest"):
        self.model = model
        self.llm = ChatOllama(model=self.model)
        self.prompt = ChatPromptTemplate.from_template(
            """
            1. Generate a summary for the following tables given: \n {doc}
            2. Provide a title from the summary
            """
        )
        
    def summarize_tables(self, table_html: List[str]) -> List[str]:
        summary_chain = (
            {"doc": lambda x: x}
            | self.prompt
            | self.llm
            | StrOutputParser()  
        )
        response = summary_chain.batch(table_html, {"max_concurrency": 5})
        return response
    
    def extract_summary_and_title(self, response: List[str]) -> List[Dict[str, str]]:
        summaries, titles = [], []
        
        for entry in response:
            if '**Summary:**' in entry and '**Title:**' in entry:
                parts = entry.split('**Title:**')
                summary = parts[0].replace('**Summary:**', '').strip()
                title = parts[1].strip()
            else:
                summary = entry.replace('**Summary:**', '').strip()
                title = summary[:230] if summary else "No title available"
            
            summaries.append(summary)
            titles.append(title)

        return [{"summary": summary, "title": title} for summary, title in zip(summaries, titles)]
    
    def table_data(self, table_html: List[str], titles: List[str]) -> List[Element]:
        table_data = []
        for i, element in enumerate(table_html):
            title = titles[i] if i < len(titles) else "Default Title"
            table_data.append(
                Element(
                    type="table",
                    title=str(title),
                    page_content=str(element)
                )
            )
        return table_data






