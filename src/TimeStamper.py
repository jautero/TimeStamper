#!/usr/bin/env python
# TimeStamper.py TimeStamper library
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
import time

class Stamper:
    """Stamper class"""
    threshold=30*60
    def __init__(self):
            self.starttime=None
            self.endtime=None
            self.timeranges=[]
    def addStamp(self,timestamp=None):
        if timestamp==None:
            timestamp=time.time()
        if not self.starttime:
            self.starttime=timestamp
            self.endtime=timestamp
        if timestamp < self.endtime+self.threshold:
            self.endtime=timestamp
        else:
            self.timeranges.append((self.starttime,self.endtime))
            self.starttime=timestamp
            self.endtime=timestamp
    def addStamps(self,stampiterator):
        for stamp in stampiterator:
            self.addStamp(stamp)
