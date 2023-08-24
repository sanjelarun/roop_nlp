def map_operation(dataset, operation, result_dataset):
    return f"{result_dataset} = {dataset}.map(lambda {operation.variables[0]}: {operation.operation_str}).collect()"

def filter_operation(dataset, condition, result_dataset):
    return f"{result_dataset} = {dataset}.filter(lambda {condition.split()[0]}: {condition}).collect()"

def reduce_operation(dataset, operation):
    return f"{operation.variables[0]} = {dataset}.reduce(lambda {operation.variables[0]}, {operation.variables[1]}: {operation.operation_str})"

def join_operation(dataset, secondary_dataset, result_dataset):
    if result_dataset:
        return f"{result_dataset} = {dataset}.join({secondary_dataset}).collect()"
    return f"{dataset} = {dataset}.join({secondary_dataset})"

def union_operation(dataset, secondary_dataset, result_dataset=""):
    if result_dataset:
        return f"{result_dataset} = {dataset}.union({secondary_dataset})"
    return f"{dataset} = {dataset}.union({secondary_dataset}_rdd)"
def flatmap_operation(dataset, operation):
    return f"{dataset}.flatMap(lambda {operation.variables[0]}: {operation.operation_str})"

def sum_operation(dataset):
    return f"{dataset}.sum()"

def count_operation(dataset):
    return f"{dataset}.count()"


def refactor_loop(loop, predictions):
    """Refactor the given loop based on the predictions from ORACLE NLP."""
    
    if not loop.input_datasets:
        # If there are no input datasets, then we can't refactor the loop.
        return None

    primary_dataset = loop.input_datasets[0] + "_rdd"
    refactored_code = None
    for prediction in predictions:
        if prediction == "map()" and loop.operations:
            operation = loop.operations[0]
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code = map_operation(primary_dataset, operation, result_dataset)

        elif prediction == "filter()" and loop.conditions:
            condition = next(iter(loop.conditions.values()))
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code = filter_operation(primary_dataset, condition, result_dataset)

        elif prediction == "reduce()" and loop.operations:
            operation = loop.operations[0]
            refactored_code = reduce_operation(primary_dataset, operation)

        elif prediction == "join()" and len(loop.input_datasets) >= 2:
            secondary_dataset = loop.input_datasets[1] + "_rdd"
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code = join_operation(primary_dataset, secondary_dataset, result_dataset)

        elif prediction == "union()" and len(loop.input_datasets) >= 2:
            secondary_dataset = loop.input_datasets[1] + "_rdd"
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code = union_operation(refactored_code, secondary_dataset, result_dataset)

        elif prediction == "flatMap()" and loop.operations:
            operation = loop.operations[0]
            refactored_code = flatmap_operation(refactored_code, operation)

        elif prediction == "sum()":
            refactored_code = sum_operation(refactored_code)

        elif prediction == "count()":
            refactored_code = count_operation(refactored_code)

    return refactored_code
