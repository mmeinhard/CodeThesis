#!/bin/bash
#dont kill on error
set +e
source env.sh
#manually copy the data configuration
#cp heppy_config_data.py heppy_config.py

python heppy_crab_script.py $@ --isData &> log
EXITCODE=$?
./post.sh $EXITCODE
echo Finished_nano $EXITCODE
echo "=========== START LOG SNIP STEP 1 ==========="
head -n 80 log
echo "=== SNIP ==="
tail -n 20 log
echo "============ END LOG SNIP STEP 1  ============"

python mem_crab_script.py $@ --isData >> log2 2>&1
EXITCODE=$?
echo Finished_tthbb13 $EXITCODE
head -n 70 log2
echo "=== SNIP ==="
tail -n 70 log2
./post.sh $EXITCODE
