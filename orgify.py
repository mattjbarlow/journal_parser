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

def fix_date(txtfile):
    old_date = re.search(r'(<)(.*)(>)', txtfile)
    fixed_date = convert_date(old_date.group(2))
    return re.sub(r'(<)(.*)(>)', fixed_date, txtfile)

def fix_files(journal_dir):
    for journal in os.listdir(journal_dir):
        f = open(os.path.join(journal_dir, journal), 'r')
        txt = f.read()
        newtxt = fix_date(txt)
        f = open(os.path.join(journal_dir, journal), 'w')
        f.write(newtxt)
        f.close()
        
def fill_file(text):
    para_edge = re.compile(r"(\n\s*\n)", re.MULTILINE)
    paragraphs = para_edge.split(text)
    wrapped_file = []
    for para in paragraphs:
        wrapped_file.append(textwrap.fill(para, 70))

    return wrapped_file

def parse_all_journals(text):
    journal_edge = re.compile(r"(^Date: .*$\nTopic: .*$)", re.MULTILINE)
    journals = journal_edge.split(text)
    header = re.compile(r'(Date|Topic): .*', re.M)
    journal_file = []
    journal_file.append(journals[0])
    for journal in journals:
        if re.match(header, journal):
            journal_file.append(journal)
        else:
            journal_file[-1] += journal

    journal_file.pop(0)
    return journal_file
    
def write_file(txt):
    topic = match_headers(txt, "Topic")
    date = match_headers(txt, "Date")
    wrapped_file = fill_file(txt)
    orgfilename = re.sub(r'[!?\\\'/]', '', topic)
    orgfilename = orgfilename.replace(' ', '-') + ".org"

    if orgfilename in os.listdir('.'):
        while orgfilename in os.listdir('.'):
            print "{} already exists. Choose another name: ".format(orgfilename)
            orgfilename = raw_input()

    header = re.compile(r'(Date|Topic): .*', re.M)
    
    f = open(orgfilename, 'w')
    f.write("* " + topic + "\n")
    f.write(convert_date(date) + "\n")

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
    whole_journal = open(ospath, 'r')
    txt = whole_journal.read()
    journal_files = parse_all_journals(txt)

    for journal in journal_files:
        write_file(journal)
