#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

# Make sure we process all events (as currently using file based splitting)
# Change back if we go to event bases
export SKIP_EVENTS=0
export MAX_EVENTS=9999999999

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
#export SKIP_EVENTS=0
#export MAX_EVENTS=200
#export DATASETPATH=__JetHT
#export FILE_NAMES=root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/koschwei/tth/ttH_AH_v1/JetHT/ttH_AH_v1/180522_140221/0000/tree_330.root
#export GC_SCRATCH=./


#print out the environment
env

#python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg
python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/config_FH.cfg

mv $GC_SCRATCH/Loop/tree.root out.root

echo $OFNAME > output.txt

