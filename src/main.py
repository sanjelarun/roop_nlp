import os
from extraction.extractors import extract_loops_from_code_v4
from refactoring.refactor import refactor_loop
from generation.code_generator import generate_pyspark_code
import traceback

def read_file_to_string(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a string.
    
    Args:
    - file_path (str): Path to the file.

    Returns:
    - str: Content of the file.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_string_to_file(content: str, file_path: str):
    """
    Writes the given string content to a file.
    
    Args:
    - content (str): The content to write to the file.
    - file_path (str): Path to the output file.
    """
    with open(file_path, 'w') as file:
        file.write(content)

def print_extracted_loops(extracted_loops):
    """
    Prints details of the extracted loops for debugging and clarity.
    """
    for loop in extracted_loops:
        print("="*50)
        print(f"Loop ID: {loop.loop_id}")
        print(f"Start Line: {loop.start_line}")
        print(f"End Line: {loop.end_line}")
        print(f"Input Datasets: {', '.join(loop.input_datasets)}")
        if loop.result_datasets:
            print(f"Result Datasets: {', '.join(loop.result_datasets)}")
        if hasattr(loop, "operations"):
            print(f"Operations:")
            for operation in loop.operations:
                print(f"  - Variables: {', '.join(operation.variables)}, Operation: {operation.operation_str}")
        if hasattr(loop, "conditions") and loop.conditions:
            print(f"Conditions:")
            for condition in loop.conditions.values():
                print(f"  - {condition}")
        print("="*50)

def driver_program(file_path, out_file_path):
    try:
        python_code = read_file_to_string(file_path)
        # Step 1: Extract loops from the Python file
        extracted_loops = extract_loops_from_code_v4(python_code)
        
        # Display extraction results
        print_extracted_loops(extracted_loops)
        
        # Step 2: Refactor the code (for demonstration purposes, using predictions ["map", "filter", "reduce"] for all loops)
        predictions = [["filter"], ["map"]]  # Dummy predictions for all loops; will use NLP model later
        predictions = [["join"]] 
        predictions = [["reduce"]] 
        idx = 0
        while idx < len(extracted_loops):
            loop = extracted_loops[idx]
            refactored_code = refactor_loop(loop, predictions[idx])
            loop.refactored_code = refactored_code
            if loop.is_nested:
                idx += 2 
            else:
                idx += 1
        
        # Step 3: Generate PySpark code
        python_code = read_file_to_string(file_path)
        pyspark_code = generate_pyspark_code(python_code, extracted_loops)
        write_string_to_file(pyspark_code, out_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    base_directory = "f:/Papers/IEEE-BigData-2023/roop_nlp/src/test/"
    file_path = "simple_loop.py"
    out_file_path = os.path.join(base_directory, "multiple_loop_pyspark.py")
    in_file_path = os.path.join(base_directory, file_path)
    driver_program(in_file_path, out_file_path)
