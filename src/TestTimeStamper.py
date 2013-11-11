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
        self.assert_(teststamper.starttime==timestamp, 'starttime is timestamp')
        self.assert_(teststamper.endtime==timestamp2, 'endtime is timestamp')
