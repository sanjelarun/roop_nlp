class Loop:
    """Represents a loop structure extracted from Python code."""

    def __init__(self, loop_id, original_code, start_line, end_line):
        """Initializes the Loop object with the given attributes."""
        self.loop_id = loop_id
        self.original_code = original_code
        self.start_line = start_line
        self.end_line = end_line
        
        self.input_datasets = []  # Datasets read in the loop
        self.result_datasets = []  # Datasets written to in the loop
        self.operations = []  # List of Operation objects inside the loop
        self.refactored_code = None  # Refactored PySpark code
        
        self.oracle_prediction = None  # Prediction from Oracle NLP
        self.loop_iterator = None  # Iterator used in the loop (e.g., 'i' in 'for i in data:')
        self.conditions = []  # List of conditions (Operation objects) inside the loop
        
        self.parent_loop = None  # If this is a nested loop, pointer to the parent loop
        self.child_loops = []  # If this loop contains nested loops
        
        self.is_nested = False  # Indicates if this is a nested loop
        self.has_condition = False  # Indicates if the loop has an internal condition
        
        self.status = "Extracted"

    def update_refactored_code(self, refactored_code):
        """Updates the refactored code of the loop and sets its status to "Converted".
        
        Args:
            refactored_code (str): The PySpark equivalent of the original loop code.
            
        """
        self.refactored_code = refactored_code
        self.status = "Converted"
    
    def update_status(self, new_status):
        """Updates the status of the loop.
        
        Args:
            new_status (str): The new status to set for the loop.
            
        """
        self.status = new_status
        
    def __repr__(self):
        """Returns a string representation of the Loop object."""
        return f"Loop(ID={self.loop_id}, Status={self.status}, StartLine={self.start_line}, EndLine={self.end_line})"

# Representation of Loop class
Loop
