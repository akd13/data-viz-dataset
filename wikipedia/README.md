# WiT Dataset
*Files from Wikipedia, with the image links and associated captions and alt-text when available.*

1. The files are labelled as per [this](https://github.com/google-research-datasets/wit/blob/main/DATA.md).
   1. Run the download script `python download_zip_files.py` to download the zip files into your current directory.
2. For the files downloaded, run `for file in *.tsv.gz; do gzip -d "$file"; done` to unzip the files.
3. For each file downloaded, do the following -
   4. Run `python filter_image.py --filename <file_name>.tsv` to extract those rows that have English captions and remove those rows 
   that have unsupported image types (e.g. svg, webp, etc.). This will give you the original file name appended with `-filtered`.
   5. Download the pretrained model [`vit-base-beans`](https://drive.google.com/file/d/1nc8Egnj_G4L6b8-cLz-86JNQPkU1TAWr/view?usp=drive_link) 
      which has been further fine-tuned on images of charts/graphs.
   6. Run `python extract_images.py --filename <file_name>-filtered.tsv --folder <image-folder> --model <path-to-downloaded-model>` on the file to 
      only save images of charts/graphs.
   7. The images are saved in the folder.
4. Once the script is finished running, manually sort through the images to find those that are not pictures of charts/graphs.
5. After that, to collate the final tsv file, run `python collate_tsv.py <file_name>-filtered.tsv <image-folder> <path-to-downloaded-model>`.

