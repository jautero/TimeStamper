# ApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import apachelog, datetime

class ApacheLogTimeStamper:
    def __init__(self,gettarget,logformat):
        self.parser=apachelog.parser(logformat)
        self.matchString="GET %s"%gettarget
        self.datalist=[]

    def parseLog(self,logfile):
        """Parse logfile"""
        for logline in logfile:
            data=self.parser.parse(logline)
            if data["%r"][:len(self.matchString)] == self.matchString:
                self.datalist.append(parseTimestamp(data["%t"]))
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

def main():
    pass
    
if __name__ == '__main__':
    main()