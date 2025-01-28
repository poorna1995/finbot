from unstructured_client import UnstructuredClient
from unstructured_client.models import shared, operations
from unstructured_client.models.errors import SDKError
from config import Config
from dotenv import load_dotenv 
import os
from unstructured.staging.base import dict_to_elements, elements_to_json

load_dotenv()
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
    UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")
    


class DocumentClient:
    def __init__(self):
        config = Config()
        self.client = UnstructuredClient(
            api_key_auth=Config.UNSTRUCTURED_API_KEY,
            server_url=Config.UNSTRUCTURED_API_URL,
        )

    def partition(self, pdf_path: str):
        with open(pdf_path, "rb") as f:
            files = shared.Files(
                content=f.read(),
                file_name=pdf_path  # Ensure only the file name is passed
            )
        req = operations.PartitionRequest(
            partition_parameters=shared.PartitionParameters(
                files=files,
                strategy="hi_res",
                hi_res_model_name="yolox",
                skip_infer_table_types=[],
                pdf_infer_table_structure=True,
            )
        )
        try:
            resp = self.client.general.partition(request=req)
            elements = dict_to_elements(resp.elements)
            return elements  
        except SDKError as e:
            print(f"Error during partitioning: {e}")
            return None
            
