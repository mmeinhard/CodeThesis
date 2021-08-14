#!/bin/bash

source common.sh
cd $GC_SCRATCH
xrdcp $FILE_NAMES ./
fn=`basename $FILE_NAMES`
export FILE_NAMES=$fn
echo "file", $fn
python ${CMSSW_BASE}/src/TTH/MEIntegratorStandalone/python/run_csv.py
