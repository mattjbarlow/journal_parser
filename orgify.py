#!/usr/bin/env python

import re
import sys
import os
import pdb

def split_lines(txtfile):
    pattern = re.compile(r'(^Date: )(.*)')
    match = pattern.match(txtfile)
    date = match.group(2)

    pattern = re.compile(r'(^Topic: )(.*)', re.M)
    match = pattern.search(txtfile)
    topic = match.group(2)

    print "Date is {} and Topic is {}".format(date, topic)

if __name__ == "__main__":
    journalfile = open('journal01.txt', 'r')
    txt = journalfile.read()
    split_lines(txt)
