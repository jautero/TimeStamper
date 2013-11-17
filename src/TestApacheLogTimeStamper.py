# TestApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import unittest
import ApacheLogTimeStamper

class ApacheLogTimeStamperTest(unittest.TestCase):
    def test_create(self):
        stamper=ApacheLogTimeStamper.ApacheLogTimeStamper("/testtarget")
        