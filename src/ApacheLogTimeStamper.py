# ApacheLogTimeStamper.py
#
# Parse gets for given URL and use them to generate timestamps.
#
import apachelog

class ApacheLogTimeStamper:
    def __init__(self,gettarget,logformat):
        self.gettarget=gettarget
        self.logformat=logformat
    def parseLog(self,logline):
        """Parse logfile"""
        parser=apachelog.parser(self.logformat)
        self.data=parser.parse(logline)
    
        
def main():
    pass
    
if __name__ == '__main__':
    main()