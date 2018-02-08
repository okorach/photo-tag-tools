#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3


#  coding=utf-8

import os
import sys
from filetags import file_tags

# from os.path import join

TAGLIST = {}
ARRAYTAGS = []
SEPARATOR = ";"

def parse_args():
    """Parses cmd line args"""
    parser = argparse.ArgumentParser(
        description='Tool to manipulate JPEG and TIFF images metadata (dates, author, copyright etc...)')
    parser.add_argument('-f', '--files',
                        help='comma separate list of files or directory to apply the change',
                        required=True)
    parser.add_argument('-c', '--copyright',
                        help='Set copyright to the provided string (your may use the © symbol)',
                        required=False)
    parser.add_argument('-d', '--date',
                        help='Set date picture taken (in case the camera date was wrong',
                        required=False)
    parser.add_argument('-a', '--author', help='Set the name of the picture author (photographer)',
                        required=False)
    parser.add_argument('-k', '--keywords',
                        help='Sets a list of comma separated keyword relative to the image (eg "flower,summer sun,provence")',
                        required=False)
    parser.add_argument('-r', '--read',
                        help='Reads tag to store them in a CSV file',
                        required=False)
    parser.add_argument('-t', '--taglist',
                        help='Prints list of all tags found in targeted files',
                        required=False)

    args = parser.parse_args()

    actions = {}

    if args.copyright != "":
        actions['set_copyright'] = args.copyright

    if args.author != "":
        actions['set_author'] = args.author

    if args.date != "":
        actions['set_date'] = args.date

    if args.keywords != "":
        actions['set_keywords'] = args.keywords

    # if args.taglist == "True":
    actions['print_tags'] = (args.taglist == "True")

    #if args.dryrun == "False":
    #    apply_changes = True
    return {"files": args.files, "actions": actions}

try:
    import argparse
except ImportError:
    if sys.version_info < (2, 7, 0):
        print("Error:")
        print("You are running an old version of python. Two options to fix the problem")
        print("  Option 1: Upgrade to python version >= 2.7")
        print("  Option 2: Install argparse library for the current python version")
        print("            See: https://pypi.python.org/pypi/argparse")

ARGUMENTS = parse_args()

FILES_OR_DIR = ARGUMENTS["files"]
ACTIONS = ARGUMENTS["actions"]
FILELIST = []
print("Files = ", FILES_OR_DIR)
for root, dirs, files in os.walk(FILES_OR_DIR):
    #print("Current directory", root)
    #print("Sub directories", dirs)
    #print("Files ", files)
    for file in files:
        FILELIST.append(root + "/" + file)

if not FILELIST:
    FILELIST.append(FILES_OR_DIR)


TAGLIST = {}

for file in FILELIST:
    print("Treating File = ", file)
    tags = file_tags.FileTags(file)
    tags.read()
    tags.print()
    if ACTIONS['set_copyright']:
        print("Setting copyright", ACTIONS['set_copyright'], "in file", file)
        tags.set_copyright(ACTIONS['set_copyright'])
    elif ACTIONS['set_date']:
        tags.set_date_picture_taken(ACTIONS['set_date'])
    elif ACTIONS['set_author']:
        tags.set_author(ACTIONS['set_author'])
    # elif ACTIONS['set_keywords']:
        # tags.set_keywords(keywords)
    elif ACTIONS['print_tags']:
        TAGLIST = tags.merge_tag_list(TAGLIST)
        ARRAYTAGS.append(tags.get_flat_tags())
        # print('-------------------------------------')
        # print(file)
        # print('-------------------------------------')
    if ACTIONS['set_copyright'] or ACTIONS['set_author'] or ACTIONS['set_date']:
        tags.write()

    # Print table of all files tags
if ACTIONS['print_tags']:
    for filetags in ARRAYTAGS:
        print(filetags["filename"], end=SEPARATOR)
        for tag in TAGLIST:
            if tag in filetags.keys():
                print(filetags[tag], end=SEPARATOR)
            else:
                print('', end=SEPARATOR)
            print("")
