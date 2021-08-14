#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

# Create output directory
mkdir out

echo "Running MakeCategory" $rootfile $config $category
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeCategory.py --rootfile=$sparsefile --config=$config --category=$category --outdir="."
echo "Done MakeCategory"
