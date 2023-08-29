import pytest
import xml.etree.ElementTree as ET
from refactoring.refactor import refactor_loop

import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'

class Verifier:
    LOG_PATH = "verifier/logs/test.xml"

    @staticmethod
    def invoke_pytest(filepath):
        pytest.main([filepath, "--junitxml", Verifier.LOG_PATH])

    @staticmethod
    def parse_test_xml(xml_file=LOG_PATH):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        failed_test_cases = []
        for rt in root[0]:
            test_case_name = rt.attrib['name']
            for child in rt:
                failure_message = child.attrib['message']
                tmp = {'test_case_name': test_case_name, 'failure_message': failure_message}
                failed_test_cases.append(tmp)
        return failed_test_cases

    @staticmethod
    def extract_test_functions(test_file_path):
        """
        Extracts test functions from the given test file path.
        """
        with open(test_file_path, "r") as file:
            return file.read()

    @staticmethod
    def verify_predictions_for_loop(original_code, loop, predictions, test_file_path):
        from generation.code_generator import generate_pyspark_code  # Import here to avoid circular dependencies

        # Read the test code content and filter out all import lines
        with open(test_file_path, "r") as test_file:
            test_code_content = test_file.read()
        # Filter out all lines that start with "import"
        test_code_content = "\n".join([line for line in test_code_content.splitlines()])

        for prediction in predictions:
            prediction=prediction.split(",")
            # Replace the loop in the original code with the prediction
            refactored_code = refactor_loop(loop, prediction)
            if refactored_code is not None:
                print(refactored_code)
                loop.refactored_code = refactored_code
                combined_code = generate_pyspark_code(original_code, [loop])  # Pass only the current loop

                # Add required imports
                combined_code += "\nimport pytest\n"
                
                # Append test functions to combined code
                combined_code += "\n\n" + test_code_content
                try:
                    compiled_code = compile(combined_code, '<string>', 'exec')
                except Exception as e:
                    print(f"Compile-time error detected: {e}")
                    continue
                try:
                    exec(compiled_code)
                except Exception as e:
                    print(f"Runtime error detected: {e}")
                    continue  # Skip this loop iteration and move to the next prediction
        
                # Save the combined code to a temporary file
                with open("temp_code.py", "w") as temp_file:
                    temp_file.write(combined_code)

                # Run pytest on the combined code
                Verifier.invoke_pytest("temp_code.py")
                failures = Verifier.parse_test_xml()
                if not failures:
                    return loop.refactored_code  # Return the first correct prediction
        return None  # If no prediction was correct

