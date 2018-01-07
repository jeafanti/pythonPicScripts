# OpenCV (Open Source Computer Vision Library: http://opencv.org)
#
# photoList.py:
#   o Takes a parameter of a file containing a list of photos
#   o Sequencially displays the list of photos one at a time
#   o The user can use the arrow keys to go back and forth in the list
#   o The user can use 'd' to delete any unwanted photos
#   QUESTION: Do deleted photos end up in the recycle bin??
#
# Usage: python photoList.py picList.txt
#

import sys
import os
from os import path
import re
import numpy as np
import cv2
import ctypes
import subprocess
from PIL import Image

maxHeight = 955
maxWidth = 1900
rightArrow = 2555904
leftArrow =  2424832
deleteKey = 3014656

argc = len(sys.argv)
argv = list(sys.argv)

usage = 0

if (argc == 1):
    usage = 1
elif (argc == 2):
    fp = open(argv[1],"r")
    # check to make sure that the file was opened
    if (fp.mode != 'r'):
        usage = 1
        print("Error: Could not open file ", argv[1])
    else:
        fp.close()
        pictureFile = argv[1]
elif (argc > 2):
    usage = 1

if usage == 1:
    print("USAGE: python photoList.py <picList.txt>")
    exit(-1)



# declare the file index list 
fileIndex = []
fileNames = []


# hard code where to look for the pictures (DOS)
# rootDir = 'C:/Users/joeea/Pictures'
# rootDir = 'C:/Users/joeea/Documents/python'
rootDir = '.'


def readPicListFile():
    fp = open(pictureFile,"r")
    # check to make sure that the file was opened
    if (fp.mode != 'r'):
        print("Error: Could not open file ", argv[2])
        exit(-1)
    lc = 0
    line = fp.readline()

    while line:
        matchObj = re.search('^Total:', line)
        if matchObj:
            break
        lc = lc + 1
        fileNames.append(line.strip())
        line = fp.readline()
    fp.close()
    return lc


# create linear index list.
def setLinearIndexList(picCount):
    # no argument seeds from current time
    for ii in range(0,picCount):
        fileIndex.append(ii)


# remove all references to this index from random stream
# Only applicable when not using uniform=True on getPicIndexList
def removeAll(list, item):
    newlist = []
    for ii in list:
        if ii != item:
            newlist.append(ii)
    return newlist

# calculate what the multiplier should be so the entire picture can be displayed on the screen
def calcMultiplier(curr,desired):
    mult = 0.99
    value = int(curr * mult)
    while value > desired:
        mult = mult - 0.01
        value = int(curr * mult)
    # print("mult=",mult)
    return mult

# figure out if hight or width is what needs to be reduced to display a pic, then call calcMultiplier
def getMultiplier(height,width):
    heightDiff = 0
    widthDiff = 0
    if height > maxHeight:    
        heightDiff = height - maxHeight
    if width > maxWidth:    
        widthDiff = width - maxWidth
    if widthDiff > heightDiff:
        mult = calcMultiplier(width,maxWidth)
    else:
        mult = calcMultiplier(height,maxHeight)
    # print ("mult = ",mult)
    return mult




# Main - Where the program starts execution
if __name__ == "__main__":

    picCount = readPicListFile()
    # sets up the fileIndex list
    setLinearIndexList(picCount)

    mainIndex = 0
    numEntries = picCount
    invalid_key = False

    while True:
        if not invalid_key:
            if (mainIndex >= numEntries):
                mainIndex = 0
            picFile = fileNames[fileIndex[mainIndex]]
            # picFile = picFile.strip()
            print(mainIndex, " ", fileIndex[mainIndex], " ", picFile)
            src = path.realpath(picFile)
            # get the file path and the file name from src string
            fpath, fname = path.split(src)
            # get the folder name from the path to display on window
            temp, folder = path.split(fpath)

            img = cv2.imread(picFile,1)
            height,width,channels = img.shape
            winName = fname + " " + str(height) + "x" + str(width) + " Folder: " + folder

            if ((height > maxHeight) or (width > maxWidth)):
                mult = getMultiplier(height,width)
                # img_half = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
                img_half = cv2.resize(img, (0,0), fx=mult, fy=mult)
                height,width,channels = img_half.shape
                # print("newHeight=",newH," newWidth=",newW)
                cv2.imshow(winName,img_half)
            else:
                cv2.imshow(winName,img)
            x = int(maxWidth/2) - int(width/2)
            cv2.moveWindow(winName,x,5) 

            # print(img.shape)

        # key = cv2.waitKey(0)
        # wait for extended key set
        key = cv2.waitKeyEx(0)

        # if ESC key to exit
        if key == 27:
            cv2.destroyAllWindows()
            exit(0)
        # if 'd' delete pic
        elif key == ord('d') or key == deleteKey:
            # remove all references to this index from random stream
            fileIndex = removeAll(fileIndex,fileIndex[mainIndex])
            # flip the forward slashes to back slashes for subprocess call
            dosf = picFile.replace('/','\\')
            subprocess.call(["del","/F",dosf],shell=True)
            cv2.destroyWindow(winName)
            invalid_key = False
            # check how many entries there are left in the index list
            numEntries = len(fileIndex)
            print("delete ", picFile)
            if (numEntries == 0):
                print("All files deleted! Exiting\n")
                exit(0)
        # if 'm' move pic to new filename
        elif key == ord('m'):
            # name = raw_input("new file name? ")
            condition = True
            while condition:
                name = input("Enter new file name for " + fname + ": ")
                src = path.realpath(fpath + os.sep + name)
                if (path.exists(src)):
                    print("Error: File " + name + " already exists\n")
                else:
                    print("path checked = " + src)
                    condition = False
            # flip the forward slashes to back slashes for subprocess call
            dosf = picFile.replace('/','\\')
            print("rename " + dosf + " " + name)
            subprocess.call(["rename",dosf,name],shell=True)
            fileNames[fileIndex[mainIndex]] = src
            cv2.destroyWindow(winName)
        # if 'n' or right arrow, next pic
        elif key == ord('n') or key == rightArrow:
            mainIndex = (mainIndex + 1) % numEntries   
            cv2.destroyWindow(winName)
            invalid_key = False
        # if 'p' or left arrow, previous pic
        elif key == ord('p') or key == leftArrow:
            cv2.destroyWindow(winName)
            if mainIndex == 0:
                mainIndex = numEntries - 1
            else:
                mainIndex = mainIndex - 1
            invalid_key = False
        # if 'r' rotate pic clockwise
        elif key == ord('r'):
            # next 2 lines work almost perfectly, except that you can end up with a thin black line around the image
            # rimg = rotate_bound(img,90)
            # cv2.imwrite(picFile,rimg,[cv2.IMWRITE_JPEG_QUALITY,100]) # 100 is highest quality
            # code is using a PIL/Pillow library call rotate() to rotate the images.
            # This does a good job, leaving no boarder, however it can drastically reduce the size (not the resolution)
            # of the picture.  This is probably OK unless it is a super important picture.
            # Let's use PIL/Pillow Image call open, to open the picture for a rotate
            pilimg = Image.open(picFile)
            # expand=True disables cropping
            pilimg = pilimg.rotate(-90, resample=Image.BICUBIC,expand=True)
            pilimg.save(picFile)
            cv2.destroyWindow(winName)
            # cv2.imshow("ROTATED",rimg)
            invalid_key = False
        # any key entered, that is not a special case above, just exit?
        else:
            invalid_key = True
            print("Invalid key=",key)

