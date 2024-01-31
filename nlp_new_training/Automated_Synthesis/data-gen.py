
import re
import pandas as pd
import scipy.stats as stats
from nltk.corpus import wordnet
import random
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download('wordnet')
random.seed(42)

python_keywords_extended = ['in', 'for', 'if', 'append', 'map', 'reduce', 'filter', 'float', 'string', 'upper', 'none', 'is',
                            'Python', 'abs', 'and', 'char', 'concat', 'dict', 'endswith', 'enumerate', 'extend', 'file',
                            'exclude', 'func', 'get',
                            'hasattr', 'inf', 'int', 'isActive', 'isReady', 'isValid', 'isalpha', 'isdigit', 'isinstance',
                            'islower', 'isnumeric', 'iterable', 'len', 'list', 'lower', 'max', 'min', 'nfor', 'not'
                            ,'sorted','keys',
                            'or', 'py', 'range', 'replace', 'round', 'set', 'split', 'startswith', 'str', 'strip', 'sum', 't',
                            'taccum', 'tarr', 'tarray', 'tcombined', 'tconcat', 'tcubed', 'tdata', 'telementues', 'tif',
                            'tintermediate', 'tlist','n','t','tfor',
                            'tif','nfor','nif'
                            'type',
                            'union', 'update', 'None', 'MyClass', 'counter', 'date']

def extract_variables(code):
    return re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)

def generate_new_var_name(visited_vars, curr_var):
    idx = 1
    while curr_var + str(idx) in visited_vars:
        idx += 1
    return curr_var + str(idx)

def replace_var_names_consistent(code, var_mapping):
    for var_name, new_var_name in var_mapping.items():
        code = re.sub(r'\b' + re.escape(var_name) + r'\b', new_var_name, code)
    return code

def bfs_variable_replacement_v3(code, num_data):
    # Extract all variables from the code
    all_vars = extract_variables(code)

    # If a variable appears more than once, it's a candidate for renaming
    var_counts = {var: all_vars.count(var) for var in all_vars}
    vars_to_replace = [var for var, count in var_counts.items() if count > 1]

    # Start BFS renaming
    visited_vars = set()
    queue = []
    for var in vars_to_replace:
        if var not in visited_vars:
            visited_vars.add(var)
            queue.append(var)
    
    var_mapping = {}
    while queue:
        curr_var = queue.pop(0)
        if curr_var in python_keywords_extended:
            continue
        synonyms = wordnet.synsets(curr_var)
        synonyms = [lemma.name() for syn in synonyms for lemma in syn.lemmas() if lemma.name().isalpha()]
        synonyms = list(set(synonyms) - set(python_keywords_extended))
        
        # Generate names by appending numbers 1-10 to the original variable name
        if num_data<10000:
            generated_var_names = [curr_var + str(i) for i in range(1, 11)]
        else:
            generated_var_names = [curr_var + str(i) for i in range(1, 31)]
        
        # Combine the two lists: synonyms from WordNet and generated variable names
        all_possible_var_names = synonyms + generated_var_names
        
        # Randomly select a new name from the combined list
        new_var_name = random.choice(all_possible_var_names)
        
        var_mapping[curr_var] = new_var_name
        visited_vars.add(new_var_name)

        # Enqueue variables that haven't been visited yet
        for var in vars_to_replace:
            if var not in visited_vars:
                visited_vars.add(var)
                queue.append(var)

    return replace_var_names_consistent(code, var_mapping)

def desired_counts_distribution(num_data):
    mean = 2.5
    std_dev = 1
    x = list(range(1, 6))
    y = stats.norm(mean, std_dev).pdf(x)
    normalized_y = [int(val * num_data / sum(y)) for val in y]
    return dict(zip(x, normalized_y))

def generate_statistics1(augmented_df):
    # 1. Basic Dataset Statistics
    total_snippets = len(augmented_df)
    snippet_lengths = augmented_df['code'].str.len()
    avg_snippet_length = snippet_lengths.mean()
    min_snippet_length = snippet_lengths.min()
    max_snippet_length = snippet_lengths.max()
    avg_api_calls = augmented_df['api_calls'].apply(len).mean()
    
    print(f"Total number of code snippets: {total_snippets}")
    print(f"Average code snippet length: {avg_snippet_length:.2f}")
    print(f"Minimum code snippet length: {min_snippet_length}")
    print(f"Maximum code snippet length: {max_snippet_length}")
    print(f"Average number of API calls per code snippet: {avg_api_calls:.2f}")
    
    
    # 3. Variable Naming Statistics - We already have BFS and WordNet replacement. 
    # For demonstration purposes, I'll show the total unique variables after augmentation.
    all_vars = augmented_df['code'].apply(extract_variables).explode().unique()
    print(f"Total unique variable names after augmentation: {len(all_vars)}")
    
    # 4. Code Structure Statistics - For simplicity, let's count the control structures
    control_structures = ['for', 'if', 'while', 'else', 'elif']
    control_counts = {struct: augmented_df['code'].str.count(struct).sum() for struct in control_structures}
    print(f"Control Structures Counts: {control_counts}")

def generate_statistics(augmented_df):
    # 1. Basic Dataset Statistics
    total_snippets = len(augmented_df)
    snippet_lengths = augmented_df['augmented_code'].str.len()
    avg_snippet_length = snippet_lengths.mean()
    min_snippet_length = snippet_lengths.min()
    max_snippet_length = snippet_lengths.max()
    avg_api_calls = augmented_df['api_calls'].apply(len).mean()
    
    print(f"Total number of code snippets: {total_snippets}")
    print(f"Average code snippet length: {avg_snippet_length:.2f}")
    print(f"Minimum code snippet length: {min_snippet_length}")
    print(f"Maximum code snippet length: {max_snippet_length}")
    print(f"Average number of API calls per code snippet: {avg_api_calls:.2f}")

    all_vars = augmented_df['augmented_code'].apply(extract_variables).explode().unique()
    print(f"Total unique variable names after augmentation: {len(all_vars)}")
    
    # 4. Code Structure Statistics - For simplicity, let's count the control structures
    control_structures = ['for', 'if', 'while', 'else', 'elif']
    control_counts = {struct: augmented_df['augmented_code'].str.count(struct).sum() for struct in control_structures}
    print(f"Control Structures Counts: {control_counts}")

def balance_dataset(initial_dataset, num_data):
    records = []
    with open(initial_dataset, 'r') as csvfile:
        for line in csvfile:
            if len(line) > 5:
                a, b = line.split('",', 1)
                bs = re.findall(r"'([^']*)'|" + r'"([^"]*)"', b)
                bs = [str(elem) for tup in bs for elem in tup if elem]
                records.append((a, bs))
    df = pd.DataFrame(records, columns=["code", "api_calls"])
    generate_statistics1(df)
    # Start with a new DataFrame for augmented samples
    augmented_df = df.copy()
    augmented_df['augmented_code'] = augmented_df['code'].apply(lambda code: bfs_variable_replacement_v3(code,num_data))

    desired_counts = desired_counts_distribution(num_data)
    for api_count, desired_count in desired_counts.items():
        rows_with_api_count = augmented_df[augmented_df["api_calls"].apply(len) == api_count]
        actual_count = len(rows_with_api_count)
        if actual_count > 0 and actual_count < desired_count:
            additional_rows = rows_with_api_count.sample(desired_count - actual_count, replace=True)
            additional_rows['augmented_code'] = additional_rows['augmented_code'].apply(lambda code: bfs_variable_replacement_v3(code,num_data))
            augmented_df = pd.concat([augmented_df, additional_rows])

    while len(augmented_df) < num_data:
        additional_rows = augmented_df.sample(num_data - len(augmented_df), replace=True)
        additional_rows['augmented_code'] = additional_rows['augmented_code'].apply(lambda code: bfs_variable_replacement_v3(code,num_data))
        augmented_df = pd.concat([augmented_df, additional_rows])

    augmented_df.reset_index(drop=True, inplace=True)
    generate_statistics(augmented_df)
    balanced_dataset = initial_dataset.replace(".csv", "_balanced_normal.csv")

    with open(balanced_dataset, 'w') as f:
        for i in range(augmented_df.shape[0]):
            code = '"' + augmented_df.loc[i, 'augmented_code'] + '"'
            api_calls = augmented_df.loc[i, 'api_calls']
            api_calls_str = ', '.join([f"'{api_call}'" for api_call in api_calls])
            f.write(f'({code}, [{api_calls_str}])\n')

    return balanced_dataset


balanced_dataset = balance_dataset("train.csv", num_data=10000)
#balanced_dataset = balance_dataset("new_generated_class.csv", num_data=100000)

