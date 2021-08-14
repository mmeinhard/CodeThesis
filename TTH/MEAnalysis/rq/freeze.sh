#!/bin/bash
set +e
set -v

datacard=$1
combine -M MultiDimFit --saveWorkspace -n _step1 --minimizerStrategy 1 --minimizerTolerance 0.0000001 --rMin -10 --rMax 10 $datacard
CMD="combine higgsCombine_step1.MultiDimFit.mH120.root -w w --snapshotName MultiDimFit --robustFit 0 -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.000001 --minos all --rMin -20 --rMax 20"
$CMD > freeze_none.log &
$CMD -n freeze_all --freezeNuisanceGroups exp,theory > freeze_all.log &
$CMD -n freeze_exp --freezeNuisanceGroups exp > freeze_exp.log &
$CMD -n freeze_theory --freezeNuisanceGroups theory > freeze_theory.log &
$CMD -n freeze_jec --freezeNuisanceGroups jec > freeze_jec.log &
$CMD -n freeze_btag --freezeNuisanceGroups btag > freeze_btag.log &
$CMD -n freeze_mcstat --freezeNuisanceGroups mcstat > freeze_mcstat.log &
$CMD -n freeze_misc --freezeNuisanceGroups misc > freeze_misc.log &
$CMD -n freeze_QCDscale --freezeNuisanceGroups QCDscale > freeze_QCDscale &
$CMD -n freeze_isrfsr --freezeNuisanceGroups isrfsr > freeze_isrfsr &
$CMD -n freeze_bgnorm --freezeNuisanceGroups bgnorm > freeze_bgnorm &
$CMD -n freeze_pdf --freezeNuisanceGroups pdf > freeze_pdf &
$CMD -n freeze_tunehdamp --freezeNuisanceGroups tunehdamp > freeze_tunehdamp &
wait
