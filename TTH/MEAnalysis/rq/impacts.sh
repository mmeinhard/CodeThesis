#!/bin/bash
set +e
set -o xtrace

MASS=125

DCARD=`basename $1`
DCARD="${DCARD%.*}"
cd `dirname $1`
opts="--verbose 2 --robustFit 0 --named CMS_ttjetsisr,CMS_ttjetsfsr,bgnorm_ttbarPlus2B,bgnorm_ttbarPlusB,bgnorm_ttbarPlusBBbar,bgnorm_ttbarPlusCCbar,CMS_ttjetshdamp,CMS_ttjetstune,CMS_pu,CMS_ttH_CSVhf,CMS_ttH_CSVlf,CMS_ttH_CSVcferr1,CMS_ttH_CSVcferr2,CMS_ttH_CSVjes,QCDscale_ttH,CMS_scaleFlavorQCD_j,CMS_ttH_scaleME,pdf_Higgs_ttH,lumi,CMS_scalePileUpPtRef_j,CMS_scaleAbsoluteMPFBias_j,CMS_scalePileUpDataMC_j,CMS_scalePileUpPtBB_j,CMS_scaleSinglePionECAL_j,CMS_scaleSinglePionHCAL_j --rMin -10 --rMax 10"
text2workspace.py $DCARD.txt -m $MASS
combineTool.py -M Impacts -d $DCARD.root $opts --doInitialFit --minimizerStrategy 1 --minimizerTolerance 0.000000001 -m $MASS
combineTool.py -M Impacts -d $DCARD.root $opts --doFits --minimizerStrategy 1 --minimizerTolerance 0.000000001 -m $MASS --parallel 30
combineTool.py -M Impacts -d $DCARD.root $opts -m $MASS -o impacts.json
plotImpacts.py -i impacts.json -o impacts
