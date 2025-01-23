from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_vector import MultiVectorRetriever
from config import ChromdbConfig
from indexer import DocumentIndexer
from langchain_core.runnables import RunnablePassthrough


class QueryProcessor:
    def __init__(self):
        # Initialize the retriever from the DocumentIndexer
        self.indexer = DocumentIndexer()
        self.retriever = self.indexer.retriever
        self.model = ChatOpenAI(model="gpt-3.5-turbo")

        # Define the prompt template
        self.template = """Answer the question based only on the following context, which can include text and tables:
        {context}
        Question: {question}
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)

    def query_documents(self, question: str):
        """Process the user query and return an answer based on indexed documents."""
        # Use retriever to get relevant documents
        context = self.retriever

        # Format the prompt with the context and the question
        prompt_input = {
            "context": context,
            "question": question
        }

        # Generate the answer using the model
        chain = self.prompt | self.model | StrOutputParser()
        response = chain.invoke(prompt_input)
        return response
