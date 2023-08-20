class Operation:
    """Represents an operation extracted from Python code."""
    
    def __init__(self, variables, operation_str, operation_type=""):
        """Initializes the Operation object with the given attributes."""
        self.variables = variables          # List of variables involved in the operation.
        self.operation_str = operation_str  # String representation of the operation.
        self.operation_type = operation_type  # Type of the operation (e.g., 'assignment', 'arithmetic').
        
    def __repr__(self):
        """Returns a string representation of the Operation object."""
        return f"Operation(Type={self.operation_type}, Variables={self.variables}, OperationStr={self.operation_str})"
