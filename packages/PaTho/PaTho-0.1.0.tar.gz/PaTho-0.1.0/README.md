# PaTho
a python package to get images from HPA. Works great with pathology streamlit.

## Installation
Installing PaTho is as simple as running:
```
pip install patho
```

## Usage
You need to provide a list of image urls you want to download in a file. Then you can run the following command to download the images:
```
PaTho -f <path/to/file> -d <directory/to/save/images> -b <optional the base-url>
```
For example:

```
PaTho -f files.txt -d images -b http://images.proteinatlas.org/
```