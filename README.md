# pythonPicScripts
Phython scripts to help clean up my pictures folder. (Novice python)


Python Picture scripts
-----------------------

Best way to use the picture scripts
-----------------------------------

o Open up 2 DOS windows
o Put the windows so there is a upper one and a lower one.
o In the upper window cd into the Pictures direcotry "C:\Users\joeea\Pictures>"
o In the lower window cd into the directory with the pictures scripts i.e "C:\Users\joeea\Documents\python>"
o In th upper window execute the python scripts that create picture files
    (picListAll.py, picListSameName.py, or picListSameSize.py)
  Example:
    // Generate the sameName.txt File 
    C:\Users\joeea\Pictures>python c:\Users\joeea\Documents\python\picListSameName.py
o After you have generated one of the picture list test files (AllPics.txt, sameName.txt, or sameSize.txt)
o Goto the lower window and use the ShowPhoto scripts (ShowPhotoList.py, ShowPhotoListRand.py)
  Example:
    // To Display the pictures in the sameName.txt File
    C:\Users\joeea\Documents\python>python ShowPhotoList.py c:\Users\joeea\Pictures\sameName.txt


Checked in python picture scripts to github.
--------------------------------------------

(www.github.com  jeafanti  'joe code')

Checked in from the directory ~/Documents/Joe/Python

Used a Git Bash windows to exersize the following commands:
(Clicked on the 'Git Bash' desktop icon)


$ git init   // creates the .git directory make this directory ready for git usage
// set up some git config stuff
$ git config --global user.name "Joe Eafanti"
$ git config --global user.email 'joe.eafanti@gmail.com'
$ git config --global core.editor vim
$ git config --list  // Show the git config info

// Copied the files I wanted to check in into the git directory
$ git add picListAll.py  // Add this file to the repository
$ git status  // check repository status
$ git add .   // add all files to the repository
$ git commit  // commit all staged changes (requires comment)
$ git commit -m 'made changes to the file headers'

# Created a repository in github
$ git remote
// github will supply you with this https link. 
$ git remote add origin https://github.com/jeafanti/pythonPicScripts.git
$ git push -u origin master  // push all the code changes to github repository

// to turn off the following warnings
<warning: LF will be replaced by CRLF in ShowPhotoList.py.
The file will have its original line endings in your working directory.>
// typ the following command
$ git config core.autocrlf true

