#!/usr/bin/env python

import re
import sys
import os
import pdb
import datetime
import time

def match_headers(txtfile, match_string):
    pattern = re.compile(r'(^{}: )(.*)'.format(match_string), re.M)
    match = pattern.search(txtfile)
    content = match.group(2)

    return content

def convert_date(journal_date):
    converted_time = time.strptime(journal_date, "%B %d, %Y %I:%M %p")
    return time.strftime("<%Y-%m-%d %a>", converted_time)
    

if __name__ == "__main__":
    journalfile = open('journal01.txt', 'r')
    txt = journalfile.read()
    print convert_date(match_headers(txt, "Date"))
    print match_headers(txt, "Topic")
