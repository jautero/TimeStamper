# ApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import apachelog

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
                self.datalist.append(data["%t"][1:-1])

def main():
    pass
    
if __name__ == '__main__':
    main()