import pandas as pd

def check_class_balance(file_path, target_col):
    """
    Checks the distribution of the target variable in a dataset.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"\n--- Class Distribution for '{target_col}' in '{file_path}' ---")
        if target_col in df.columns:
            print(df[target_col].value_counts(normalize=True).sort_index())
        else:
            print(f"Error: Target column '{target_col}' not found in the file.")
    except FileNotFoundError:
        print(f"\nError: '{file_path}' not found. Please ensure the file is in the same directory.")
    except Exception as e:
        print(f"\nAn error occurred while processing '{file_path}': {e}")

if __name__ == "__main__":
    # Check the first dataset
    check_class_balance('Impact_of_Remote_Work_on_Mental_Health.csv', 'Mental_Health_Impact')

    print("\n" + "="*50 + "\n")

    # Check the second dataset
    check_class_balance('StressLevelDataset.csv', 'StressLevel')