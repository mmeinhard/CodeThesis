#!/bin/bash
JOBS=`qstat -u $USER | grep "rq_worker" | awk '{print $1}' | xargs`
qdel $JOBS
