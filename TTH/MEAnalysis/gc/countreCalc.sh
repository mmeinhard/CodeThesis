#!/bin/bash
set -e
source common.sh

#go to work directory
cd $GC_SCRATCH

python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/reCalcCount.py out.root $FILE_NAMES
