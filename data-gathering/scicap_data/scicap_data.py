import pandas as pd
import os
import json

captions_dir = "SciCap-Caption-All"
subfig_dir = "SciCap-Yes-Subfig-Img"
no_subfig_dir = "SciCap-No-Subfig-Img"

types = ['train', 'test', 'val']

caption_files = set()
for t in types:
    captions = os.listdir(os.path.join(captions_dir, t))
    caption_files.update(captions)

print("Number of caption files: {}".format(len(caption_files)))

subfig_images = {}
for t in types:
    subfig_images[t] = os.listdir(os.path.join(subfig_dir, t))

for t, images in subfig_images.items():
    print(t, len(images))
    try:
        subfig_images[t].remove('.DS_Store')
    except Exception:
        print('DS_Store not in {}'.format(t))

key = '1-lowercase-and-token-and-remove-figure-index'
subfig_data = []

for im_type, im_list in subfig_images.items():
    for im in im_list:
        json_file = im.split('.png')[0] + '.json'
        f = open(os.path.join(captions_dir, im_type, json_file))
        data = json.load(f)
        row = [im, data[key]['caption'], data[key]['token'], im_type]
        subfig_data.append(row)
        f.close()

print("Number of subfig images: {}".format(len(subfig_data)))

df_subfig = pd.DataFrame(subfig_data)
df_subfig.to_csv('subfig.csv', index=False, header=["name", "caption", "tokens", "split"])

no_subfig_images = {}
for t in types:
    no_subfig_images[t] = os.listdir(os.path.join(no_subfig_dir, t))
    try:
        no_subfig_images[t].remove('.DS_Store')
    except Exception:
        print('DS_Store not in {}'.format(t))

for t, images in no_subfig_images.items():
    print(t, len(images))

no_subfig_data = []
key = '1-lowercase-and-token-and-remove-figure-index'

for im_type, im_list in no_subfig_images.items():
    for im in im_list:
        json_file = im.split('.png')[0] + '.json'
        f = open(os.path.join(captions_dir, im_type, json_file))
        data = json.load(f)
        row = [im, data[key]['caption'], data[key]['token'], im_type]
        no_subfig_data.append(row)
        f.close()

print("Number of no subfig images: {}".format(len(no_subfig_data)))

df = pd.DataFrame(no_subfig_data)
df.to_csv('no_subfig.csv', index=False, header=["name", "caption", "tokens", "split"])
