import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import re
random.seed(42)
def read_dataset(dataset):
    records = []
    with open(dataset, 'r') as csvfile:
        for line in csvfile:
            if len(line) > 5:
                a, b = line.split('",', 1)
                bs = re.findall(r"'([^']*)'|" + r'"([^"]*)"', b)
                bs = [elem for tup in bs for elem in tup if elem]
                records.append((a, bs))
    df = pd.DataFrame(records, columns=["code", "api_calls"])
    return df

def modified_generate_bar_plot(df):
    # Set font size and weight
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.weight'] = 'bold'
    
    # Compute the frequency of each API call combination and take the top 25
    api_calls_frequency = df['api_calls'].str.join(', ').value_counts().head(25)
    
    plt.figure(figsize=[10,8])
    api_calls_frequency.plot(kind='bar', color=[plt.cm.Paired(random.random()) for _ in range(len(api_calls_frequency))])
    plt.title('Frequency of Top 25 API calls')
    plt.ylabel('Frequency')
    plt.xlabel('API calls')
    plt.xticks(rotation=45, ha='right')  # rotation and horizontal alignment
    plt.tight_layout()
    plt.savefig('top_25_bar_plot.png')
    plt.show()
    
    # Reset font size and weight to defaults
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.weight'] = 'normal'

def adjusted_generate_pie_chart(df):
    # Set font size and weight
    plt.rcParams['font.size'] = 14
    plt.rcParams['font.weight'] = 'bold'
    
    # Count the number of API calls for each code snippet
    num_api_calls = df['api_calls'].apply(len)
   
    # Adjust bins and labels for 1 to 5 API calls
    bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]  # Including 6 as the upper edge for 5 API calls
    names = ['1', '2', '3', '4', '5']
    
    # Group the data into the bins
    num_api_categories = pd.cut(num_api_calls, bins, labels=names, right=False).value_counts()
    colormap = plt.cm.Paired
    colors = [colormap(i) for i in range(len(num_api_categories))]
    plt.figure(figsize=[10,8])
    num_api_categories.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title('Distribution of Number of API Calls per Code Snippet (1 to 5 calls)')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('adjusted_api_calls_pie_chart.png')
    plt.show()
    
    # Reset font size and weight to defaults
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.weight'] = 'normal'

# As the main function contains the call to read_dataset which requires an external dataset, 
# running the main function here would result in an error.
# Therefore, the provided modifications were made directly to the plotting functions.

def main():
    dataset = "new_generated_class_balanced_normal.csv"  # replace with your dataset name
    df = read_dataset(dataset)
    modified_generate_bar_plot(df)
    adjusted_generate_pie_chart(df)
if __name__ == "__main__":
    main()
