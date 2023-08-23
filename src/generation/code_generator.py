from typing import List
from data_models.loop import Loop

def generate_pyspark_code(python_code: str, extracted_loops: List[Loop]) -> str:
    """
    Generate PySpark code by replacing original loops with refactored code.
    """
    # Split the Python code into lines
    lines = python_code.split('\n')
    
    # PySpark initialization
    pyspark_initialization = [
        "from pyspark import SparkContext, SparkConf",
        "conf = SparkConf().setAppName('MyApp').setMaster('local')",
        "sc = SparkContext(conf=conf)",
        ""
    ]
    
    refactored_lines = pyspark_initialization.copy()

    # Create a mapping of loop starting line to the loop for quick look-up
    loop_mapping = {loop.start_line: loop for loop in extracted_loops}

    line_num = 0  # 0-indexed line number
    while line_num < len(lines):
        if line_num + 1 in loop_mapping:  # Python code is 1-indexed
            loop = loop_mapping[line_num + 1]
            
            # Add parallelization code for each input dataset
            for dataset in loop.input_datasets:
                refactored_lines.append(f"{dataset}_rdd = sc.parallelize({dataset})")

            # Add refactored code
            refactored_lines.append(loop.refactored_code)

            # Skip the lines corresponding to this loop
            line_num += (loop.end_line - loop.start_line + 1)
        else:
            # Regular line, just copy it to refactored_lines
            refactored_lines.append(lines[line_num])
            line_num += 1

    return '\n'.join(refactored_lines).strip()
