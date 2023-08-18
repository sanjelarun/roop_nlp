class Loop:
    """Represents a loop structure extracted from Python code.
    
    Attributes:
        loop_id (int): A unique identifier for the loop.
        original_code (str): The original code snippet of the loop.
        start_line (int): The starting line number of the loop in the source code.
        end_line (int): The ending line number of the loop in the source code.
        datasets_used (list): A list of dataset names used within the loop.
        refactored_code (str): The refactored code (PySpark equivalent).
        status (str): The status of the loop.
        
    """
    
    def __init__(self, loop_id, original_code, start_line, end_line, datasets_used):
        """Initializes the Loop object with the given attributes."""
        self.loop_id = loop_id
        self.original_code = original_code
        self.start_line = start_line
        self.end_line = end_line
        self.datasets_used = datasets_used
        self.refactored_code = None
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
