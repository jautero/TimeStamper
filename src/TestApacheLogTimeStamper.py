# TestApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import unittest, apachelog
import ApacheLogTimeStamper

class ApacheLogTimeStamperTest(unittest.TestCase):
    testtarget="/testtarget"
    testformat=apachelog.formats["extended"]
    def setUp(self):
        self.stamper=ApacheLogTimeStamper.ApacheLogTimeStamper(self.testtarget,self.testformat)
    def test_created(self):
        self.assert_(self.stamper.gettarget==self.testtarget, 'self.stamper.gettarget is not %s: %s ' % (self.testtarget,self.stamper.gettarget))
        self.assert_(self.stamper.logformat==self.testformat, 'self.stamper.logformat is not %s: %s' % (self.testformat,self.stamper.logformat))
    def test_parselog(self):
        self.stamper.parseLog('82.181.196.220 - - [15/Nov/2013:23:40:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"')
        self.assert_(self.stamper.data['%h'], '82.181.196.220')