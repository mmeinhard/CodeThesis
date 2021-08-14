#!/bin/bash

source common.sh
#go to work directory
cd $GC_SCRATCH

touch out.json
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/dumpMEEvents.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg > out.json
