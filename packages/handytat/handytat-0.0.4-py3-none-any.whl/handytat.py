"""HandyTAT - The Handy Text Alignment Toolkit"""

__version__ = "0.0.4"

# For automatically detecting the language of the files
from langdetect import detect

# For CLI arguments
import argparse

# For Running the Hunaligner and Sublime Text
import subprocess

# For the splitSentences Function
import re

# For the tsv2tmx Funtcion
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

# For running Sublime Text
import sys

# For
import os

# For ploting the alignment graph
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


def splitSentences(text):

    # Abbreviations to exclude from sentence splitting
    abr = """
    Sr Sra 
    Dr Dra 
    Eng 
    Exma Exmo

    Mr Mrs Md
    """.split()

    # Replace newlines with spaces
    text = re.sub('\n', ' ', text)

    # Parse Abr
    re_abr = fr'\b({"|".join(abr)})\.'
    print(re_abr)

    # Sub for a special Character
    text = re.sub(re_abr, r'\1§', text, flags=re.I)

    # Split sentences on periods, unless the period is part of an abbreviation to ignore.
    pattern = r'\b\S.*?(?<![A-Z][a-z]\.|\w\.\w|\.\.\.)(?<!\w\.\w\.)(?<=\.|\?|!)\s+(?=\S)'

    sentence_list = re.findall(pattern, text)

    # Join sentences that were split by a single newline
    for i in range(len(sentence_list)-1):
        if sentence_list[i].endswith('\n') and not sentence_list[i+1].startswith('\n'):
            sentence_list[i] = sentence_list[i].rstrip(
                '\n') + ' ' + sentence_list[i+1].lstrip()
            sentence_list[i+1] = ''

    return sentence_list


def tsv2tmx(input_file, output_file, source_language, target_language):
    # Open the TSV file and read its contents
    with open(input_file, "r", encoding="utf-8") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')

        # Create the root element of the TMX file
        root = ET.Element('tmx')
        root.set('version', '1.4')
        header = ET.SubElement(root, 'header')
        header.set('creationtool', 'Python')
        header.set('srclang', source_language)
        header.set('datatype', 'PlainText')
        body = ET.SubElement(root, 'body')

        # Loop through each row in the TSV file and create a TMX segment for it
        for row in tsvreader:
            source_text = row[0]
            target_text = row[1]
            segment = ET.SubElement(body, 'tu')
            source = ET.SubElement(segment, 'tuv')
            source.set('xml:lang', source_language)
            seg_source = ET.SubElement(source, 'seg')
            seg_source.text = source_text
            target = ET.SubElement(segment, 'tuv')
            target.set('xml:lang', target_language)
            seg_target = ET.SubElement(target, 'seg')
            seg_target.text = target_text

        # Write the TMX file to disk with proper indentation
        xmlstr = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(xmlstr)
        with open(output_file, "wb") as f:
            f.write(reparsed.toprettyxml(indent="\t", encoding='utf-8'))


def readHist(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()

    y_data = [float(line.split()[-1]) for line in data]
    x_data = list(range(1, len(data) + 1))

    return {"x_data": x_data, "y_data": y_data}


def transformHist(data_dict, x):
    y_data = data_dict['y_data']
    transformed_y_data = []

    for i in range(len(y_data)):
        if i < x or i >= len(y_data) - x:
            transformed_y_data.append(y_data[i])
        else:
            left_sum = sum(y_data[i-x:i])
            right_sum = sum(y_data[i+1:i+x+1])
            avg = (left_sum + right_sum) / (2*x)
            transformed_y_data.append(avg)

    return {"x_data": data_dict['x_data'], "y_data": transformed_y_data}


def transformHist2(data_dict, x):
    y_data = data_dict['y_data']
    transformed_y_data = []

    for i in range(0, len(y_data), x):
        avg = sum(y_data[i:i+x]) / x
        transformed_y_data.extend([avg]*min(x, len(y_data)-i))

    return {"x_data": data_dict['x_data'], "y_data": transformed_y_data}


def transformHist3(data_dict, x):
    y_data = data_dict['y_data']
    transformed_y_data = []
    new_x_data = []

    for i in range(x//2, len(y_data), x):
        avg = sum(y_data[i:i+x]) / x
        transformed_y_data.append(avg)
        new_x_data.append(data_dict['x_data'][i])

    return {"x_data": new_x_data, "y_data": transformed_y_data}


def plotGraph(data_dict, save_path=None):

    x_data = data_dict['x_data']
    y_data = data_dict['y_data']

    plt.plot(x_data, y_data)
    plt.xlabel('Line Number')
    plt.ylabel('Alignment Quality Coefficient')

    if save_path:
        plt.savefig(save_path)
        print(f"Graph saved at {save_path}")
    else:
        plt.show()

# FIIXXXX


def nameDir(filename):
    """
    This function takes a file name as input and returns the file name without the last extension
    and replaces all non-alphanumeric characters with an underscore.
    """

    # Split the file name into a list of components separated by "."
    components = filename.split(".")

    # If there is only one component, return the file name as-is
    if len(components) == 1:
        return "".join([char if char.isalnum() else "_" for char in filename])

    # Otherwise, remove the last component (the file extension) and join the rest of the components
    dir_name = ".".join(components[:-1])

    # Replace all non-alphanumeric characters with an underscore
    dir_name = "".join([char if char.isalnum() else "_" for char in dir_name])

    return dir_name


def verifyLanguagesFormat(string):
    pattern = r'^[A-Za-z]{2}-[A-Za-z]{2}$'

    if re.match(pattern, string):
        return True
    else:
        return False


def open_files_in_sublime(file1, file2):
    sublime_path = "subl"  # Replace with the path to your Sublime Text executable if needed

    command = [
        sublime_path,
        "--command",
        "set_layout {\"cols\": [0.0, 0.5, 1.0], \"rows\": [0.0, 1.0], \"cells\": [[0, 0, 1, 1], [1, 0, 2, 1]]}",
        "-n",
        file1,
        "--command",
        "set_view_index {\"group\": 1, \"index\": 0, \"file\": \"%s\"}" % file2,
    ]

    '''
    command = [
        sublime_path,
        "--command",
        "set_layout {\"cols\": [0.0, 0.5, 1.0], \"rows\": [0.0, 1.0], \"cells\": [[0, 0, 1, 1], [1, 0, 2, 1]]}",
        "--command",
        "focus_group {\"group\": 0}",
        "-n",
        file1,
        "--command",
        "focus_group {\"group\": 1}",
        "-n",
        file2
    ]
    '''

    '''
    command = [
        sublime_path,
        "--command",
        "set_layout {\"cols\": [0.0, 0.5, 1.0], \"rows\": [0.0, 1.0], \"cells\": [[0, 0, 1, 1], [1, 0, 2, 1]]}",
        "--command",
        "set_view_index {\"group\": 1, \"index\": 0, \"file\": \"%s\"}" % file2,
        file1
    ]
    '''

    subprocess.Popen(command)


def parseArgs():

    parser = argparse.ArgumentParser(
        description='Toolkit for Text Alignment Tasks')

    parser.add_argument('original', help='The path to the original text')
    parser.add_argument('translated', help='The path to the translated text')

    parser.add_argument('-o', '--output', default='aligned.txt',
                        help='The path to the output file (default: align.txt)')
    parser.add_argument('-d', '--dictionary', default='null.dic',
                        help='The path to the dictionary (default: dic.null)')

    parser.add_argument('-pr', '--preprocess', action='store_true',
                        help='Preprocess the input files before running Hun Aligner')

    parser.add_argument('-ot', '--output_type', dest='output_type',
                        help='Output file type', action='store_true')

    parser.add_argument('-l', '--language_pair', dest='language_pair',
                        help='Language pair of the bi-text')

    # group = parser.add_mutually_exclusive_group(required='-ot' in str(sys.argv))
    # group.add_argument('-s', '--source', dest='source_language', help='Source language for TMX file')
    # group.add_argument('-t', '--target', dest='target_language', help='Target language for TMX file')

    parser.add_argument('-g', '--graph', dest='graph',
                        help='Plot Graph', action='store_true')

    parser.add_argument('-sg', '--save_graph', type=str,
                        help='Path to save the graph as an image')

    parser.add_argument('-sub', '--sublime', dest='sublime',
                        help='Pre-process the bi-text in Sublime Text editor', action='store_true')

    args = parser.parse_args()
    return args


def main():

    args = parseArgs()

    with open(args.original, 'r') as f:
        original_text = f.read()

    with open(args.translated, 'r') as f:
        translated_text = f.read()

    source_language_autodetect = detect(original_text)
    target_language_autodetect = detect(translated_text)

    if args.preprocess:

        sentences = splitSentences(original_text)

        project_name = "align"

        dirname = nameDir(args.original)

        if not os.path.exists(f"{project_name}/{dirname}"):
            os.makedirs(f"{project_name}/{dirname}")
        elif os.path.exists(f"{project_name}") and not os.path.exists(f"{project_name}"):
            os.makedirs(f"{project_name}/{dirname}")

        with open(f"{project_name}/{dirname}/original_pp.txt", 'w') as f:
            f.write('\n'.join(sentences))

        sentences = splitSentences(translated_text)

        with open(f"{project_name}/{dirname}/translated_pp.txt", 'w') as f:
            f.write('\n'.join(sentences))

        cl = ['/usr/local/bin/hunalign', args.dictionary,
              f"{project_name}/{dirname}/original_pp.txt", f"{project_name}/{dirname}/translated_pp.txt", '-text', '>', args.output]
    else:
        cl = ['/usr/local/bin/hunalign', args.dictionary,
              args.original, args.translated, '-text', '>', args.output]

    subprocess.run(' '.join(cl), shell=True)

    if args.output_type:

        tsv2tmx(args.output, "aligned.tmx",
                source_language_autodetect, target_language_autodetect)

    if args.output_type and args.language_pair:

        if verifyLanguagesFormat(args.language_pair):
            tsv2tmx(args.output, "aligned.tmx",
                    args.language_pair[:2], args.language_pair[-2:])
        else:
            print(
                '\033[31mERROR: \033[0mInvalid Language Pair Format! Please use the format "aa-aa".')
            print(
                '\033[33mWARNING: \033[0mAutomatic Language Detection used for generating the TMX file.')

    if args.graph:
        hist = readHist(args.output)

        hist_averaged = transformHist3(hist, 10)
        # hist_averaged = hist

        plotGraph(hist_averaged, args.save_graph)
        # plotGraph(args.output, args.save_graph)

    if args.sublime:
        open_files_in_sublime(args.original, args.translated)


if __name__ == '__main__':
    main()
