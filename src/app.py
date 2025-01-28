import time
import streamlit as st
from main import DocumentProcessor  # Import the renamed class



# Initialize Document Processor variable in session state
if 'financial_document_processor' not in st.session_state:
    st.session_state.financial_document_processor = None

def app():
    st.title("Financial Data QA Bot")
    st.write("Upload your PDF document containing P&L statements and ask questions about the financial data.")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    # Input for user query
    user_query = st.text_input("Enter your financial query (e.g., 'What is the total revenue for the year?')")

    if pdf_file is not None:
        # Save the uploaded file temporarily
        with open("uploaded_pdf.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())
        
        # Initialize Document Processor with the uploaded PDF if not already done
        if st.session_state.financial_document_processor is None:
            # Show a progress bar while processing
            with st.spinner("Processing your PDF..."):
                progress_bar = st.progress(0)
                
                # Simulate processing steps (you can adjust this part based on actual processing)
                for i in range(100):
                    # Simulate some work being done
                    time.sleep(0.01)  # Simulate time taken to process each step
                    progress_bar.progress(i + 1)
                
                # Initialize the Document Processor after simulating work
                st.session_state.financial_document_processor = DocumentProcessor("uploaded_pdf.pdf")
                st.success("PDF uploaded and processed successfully!")

    # Submit button for queries
    if st.button("Submit Query"):
        if st.session_state.financial_document_processor:
            if user_query:  # Check if user_query is not empty
                response = st.session_state.financial_document_processor.process_query(user_query)
                st.write("Generated Response:")
                st.write(response)
            else:
                st.warning("Please enter a query before submitting.")
        else:
            st.warning("Please upload a PDF before submitting a query.")

if __name__ == "__main__":
    app()
