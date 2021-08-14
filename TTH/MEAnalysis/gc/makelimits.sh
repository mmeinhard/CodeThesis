#!/bin/bash

source common.sh
cd $GC_SCRATCH

# get the datacards/root files we need as input
cp ${datacardbase}/*.root .
cp ${datacardbase}/*.txt .

# Run MakeLimits
echo "Running MakeLimits"
echo ${analysis}
echo ${group}
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py --config ${analysis} --group ${group}
echo "Done MakeLimits"

ls -l .
