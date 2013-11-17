# TestApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import unittest, apachelog, StringIO
import ApacheLogTimeStamper

class ApacheLogTimeStamperTest(unittest.TestCase):
    testtarget="/AgileToolstracker"
    testformat=apachelog.formats["extended"]
    testtimestamp1=ApacheLogTimeStamper.parseTimestamp('[15/Nov/2013:23:40:07 -0800]')
    testtimestamp2=ApacheLogTimeStamper.parseTimestamp('[15/Nov/2013:23:41:07 -0800]')
    def setUp(self):
        self.stamper=ApacheLogTimeStamper.ApacheLogTimeStamper(self.testtarget,self.testformat)
    def test_created(self):
        self.assert_(self.stamper.matchString==("GET %s" % self.testtarget), 'self.stamper.gettarget is not GET %s: %s ' % (self.testtarget,self.stamper.matchString))
        self.assert_(self.stamper.parser, 'self.stamper.parser does not exist')
    def test_parselog(self):
        testfile=StringIO.StringIO('''82.181.196.220 - - [15/Nov/2013:23:40:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.228 - - [15/Nov/2013:23:41:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
''')
        self.stamper.parseLog(testfile)
        self.assert_(self.stamper.datalist[0] == self.testtimestamp1, "First data is not %s: %s" % (self.testtimestamp1,self.stamper.datalist[0]))
        self.assert_(self.stamper.datalist[1] == self.testtimestamp2, "Second data is not %s: %s" % (self.testtimestamp2, self.stamper.datalist[1]))
    def test_targetfilter(self):
        testfile=StringIO.StringIO('''208.115.111.66 - - [15/Nov/2013:01:27:14 -0800] "GET /LoremNSA/LoremNSA.php/Counter%20Terrorism%20Security/HIC HTTP/1.1" 200 12356 "-" "Mozilla/5.0 (compatible; Ezooms/1.0; ezooms.bot@gmail.com)" 
208.115.111.66 - - [15/Nov/2013:01:27:44 -0800] "GET /wiki/HIDO/Fuckspores?action=edit&restore=diff:1275486554:1275483372:&preview=y HTTP/1.1" 200 2507 "-" "Mozilla/5.0 (compatible; Ezooms/1.0; ezooms.bot@gmail.com)" 
199.21.99.80 - - [15/Nov/2013:01:28:14 -0800] "GET /LoremNSA/LoremNSA.php/312/TWA/b9/3/Ft.%20Meade HTTP/1.1" 200 0 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
82.181.196.220 - - [15/Nov/2013:23:40:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.228 - - [15/Nov/2013:23:41:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
''')
        self.stamper.parseLog(testfile)
        self.assert_(len(self.stamper.datalist)==2, 'parser caught more than 2 lines: %d' % len(self.stamper.datalist))
        self.assert_(self.stamper.datalist[0] == self.testtimestamp1, "First data is not %s: %s" % (self.testtimestamp1,self.stamper.datalist[0]))
        self.assert_(self.stamper.datalist[1] == self.testtimestamp2, "Second data is not %s: %s" % (self.testtimestamp2, self.stamper.datalist[1]))

class ApacheLogTimestampParserTest(unittest.TestCase):
    def test_zero(self):
        self.assert_(0==ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:00:00:00 +0000]"), 'Start of epoch is not 0: %d' % ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:00:00:00:00 +0000]"))
    def test_one(self):
        parsedStamp=ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:00:00:01 +0000]")
        self.assert_(1==parsedStamp, 'Second after epoch has not timestamp 1, but %d' % parsedStamp)
    def test_timezone(self):
        parsedStamp=ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:02:01:00 +0200]")
        self.assert_(60==parsedStamp, 'Minute after epoch in Finland is not 60, but: %d' % parsedStamp)