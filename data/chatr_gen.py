import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_boxplot(df):
    """
    Generate a box plot based on the execution times DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing execution time data with columns "Folder", "Program", and "Time".

    Returns:
        None: A box plot will be displayed.
    """
    plt.figure(figsize=(7, 6), dpi=400)  # Size suitable for IEEE two-column format
    sns.set(style="whitegrid", font_scale=1.0)  # Bigger and bolder fonts

    sns.boxplot(x="Program", y="Time", hue="Folder", data=df)
    
    plt.title("Distribution of Execution Times", fontsize=12, fontweight='bold')
    plt.xlabel("Python File", fontsize=10, fontweight='bold')
    plt.ylabel("Time (s)", fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=90, fontsize=7)
    plt.yticks(fontsize=8)
    
    plt.legend(title='Test Suites', title_fontsize='10', loc='upper right', fontsize=8)
    
    plt.tight_layout()
    plt.savefig("box_plot_IEEE_format.png", dpi=300)  # Save the figure in high resolution

def generate_boxplot_from_csv(csv_path):
    """
    Generate a box plot from a CSV file containing execution time data.

    Parameters:
        csv_path (str): The path to the CSV file.

    Returns:
        None: A box plot will be displayed.
    """
    df = pd.read_csv(csv_path)
    generate_boxplot(df)

# Replace the path with the location of your CSV file
generate_boxplot_from_csv("F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\data\\execution_times_data.csv")
