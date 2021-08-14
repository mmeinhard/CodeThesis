#!/bin/bash
set -e
set -o xtrace

MOD=`basename $1`
MOD="${MOD%.*}"
cd `dirname $1`

#combine $MOD.txt \
#    -n $MOD \
#    -M MultiDimFit \
#    -P bgnorm_ttbarPlus2B \
#    -P CMS_ttH_CSVcferr1 \
#    --setParameterRanges bgnorm_ttbarPlus2B=-3,3:CMS_ttH_CSVcferr1=-3,3 \
#    --points 40000 \
#    --keepFailures \
#    --saveNLL \
#    --algo grid

#    --robustFit=1 \
#    --keepFailures \
#    --saveNLL \
combine \
    -n $MOD \
    -M MaxLikelihoodFit \
    --minos=all \
    --expectSignal=1.0 \
    --minimizerStrategy 1 \
    --minimizerTolerance 0.000001 \
    -t -1 $MOD.txt


#python $CMSSW_BASE/src/TTH/Plotting/test/diffNuisances.py -a fitDiagnostics$MOD.root > constraints_$MOD.txt
#cat constraints_$MOD.txt
