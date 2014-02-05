#!/usr/bin/env python

import re
import sys
import os
import pdb
import datetime
import time
import textwrap

def match_headers(txtfile, match_string):
    pattern = re.compile(r'(^{}: )(.*)'.format(match_string), re.M)
    match = pattern.search(txtfile)
    content = match.group(2)

    return content

def convert_date(journal_date):
    converted_time = time.strptime(journal_date, "%B %d, %Y %I:%M %p")
    return time.strftime("<%Y-%m-%d %a>", converted_time)
    
def fill_file(txtfile):
    return textwrap.fill(txtfile, 70)

def write_file(filename):
    journalfile = open(filename, 'r')
    txt = journalfile.read()
    topic = match_headers(txt, "Topic")
    date = match_headers(txt, "Date")
    filled_file = fill_file(txt)
    orgfilename = topic.replace(' ', '-') + ".org"
    end_header = re.compile(r'Topic: .*', re.M)
    journal_body = re.split(end_header, filled_file)[1]
    
    f = open(orgfilename, 'w')
    f.write("* " + topic + "\n")
    f.write(date + "\n")
    f.write(journal_body)
    f.close()
    
if __name__ == "__main__":
    journalfile = open('journal01.txt', 'r')
    txt = journalfile.read()
    print convert_date(match_headers(txt, "Date"))
    print match_headers(txt, "Topic")
