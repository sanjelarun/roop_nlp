import ast
import astor
from data_models.loop import Loop
from data_models.operations import Operation
import keyword
import tokenize
import io
import builtins

def extract_variables_from_node(node):
    """Recursively retrieve variable names from an AST node."""
    if isinstance(node, ast.Name):
        return [node.id]
    elif isinstance(node, (ast.BinOp, ast.BoolOp)):
        return extract_variables_from_node(node.left) + extract_variables_from_node(node.right)
    elif isinstance(node, ast.UnaryOp):
        return extract_variables_from_node(node.operand)
    elif isinstance(node, ast.Call):
        args_vars = [extract_variables_from_node(arg) for arg in node.args]
        return sum(args_vars, [])
    else:
        return []







def extract_variable_names_from_operation(op_str):
    """Extract variable names from a given operation string."""
    tokens = tokenize.tokenize(io.BytesIO(op_str.encode('utf-8')).readline)
    return [
        token.string for token in tokens 
        if token.type == tokenize.NAME 
        and not keyword.iskeyword(token.string) 
        and token.string not in dir(builtins)
    ]
def extract_operations(operation_nodes, code):
    """Extracts operations from a list of AST nodes."""
    operations_list = []

    for n in operation_nodes:
        # Assignments (e.g., result = num * 5)
        if isinstance(n, ast.Assign):
            for target in n.targets:
                left_var = ast.get_source_segment(code, target).strip()
                right_op = ast.get_source_segment(code, n.value).strip()
                involved_vars = set([left_var] + extract_variables_from_node(n.value))
                operation = Operation(variables=involved_vars, operation_str=right_op)
                operations_list.append(operation)
        # Augmented assignments (e.g., a += 1)
# Augmented assignments (e.g., a += 1)
        elif isinstance(n, ast.AugAssign):
            print("Found AugAssign")  # Debug print
            target_var = ast.get_source_segment(code, n.target).strip()
            right_op = ast.get_source_segment(code, n.value).strip()
            
            # Get the operator directly from the AugAssign node
            op_map = {
                ast.Add: '+',
                ast.Sub: '-',
                ast.Mult: '*',
                ast.Div: '/',
                # ... add other operators as needed
            }
            op_segment = op_map.get(type(n.op), None)
            if not op_segment:
                print(f"Unsupported operator: {type(n.op)}")  # Debug print
                continue
            
            expanded_op = target_var + " " + op_segment + " " + right_op  # Expand to non-augmented form
            involved_vars = set([target_var] + extract_variables_from_node(n.value))
            operation = Operation(variables=involved_vars, operation_str=expanded_op)
            operations_list.append(operation)


        # Function calls (e.g., append, extend)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            # Check if the function is 'append' or 'extend'
            if n.func.attr in ["append", "extend"]:
                operation_inside_call = ast.get_source_segment(code, n.args[0]).strip()
                involved_vars = extract_variable_names_from_operation(operation_inside_call)
                operation = Operation(variables=involved_vars, operation_str=operation_inside_call)
                operations_list.append(operation)


    return operations_list




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



def extract_conditions_with_astor(node):
    """Extracts conditions (if statements) from a given AST node using astor."""
    conditions = {}
   
    for n in ast.walk(node):
        if isinstance(n, ast.If):
            condition_code = astor.to_source(n.test).strip()
            # Assuming the condition involves a variable (e.g., num % 2 == 0)
            if " " in condition_code:
                var_name = condition_code.split(" ")[0][1:]
                print(var_name)
                conditions[var_name] = condition_code
                
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
            
            # Filtering nodes of interest for operation extraction
            operation_nodes = [n for n in ast.walk(node) if isinstance(n, (ast.Assign, ast.AugAssign, ast.Call))]
            
            operations = extract_operations(operation_nodes, code)
            conditions = extract_conditions_with_astor(node)
            
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