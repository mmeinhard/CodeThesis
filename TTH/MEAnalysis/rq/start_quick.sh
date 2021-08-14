#!/bin/bash
for i in `seq 1 20`; do
    SGE_O_WORKDIR=`pwd` JOB_ID=$i ./worker.sh default &
done
wait
