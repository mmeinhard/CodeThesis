#!/usr/bin/env python
#This script recursively adds root files in directories
# e.g. /a/b/c/output_*.root -> /a/b/c.root
from TTH.MEAnalysis.ParHadd import par_hadd
import glob
import sys
import os, fnmatch

#recurse over the given path
for path, dirs, files in os.walk(sys.argv[1]):
    #allow alternative destination
    if(len(sys.argv)>2):
        destination = sys.argv[2]
    else:
        destination = ""
    #Check if there are root files in this path
    rootfiles = filter(lambda x: x.endswith("root"), files)
    #If yes, this is a sample directory
    isSample = False
    if len(rootfiles)>0:
        isSample = True
    if not isSample:
        continue
    #Add the full path
    rootfiles = map(lambda f: os.path.join(path, f), rootfiles)

    print "adding", path
    #do the hadd (in parallel)
    if(destination == ""):
        par_hadd(path + ".root", rootfiles, 250, 10, 3)
    else:
        name = path.split("/")[-1]
        par_hadd(destination + name + ".root", rootfiles, 250, 10, 3)
