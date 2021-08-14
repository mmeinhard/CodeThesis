#!/bin/bash
source env.sh
cd $SGE_O_WORKDIR
/mnt/t3nfs01/data01/shome/jpata/.local/bin/rq worker --worker-ttl 60  -c settings -n $JOB_ID $@
