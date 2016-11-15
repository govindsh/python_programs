# Python program to remind someone to take a break every 'x' hours
# Srikkanth Govindaraajan - https://github.com/govindsh

# Steps:
# Set number of breaks needed.
# sleep for 'x' hours
# open youtube URL for taking a break

# Library imports
import webbrowser
import time
from sys import argv

program_name,user = argv

# Variables
total_breaks=3;
break_count=0

while (break_count < total_breaks):
    print "Program %s started on "%program_name+time.ctime()
    time.sleep(2*60*60)
    print "Time for a break %s\n"%user
    time.sleep(5)
    webbrowser.open("https://www.youtube.com/watch?v=2mwj_IDzBts")
    break_count=break_count+1
print "Three breaks over for the day %s, thank you for using %s program"%(user,program_name)
