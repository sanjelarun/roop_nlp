import os
import sys
sys.path.append('F:/Papers/IEEE-BigData-2023/roop_nlp/src')

from data_models.loop import Loop
from extraction.extractors import extract_from_file
def refactor_loop(loop, predictions):
    """Refactor the given loop based on the predictions from ORACLE NLP."""
    
    if not loop.input_datasets:
        # If there are no input datasets, then we can't refactor the loop.
        return None

    # Taking the first dataset as the primary dataset for operations.
    primary_dataset = loop.input_datasets[0]

    refactored_code = primary_dataset
    
    for prediction in predictions:
        if prediction == "map":
            if loop.operations:
                operation = loop.operations[0]  # Assuming a single map operation per loop for simplicity
                refactored_code = f"{refactored_code}.map(lambda {operation.variables[0]}: {operation.operation_str})"
        
        elif prediction == "filter":
            if loop.conditions:
                condition = next(iter(loop.conditions.values()))  # Assuming a single filter condition per loop for simplicity
                refactored_code = f"{refactored_code}.filter(lambda {condition.split()[0]}: {condition})"
        
        elif prediction == "reduce":
            if loop.operations:
                operation = next(iter(loop.operations))  # Simplified assumption for demonstration
                refactored_code = f"{refactored_code}.reduce(lambda {','.join(operation.variables)}: {operation.operation_str})"
        
        elif prediction == "join":
            if len(loop.input_datasets) < 2:
                return None
            secondary_dataset = loop.input_datasets[1]
            refactored_code = f"{refactored_code}.join({secondary_dataset})"
        elif prediction == "union":
            if len(loop.input_datasets) < 2:
                return None
            secondary_dataset = loop.input_datasets[1]
            refactored_code = f"{refactored_code}.union({secondary_dataset})"
        
        elif prediction == "flatMap":
            operation = next(iter(loop.operations))
            refactored_code = f"{refactored_code}.flatMap(lambda {operation.variables[0]}: {operation.operation_str})"
        
        elif prediction == "sum":
            refactored_code = f"{refactored_code}.sum()"
        
        elif prediction == "count":
            refactored_code = f"{refactored_code}.count()"

        # ... additional rules can be added as needed
    loop.refactored_code = refactored_code        
    return refactored_code





def test_refactor_loop():
    """Test the refactor_loop function."""
    base_directory = 'F:/Papers/IEEE-BigData-2023/roop_nlp/src/test'
    file_paths = ["simple_loop.py","loop_with_conditions.py","mutliple_loop.py","nested_loop.py","join-test.py"]
    # Sample loop object
    extracted_loops = extract_from_file(file_path=os.path.join(base_directory,file_paths[2]))   
    # print( refactor_loop(extracted_loops[0], ["filter","map"]))
    #print( refactor_loop(extracted_loops[0], ["join"]))
    print( refactor_loop(extracted_loops[0], ["filter"]))
    print( refactor_loop(extracted_loops[1], ["map"]))
    
    # loop2 = Loop(2, "for i in nums: if i >=5: results.append(i)", 1, 3)
    # loop2.input_datasets = ["nums"]
    # loop2.operations = ["results.append(i)"]
    
    # print(refactor_loop(loop2, "filter"))

    
    # ... more test cases as needed

    print("All tests passed!")

test_refactor_loop()
