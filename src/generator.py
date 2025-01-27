
from langchain_core.runnables import RunnablePassthrough,RunnableMap
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class QueryGenerator:
    """Generates additional queries or content based on input."""
    
    ENHANCED_PROMPT: str = (
        "You are a helpful assistant that provides a detailed and informative response based on the provided context and question.\n"
        "Provide a step by step calculator if it is required"
        "Context: {context}\n"
        "Question: {question}\n"
        "Response:"
    )

    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")

    def handle_query(self, context: str, question: str, reference:str) -> str:
        """Generate a natural language response based on context and question."""
        prompt_template = ChatPromptTemplate.from_template(self.ENHANCED_PROMPT)
        print(f"context:{context}")
        
        # Create a chain that processes the context and question through the model
        chain = (
            RunnableMap({"context": RunnablePassthrough(), "question": RunnablePassthrough()})
            | prompt_template
            | self.model
            | StrOutputParser()
        )
        
        # Invoke the chain with the provided context and question
        prompt_obj = chain.invoke({"context": context, "question": question})
        
        return f"{prompt_obj} \n Reference:{reference}"