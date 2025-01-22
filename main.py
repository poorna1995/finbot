from client import DocumentClient
from extractor import DocumentExtractor
from config import Config
from indexer import summaries


def main(pdf_path: str):
    document_client = DocumentClient()
    document_extractor = DocumentExtractor()

    elements = document_client.partition(pdf_path)

    if elements is not None:
        categorized_elements = document_extractor.extract_data(elements)
        table_elements, text_elements = document_extractor.get_table_text(categorized_elements)

        print("Table Elements:", len(table_elements))
        print("Text Elements:", len(text_elements))
        if table_elements:
            table_summaries = summaries(table_elements)
            print(f"Table Summaries: {table_summaries}")
    else:
        print("No elements were extracted from the PDF.")




if __name__ == "__main__":
    pdf_path = "statement.pdf"  
    main(pdf_path)
