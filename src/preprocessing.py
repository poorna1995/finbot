from utilities import save_metadata, save_csv
from langchain.llms import OpenAI
from pydantic import BaseModel
from config import Metadata, TableMetaData
from typing import List,Dict,Any
from uuid import uuid4
from langchain.schema import Document
import os


class DataProcessor:
    def __init__(self):
        self.llm = OpenAI()

    def generate_metadata(self, text: str, page_content: str) -> Metadata:
        summary = self.llm.invoke(f"Summarize the following content: {text}")
        title = self.llm.invoke(f"Provide a title for the following content: {text}")
        keywords_prompt = f"Extract 5-8 precise and relevant keywords from the following content: {text}"
        keywords = self.llm.invoke(keywords_prompt)

        return Metadata(
            summary=summary,
            title=title,
            keywords=keywords,
            page_content=page_content
        )

    def structure_data(self, elements) -> List[TableMetaData]:
        structured_data = []
        for element in elements:
            if element.category == "Table":
                element_id = element.id
                structured_data.append(TableMetaData(
                    element_id=element_id,
                    page_number=element.metadata.page_number,
                    table_content=element.metadata.text_as_html,
                    metadata=self.generate_metadata(element.text, element.metadata.text_as_html)
                ))
        return structured_data

    def link_metadata(self, structured_data):
        metadata_list = []
        for idx, data in enumerate(structured_data):
            doc_num = idx + 1
            page_num = data.page_number
            json_path = f"data/doc{doc_num}_page{page_num}_table_schema.json"
            csv_path = f"data/doc{doc_num}_page{page_num}_table_data.csv"
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            data_dict = data.dict()
            save_metadata(data_dict, json_path)
            save_csv(data_dict, csv_path)

            metadata_list.append({"json_path": json_path, "csv_path": csv_path})

        return metadata_list
    
    def create_documents(self, structured_data : List[TableMetaData], metadata_list):
        table_ids = [str(uuid4()) for _ in structured_data]
        document_list = [
            Document(
                id=table_ids[i],  # Assigning the ID correctly
                page_content=tab_data.metadata.summary,  
                metadata={**tab_data.metadata.dict(),  
                          "json_path": metadata_list[i]["json_path"],
                          "csv_path": metadata_list[i]["csv_path"]}  
            )
            for i, tab_data in enumerate(structured_data)
        ]

        return document_list