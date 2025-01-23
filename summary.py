from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 
from config import Config, Element
import logging
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import re
from typing import List
from config import Element,Template
from typing import List, Dict,Tuple
from langchain_openai import ChatOpenAI




class ExtractData:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.llm = ChatOpenAI(model=self.model)
        self.prompt = ChatPromptTemplate.from_template(Template.PROMPT_TEMPLATE)

    def summarize_tables(self, table_html: List[str]) -> List[str]:
        """
        Generate summaries for a list of HTML tables.
        """
        summary_chain = (
            {"doc": lambda x: x} | self.prompt | self.llm | StrOutputParser()
        )
        return summary_chain.batch(table_html, {"max_concurrency": 5})


    def extract_summary_and_title(self, response: List[str]) -> Tuple[List[str], List[str]]:
        """
        Extract summaries and titles from the model's response using regex.
        """
        summaries = []
        titles = []
        for entry in response:
            summary = re.search(r"- Summary:\s*(.*?)(?=\n)", entry, re.DOTALL)
            title = re.search(r"- Title:\s*(.*)", entry)
            if summary and title:
                summaries.append(summary.group(1).strip())
                titles.append(title.group(1).strip())
        return summaries, titles

    def table_data(self, table_html: List[str], titles: List[str]) -> List[Element]:
        assert len(titles) == len(table_html)
        """
        Combine HTML table data with extracted titles into Element objects.
        
        """
        table_list =[]
        # Retrieve the corresponding title from the titles list
        for i, element in enumerate(table_html):
            # Retrieve the corresponding title from the titles list
            title = titles[i] if i < len(titles) else "Default Title"
            # Append the Element instance to the categorized_elements list
            table_list.append(
                Element(
                    type="table",
                    title=str(title),       
                    page_content=str(element)  
                )
            )
        return table_list





