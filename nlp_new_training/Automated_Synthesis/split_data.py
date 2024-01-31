import pandas as pd
from sklearn.model_selection import train_test_split
import re


def split_dataset(csv_file_path, test_size=0.10):
    """
    Splits a CSV file into train and test sets.

    :param csv_file_path: Path to the CSV file
    :param test_size: Proportion of the dataset to include in the test split
    :return: train_set, test_set
    """

    # Load the dataset
    df = ""
    try:
        records = []
        with open(csv_file_path, 'r') as csvfile:
            for line in csvfile:
                if len(line) > 5:
                    a, b = line.split('",', 1)
                    bs = re.findall(r"'([^']*)'|" + r'"([^"]*)"', b)
                    bs = [str(elem) for tup in bs for elem in tup if elem]
                    #newstr = (a+'",['+",".join(bs)+']')
                    records.append((a,bs))
        df = pd.DataFrame(records, columns=["code", "api_calls"])
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None, None

    # Splitting the data into train and test sets
    train, test = train_test_split(df, test_size=test_size, random_state=42)

    train = train.reset_index(drop=True)
    test = test.reset_index(drop=True)
    # train = pd.DataFrame(train)
    # test = pd.DataFrame(test)
    with open("train.csv", 'w') as f:
        for i in range(train.shape[0]):
            code =  train.loc[i,'code']+'"'
            if code[0]=='(':
                code = code[1:]
            api_calls = train.loc[i, 'api_calls']
            api_calls_str = ', '.join([f"'{api_call}'" for api_call in api_calls])
            f.write(f'{code}, [{api_calls_str}]\n')
    
    with open("test.csv", 'w') as f:
        for i in range(test.shape[0]):
              
            code = test.loc[i,'code']+'"'
            if code[0]=='(':
                code = code[1:]
            api_calls = test.loc[i, 'api_calls']
            api_calls_str = ', '.join([f"'{api_call}'" for api_call in api_calls])
            f.write(f'{code}, [{api_calls_str}]\n')


    return train, test

# Example usage
csv_path = "Automated_Synthesis//new_generated_class.csv"  # Replace with your CSV file path
train, test = split_dataset(csv_path, test_size=0.10)
