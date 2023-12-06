"""HandyTAT - The Handy Text Alignment Toolkit"""

__version__ = "0.1.1"

import argparse
import subprocess

import re
#import argparse

import csv
#import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

import sys


def splitSentences(text):

    # Abbreviations to exclude from sentence splitting
    # ignore_abbr = ['Sr.', 'Sra.', '...']
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
            sentence_list[i] = sentence_list[i].rstrip('\n') + ' ' + sentence_list[i+1].lstrip()
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


def parseArgs():

    parser = argparse.ArgumentParser(description='Toolkit for Text Alignment Tasks')
    
    parser.add_argument('original', help='The path to the original text')
    parser.add_argument('translated', help='The path to the translated text')

    parser.add_argument('-o', '--output', default='aligned.txt', help='The path to the output file (default: align.txt)')
    parser.add_argument('-d', '--dictionary', default='null.dic', help='The path to the dictionary (default: dic.null)')

    parser.add_argument('-pr', '--preprocess', action='store_true', help='Preprocess the input files before running Hun Aligner')

    parser.add_argument('-ot', '--output_type', dest='output_type', help='Output file type', action='store_true')

    parser.add_argument('-s', '--source', dest='source_language', help='Source language for TMX file')
    parser.add_argument('-t', '--target', dest='target_language', help='Target language for TMX file')

    #group = parser.add_mutually_exclusive_group(required='-ot' in str(sys.argv))
    #group.add_argument('-s', '--source', dest='source_language', help='Source language for TMX file')
    #group.add_argument('-t', '--target', dest='target_language', help='Target language for TMX file')

    args = parser.parse_args()
    return args

def main():

    args = parseArgs()

    if args.preprocess:
        with open(args.original, 'r') as f:
            text = f.read()

        sentences = splitSentences(text)
        
        with open("tmp/original_pp.txt", 'w') as f:
            f.write('\n'.join(sentences))

        with open(args.translated, 'r') as f:
            text = f.read()

        sentences = splitSentences(text)
        
        with open("tmp/translated_pp.txt", 'w') as f:
            f.write('\n'.join(sentences))

        cl = ['/usr/local/bin/hunalign', args.dictionary, "tmp/original_pp.txt", "tmp/translated_pp.txt",'-text', '>', args.output]
    else:
        cl = ['/usr/local/bin/hunalign', args.dictionary, args.original, args.translated,'-text', '>', args.output]
    
    subprocess.run(' '.join(cl), shell=True)

    if args.output_type:
        # Convert the TSV file to a TMX file
        tsv2tmx(args.output, "aligned.tmx", args.source_language, args.target_language)

if __name__ == '__main__':
    main()
