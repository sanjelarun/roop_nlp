import ast
from data_models.loop import Loop


def extract_operations(node, code):
    """Extracts operations (expressions/assignments) from a given AST node."""
    operations = []
    
    # Extracting assignment operations
    for n in ast.walk(node):
        if isinstance(n, ast.Assign):
            for target in n.targets:
                left = ast.get_source_segment(code, target)
                right = ast.get_source_segment(code, n.value)
                if left and right:
                    op_code = left + " = " + right
                    operations.append(op_code)
                
        # Extracting augmented assignments (e.g., a += 1)
        elif isinstance(n, ast.AugAssign):
            target = n.target
            op = ast.get_source_segment(code, n.op)
            value = ast.get_source_segment(code, n.value)
            if target and op and value:
                op_code = target + " " + op + " " + value
                operations.append(op_code)

        # Extracting function calls (e.g., append)
        elif isinstance(n, ast.Call):
            func_call = ast.get_source_segment(code, n)
            if func_call:
                operations.append(func_call)
        
        # Extracting arithmetic operations
        elif isinstance(n, ast.BinOp):
            left = ast.get_source_segment(code, n.left)
            right = ast.get_source_segment(code, n.right)
            op = ast.get_source_segment(code, n.op)
            if left and right and op:
                op_code = left + " " + op + " " + right
                operations.append(op_code)

    return operations

def extract_input_datasets(node):
    """Extracts the dataset being iterated over in a for loop, including nested loops, from the given AST node."""
    input_datasets = []
    
    if isinstance(node.iter, ast.Name):
        input_datasets.append(node.iter.id)
    
    # Checking for nested loops
    for inner_node in ast.walk(node):
        if isinstance(inner_node, ast.For) and inner_node is not node:
            input_datasets.extend(extract_input_datasets(inner_node))
            
    return input_datasets






def extract_result_datasets(node):
    """Extracts result datasets from the given AST node.
    
    This function identifies datasets (list variables) that are being written to 
    within the provided AST node. This typically includes lists that have methods 
    like 'append' or 'extend' called on them.
    
    Args:
        node (ast.Node): The AST node to inspect.
        
    Returns:
        list: A list of result dataset names identified within the node.
    """
    
    result_datasets = set()
    
    # Identify all list variables that are being written to (e.g., using append or extend)
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ['append', 'extend']:
            if isinstance(n.func.value, ast.Name):
                result_datasets.add(n.func.value.id)
                
    return list(result_datasets)

def extract_conditions(node, code):
    """Extracts conditions (if statements) from a given AST node."""
    conditions = []
    
    for n in ast.walk(node):
        if isinstance(n, ast.If):
            condition_code = ast.get_source_segment(code, n.test)
            if condition_code:
                conditions.append(condition_code)
                
    return conditions

def extract_loops_from_code_v4(code: str):
    loops = []
    parsed_code = ast.parse(code)
    
    class LoopVisitor(ast.NodeVisitor):
        def visit_For(self, node):
            loop_code = ast.get_source_segment(code, node)
            start_line = node.lineno
            end_line = node.lineno + len(loop_code.splitlines()) - 1
            
            result_datasets = extract_result_datasets(node)
            input_datasets = extract_input_datasets(node)
            operations = extract_operations(node, code)
            conditions = extract_conditions(node, code)
            
            loop_obj = Loop(loop_id=len(loops)+1, 
                            original_code=loop_code, 
                            start_line=start_line, 
                            end_line=end_line)
            
            # Checking for nested loops and conditions
            for inner_node in node.body:
                if isinstance(inner_node, ast.For):
                    loop_obj.is_nested = True
            
            loop_obj.input_datasets = input_datasets
            loop_obj.result_datasets = result_datasets
            loop_obj.operations = operations
            loop_obj.conditions = conditions  # Storing extracted conditions in Loop object
            loops.append(loop_obj)
            
            # This line allows us to handle nested loops
            self.generic_visit(node)
    
    visitor = LoopVisitor()
    visitor.visit(parsed_code)
    
    return loops




def extract_from_file(file_path: str):
    """Extracts for loops from a given Python file and returns a list of Loop objects.
    
    Args:
        file_path (str): The path to the Python file to inspect and extract loops from.
        
    Returns:
        list: A list of Loop objects representing each extracted loop.
    """
    with open(file_path, 'r') as file:
        code_content = file.read()
    
    return extract_loops_from_code_v4(code_content)