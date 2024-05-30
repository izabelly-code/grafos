import pandas as pd

def read_csv_file(file_path):
    data = pd.read_csv(file_path)
    return data

# Example usage
file_path = "netflix_amazon_disney_titles.csv"
data = read_csv_file(file_path)

print(data.head())