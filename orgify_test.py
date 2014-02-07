import unittest
import orgify
import StringIO
import pdb

class OrgifyTests(unittest.TestCase):

    def setUp(self):
        journalfile = open('journal01.txt', 'r')
        self.txt = journalfile.read()
        
    def tearDown(self):
        pass

    def test_match_headers_returns_date(self):
        sample_date = orgify.match_headers(self.txt, "Date")
        self.assertEqual(sample_date, "November 20, 2005 8:59 AM")

    def test_match_headers_returns_topic(self):
        sample_topic = orgify.match_headers(self.txt, "Topic")
        self.assertEqual(sample_topic, "This is sample journal entry")

    def test_convert_date_returns_date(self):
        converted_time = orgify.convert_date("January 1, 2014 10:59 AM")
        self.assertEqual(converted_time, "<2014-01-01 Wed>")

    def test_fill_file_limits_columns(self):
        wrapped_file = orgify.fill_file(self.txt)
        for para in wrapped_file:
            s = StringIO.StringIO(para)
            for line in s:
                assert line.__len__() <= 71
        
