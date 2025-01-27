from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from config import Template
from langchain_core.runnables import RunnablePassthrough,RunnableMap
from langchain_core.output_parsers import StrOutputParser


class QueryHandler:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
    def handle_query(self, context: str, question: str) -> str:
        prompt = ChatPromptTemplate.from_template(Template.ENHANCED_PROMPT)
        chain = (
            RunnableMap({"context": RunnablePassthrough(), "question": RunnablePassthrough()})
            | prompt
            | self.model
            | StrOutputParser()
        )
        prompt_obj = chain.invoke({"context": context, "question": question})
        result_with_metadata = f"{prompt_obj} "
        return result_with_metadata
