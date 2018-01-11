#!/usr/bin/python
#
#
# picListSameSize.py - Generate a text file listing all the picture files, under current directory,
#                      that are the same size.
#                      This is intended to help find duplicate pictures so that they can be deleted.
#
# Example: 
#     C:\Users\joeea\Pictures>python c:\Users\joeea\Documents\python\picListSameSize.py
#     18 Duplicate Size Detected.  see sameSize.txt
#
# Note: The generated text file is intended to be used with the ShowPhotoList.py python script,
#       which will display, one by one, all the pictures contained in the file.
#
# Note: Run on a DOS command prompt windows. (not tested in cygwin)
#
# Note:  Python 3.0 Removed. dict.has_key() – use the 'in' operator instead.
#
import sys, getopt, re
import os
import time


# open file for all the duplicate picture names
sameSizefp = open("sameSize.txt","w")

# declare the picture name list
picName = {}  # Hash table index: filesize, entry: pathfile
fileList = []
foundTwice = {}
total = 0

DupSizesDetected = 0

def sortSize(str):
    num = re.search(r'(^\d*)',str)
    return int(num.group(1))
 
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

            # Get the file size
            fsize = os.path.getsize(filepath)

            # if the file size already exist as a picName index
            if (fsize in picName):
                # if have not already seen this file size
                if (fsize not in foundTwice):
                    # add the previously discovered file to duplicate fileList (pre add file size for sorting)
                    fileList.append(str(fsize) + os.sep + picName[fsize] + '\n')
                    foundTwice[fsize] = True
                # add current file name to the duplicate fileList (pre add file size for sorting)
                fileList.append(str(fsize) + os.sep + filepath + '\n')
                DupSizesDetected = DupSizesDetected + 1
            else:
                picName[fsize] = filepath

# sort the list by file name
slist = sorted(fileList, key=sortSize)
for filepath in slist:
    # strip off the file size that you added to the front for sorting
    stripfile = re.sub(".*C:",'C:',filepath)
    sameSizefp.write(stripfile)
    total = total + 1
sameSizefp.write("Total: " + str(total))
sameSizefp.close()
print(DupSizesDetected, " Duplicate Sizes Detected, see sameSize.txt")
