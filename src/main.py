import os,sys
from extraction.extractors import extract_loops_from_code_v4
from generation.code_generator import generate_pyspark_code
from nlp.prediction import Top5Predictions
import traceback
from verifier.verifier import Verifier
import argparse
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
        skip_next = False
                #  Step 2: Refactor the code using predictions and verify them using the test file
        id = 0
        num_loops = len(extracted_loops)
       
        for loop in extracted_loops:
            # If skip_next is True, reset it and skip this iteration
            if skip_next:
                skip_next = False
                continue
           
            predictions = top5.make_prediction(loop.original_code)
            correct_prediction,id = Verifier.verify_predictions_for_loop(python_code, loop, predictions, test_file_path, id)
            num_api_calls = id
            if correct_prediction:
                loop.refactored_code = correct_prediction

            else:
                print(f"No correct prediction found for loop {loop.loop_id}")
            # If the current loop's is_nested flag is set, mark skip_next as True
            if loop.is_nested:  # Assuming the flag is named `is_nested`
                skip_next = True

        # Step 3: Generate PySpark code
        pyspark_code = generate_pyspark_code(python_code, extracted_loops)
        write_string_to_file(pyspark_code, out_file_path)
        return num_loops, num_api_calls
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())


# if __name__ == "__main__":
#     input_dir = "src\examples\simple_operations"
#     output_dir = "src\output"
#     file_path = "multiple_loop.py"
#     test_file_path = os.path.join(input_dir, "test_"+file_path)
#     out_file_path = os.path.join(output_dir, file_path[:-3] +"_pyspark.py")
#     in_file_path = os.path.join(input_dir, file_path)
#     driver_program(in_file_path, out_file_path, test_file_path)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PySpark code from a Python program.")
    parser.add_argument('--input_dir', type=str, help='Input directory containing the Python file and its test.')
    parser.add_argument('--output_dir', type=str, help='Output directory for the generated PySpark code.')
    parser.add_argument('--file_name', type=str, help='Name of the Python file to process.')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    output_dir = args.output_dir
    file_name = args.file_name
    
    in_file_path = os.path.join(input_dir, file_name)
    test_file_path = os.path.join(input_dir, "test_" + file_name)
    out_file_path = os.path.join(output_dir, file_name[:-3] + "_pyspark.py")
    
    num_loops, num_api_calls = driver_program(in_file_path, out_file_path, test_file_path)
    
    print(f"Number of loops processed: {num_loops}")
    print(f"Number of API calls predicted: {num_api_calls}")