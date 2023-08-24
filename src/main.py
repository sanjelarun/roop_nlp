import os
from extraction.extractors import extract_loops_from_code_v4
from generation.code_generator import generate_pyspark_code
from nlp.prediction import Top5Predictions
import traceback
from verifier.verifier import Verifier

def read_file_to_string(file_path: str) -> str:
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_string_to_file(content: str, file_path: str):
    with open(file_path, 'w') as file:
        file.write(content)

def print_extracted_loops(extracted_loops):
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

def driver_program(file_path, out_file_path, test_file_path):
    try:
        python_code = read_file_to_string(file_path)
        
        # Step 1: Extract loops from the Python file
        extracted_loops = extract_loops_from_code_v4(python_code)
        
        # Display extraction results
        print_extracted_loops(extracted_loops)
        
        # Initialize the BERT classifier to get predictions
        top5 = Top5Predictions()
        
        # Step 2: Refactor the code using predictions and verify them using the test file
        for loop in extracted_loops:
            predictions = top5.make_prediction(loop.original_code)
            print(predictions)
            correct_prediction = Verifier.verify_predictions_for_loop(python_code, loop, predictions, test_file_path)
            if correct_prediction:
                loop.refactored_code = correct_prediction
            else:
                print(f"No correct prediction found for loop {loop.loop_id}")
        
        # Step 3: Generate PySpark code
        pyspark_code = generate_pyspark_code(python_code, extracted_loops)
        write_string_to_file(pyspark_code, out_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    base_directory = "f:/Papers/IEEE-BigData-2023/roop_nlp/src/test/"
    file_path = "multiple_loop.py"
    test_file_path = os.path.join(base_directory, "test_multiple_loop.py")
    out_file_path = os.path.join(base_directory, "multiple_loop_pyspark.py")
    in_file_path = os.path.join(base_directory, file_path)
    driver_program(in_file_path, out_file_path, test_file_path)
