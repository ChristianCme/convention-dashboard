import os
import pandas as pd

# Set the directory containing CSV files
csv_directory = './processed'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_directory, filename)
        # Read each CSV file into a DataFrame and append it to the list
        df = pd.read_csv(file_path)
        # Add a new column with the file name (without '.csv' extension)
        df['Vote'] = os.path.splitext(filename)[0]
        dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Now 'combined_df' contains all the data from the CSV files with an added 'SourceFile' column
# containing the name of the file without '.csv' extension

# Print the first few rows of the combined DataFrame
print(combined_df.head())

combined_df.to_csv("combined_votes.csv", index=False)