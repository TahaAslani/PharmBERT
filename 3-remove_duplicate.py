import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Remove duplicates')

parser.add_argument('--input-path', '-i', required=True, type=str,
    help='input path.')
parser.add_argument('--output-path', '-o', required=True, type=str,
    help='Output path.')

args = parser.parse_args()

input_path = args.input_path
output_path = args.output_path

# Load data
original = pd.read_csv(input_path)

# Get columns
my_columns = original.columns

# get len
original_len = original.shape[0]

# Loop through the columns
for col in my_columns:
    print(col)
    # We do not want to ignore duplicates for this column
    # because this column mut remain intact
    if col=='APPLICATION_NO':
        continue
    
    rep_ind = np.setdiff1d(original.index, \
        original.drop_duplicates(subset=[col]).index)
    
    original.loc[rep_ind,col] = ''

# Save the results
original.to_csv(output_path, index=False)
