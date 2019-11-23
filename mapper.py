#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re


def main():
    # list for storing years and months
    years =[]
    months = []
    
    # change abbreviation to string
    monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03','Apr': '04','May': '05','Jun': '06',
                 'Jul': '07','Aug': '08','Sep': '09','Oct': '10','Nov': '11','Dec': '12'}
    
    try:
        for line in sys.stdin:
            ## find year and month
            year = re.findall(r'\d{2}/\w{3}/(\d{4})',line)
            month = re.findall(r'\d{2}/(\w{3})/\d{4}',line)
            years.append(year[0])
            months.append(monthdict[month[0]])

    
    except EOFError:
        return None
    
    ## print result
    for i in range(0,len(years)):
        print(years[i]+'-'+months[i]+'\t1')
    
if __name__ == "__main__":
    main()

    


