Download SciCap dataset: [here](https://www.dropbox.com/s/t1sjqesl0pynaxo/scicap_data.zip?dl=0)
## Data Preparation
### Folder Structure

1. Download the data and unzip it. This is the folder structure:
```
scicap_data.zip
├── SciCap-Caption-All                  #caption text for all figures
│	├── Train
│	├── Val
│	└── Test
├── SciCap-No-Subfig-Img                #image files for the figures without subfigures
│	├── Train
│	├── Val
│	└── Test
├── SciCap-Yes-Subfig-Img               #image files for the figures with subfigures
│	├── Train
│	├── Val
│	└── Test
├── arxiv-metadata-oai-snapshot.json    #arXiv paper's metadata (from arXiv dataset)
└── List-of-Files-for-Each-Experiments  #list of figure names used in each experiment 
    ├── Single-Sentence-Caption
    │   ├── No-Subfig
    │   │   ├── Train
    │	│   ├── Val
    │	│   └── Test
    │	└── Yes-Subfig
    │       ├── Train
    │       ├── Val
    │       └── Test
    ├── First-Sentence                  #Same as in Single-Sentence-Caption
    └── Caption-No-More-Than-100-Tokens #Same as in Single-Sentence-Caption
```
### Script
1. Run the script as follows:
```
python3 scicap_data.py
```