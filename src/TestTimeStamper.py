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

import unittest, time
import TimeStamper

class TimeStamperUnitTest(unittest.TestCase):
    """TimeStamper unit tests"""
    def test_create(self):
        teststamper=TimeStamper.Stamper()
    def test_addtimestamp(self):
        teststamper=TimeStamper.Stamper()
        timestamp=time.time()
        teststamper.addStamp(timestamp)
        self.assert_(teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(teststamper.endtime==timestamp, 'endtime is timestamp')
    
    def test_periodupdate(self):
        teststamper=TimeStamper.Stamper()
        timestamp=10
        teststamper.addStamp(timestamp)
        self.assert_(teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(teststamper.endtime==timestamp, 'endtime is timestamp')
        timestamp2=20
        teststamper.addStamp(timestamp2)
        self.assert_(teststamper.starttime==timestamp, 'starttime is not updated')
        self.assert_(teststamper.endtime==timestamp2, 'endtime is timestamp')
        timestamp2=30
        teststamper.addStamp(timestamp2)
        self.assert_(teststamper.starttime==timestamp, 'starttime is not updated')
        self.assert_(teststamper.endtime==timestamp2, 'endtime is timestamp')

    def test_createperiod(self):
        teststamper=TimeStamper.Stamper()
        timestamp=10
        teststamper.addStamp(timestamp)
        self.assert_(teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(teststamper.endtime==timestamp, 'endtime is timestamp')
        timestamp2=20
        teststamper.addStamp(timestamp2)
        self.assert_(teststamper.starttime==timestamp, 'starttime is not updated')
        self.assert_(teststamper.endtime==timestamp2, 'endtime is timestamp')
        timestamp3=4000
        teststamper.addStamp(timestamp3)
        self.assert_(teststamper.starttime==timestamp3, 'starttime is timestamp')
        self.assert_(teststamper.endtime==timestamp3, 'endtime is timestamp')
        self.assert_(len(teststamper.timeranges)==1, 'old period is added to list')
        self.assert_(teststamper.timeranges[0] == (timestamp,timestamp2), 'verify the item')
    def test_addstamplist(self):
        teststamper=TimeStamper.Stamper()
        teststamper.addStamps([1000,1100,1200,1300,3200,3250,5500,6000])
        self.assert_(teststamper.starttime == 5500, 'current range is the last timestamps')
        self.assert_(teststamper.endtime == 6000, 'current range is the last timestamps')
        self.assert_(teststamper.timeranges == [(1000,1300),(3200,3250)], 'rest of the ranges are in list')