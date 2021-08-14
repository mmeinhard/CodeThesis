#!/bin/bash
set +e
set -o xtrace

MASS=125

DCARD=`basename $1`
DCARD="${DCARD%.*}"
cd `dirname $1`

#bkg only fit
#combine $DCARD.txt \
#    -n scan_r_sig0 \
#    -M MultiDimFit \
#    -t -1 \
#    -P r \
#    --point 100 \
#    --algo grid \
#    --robustFit 1 \
#    --expectSignal 0 \
#    --saveSpecifiedNuis bgnorm_ttbarPlusBBbar,CMS_ttH_CSVhf,CMS_scaleFlavorQCD_j,CMS_ttjetsisr \
#    --saveInactivePOI 1 \
#    --setPhysicsModelParameterRanges r=-3,3
#
##Freeze all nuisances, 
#combine $DCARD.txt \
#    -n scan_r_sig0_freeze \
#    -M MultiDimFit \
#    -t -1 \
#    -P r \
#    --point 100 \
#    --algo grid \
#    --robustFit 1 \
#    --expectSignal 0 \
#    --freezeNuisances "rgx{.*}" \
#    --setPhysicsModelParameterRanges r=-3,3
#
#combine $DCARD.txt \
#    -n scan_r_sig_bestfit \
#    -M MultiDimFit \
#    -t -1 \
#    -P r \
#    --point 100 \
#    --algo grid \
#    --robustFit 1 \
#    --expectSignal -0.07 \
#    --saveSpecifiedNuis bgnorm_ttbarPlusBBbar,CMS_ttH_CSVhf,CMS_scaleFlavorQCD_j,CMS_ttjetsisr \
#    --saveInactivePOI 1 \
#    --setPhysicsModelParameterRanges r=-3,3
#
#combine $DCARD.txt \
#    -n scan_r_sig_bestfit_freeze \
#    -M MultiDimFit \
#    -t -1 \
#    -P r \
#    --point 100 \
#    --algo grid \
#    --robustFit 1 \
#    --expectSignal -0.07 \
#    --freezeNuisances "rgx{.*}" \
#    --setPhysicsModelParameterRanges r=-3,3
#
#combine $DCARD.txt \
#    -n scan_r_sig1 \
#    -M MultiDimFit \
#    -t -1 \
#    -P r \
#    --point 100 \
#    --algo grid \
#    --robustFit 1 \
#    --expectSignal 1 \
#    --saveSpecifiedNuis bgnorm_ttbarPlusBBbar,CMS_ttH_CSVhf,CMS_scaleFlavorQCD_j,CMS_ttjetsisr \
#    --saveInactivePOI 1 \
#    --setPhysicsModelParameterRanges r=-3,3

combine $DCARD.txt \
    -n scan_r_sig1_freeze \
    -M MultiDimFit \
    -t -1 \
    -P r \
    --point 100 \
    --algo grid \
    --robustFit 1 \
    --expectSignal 1 \
    --freezeNuisances "rgx{.*}" \
    --setPhysicsModelParameterRanges r=-3,3
