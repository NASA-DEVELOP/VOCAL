#!/opt/local/bin/python2.7
#
#   PCF_genTimeUtils.py
#   Brian Magill
#   5/9/2014
#
#   Tools for manipulating and determining dates and times for filling in
#   Level 2 PCF's
#
import re

def fixISO_format(date_time):

#   Perhaps there are more elegant ways to do this but this will work for now

    parse = re.compile("(\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2})") 
    date_list = parse.match(date_time)
    
    if date_list == None: 
        return None
    fix_isoStr = "%s-%s-%sT%s:%s:%s" % date_list.groups()
    
    return fix_isoStr   

def calipsoISO_to_times(iso_date_time):

    "Returns (year, month, day, hour, minute, sec)"
    parse = re.compile("(\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2})") 
    date_list = parse.match(iso_date_time)

    if date_list == None:
        return None

    (year, month, day, hour, minute, sec) = map(int, date_list.groups())
    
    return (year, month, day, hour, minute, sec)

def extractDatetime(name):

#    result = re.search("(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})Z(\w)", "A2010-10-01T02-48-44ZN")    
    result = re.search("(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})Z(\w)", name)
    if result == None:
        return None
    granuleDatetime = result.groups()
    
    return granuleDatetime
    
        
if __name__ == "__main__":

    testDate = "2012-03-05T23-13-06"
#    testDate = "2010-10-01T02-48-44"
    
    print testDate, " => ", fixISO_format(testDate) 
    print testDate, " => ", calipsoISO_to_times(testDate) 

    filename = "CAL_LID_L1-ValStage1-V3-01.2010-10-01T02-48-44ZD.hdf"
    
    print filename, " => ", extractDatetime(filename)
    
    
    
        
#from dateutil.parser import *
#In [10]: parse("2003-09-25T10:49:41ZN")
#Out[10]: datetime.datetime(2003, 9, 25, 10, 49, 41)
#
#In [11]: import re
#
#In [20]: myPattern = re.compile(r'T(\d{2})-(\d{2})-(\d{2})')
#In [22]: myPattern.search("T12-03-57").groups()
#Out[22]: ('12', '03', '57')
