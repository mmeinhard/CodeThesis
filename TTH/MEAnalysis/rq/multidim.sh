#!/bin/bash

set -e
set -o xtrace

MOD=`basename $1`
MOD="${MOD%.*}"
cd `dirname $1`

combine $MOD.txt \
    -n $MOD \
    -M MultiDimFit \
    -P bgnorm_ttbarPlus2B \
    -P r \
    --setPhysicsModelParameterRanges bgnorm_ttbarPlus2B=-3,3:r=-3,3 \
    --points 10000 \
    --keepFailures \
    --saveNLL \
    --algo grid \
