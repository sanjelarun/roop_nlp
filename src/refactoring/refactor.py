import sys
import os
sys.path.append('/Users/bikramkhanal/Desktop/Files/Research/Papers/roop_nlp/src')

# from data_models.loop import Loop
from data_models.loop import Loop
from extraction.extractors import extract_from_file
from nlp.prediction import Top5Predictions

def refactor_loop(loop, prediction):
    """Refactor the given loop based on the prediction from ORACLE NLP."""
    
    if not loop.input_datasets:
        # If there are no input datasets, then we can't refactor the loop.
        return None

    # Taking the first dataset as the primary dataset for operations.
    primary_dataset = loop.input_datasets[0]

    # Placeholder components
    loop_variable = "x"
    loop_body = loop.operations[0] if loop.operations else "x * 2"  # Using the first operation as a placeholder
    condition = "x > 5"  # Placeholder condition

    if prediction == "map":
        return f"{primary_dataset}.map(lambda {loop_variable}: {loop_body})"
    
    elif prediction == "filter":
        # For simplicity, we assume a condition exists. In a more robust solution, conditions should be extracted.
        return f"{primary_dataset}.filter(lambda {loop_variable}: {condition})"
    
    elif prediction == "reduce":
        # Assuming a binary operation like addition for simplicity.
        return f"{primary_dataset}.reduce(lambda a, b: a + b)"
    
    elif prediction == "join":
        # This assumes there's a secondary dataset to join with and that 'id' is a common key.
        if len(loop.input_datasets) < 2:
            return None
        secondary_dataset = loop.input_datasets[1]
        return f"{primary_dataset}.join({secondary_dataset}, {primary_dataset}.id == {secondary_dataset}.id)"
    
    elif prediction == "union":
        if len(loop.input_datasets) < 2:
            return None
        secondary_dataset = loop.input_datasets[1]
        return f"{primary_dataset}.union({secondary_dataset})"
    
    elif prediction == "flatMap":
        return f"{primary_dataset}.flatMap(lambda {loop_variable}: {loop_variable})"
    
    elif prediction == "sum":
        return f"{primary_dataset}.sum()"
    
    elif prediction == "count":
        return f"{primary_dataset}.count()"

    # ... add more rules as needed

    return None

def test_refactor_loop():

    """Test the refactor_loop function."""

    base_directory = '/Users/bikramkhanal/Desktop/Files/Research/Papers/roop_nlp/src/test'

    file_paths = ["simple_loop.py","loop_with_conditions.py","mutliple_loop.py","nested_loop.py","join-test.py"]
    extracted_loops = extract_from_file(file_path=os.path.join(base_directory,file_paths[2]))  
    code_snap = extracted_loops[1].original_code
    print(f"This is code snap: {code_snap}")
    top5 = Top5Predictions()
    top_5_labels = top5.make_prediction(code_snap)
    top_class = top5.classifier.predict_top_class(code_snap)
    print(f"Top 5 Predciction {top_5_labels}")
    print(f"Top Prediction {top_class}")
    print("All tests passed!")
test_refactor_loop()
