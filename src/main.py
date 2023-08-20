import os
from extraction.extractors import extract_from_file
from refactoring.refactor import refactor_loop

def driver_program(file_path):
    # Step 1: Extract loops from the Python file
    extracted_loops = extract_from_file(file_path)
    
    # Display extraction results
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
    
    # Step 2: Refactor the code (for demonstration purposes, using predictions ["map", "filter", "reduce"] for all loops)
    refactored_code_list = []
    predictions = ["map", "filter", "reduce"]  # Dummy predictions for all loops # We will use NLP model late for this
    
    for loop in extracted_loops:
        refactored_code = refactor_loop(loop, predictions)
        refactored_code_list.append(refactored_code)
    
    # Display refactored code
    print("\nRefactored Code:")
    print("-"*50)
    for code in refactored_code_list:
        print(code)
        print("-"*50)

# if __name__ == "__main__":
#     # Taking the file path as command line argument
#     if len(sys.argv) != 2:
#         print("Usage: python driver_program.py <path_to_python_file>")
#         sys.exit(1)
    
#     file_path = sys.argv[1]
#     driver_program(file_path)
base_directory = 'F:/Papers/IEEE-BigData-2023/roop_nlp/src/test'
file_path="mutliple_loop.py"
file_path = os.path.join(base_directory,file_path)
driver_program(file_path)