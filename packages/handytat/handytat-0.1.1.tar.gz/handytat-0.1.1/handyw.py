import sys
import os
from bs4 import BeautifulSoup
import shutil


# Check if the required libraries are installed
try:
    import bs4
except ImportError:
    sys.exit(
        "Please install the required library 'beautifulsoup4' using 'pip install beautifulsoup4'.")

# Check if a valid input file is provided
if len(sys.argv) != 2:
    sys.exit("Usage: python split_and_open.py input_file.tmx/tsv")

input_file = sys.argv[1]

# Check if the input file exists
if not os.path.exists(input_file):
    sys.exit(f"The input file '{input_file}' does not exist.")

# Determine the file format based on the file extension
file_extension = input_file.split('.')[-1].lower()
if file_extension not in ['tmx', 'tsv']:
    sys.exit("Supported formats are TMX and TSV.")

# Initialize language_suffixes
language_suffixes = {}

# Create a directory for temporary files with the "temp" suffix
base_filename = os.path.splitext(os.path.basename(input_file))[0]
temp_dir = f"{base_filename}.temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Copy the input file to the temporary directory
shutil.copy(input_file, os.path.join(temp_dir, os.path.basename(input_file)))


# Initialize dictionaries to hold source and target segments
temp_sources = {}
temp_targets = {}

# Parse the input file based on format
if file_extension == 'tmx':
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')

    for tu in soup.find_all('tu'):
        tuvs = tu.find_all('tuv')
        if len(tuvs) == 2:
            source_tuv, target_tuv = tuvs
            source_lang = source_tuv.get('xml:lang')
            target_lang = target_tuv.get('xml:lang')
            source_seg = source_tuv.find('seg')
            target_seg = target_tuv.find('seg')
            if source_lang and source_seg:
                if source_lang not in temp_sources:
                    temp_sources[source_lang] = []
                temp_sources[source_lang].append(source_seg.text.strip())
                language_suffixes[source_lang] = True
            if target_lang and target_seg:
                if target_lang not in temp_targets:
                    temp_targets[target_lang] = []
                temp_targets[target_lang].append(target_seg.text.strip())
                language_suffixes[target_lang] = True
else:
    # Handle TSV format parsing (you need to define the delimiter)
    import csv
    delimiter = '\t'  # Set the delimiter based on your TSV format
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if len(row) >= 4:
                # Assuming the first column is the source language code
                source_lang = row[0]
                # Assuming the second column is the target language code
                target_lang = row[1]
                # Assuming the third column is the source text
                source_text = row[2]
                # Assuming the fourth column is the target text
                target_text = row[3]
                if source_lang and source_text:
                    if source_lang not in temp_sources:
                        temp_sources[source_lang] = []
                    temp_sources[source_lang].append(source_text)
                    language_suffixes[source_lang] = True
                if target_lang and target_text:
                    if target_lang not in temp_targets:
                        temp_targets[target_lang] = []
                    temp_targets[target_lang].append(target_text)
                    language_suffixes[target_lang] = True

# Create temporary files for source and target with language suffixes
temp_files = {}
for lang in language_suffixes:
    temp_file_path = os.path.join(temp_dir, f"{base_filename}.{lang}.txt")
    content = "\n".join(temp_sources[lang]) if lang in temp_sources else "\n".join(
        temp_targets[lang])
    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(content)
    temp_files[lang] = temp_file


layout = [
    "subl --launch-or-new-window ",
    "--command 'set_layout {",
    "\"cols\": [0.0, 0.5, 1.0], ",
    "\"rows\": [0.0, 1.0], ",
    "\"cells\": [[0, 0, 1, 1], [1, 0, 2, 1]]",
    "}'",
]

file1 = None
file2 = None

for file_key, file in temp_files.items():
    if file1 is None:
        file1 = file.name
    else:
        file2 = file.name
        break

# Get the current working directory using getcwd
current_directory = os.getcwd()

# Combine the current directory and the file path
file1 = os.path.join(current_directory, file1)
file2 = os.path.join(current_directory, file2)

command = "".join(layout)

command = command + " " + \
    "--command 'focus_group {\"group\": 0}' " + \
    "--command 'open_file {\"file\": \"" + file1 + "\"}' " + \
    "--command 'focus_group {\"group\": 1}' " + \
    "--command 'open_file {\"file\": \"" + file2 + "\"}' " + \
    "--command 'focus_group {\"group\": 0}' " + \
    "--command 'toggle_both_lines_highlighting_mode {\"forced\": 1}' " + \
    "--command 'toggle_cursor_sync_mode {\"forced\": 1}' " + \
    "--command 'custom_toggle_minimap {\"force_disable\": 1}' "

print(command)


def main():
    os.system(command)

if __name__ == '__main__':
    main()