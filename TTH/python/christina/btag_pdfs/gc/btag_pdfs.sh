#!/bin/bash
source common.sh
cd $GC_SCRATCH
MAX_EVENTS=-1
python ${CMSSW_BASE}/src/TTH/Plotting/python/christina/btag_pdfs/btag_pdfs.py
