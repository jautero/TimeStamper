#!/usr/bin/env python
# ApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
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
#

import apachelog, datetime, TimeStamper, time, os

stamperstore=os.path.expand("~/Dropbox/apachelog.json")

class ApacheLogTimeStamper:
    def __init__(self,gettarget,logformat):
        self.parser=apachelog.parser(logformat)
        self.matchString="GET %s"%gettarget
        self.stamper=TimeStamper.Stamper()

    def parseLog(self,logfile):
        """Parse logfile"""
        self.stamper.readfile(logfile,self.logfilter,self.logselector)
        
    def getTimeranges(self):
        self.stamper.closeStamper()
        return self.stamper.timeranges
    

    def logfilter(self, logline):
        """Filter for stamper.readfile"""
        data=self.parser.parse(logline)
        return parseTimestamp(data["%t"])

    def logselector(self, logline):
        """Selectior for stamper.readfile"""
        data=self.parser.parse(logline)
        return data["%r"][:len(self.matchString)] == self.matchString

def parseTimestamp(logTimestamp):
    """convert timestamp string to unix timestamp"""
    timeTuple=apachelog.parse_date(logTimestamp)
    datelist=[]
    index=0
    for width in [4,2,2,2,2,2]:
        datelist.append(int(timeTuple[0][index:index+width]))
        index+=width
    resultDate=datetime.datetime(*datelist)
    if timeTuple[1][0]=="-":
        multiplier=1
    else:
        multiplier=-1
    resultDate=resultDate + multiplier * datetime.timedelta(minutes=int(timeTuple[1][-2:]),hours=int(timeTuple[1][1:3]))
    timeDelta=(resultDate-datetime.datetime(1970,1,1))
    return timeDelta.days*86400+timeDelta.seconds

def main(argc,argv):
    if (argc>2):
        format=apachelog.formats[argv[2]]
    else:
        format=apachelog.formats["extended"]
    if (argc>1):
        fh=file(argv[1])
    else:
        fh=sys.stdin
    stamper=ApacheLogTimeStamper(argv[0],format)
    storefile=file(stamperstore)
    stamper.stamper.load(storefile)
    storefile.close()
    stamper.parseLog(fh)
    totaltime=0
    for timerange in stamper.getTimeranges():
        timediff=timerange[1]-timerange[0]
        totaltime += timediff
        print time.ctime(timerange[0]),timediff
    storefile=file(stamperstore,"w")
    stamper.stamper.store(storefile)
    storefile.close()
    print totaltime
    
if __name__ == '__main__':
    import sys, os.path
    argc=len(sys.argv)-1
    if argc<1 or argc>3:
        print >>sys.stderr, "Usage:"
        print >>sys.stderr, "\t%s <getpath> [ <file> [ <format> ] ]" % os.path.basename(sys.argv[0])
        sys.exit(1)
    main(argc,sys.argv[1:])
