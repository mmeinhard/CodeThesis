#!/bin/bash

datacard=$1

combine $datacard \
    -n 2dscan_$datacard \
    -M MultiDimFit \
    -P r \
    -P bgnorm_ttbarPlusBBbar \
    --point 10000 \
    --setPhysicsModelParameterRanges r=-3,3:bgnorm_ttbarPlusBBbar=-3,3 \
    --algo grid

for poi in r bgnorm_ttbarPlusBBbar CMS_ttjetsisr; do
    combine $datacard \
        -n $datacard_$poi \
        -M MultiDimFit \
        -P $poi \
        --point 100 \
        --algo grid

    python /mnt/t3nfs01/data01/shome/jpata/tth/sw-combine/CMSSW/src/CombineHarvester/CombineTools/scripts/plot1DScan.py \
        higgsCombine$poi.MultiDimFit.mH120.root --POI $poi \
        --output scan_$poi
done
