import os
import subprocess
import time

def traverse_and_run_main_with_error_handling(base_path, main_py_path):
    results = []
    
    for subdir, _, _ in os.walk(base_path):
        folder_name = os.path.basename(subdir)
        python_files = [f for f in os.listdir(subdir) if f.endswith('.py') and not f.startswith('test_')]
        test_files = [f for f in os.listdir(subdir) if f.startswith('test_')]
        
        for py_file in python_files:
            test_file = f'test_{py_file}'
            if test_file in test_files:
                print(f"Processing {py_file} in folder {folder_name}...")
                input_dir = subdir
                output_dir = os.path.join(subdir, 'output')
                os.makedirs(output_dir, exist_ok=True)
                
                cmd = [
                        'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe',  # Replace with your virtual environment's Python path
                        main_py_path, 
                        '--input_dir', input_dir, 
                        '--output_dir', output_dir, 
                        '--file_name', py_file
                    ]
                                    
                start_time = time.time()
                proc = subprocess.run(cmd, capture_output=True, text=True)
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                print(f"Finished processing {py_file}. Time taken: {elapsed_time} seconds.")
                # Check for errors in main.py
                if proc.returncode != 0:
                    error_message = proc.stderr
                    print(f"An error occurred while running main.py for {py_file} in folder {folder_name}: {error_message}")
                    continue  # Skip to the next file
                
                output_lines = proc.stdout.split('\n')
                num_loops_line = [line for line in output_lines if "Number of loops processed:" in line]
                num_api_calls_line = [line for line in output_lines if "Number of API calls predicted:" in line]
                
                num_loops = int(num_loops_line[0].split(':')[-1].strip()) if num_loops_line else None
                num_api_calls = int(num_api_calls_line[0].split(':')[-1].strip()) if num_api_calls_line else None
                
                results.append({
                    'folder': folder_name,
                    'python_file': py_file,
                    'elapsed_time': elapsed_time,
                    'num_loops': num_loops,
                    'num_api_calls': num_api_calls,
                    'error': None  # No error
                })
                
    return results

# For demonstration, using placeholders for paths
base_path = 'src\examples'  # Replace with actual path to the 'examples' directory
main_py_path = 'src\main.py'  # Replace with actual path to the modified main.py

# Run the function and print the results
results_with_error_handling = traverse_and_run_main_with_error_handling(base_path, main_py_path)
for result in results_with_error_handling:
    print(f"Folder: {result['folder']}, Python File: {result['python_file']}, Time: {result['elapsed_time']}s, Loops: {result['num_loops']}, API Calls: {result['num_api_calls']}, Error: {result['error']}")
