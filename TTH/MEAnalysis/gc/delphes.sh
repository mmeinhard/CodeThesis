#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

#print out the environment
env

python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/Delphes_Analysis_heppy.py 
mv $GC_SCRATCH/Loop/tree.root out.root

echo $FILE_NAMES > inputs.txt

