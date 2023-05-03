GIF Creator

GIF Creator is a Python script that processes a folder of .CR3 image files and automatically groups images into sequences based on 
their capture time. It helps photographers and content creators to quickly identify and organize image sequences that can be used 
to create GIFs or other similar animations.

Features

Automatically groups images taken within 2 seconds of each other into sequences.
Only considers sequences with 10 or more images.
Creates a directory tree for organizing the output, including separate folders for each sequence and corresponding GIF exports.
Provides progress updates in the terminal while processing images.
Usage

To use the script, follow these steps:

Ensure you have Python 3 and the necessary libraries installed (tqdm and Pillow).
Clone the repository or download the gif_creator.py script to your computer.
Open a terminal and navigate to the folder containing the script.
Run the script by providing the path to the folder containing the .CR3 image files as an argument:
bash
Copy code
python3 gif_creator.py /path/to/image/folder
The script will then process the images in the specified folder and create the output directory structure in the current working 
directory. It will generate folders for each image sequence and corresponding GIF exports.

Example of the output directory structure:

markdown
Copy code
GIFs
│
├── RAW_GIFs
│   ├── GIF1 | 77 images
│   ├── GIF2 | 35 images
│   └── ...
│
└── GIF_EXPORTS
    ├── GIF1 | 77 images
    ├── GIF2 | 35 images
    └── ...
License

This project is licensed under the MIT License - see the LICENSE file for details.# 
gif_creator
