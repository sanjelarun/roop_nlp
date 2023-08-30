def map_operation(dataset, operation, result_dataset):
    return f"{result_dataset} = {dataset}.map(lambda {operation.variables[0]}: {operation.operation_str})"

def filter_operation(dataset, condition, result_dataset):
    return f"{result_dataset} = {dataset}.filter(lambda {condition.split()[0]}: {condition})"

def reduce_operation(dataset, operation):
    return f"{operation.variables[0]} = {dataset}.reduce(lambda {operation.variables[0]}, {operation.variables[1]}: {operation.operation_str})"

def join_operation(dataset, secondary_dataset, result_dataset):
    if result_dataset:
        return f"{result_dataset} = {dataset}.join({secondary_dataset})"
    return f"{dataset} = {dataset}.join({secondary_dataset})"

def union_operation(dataset, secondary_dataset, result_dataset=""):
    if result_dataset:
        return f"{result_dataset} = {dataset}.union({secondary_dataset})"
    return f"{dataset} = {dataset}.union({secondary_dataset}_rdd)"

def flatmap_operation(dataset, result_dataset):
    if result_dataset:
        return f"{result_dataset} = {dataset}.flatMap(lambda x: x)"
    return f"{dataset} = {dataset}.flatMap(lambda x: x)"

def sum_operation(dataset,operation):
    return f"{operation.variables[0]} = {dataset}.sum()"

def count_operation(dataset,operation,last_prediction):
    if last_prediction =="union()":
        return f"{dataset} ={dataset}.count()"
    return f"{operation.variables[0]} ={dataset}.count()"

def distinct_operation(refactored_code):
    return refactored_code +".distinct()"

def refactor_loop(loop, predictions):
    """Refactor the given loop based on the predictions from ORACLE NLP."""
    
    if not loop.input_datasets:
        # If there are no input datasets, then we can't refactor the loop.
        return None

    primary_dataset = loop.input_datasets[0] + "_rdd"
    refactored_code = ""
    cnt  = 0
    last_prediction = ""
    for prediction in predictions:
        prediction = prediction.strip()
        if prediction == "map()" and loop.operations:
            if cnt > len(loop.operations)-1:
                continue
            operation = loop.operations[cnt]
            result_dataset = loop.result_datasets[0] if loop.result_datasets else primary_dataset
            refactored_code += "\n"+ map_operation(primary_dataset, operation, result_dataset)
            primary_dataset = result_dataset
            cnt += 1
            last_prediction = "map()"

        elif prediction == "filter()" and loop.conditions:
            condition = next(iter(loop.conditions.values()))
            if last_prediction in {"flatMap()", "union()", "join()"}:
                refactored_code +=  f".filter(lambda {condition.split()[0]}: {condition})"
            elif last_prediction is ""  and len(loop.operations)>1:
                result_dataset = loop.operations[1].variables[0]
                refactored_code += "\n"+filter_operation(primary_dataset, condition, result_dataset)
                primary_dataset = result_dataset
            else:
                result_dataset = loop.result_datasets[0] if loop.result_datasets else primary_dataset
                refactored_code += "\n"+filter_operation(primary_dataset, condition, result_dataset)
                primary_dataset = result_dataset
            cnt += 1
            last_prediction = "filter()"


        elif prediction == "reduce()" and loop.operations:
            if cnt > len(loop.operations)-1:
                continue
            operation = loop.operations[cnt]
            if len(operation.variables) > 1:
                refactored_code += "\n"+ (reduce_operation(primary_dataset, operation))
                cnt += 1
                last_prediction = "reduce()"

        elif prediction == "join()" and len(loop.input_datasets) >= 2:
            secondary_dataset = loop.input_datasets[1] + "_rdd"
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code += "\n"+ join_operation(primary_dataset, secondary_dataset, result_dataset)
            primary_dataset = result_dataset
            cnt += 1
            last_prediction="join()"

        elif prediction == "union()" and len(loop.input_datasets) >= 2:
            secondary_dataset = loop.input_datasets[1] + "_rdd"
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code +=  "\n"+ union_operation(primary_dataset, secondary_dataset, result_dataset)
            primary_dataset = result_dataset
            last_prediction = "union()"

        elif prediction == "flatMap()":
            result_dataset = loop.result_datasets[0] if loop.result_datasets else None
            refactored_code += "\n"+flatmap_operation(primary_dataset, result_dataset)
            last_prediction = "flatMap()"
        
        elif prediction == "sum()":
            if cnt > len(loop.operations)-1:
                continue
            refactored_code += '\n'+sum_operation(primary_dataset, loop.operations[cnt])
            cnt += 1
            last_prediction= "sum()"

        elif prediction == "count()":
            refactored_code += ".count()"
            # if cnt > len(loop.operations)-1:
            #     continue
            # refactored_code += '\n'+count_operation(primary_dataset, loop.operations[cnt],last_prediction)
            # cnt += 1
            # last_prediction = "count()"
            last_prediction = "count()"

        elif prediction == "distinct()":
            refactored_code += ".distinct()"
            last_prediction = "distinct()"

        elif prediction == "sortBy()":
            refactored_code += ".sortBy(lambda x: x)"
            last_prediction = "sortBy()"
    
    # Check last prediction and append .collect() if necessary
    if last_prediction in {"map()", "filter()", "join()", "union()", "flatMap()","distict()","sortBy()"}:
        refactored_code += ".collect()"

    return refactored_code
