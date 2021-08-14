#!/bin/bash
source common.sh
cd $GC_SCRATCH
#MAX_EVENTS=-1
OUTFILTER=@outfilter@ ANALYSIS_CONFIG=${CMSSW_BASE}/src/TTH/MEAnalysis/data/default_Boosted.cfg python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/sparsinator.py --skipEvents $SKIP_EVENTS --maxEvents $MAX_EVENTS
