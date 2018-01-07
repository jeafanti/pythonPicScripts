#!/usr/bin/python
#
# python /cygdrive/c/Users/joeea/Documents/python/picSameName.py
# C:\Users\joeea\Pictures>python C:\Users\joeea\Documents\python\picSameName.py
#   Python 3.0 Removed. dict.has_key() – use the in operator instead.
#
import sys, getopt, re
import os
import time


# open file for all the duplicate picture names
sameNamefp = open("sameName.txt","w")

# declare the picture name list
picName = {}     # list of all the files (not yet determined as a duplicate)
fileList = []    # list for all duplicate files
foundTwice = {}  # Boolean Hash table to determine when original file should be added
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
            # print filepath, "size: ", os.path.getsize(filepath), " time: ",time.ctime(os.path.getmtime(filepath))
            # print(path)
            # or os.stat(filepath).st_size
            # See: https://docs.python.org/3/library/os.html#os.stat for more attribuites

            # if the file name already exist as a picName index
            if (file in picName):
                if (file not in foundTwice):
                    # add the previously discovered file to duplicate fileList
                    fileList.append(file + os.sep + picName[file] + file + '\n')
                    foundTwice[file] = True
                # Add the current file to the duplicate fileList
                fileList.append(file + os.sep + filepath + '\n')
                # increment the duplicate name counter
                DupNamesDetected = DupNamesDetected + 1
            # else, not a duplicate name
            else:
                # add to the picture list
                picName[file] = path

slist = sorted(fileList)
for filepath in slist:
    stripfile = re.sub(".*C:",'C:',filepath)
    sameNamefp.write(stripfile)
    total = total + 1
sameNamefp.write("Total: " + str(total))
sameNamefp.close()
# Print out the number of duplicate file names detected
print(DupNamesDetected, " Duplicate Names Detected, see sameName.txt")
