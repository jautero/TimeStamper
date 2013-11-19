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
import time, json

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
    def closeStamper(self):
        if self.starttime != None and self.starttime != self.endtime:
            self.timeranges.append((self.starttime,self.endtime))
        self.starttime=None
        self.endtime=None
    def store(self,storefile):
        storedata={"timeranges": self.timeranges, "starttime": self.starttime, "endtime": self.endtime}
        storefile.write(json.dumps(storedata))
    def load(self, storefile):
        storedata=json.loads(storefile.read())
        self.timeranges=[(timerange[0],timerange[1]) for timerange in storedata["timeranges"]]
        self.starttime=storedata["starttime"]
        self.endtime=storedata["endtime"]
    
    def readfile(self,file,processor=int,selector=lambda x:True):
        self.addStamps((processor(line) for line in file.readlines() if selector(line)))
