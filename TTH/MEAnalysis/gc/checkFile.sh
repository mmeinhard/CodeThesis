#!/bin/bash
#Copies the files supplied in $FILE_NAMES as LFN-s from SRC to DST using gfal-copy via xrootd.
#Also creates an output file that contains the number of events per file contained in the TTree Events.

#crash in case of error
set -e
#print out
#set -x

source common.sh
cd $GC_SCRATCH
for fi in $FILE_NAMES; do

    #Replace the username "arizzi" in the LFN with your own user name
    #On T3 we can only copy to our own directory
    echo $fi

    #Add a line to the output file with the filename and number of events
    python $CMSSW_BASE/src/TTH/MEAnalysis/test/getBranches.py $fi Events | grep " = " >> out.txt
done
