class Dataset:
    """Represents a dataset structure identified from Python code.
    
    Attributes:
        name (str): Name of the dataset (variable name).
        data_type (str): Type of the dataset (e.g., list, dict).
        original_data (list/dict/str/...): The actual data values.
        transformed_data (list/dict/str/...): Transformed data for use with PySpark.
        parallelized (bool): Boolean flag to indicate if data has been parallelized for PySpark.
        
    """
    
    def __init__(self, name, data_type, original_data):
        """Initializes the Dataset object with the given attributes."""
        self.name = name
        self.data_type = data_type
        self.original_data = original_data
        self.transformed_data = None
        self.parallelized = False
    
    def parallelize_data(self, transformed_data):
        """Updates the transformed data of the dataset and sets its parallelized status to True.
        
        Args:
            transformed_data (list/dict/str/...): The PySpark compatible version of the original data.
            
        """
        self.transformed_data = transformed_data
        self.parallelized = True
        
    def __repr__(self):
        """Returns a string representation of the Dataset object."""
        return f"Dataset(Name={self.name}, Type={self.data_type}, Parallelized={self.parallelized})"
