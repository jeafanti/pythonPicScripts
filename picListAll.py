#!/usr/bin/python
#
# picListAll.py - Generate a file with all pictures files (all .jpg files under current directory)
#
# Example: 
#     C:\Users\joeea\Pictures>python c:\Users\joeea\Documents\python\picListAll.py
#     18359 Total Pictures Found.  see AllPics.txt
#
# Note: Run on a DOS command prompt windows. (not tested in cygwin)
#
import sys, getopt, re
import os
import time


# open file for all the duplicate picture names
allPicsfp = open("AllPics.txt","w")

# declare the picture name list
total = 0        # for putting total file entries at the end of the file

DupNamesDetected = 0
 
rootDir = '.'
for subdir, dirs, files in os.walk(rootDir):
    for file in files:
        # print os.path.join(subdir, file)
        path = os.path.realpath(subdir) + os.sep
        filepath = path + file

        # if is a picture file
        if file.endswith((".JPG", ".jpg")):
            total = total + 1
            allPicsfp.write(filepath + '\n')

allPicsfp.write("Total Pics: " + str(total))
allPicsfp.close()
# Print out the number of duplicate file names detected
print(str(total) + " Total Pictures Found.  see AllPics.txt")
