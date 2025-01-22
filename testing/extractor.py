from typing import List, Tuple
from config import Element
from unstructured.staging.base import dict_to_elements, elements_to_json

class DocumentExtractor:
    def extract_data(self, elements: List) -> List[Element]: 
        categorized_elements = []

        for element in elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                categorized_elements.append(Element(
                    type="table",
                    page_content=str(element.metadata.text_as_html)
                ))
            elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                categorized_elements.append(Element(
                    type="text",
                    page_content=str(element),

                ))
        # print(f'the length of the data context {len(categorized_elements)}')
        print(f'total data context {categorized_elements}')

        return categorized_elements

    def get_table_text(self, categorized_elements: List[Element]) -> Tuple[List[Element], List[Element]]:
        table_elements = [element for element in categorized_elements if element.type == "table"]
        print(f'the lenght of the table_elements{len(table_elements)}')
        text_elements = [element for element in categorized_elements if element.type == "text"]
        print(f'the lenght of the table_elements{len(text_elements)}')
        return table_elements, text_elements
