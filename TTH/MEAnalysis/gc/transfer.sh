#!/bin/bash

source common.sh

# Go to work directory
cd $GC_SCRATCH

#print out the environment
env

#python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/JetTransfer.py
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/SubjetTransferAK8.py
#python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/TopSubjetTransfer.py





