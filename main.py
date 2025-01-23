from client import DocumentClient
from config import Config
from indexer import DocumentIndexer
from summary import ExtractData
from client import DocumentClient
from typing import List, Dict
from query import QueryProcessor
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_vector import MultiVectorRetriever
from config import ChromdbConfig,Element
# from indexer import DocumentIndexer
from langchain_core.runnables import RunnablePassthrough



import os
from config import Config, ChromdbConfig, Element, Document
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()



def main(pdf_path: str):
    """
    Main function to run the document processing pipeline.
    It partitions the document, generates summaries, and indexes them.
    """
    # Initialize the Document Client to partition the document
    client = DocumentClient()
    elements = client.partition(pdf_path)
    if not elements:
        logger.error(f"No elements found in the document: {pdf_path}")
        return
    
    # Extract the HTML table content and titles from the elements
    table_elements = [element for element in elements if element.category == "Table"]
    table_html = [table.metadata.text_as_html for table in table_elements]
    
    
    print(table_html)

    # Use the ExtractData class to summarize and extract titles
    extractor = ExtractData()
    summarize_tables = extractor.summarize_tables(table_html)
    summary,titles = extractor.extract_summary_and_title(summarize_tables)
    table_list =extractor.table_data(table_html,titles)
    

    # Index the summarized documents using DocumentIndexer
    indexer = DocumentIndexer()
    indexer.index_documents(table_list,titles,summary)

    retriever = indexer.retriever
    print(retriever.invoke("What is the total equity value in March 29, 2023?"))
    
    # Define your prompt template
    template = """Answer the question based only on the following context, which can include text and tables:
    {context}
    Question: {question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=0.1, model ="gpt-3.5-turbo")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    question = "What is the total equity value in March 29, 2023?"
    # Pass data through the chain
    response = chain.invoke(question)
    
    # Print the response from the model
    print(f"Answer: {response}")


    

if __name__ == "__main__":
    # Example PDF file to process
    pdf_path = "statement.pdf"

    # Run the document processing pipeline
    main(pdf_path)
