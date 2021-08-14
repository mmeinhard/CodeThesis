#!/bin/bash


export CMSSW_BASE=/mnt/t3nfs01/data01/shome/jpata/tth/sw-combine/CMSSW
export SCRAM_ARCH=slc6_amd64_gcc491
export USER=jpata
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $CMSSW_BASE
eval `scram runtime -sh`

#go to work directory
cd $GC_SCRATCH

#print out the environment
env

echo combine $FILE_NAMES -s ${SEED_0} -n seed_${SEED_0} \
    -M MaxLikelihoodFit -t 100 --minimizerStrategy=0 --minimizerTolerance=0.000001 --robustFit=0 --rMin -20 --rMax 20 \
    --expectSignal @SIG@ --noErrors --minos none

combine $FILE_NAMES -s ${SEED_0} -n seed_${SEED_0} \
    -M MaxLikelihoodFit -t 100 --minimizerStrategy=0 --minimizerTolerance=0.000001 --robustFit=0 --rMin -20 --rMax 20 \
    --expectSignal $SIG --noErrors --minos none
