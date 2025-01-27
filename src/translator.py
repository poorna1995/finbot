
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import QueryPrompts



class QueryTranslator:
    """Translates or enhances queries to improve search quality."""
    def __init__(self, llm: BaseChatModel=ChatOpenAI(temperature=0)):
        super().__init__()
        self.llm = llm
        self.prompt_enhancer = ChatPromptTemplate.from_template(QueryPrompts().ENHANCER_TEMPLATE)

    def translate(self, query: str) -> str:
        """Enhance the query using an LLM."""
        # Simulate translation or enhancement using an LLM
        # For production, replace this with actual LLM integration.
        response = self.prompt_enhancer | self.llm | StrOutputParser()
        enhanced_queries = response.invoke({"question":query})
        translated_query = f"Enhanced: {enhanced_queries}"
        return enhanced_queries.split("\n")