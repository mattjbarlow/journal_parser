#!/usr/bin/env python

import re
import sys
import os
import pdb
import datetime
import time
import textwrap
import argparse

def read_args():
    parser = argparse.ArgumentParser(description='Convert files to Org format.')
    parser.add_argument('--file', dest='ospath', help="path to file", required=True)
    return parser.parse_args()

def match_headers(txtfile, match_string):
    pattern = re.compile(r'(^{}: )(.*)'.format(match_string), re.M)
    match = pattern.search(txtfile)
    content = match.group(2)

    return content

def convert_date(journal_date):
    converted_time = time.strptime(journal_date, "%B %d, %Y %I:%M %p")
    return time.strftime("<%Y-%m-%d %a>", converted_time)

def fill_file(text):
    para_edge = re.compile(r"(\n\s*\n)", re.MULTILINE)
    paragraphs = para_edge.split(text)
    wrapped_file = []
    for para in paragraphs:
        wrapped_file.append(textwrap.fill(para, 70))

    return wrapped_file
    
def write_file(txt):
    topic = match_headers(txt, "Topic")
    date = match_headers(txt, "Date")
    wrapped_file = fill_file(txt)
    orgfilename = topic.replace(' ', '-') + ".org"
    header = re.compile(r'(Date|Topic): .*', re.M)
    
    f = open(orgfilename, 'w')
    f.write("* " + topic + "\n")
    f.write('<' + date + '>' + "\n")

    for para in wrapped_file:
        if re.match(header, para):
            pass
        else:
            f.write(para)
            f.write("\n")

    f.close()
    
if __name__ == "__main__":
    args = read_args()
    ospath = args.ospath
    journalfile = open(filename, 'r')
    txt = journalfile.read()
    write_file(txt)
