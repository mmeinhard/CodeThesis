#!/bin/bash

datacard=shapes_group_group_sldl.txt
nui=bgnorm_ttbarPlusBBbar

combine $datacard \
    -n scan_freeze_none -M MultiDimFit -t -1 \
    -P $nui --point 100 --algo grid \
    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
    --floatOtherPOIs 1 --saveInactivePOI 1 \
    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
    --saveSpecifiedNuis bgnorm_ttbarPlusCCbar,bgnorm_ttbarPlus2B,bgnorm_ttbarPlusB,CMS_ttjetsisr,CMS_ttjetsfsr,CMS_ttjetstune,CMS_ttjetshdamp,CMS_ttH_CSVhf,CMS_ttH_CSVcferr1,CMS_scaleFlavorQCD_j,CMS_res_j \
    --setPhysicsModelParameterRanges $nui=-2,2 &

#combine $datacard \
#    -n scan_freeze_bgnorm -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups bgnorm &
#
#combine $datacard \
#    -n scan_freeze_isrfsr -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups isrfsr &
#
#combine $datacard \
#    -n scan_freeze_jes -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups jes &
#
#combine $datacard \
#    -n scan_freeze_btag -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups btag &
#
#combine $datacard \
#    -n scan_freeze_qcdscale -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups QCDscale &
#
#combine $datacard \
#    -n scan_freeze_misc -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups misc &
#
#combine $datacard \
#    -n scan_freeze_pdf -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups pdf &
#
#combine $datacard \
#    -n scan_freeze_mcstat -M MultiDimFit -t -1 \
#    -P $nui --point 100 --algo grid \
#    --robustFit 1 --expectSignal 1 --redefineSignalPOIs r \
#    --floatOtherPOIs 1 --saveInactivePOI 1 \
#    --minimizerStrategy 1 --minimizerTolerance 0.0000001 \
#    --setPhysicsModelParameterRanges $nui=-2,2 \
#    --freezeNuisanceGroups mcstat &

wait
