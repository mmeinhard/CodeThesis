#!/bin/bash
source common.sh
cd $GC_SCRATCH
MAX_EVENTS=-1
python ${CMSSW_BASE}/src/TTH/Plotting/python/christina/ttbar_classification/read_data.py
