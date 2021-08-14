#!/bin/bash
#dont kill on error
set +e
source env.sh
#manually copy the data configuration

python heppy_crab_script.py $@ --isMC &> log
EXITCODE=$?
./post.sh $EXITCODE
echo Finished_nano $EXITCODE
echo "=========== START LOG SNIP STEP 1 ==========="
head -n 100 log
echo "=== SNIP ==="
tail -n 100 log
echo "============ END LOG SNIP STEP 1  ============"

python mem_crab_script.py $@  --isMC >> log2 2>&1
EXITCODE=$?
echo Finished_tthbb13 $EXITCODE
head -n 70 log2
echo "=== SNIP ==="
tail -n 70 log2
./post.sh $EXITCODE
