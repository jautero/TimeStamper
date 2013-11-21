#!/usr/bin/env python
#
# UpdateProjectTimeStamp.py
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

import os.path, ApacheLogTimeStamper, apachelog, datetime, sys

GetPath = "/TimeStampers/%s"
StoreFile = os.path.expanduser("~/Dropbox/TimeStampers/%s.json")
accesslogpath="jaguars.dreamhost.com:logs/jautero.net/http/"
logformat=apachelog.formats["extended"]

def load_parser(name):
    parser=ApacheLogTimeStamper.ApacheLogTimeStamper(GetPath%name,logformat)
    try:
        storefile=file(StoreFile%name)
        parser.stamper.load(storefile)
        storefile.close()
    except:
        pass
    return parser

def get_access_log_name():
    remotepath=os.path.join(accesslogpath,"access.log.0")
    return remotepath
    
def fetch_logfile(remotepath):
    scp_result=os.system("scp %s access.log" % remotepath)
    if scp_result != 0:
        sys.exit(scp_result)
    return file("access.log")
    
def store_parser(name,parser):
    parser.stamper.store(file((StoreFile%name),"w"))

def update_project(projectname):
    timestampparser=load_parser(projectname)
    logFileHandle=fetch_logfile(get_access_log_name())
    timestampparser.parseLog(logFileHandle)
    store_parser(projectname,timestampparser)

if __name__ == '__main__':
    if len(sys.argv)==2:
        update_project(sys.argv[1])
