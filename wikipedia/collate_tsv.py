import argparse
import os

import pandas as pd

parser = argparse.ArgumentParser(description='Process TSV file and image folder')
parser.add_argument('tsv_file_path', type=str, help='Path to the input TSV file')
parser.add_argument('image_folder_path', type=str, help='Path to the image folder')
parser.add_argument('output_tsv_path', type=str, help='Path to the output TSV file')
args = parser.parse_args()

tsv_file_path = args.tsv_file_path
image_folder_path = args.image_folder_path
output_tsv_path = args.output_tsv_path

# Read the input TSV file
df = pd.read_csv(tsv_file_path, sep='\t')

# Extract indices from image filenames in the directory
image_indices = [int(filename.split('-')[-1].split('.')[0]) for filename in os.listdir(image_folder_path)]

# Filter rows from DataFrame based on extracted indices
selected_df = df[df['index'].isin(image_indices)]

# Save the selected DataFrame to output TSV
selected_df.to_csv(output_tsv_path, sep='\t', index=False)
