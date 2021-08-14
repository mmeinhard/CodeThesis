#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

#print out the environment
env

python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/nano_postproc.py --input $FILE_NAMES --skipEvents $SKIP_EVENTS --maxEvents $MAX_EVENTS
