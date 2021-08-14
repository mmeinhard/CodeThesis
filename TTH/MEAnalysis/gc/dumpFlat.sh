#!/bin/bash
source common.sh
#go to work directory
cd $GC_SCRATCH

export PATH=/swshare/anaconda/bin/:$PATH
export PYTHONPATH=${CMSSW_BASE}/python:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed4/lib

python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/dumpFlat.py
