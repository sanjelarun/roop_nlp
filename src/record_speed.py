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

from statistics import mean, stdev

def run_experiment(num_runs=10):
    all_results = []
    
    for run_num in range(1, num_runs + 1):
        print(f"=== Running experiment {run_num} ===")
        single_run_results = traverse_and_run_main_with_error_handling(base_path, main_py_path)
        
        for result in single_run_results:
            result['run_num'] = run_num
        
        all_results.extend(single_run_results)
    
    # Group results by Python file
    grouped_results = {}
    for result in all_results:
        key = (result['folder'], result['python_file'])
        if key not in grouped_results:
            grouped_results[key] = []
        grouped_results[key].append(result['elapsed_time'])
    
    # Calculate min, max, avg, and stdev for each Python file
    summary_results = []
    for (folder, python_file), times in grouped_results.items():
        summary_results.append({
            'folder': folder,
            'python_file': python_file,
            'min_time': min(times),
            'avg_time': mean(times),
            'max_time': max(times),
            'stdev_time': stdev(times) if len(times) > 1 else 0,  # Standard deviation is zero if there's only one value
            'all_times': times
        })
    
    # Print summary
    for summary in summary_results:
        print(f"Folder: {summary['folder']}, Python File: {summary['python_file']}, Min Time: {summary['min_time']}s, Avg Time: {summary['avg_time']}s, Max Time: {summary['max_time']}s, Std Dev: {summary['stdev_time']}s, All Times: {summary['all_times']}")

# For demonstration, using placeholders for paths
base_path = 'src\examples'  # Replace with actual path to the 'examples' directory
main_py_path = 'src\main.py'  # Replace with actual path to the modified main.py

# Run the experiment
run_experiment(num_runs=10)

