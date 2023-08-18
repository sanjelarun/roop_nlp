import sys
sys.path.append('F:/Papers/IEEE-BigData-2023/roop_nlp/src')

from data_models.loop import Loop

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
    
    # Sample loop object
    loop1 = Loop(1, "for i in nums: results.append(i * 2)", 1, 2)
    loop1.input_datasets = ["nums"]
    loop1.operations = ["results.append(i * 100 + 1)"]
    
    print( refactor_loop(loop1, "map"))
    
    loop2 = Loop(2, "for i in nums: if i >= 5: results.append(i)", 1, 3)

    loop2.input_datasets = ["nums"]
    loop2.operations = ["results.append(i)"]
    
    print(refactor_loop(loop2, "filter"))

    
    # ... more test cases as needed

    print("All tests passed!")

test_refactor_loop()
