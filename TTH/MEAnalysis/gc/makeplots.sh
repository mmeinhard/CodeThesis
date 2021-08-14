#!/bin/bash

source common.sh
cd $GC_SCRATCH

# Run Plotting
echo "Running plotting"
#python ${CMSSW_BASE}/src/TTH/Plotting/python/gregor/HiggsMasses.py 
python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/ObjectSync.py --cfg ${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg
#python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/btag/hists.py hists.root $FILE_NAMES

#hadd -f out.root hists.root
echo "Done plotting"




