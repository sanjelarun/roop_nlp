import sys
import os
sys.path.append('F:/Papers/IEEE-BigData-2023/roop_nlp/src')

from extraction.extractors import extract_from_file

base_directory = 'F:/Papers/IEEE-BigData-2023/roop_nlp/src/test'

def test_extraction_from_file(file_paths: list):
    """Tests the extraction function for a list of file paths.
    
    Args:
        file_paths (list): List of paths to the Python files to be tested.
        
    Returns:
        dict: A dictionary where keys are file paths and values are lists of extracted Loop objects.
    """
    results = {}
    for file_path in file_paths:
        file_path = os.path.join(base_directory,file_path)
        extracted_loops = extract_from_file(file_path)
        results[file_path] = extracted_loops
    return results

def print_extraction_results(results: dict):
    """Prints the extraction results in a formatted manner.
    
    Args:
        results (dict): A dictionary where keys are file paths and values are lists of extracted Loop objects.
    """
    for file_path, extracted_loops in results.items():
        print(f"File: {file_path}")
        print("-" * len(f"File: {file_path}"))
        for loop in extracted_loops:
            print(f"Loop ID: {loop.loop_id}")
            print(f"Status: {loop.status}")
            print(f"Start Line: {loop.start_line}")
            print(f"End Line: {loop.end_line}")
            print(f"Input Datasets: {', '.join(loop.input_datasets)}")
            print(f"Result Datasets: {', '.join(loop.result_datasets)}")
            print(f"Operations:")
            for op in loop.operations:
                print(f"  - Variables: {op.variables}, Operation: {op.operation_str}")
            
            # Print conditions, if any
            if loop.conditions:
                print(f"Conditions:")
                for var_name, cond in loop.conditions.items():
                    print(f"  - Variables: {var_name}, Condition: {cond}")
            print()
        print("=" * 50)
        print()



file_paths = ["simple_loop.py","loop_with_conditions.py","mutliple_loop.py","nested_loop.py"]
print_extraction_results(test_extraction_from_file([file_paths[1]]))
