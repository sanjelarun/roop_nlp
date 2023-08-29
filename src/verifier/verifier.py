import os
import subprocess
import xml.etree.ElementTree as ET
from refactoring.refactor import refactor_loop

os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'
LOG_PATH = "src/verifier/logs/test.xml"
class Verifier:
    

    @staticmethod
    def run_pytest_isolated():
        result = subprocess.run(["pytest", "temp_code.py", "--junitxml", LOG_PATH, "-q", "--disable-warnings"])
        return result.returncode == 0

    @staticmethod
    def parse_test_xml(xml_file=LOG_PATH):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        failed_test_cases = []
        for rt in root[0]:
            test_case_name = rt.attrib['name']
            for child in rt:
                failure_message = child.attrib['message']
                failed_test_cases.append({'test_case_name': test_case_name, 'failure_message': failure_message})
        return failed_test_cases

    @staticmethod
    def get_test_code_content(test_file_path):
        with open(test_file_path, "r") as file:
            return "\n".join([line for line in file.read().splitlines()])

    @staticmethod
    def execute_code_and_write_to_file(combined_code):
        try:
            compiled_code = compile(combined_code, '<string>', 'exec')
            exec(compiled_code)
        except Exception as e:
            print(f"Error detected: {e}")
            return False
        
        with open("temp_code.py", "w") as temp_file:
            temp_file.write(combined_code)
        
        return True

    @staticmethod
    def verify_predictions_for_loop(original_code, loop, predictions, test_file_path, id):
        from generation.code_generator import generate_pyspark_code  # Import here to avoid circular dependencies

        test_code_content = Verifier.get_test_code_content(test_file_path)

        for prediction in predictions:
            refactored_code = refactor_loop(loop, prediction.split(","))
            if refactored_code is None:
                continue
            
            loop.refactored_code = refactored_code
            combined_code = generate_pyspark_code(original_code, [loop], id)  # Pass only the current loop
            id += 1

            combined_code += "\nimport pytest\n" + "\n\n" + test_code_content

            if not Verifier.execute_code_and_write_to_file(combined_code):
                continue

            if Verifier.run_pytest_isolated():
                return loop.refactored_code, id

        return None, id  # If no prediction was correct
