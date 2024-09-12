import gc
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import requests
import torch
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification

parser = argparse.ArgumentParser(description='Image processing and classification')
parser.add_argument('--filename', type=str, help='Input CSV filename')
parser.add_argument('--folder', type=str, help='Path to save images')
parser.add_argument('--model', type=str, help='Path to the model')
args = parser.parse_args()

filename = args.filename
folder_path = args.folder
model_path = args.model_path
test_folder = folder_path

df = pd.read_csv(filename, sep='\t')

gc.collect()

LABEL_OTHERS = 2  # this is the label for 'others', aka images that are not charts/graphs
# create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "gpu"
else:
    device = "cpu"

model = ViTForImageClassification.from_pretrained(model_path).to(device)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_path, device=device)


# Define the transformation function
def transform(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = feature_extractor(images=image.convert('RGB'), return_tensors='pt', device=device)
    return inputs.pixel_values


# Define a function to predict a single image
def predict_image(image, model):
    # Transform the image to the required format
    inputs = transform(image)
    # Make the prediction and return the class index
    with torch.no_grad():
        inputs = inputs.to(device)
        outputs = model(inputs)
        labels = outputs[0].cpu()
    return np.argmax(labels.numpy())


label_counts = {}


# Define a function to process each row of the dataframe
def process_row(row):
    # Get the image URL and predicted label
    image_url = row['image_url']
    image_path = None
    try:
        # Download and save the image
        response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        mime_type = image_url.split('.')[-1]
        image_path = os.path.join(folder_path, f'{filename.split(".")[0]}-{row[0]}.{mime_type}')
        with open(image_path, 'wb') as f:
            f.write(response.content)
        # Predict the label and update the counts
        predicted_label = predict_image(image_path, model)
        if predicted_label not in label_counts:
            label_counts[predicted_label] = 0
        label_counts[predicted_label] += 1
        if predicted_label == LABEL_OTHERS:
            os.remove(image_path)
    except Exception as e:
        print(f"Exception is {e} for {image_url}")
        if image_path:
            os.remove(image_path)


last_index_processed = None

# Create a thread pool with 10 threads
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
    for future in as_completed(futures):
        # Collect any exceptions from the threads
        if future.exception() is not None:
            print(f"Exception occurred: {future.exception()}")

print("Label counts", label_counts)
