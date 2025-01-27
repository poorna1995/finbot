
# test_query_processing_pipeline.py

import time  # Import the time module to track time
from main import DocumentProcessor  # Import the necessary main function



# Sample questions to process
SAMPLESET_QUESTIONS = [
    "How did gross profit change from 2023 to 2024?"
    "What was the operating profit for Q1 2024?"
    "What were total operating expenses for FY 2024?"
    "What was the profit attributable to owners for both years?"
    " What was total comprehensive income for Q1 2024?"
    "How does profit for Q1 2024 compare with Q1 2023?"
    "What was the revenue from operations for the year ending March 31, 2024, and how does it compare to March 31, 2023?"
    "What was the cost of sales for the year ending March 31, 2024, compared to March 31, 2023?",
    "How does the gross profit for the three months ending March 31, 2024, differ from the same period in 2023?",
    "What are the components of operating expenses, including selling, marketing, and administration, and how have they changed between FY 2023 and FY 2024?",
    "What was the total spending on selling and marketing expenses for the year ending March 31, 2024, compared to the previous year?",
    "How did general and administration expenses vary between FY 2023 and FY 2024?",
    "What was the finance cost incurred during the three months and year ending March 31, 2024?",
    "What was the current tax expense for FY 2024, and how does it compare to FY 2023?",
    "How has the deferred tax expense changed in FY 2024 relative to FY 2023?",
    "What was the profit for the period for FY 2024 compared to FY 2023?",
    "How did the exchange differences on the translation of foreign operations change between FY 2023 and FY 2024?",
    "What was the profit attributable to the owners of the company for FY 2024 compared to FY 2023?",
    "How much profit was attributable to non-controlling interests for FY 2024?",
    "What was the total comprehensive income attributable to the owners of the company for FY 2024 compared to FY 2023?",
]


# Function to simulate the pipeline for each query and track the time
def run_pipeline(document_processor, query):
    start_time = time.time()  # Record the start time
    print(f"Processing query: {query}")
    
    # Run the pipeline
    response = document_processor.process_query(query)
    
    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time  # Calculate the time taken for the process
    
    return response, time_taken


# Main execution
output_file = "query_responses.txt"
pdf_path = "statement.pdf"  # PDF file path

try:
    # Initialize DocumentProcessor once
    document_processor = DocumentProcessor(pdf_path)
    
    # Open the output file in append mode
    with open(output_file, "a") as file:
        for query in SAMPLESET_QUESTIONS:
            file.write("------------------------------------------------------------------------------------------\n")
            file.write(f">>> User Question: {query}\n")
            
            response, time_taken = run_pipeline(document_processor, query)
            
            # Store the time taken for the query and response in the text file
            file.write(f">>> Time taken for query: {time_taken:.2f} seconds.\n")
            file.write(f">>> Response: {response}\n")
            file.write("Pipeline executed for query.\n\n")
    
    print(f"Results have been written to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")




















# SAMPLESET_QUESTIONS  = [
#     "What was the revenue from operations for Q1 2024 vs. Q1 2023?",
#     "How did gross profit change from 2023 to 2024?",
#     # "What was the operating profit for Q1 2024?",
#     # "What were total operating expenses for FY 2024?",
#     # "How did selling and marketing expenses change year-over-year?",
#     # "What was the current tax expense for Q1 2024?",
#     # "How did deferred tax expenses differ between the two years?",
#     # "What was the total other comprehensive income for Q1 2024?",
#     # "How did exchange differences affect total comprehensive income in FY 2024?",
#     # "What was the profit attributable to owners for both years?",
#     # "How did comprehensive income for non-controlling interests compare between years?",
#     # "What was total comprehensive income for Q1 2024?",
#     # "How does profit for Q1 2024 compare with Q1 2023?"
# ]


# # Function to simulate the pipeline for each query and track the time
# def run_pipeline_for_queries():
#     # Process each question in the sample set
#     for query in SAMPLESET_QUESTIONS:
#         start_time = time.time()  # Record the start time
#         print(f"Processing query: {query}")

#         # Run the pipeline using your main function, passing the query
#         main("statement.pdf", query)  # Adjusted to pass query to the main function
        
#         end_time = time.time()  # Record the end time
#         time_taken = end_time - start_time  # Calculate the time taken for the process

#         # Print the time taken for the current query
#         print(f"Time taken for query: {query} is {time_taken:.2f} seconds.")
#         print("Pipeline executed for query.")

# if __name__ == "__main__":
#     run_pipeline_for_queries()  # Execute the pipeline for all queries




# import time  # Import the time module to track time
# from main import main  # Import the necessary main function

# SAMPLESET_QUESTIONS = [
#     "What was the revenue from operations for Q1 2024 vs. Q1 2023?",
#     "How did gross profit change from 2023 to 2024?",
#     # "What was the operating profit for Q1 2024?",
#     # "What were total operating expenses for FY 2024?",
#     # "How did selling and marketing expenses change year-over-year?",
#     # "What was the current tax expense for Q1 2024?",
#     # "How did deferred tax expenses differ between the two years?",
#     # "What was the total other comprehensive income for Q1 2024?",
#     # "How did exchange differences affect total comprehensive income in FY 2024?",
#     # "What was the profit attributable to owners for both years?",
#     # "How did comprehensive income for non-controlling interests compare between years?",
#     # "What was total comprehensive income for Q1 2024?",
#     # "How does profit for Q1 2024 compare with Q1 2023?"
# ]

# # Function to simulate the pipeline for each query and track the time
# def run_pipeline(query):
#     # Initialize the pipeline here (if main initializes resources, it will do it only once)
#     start_time = time.time()  # Record the start time
#     print(f"Processing query: {query}")

#     # Run the pipeline using your main function, passing the query
#     response = main("statement.pdf", query)  # Assuming main function returns the response
    
#     end_time = time.time()  # Record the end time
#     time_taken = end_time - start_time  # Calculate the time taken for the process
    
#     return response, time_taken

# # File to store the results
# output_file = "query_responses.txt"

# # Open the file in append mode
# with open(output_file, "a") as file:
#     # Loop over all queries
#     for query in SAMPLESET_QUESTIONS:
#         file.write("------------------------------------------------------------------------------------------\n")
#         file.write(f">>> User Question: {query}\n")
        
#         response, time_taken = run_pipeline(query=query)
        
#         # Store the time taken for the query and response in the text file
#         file.write(f">>> Time taken for query: {query} is {time_taken:.2f} seconds.\n")
#         file.write(f">>> Response: {response}\n")  # Storing the response
#         file.write("Pipeline executed for query.\n\n")

# print(f"Results have been written to {output_file}")
