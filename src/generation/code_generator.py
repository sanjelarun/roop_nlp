from typing import List
from data_models.loop import Loop
from itertools import takewhile

def generate_pyspark_code(python_code: str, extracted_loops: List[Loop],contextID=0) -> str:
    """
    Generate PySpark code by replacing original loops with refactored code.
    """
    # Split the Python code into lines
    lines = python_code.split('\n')
    
    # PySpark initialization
    pyspark_initialization = [
        "sc = get_or_create_spark_context()",
    ]
    
    refactored_lines = [
        "from pyspark import SparkContext, SparkConf",
        "",
        "def get_or_create_spark_context():",
        "    conf = SparkConf().setAppName('App"+str(contextID)+"').setMaster('local[2]')",
        "    return SparkContext.getOrCreate(conf)",
        ""
    ]

    # Create a mapping of loop starting line to the loop for quick look-up
    loop_mapping = {loop.start_line: loop for loop in extracted_loops}

    line_num = 0  # 0-indexed line number
    while line_num < len(lines):
        if line_num + 1 in loop_mapping:  # Python code is 1-indexed
            loop = loop_mapping[line_num + 1]

            # Extract indentation from the loop's starting line
            indentation = "".join(takewhile(str.isspace, lines[line_num]))

            # Insert PySpark initialization with correct indentation
            for init_line in pyspark_initialization:
                refactored_lines.append(indentation + init_line)

            # Add parallelization code for each input dataset with correct indentation
            skip = False
            for dataset in loop.input_datasets:
                if not skip:
                    refactored_lines.append(indentation + f"{dataset}_rdd = sc.parallelize({dataset})")
                if "flatMap(" in loop.refactored_code:
                    skip = True 
            # Add refactored code with correct indentation
            refactored_code_lines = loop.refactored_code.split('\n')
            for code_line in refactored_code_lines:
                refactored_lines.append(indentation + code_line)

            # Clear the cache and then stop the Spark context
            
            refactored_lines.append(indentation + "sc.stop()")

            # Skip the lines corresponding to this loop
            line_num += (loop.end_line - loop.start_line + 1)
        else:
            # Regular line, just copy it to refactored_lines
            refactored_lines.append(lines[line_num])
            line_num += 1

    return '\n'.join(refactored_lines).strip()
