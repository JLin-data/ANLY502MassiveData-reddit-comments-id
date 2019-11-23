#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys

if __name__ == '__main__':
    
    current_dateS = None
    current_count = 0 
    dateS = None 

    for line in sys.stdin:         
        line = line.strip()
        dateS, count = line.split('\t',1)
        try:            
            count = int(count)      
        except:
            continue
    
     #           if current_dateS == dateS:
        if (dateS == current_dateS):
            current_count += count
        else:
            if current_dateS:
                sys.stdout.write("{},{}\n".format(current_dateS, current_count))
               # print('%s\t%s' % (current_dateS, current_count))
            current_dateS = dateS
            current_count = count
    
    if dateS == current_dateS:
        sys.stdout.write("{},{}\n".format(current_dateS, current_count))
     #print('%s\t%s' % (current_dateS, current_count))
