import ast
import astor
from data_models.loop import Loop
from data_models.operations import Operation
import keyword
import tokenize
import io,re
import builtins
from collections import OrderedDict


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

def adjust_operations(operations):
    """Adjust special method calls like str.lower() to use the correct variable."""
    for operation in operations:
        method_calls = re.findall(r'str\.(\w+)\(\)', operation.operation_str)
        for method in method_calls:
            variable = operation.variables[0]
            operation.operation_str = operation.operation_str.replace(f'str.{method}()', f"{variable}.{method}()")

def sort_operations_by_line_number(operations):
    operations.sort(key=lambda x: x.line_number)

def extract_operations(operation_nodes, code):
    """Extracts operations from a list of AST nodes."""
    operations_list = []

    for n in operation_nodes:
        line_number = n.lineno
        # Assignments (e.g., result = num * 5)
        if isinstance(n, ast.Assign):
            for target in n.targets:
                left_var = ast.get_source_segment(code, target).strip()
                right_op = ast.get_source_segment(code, n.value).strip()
                involved_vars_ordered_dict = OrderedDict.fromkeys([left_var] + extract_variables_from_node(n.value))
                involved_vars = list(involved_vars_ordered_dict.keys())
                operation = Operation(variables=involved_vars, operation_str=right_op, line_number=line_number)
                operations_list.append(operation)
        # Augmented assignments (e.g., a += 1)
        elif isinstance(n, ast.AugAssign):
            target_var = ast.get_source_segment(code, n.target).strip()
            right_op = ast.get_source_segment(code, n.value).strip()
            op_map = {
                ast.Add: '+',
                ast.Sub: '-',
                ast.Mult: '*',
                ast.Div: '/',
            }
            op_segment = op_map.get(type(n.op), None)
            if not op_segment:
                continue
            expanded_op = target_var + " " + op_segment + " " + right_op  # Expand to non-augmented form
            involved_vars_ordered_dict = OrderedDict.fromkeys([target_var] + extract_variables_from_node(n.value))
            involved_vars = list(involved_vars_ordered_dict.keys())
            operation = Operation(variables=involved_vars, operation_str=expanded_op, line_number=line_number)
            operations_list.append(operation)
        # Function calls (e.g., append, extend)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            # Check if the function is 'append' or 'extend'
            if n.func.attr in ["append", "extend"]:
                operation_inside_call = ast.get_source_segment(code, n.args[0]).strip()
                involved_vars = extract_variable_names_from_operation(operation_inside_call)
                operation = Operation(variables=involved_vars, operation_str=operation_inside_call,line_number=line_number)
                operations_list.append(operation)

    # Apply the adjustments for special method calls
    adjust_operations(operations_list)
    sort_operations_by_line_number(operations_list)
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
                conditions[var_name] = condition_code[1:-1]
                
    return conditions

def merge_loops(loop1, loop2):
    """Merge operations of two loops that operate on the same result dataset."""
    loop1.operations.extend(loop2.operations)
    loop1.end_line = loop2.end_line
    loop1.input_datasets.extend(loop2.input_datasets)
    sort_operations_by_line_number(loop1.operations)
    loop1.original_code += '\n' + loop2.original_code  # Combine the original code for reference
    return loop1

from collections import OrderedDict

def extract_loops_from_code_v4(code: str):
    loops = []
    parsed_code = ast.parse(code)
    
    dataset_to_loop_map = {}  # Variable to keep track of datasets and their loops
    dataset_to_code_map = {}  # Variable to keep track of datasets and additional lines of code
    
    class LoopVisitor(ast.NodeVisitor):
        def visit_For(self, node):
            loop_code = ast.get_source_segment(code, node)
            start_line = node.lineno
            end_line = node.lineno + len(loop_code.splitlines()) - 1
            
            result_datasets = extract_result_datasets(node)
            input_datasets = extract_input_datasets(node)
            
            operation_nodes = [n for n in ast.walk(node) if isinstance(n, (ast.Assign, ast.AugAssign, ast.Call))]
            
            operations = extract_operations(operation_nodes, code)
            conditions = extract_conditions_with_astor(node)
            
            loop_obj = Loop(loop_id=len(loops) + 1, 
                            original_code=loop_code, 
                            start_line=start_line, 
                            end_line=end_line)
            
            for inner_node in node.body:
                if isinstance(inner_node, ast.For):
                    loop_obj.is_nested = True
            
            loop_obj.input_datasets = input_datasets
            loop_obj.result_datasets = result_datasets
            loop_obj.operations = operations
            loop_obj.conditions = conditions
            
            merged = False
            for dataset in result_datasets:
                if dataset in dataset_to_loop_map:
                    previous_loop = dataset_to_loop_map[dataset]
                    merge_loops(previous_loop, loop_obj)
                    merged = True
                    break
            
            if not merged:
                loops.append(loop_obj)
                for dataset in result_datasets:
                    dataset_to_loop_map[dataset] = loop_obj
            
            self.generic_visit(node)
        
        def visit_Assign(self, node):
            self.update_dataset_to_code_map(node)
        
        def visit_AugAssign(self, node):
            self.update_dataset_to_code_map(node)
        
        def update_dataset_to_code_map(self, node):
            line = ast.get_source_segment(code, node).strip()
            line_number = node.lineno
            target = None
            if isinstance(node, ast.Assign):
                target = node.targets[0]
            elif isinstance(node, ast.AugAssign):
                target = node.target
            target_var = ast.get_source_segment(code, target).strip()
            if target_var in dataset_to_loop_map:
                loop = dataset_to_loop_map[target_var]
                loop.original_code += '\n' + line
                loop.end_line = line_number
    
    visitor = LoopVisitor()
    visitor.visit(parsed_code)
    
    return loops


