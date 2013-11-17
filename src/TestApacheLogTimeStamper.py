# TestApacheLogTimeStamper.py
#
# Test ApacheLogTimeStamper.py
#
# Copyright (C) 2013 Juha Autero <jautero@iki.fi>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        self.check_stamper()
    def check_stamper(self):
        self.assert_(len(self.stamper.stamper.timeranges)==0, 'stamper.stamper.timeranges not empty: %d' % len(self.stamper.stamper.timeranges))
        self.assert_(self.stamper.stamper.starttime == self.testtimestamp1, "starttime is not %s: %s" % (self.testtimestamp1,self.stamper.stamper.starttime))
        self.assert_(self.stamper.stamper.endtime == self.testtimestamp2, "endtime is not %s: %s" % (self.testtimestamp2, self.stamper.stamper.endtime))

    def test_targetfilter(self):
        testfile=StringIO.StringIO('''208.115.111.66 - - [15/Nov/2013:01:27:14 -0800] "GET /LoremNSA/LoremNSA.php/Counter%20Terrorism%20Security/HIC HTTP/1.1" 200 12356 "-" "Mozilla/5.0 (compatible; Ezooms/1.0; ezooms.bot@gmail.com)" 
208.115.111.66 - - [15/Nov/2013:01:27:44 -0800] "GET /wiki/HIDO/Fuckspores?action=edit&restore=diff:1275486554:1275483372:&preview=y HTTP/1.1" 200 2507 "-" "Mozilla/5.0 (compatible; Ezooms/1.0; ezooms.bot@gmail.com)" 
199.21.99.80 - - [15/Nov/2013:01:28:14 -0800] "GET /LoremNSA/LoremNSA.php/312/TWA/b9/3/Ft.%20Meade HTTP/1.1" 200 0 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
82.181.196.220 - - [15/Nov/2013:23:40:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.228 - - [15/Nov/2013:23:41:07 -0800] "GET /AgileToolstracker HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
''')
        self.stamper.parseLog(testfile)
        self.check_stamper()

class ApacheLogTimestampParserTest(unittest.TestCase):
    def test_zero(self):
        self.assert_(0==ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:00:00:00 +0000]"), 'Start of epoch is not 0: %d' % ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:00:00:00:00 +0000]"))
    def test_one(self):
        parsedStamp=ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:00:00:01 +0000]")
        self.assert_(1==parsedStamp, 'Second after epoch has not timestamp 1, but %d' % parsedStamp)
    def test_timezone(self):
        parsedStamp=ApacheLogTimeStamper.parseTimestamp("[01/Jan/1970:02:01:00 +0200]")
        self.assert_(60==parsedStamp, 'Minute after epoch in Finland is not 60, but: %d' % parsedStamp)

class ApacheLogTimeStamperRangeTest(unittest.TestCase):
    """docstring for ApacheLogTimeStamperTest"""
    def __init__(self, arg):
        super(ApacheLogTimeStamperRangeTest, self).__init__(arg)
        self.testfile=StringIO.StringIO('''82.181.196.220 - - [15/Nov/2013:23:40:07 -0800] "GET /teststamper HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.220 - - [15/Nov/2013:23:41:07 -0800] "GET /teststamper HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.220 - - [15/Nov/2013:23:41:37 -0800] "GET /teststamper HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.220 - - [15/Nov/2013:23:42:00 -0800] "GET /teststamper HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.220 - - [16/Nov/2013:02:00:00 -0800] "GET /teststamper HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"
82.181.196.220 - - [16/Nov/2013:02:15:00 -0800] "GET /teststamper HTTP/1.1" 404 1018 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36"''')

    def setUp(self):
        self.testfile.seek(0)
        self.stamper=ApacheLogTimeStamper.ApacheLogTimeStamper("/teststamper",apachelog.formats["extended"])

    def test_timeranges(self):
        self.stamper.parseLog(self.testfile)
        self.assert_(len(self.stamper.stamper.timeranges)==1, 'Number of timeranges is not 1: %s' % len(self.stamper.stamper.timeranges))
        timerange=self.stamper.stamper.timeranges[0]
        testrange=(ApacheLogTimeStamper.parseTimestamp('[15/Nov/2013:23:40:07 -0800]'),ApacheLogTimeStamper.parseTimestamp('[15/Nov/2013:23:42:00 -0800]'))
        self.assert_(timerange==testrange, 'Incorrect timerange: %s (not %s)' % (timerange,testrange))
        teststarttime=ApacheLogTimeStamper.parseTimestamp('[16/Nov/2013:02:00:00 -0800]')
        testendtime=ApacheLogTimeStamper.parseTimestamp('[16/Nov/2013:02:15:00 -0800]')
        self.assert_(self.stamper.stamper.starttime == teststarttime, 'stamper.starttime is not %d: %d' % (teststarttime,self.stamper.stamper.starttime))
        self.assert_(self.stamper.stamper.endtime == testendtime, 'stamper.endtime is not %d: %d' % (testendtime,self.stamper.stamper.endtime))
