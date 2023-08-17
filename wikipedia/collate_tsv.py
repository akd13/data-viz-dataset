import os
import sys

import pandas as pd

tsv_file_path = sys.argv[1]
image_folder_path = sys.argv[2]
output_tsv_path = sys.argv[3]

# Read the input TSV file
df = pd.read_csv(tsv_file_path, sep='\t')

# Extract indices from image filenames in the directory
image_indices = [int(filename.split('-')[-1].split('.')[0]) for filename in os.listdir(image_folder_path)]

# Filter rows from DataFrame based on extracted indices
selected_df = df[df['index'].isin(image_indices)]

# Save the selected DataFrame to output TSV
selected_df.to_csv(output_tsv_path, sep='\t', index=False)
