import pandas as pd
import unicodedata


# Example usage
file_path = "netflix_amazon_disney_titles.csv"
data = pd.read_csv(file_path)

fifth_column = data.iloc[:, 4]
split_data = fifth_column.str.split(',')

for index, row in split_data.items():
    for item in row:
        item=unicodedata.normalize('NFD', item).encode('ascii', 'ignore')
        print(item)