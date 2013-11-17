# TimeStamperTest.py -- Unit Tests for TimeStamper
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

import unittest, time, StringIO
import TimeStamper

class TimeStamperUnitTest(unittest.TestCase):
    """TimeStamper unit tests"""
    testlist=[1000,1100,1200,1300,3200,3250,5500,6000]
    def setUp(self):
        self.teststamper=TimeStamper.Stamper()

    def test_addtimestamp(self):
        timestamp=time.time()
        self.teststamper.addStamp(timestamp)
        self.assert_(self.teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(self.teststamper.endtime==timestamp, 'endtime is timestamp')
    
    def test_periodupdate(self):
        timestamp=10
        self.teststamper.addStamp(timestamp)
        self.assert_(self.teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(self.teststamper.endtime==timestamp, 'endtime is timestamp')
        timestamp2=20
        self.teststamper.addStamp(timestamp2)
        self.assert_(self.teststamper.starttime==timestamp, 'starttime is not updated')
        self.assert_(self.teststamper.endtime==timestamp2, 'endtime is timestamp')
        timestamp2=30
        self.teststamper.addStamp(timestamp2)
        self.assert_(self.teststamper.starttime==timestamp, 'starttime is not updated')
        self.assert_(self.teststamper.endtime==timestamp2, 'endtime is timestamp')

    def test_createperiod(self):
        timestamp=10
        self.teststamper.addStamp(timestamp)
        self.assert_(self.teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(self.teststamper.endtime==timestamp, 'endtime is timestamp')
        timestamp2=20
        self.teststamper.addStamp(timestamp2)
        self.assert_(self.teststamper.starttime==timestamp, 'starttime is not updated')
        self.assert_(self.teststamper.endtime==timestamp2, 'endtime is timestamp')
        timestamp3=4000
        self.teststamper.addStamp(timestamp3)
        self.assert_(self.teststamper.starttime==timestamp3, 'starttime is timestamp')
        self.assert_(self.teststamper.endtime==timestamp3, 'endtime is timestamp')
        self.assert_(len(self.teststamper.timeranges)==1, 'old period is added to list')
        self.assert_(self.teststamper.timeranges[0] == (timestamp,timestamp2), 'verify the item')

    def test_addstamplist(self):
        self.teststamper.addStamps(self.testlist)
        self.verify_aftertestlist()
        
    def verify_aftertestlist(self):
        self.assert_(self.teststamper.starttime == 5500, 'TimeStamper.starttime is not 5500: %d' % self.teststamper.starttime)
        self.assert_(self.teststamper.endtime == 6000, 'TimeStamper.endtime is not 6000: %d' % self.teststamper.endtime)
        self.assert_(self.teststamper.timeranges == [(1000,1300),(3200,3250)], 'timeranges are not (1000,1300) and (3200,3250): %s' % self.teststamper.timeranges)
        
    def test_addstampiterator(self):
        self.teststamper.addStamps((x for x in self.testlist))
        self.verify_aftertestlist()
    
    def test_readstampsfile(self):
        testfile=StringIO.StringIO()
        for stamp in self.testlist:
            testfile.write("%d\n" % stamp)
        testfile.seek(0)
        self.teststamper.readfile(testfile)
        self.verify_aftertestlist()
        
    def test_readstampsfilefilter(self):
        testfile=StringIO.StringIO()
        for stamp in self.testlist:
            testfile.write("%s\n" % time.ctime(stamp))
        testfile.seek(0)
        self.teststamper.readfile(testfile,lambda x:time.mktime(time.strptime(x.strip())))
        self.verify_aftertestlist()
