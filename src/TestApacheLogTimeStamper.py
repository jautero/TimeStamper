# TestApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import unittest, apachelog
import ApacheLogTimeStamper

class ApacheLogTimeStamperTest(unittest.TestCase):
    testtarget="/testtarget"
    testformat=apachelog.formats["extended"]
    def test_create(self):
        stamper=ApacheLogTimeStamper.ApacheLogTimeStamper(self.testtarget,self.testformat)
        self.assert_(stamper.gettarget==self.testtarget, 'stamper.gettarget is not %s: %s ' % (self.testtarget,stamper.gettarget))
        self.assert_(stamper.format==self.testformat, 'stamper.format is not %s: %s' % (self.testformat,stamper.format))