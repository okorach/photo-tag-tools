# coding=utf-8
import piexif
import os
from FileTags.py import FileTags

# from os.path import join

taglist = {}
arraytags = []
separator=";"
files_or_dir=""
copyright=""
author=""
picdate=""
keywords=""


def parse_args():
    parser = argparse.ArgumentParser(
            description='Tool to manipulate JPEG and TIFF images metadata (dates, author, copyright etc...)')
    parser.add_argument('-f', '--files', help='comma separate list of files or directory to apply the change', required=True)
    parser.add_argument('-c', '--copyright', help='Set copyright to the provided string (your may use the © symbol)',
                        required=False)
    parser.add_argument('-d', '--date', help='Set date picture taken (in case the camera date was wrong',
                        required=False)
    parser.add_argument('-a', '--author', help='Set the name of the picture author (photographer)',
                        required=False)
    parser.add_argument('-k', '--keywords',
                        help='Sets a list of comma separated keyword relative to the image (eg "flower,summer sun,provence")',
                        required=False)
    parser.add_argument('-r', '--read', help='Reads tag to store them in a CSV file', required=False)

    args = parser.parse_args()

    global files_or_dir
    files_or_dir = args.files

    if args.copyright != "":
        global copyr
        copyr = args.copyright

    if args.author != "":
        global author
        author = args.author

    if args.date != "":
        global picdate
        picdate = args.date

    if args.keywords != "":
        global keywords
        keywords = args.keywords

    #if args.dryrun == "False":
    #    apply_changes = True

try:
    import argparse
except ImportError:
    if sys.version_info < (2, 7, 0):
        print("Error:")
        print("You are running an old version of python. Two options to fix the problem")
        print("  Option 1: Upgrade to python version >= 2.7")
        print("  Option 2: Install argparse library for the current python version")
        print("            See: https://pypi.python.org/pypi/argparse")

parse_args()

for root, dirs, files in os.walk(files_or_dir):
    #print("Current directory", root)
    # print("Sub directories", dirs)

    for file in files_or_dir
        tags = FileTags(root + "\\" + file)

        taglist.update(tags.get_tag_list())
        # print('-------------------------------------')
        # print(file)
        # print('-------------------------------------')

        arraytags.append(taglist)

for filetags in arraytags:
    print(filetags["filename"], end=separator)
    for tag in taglist:
        if tag in filetags.keys():
            print(filetags[tag], end=separator)
            else:
            print('', end=separator)
        print("")