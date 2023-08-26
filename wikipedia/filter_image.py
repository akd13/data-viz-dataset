import argparse

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Filter and process CSV file.')
    parser.add_argument('filename', type=str, help='Input CSV filename')
    args = parser.parse_args()

    filename = args.filename
    df = pd.read_csv(filename, encoding='utf-8', sep='\t')
    df_new = df[df.language == 'en']
    df_final = df_new[~df_new.mime_type.isin(['image/svg+xml', 'image/webp'])]
    df_final = df_final.reset_index(drop=False).rename(columns={'index': 'index'})
    df_final.to_csv(f'{filename.split(".")[0]}-filtered.tsv', sep='\t', index=True)


if __name__ == "__main__":
    main()
