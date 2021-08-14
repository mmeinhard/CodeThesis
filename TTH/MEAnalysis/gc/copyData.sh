#!/bin/bash
#Copies the files supplied in $FILE_NAMES as LFN-s from SRC to DST using gfal-copy via xrootd.
#Also creates an output file that contains the number of events per file contained in the TTree Events.

#crash in case of error
set -e
#print out
#set -x

#Source of files
#SRC=srm://storm-se-01.ba.infn.it:8444/srm/managerv2?SFN=/cms #Directly from T2_IT_Bari
#SRC=root://cms-xrd-global.cern.ch #Global redirector, sometimes can be very unreliable
SRC=root://xrootd-cms.infn.it #Europe redirector, should be best general choice

#Target destination of files, must be writeable
DST=srm://t3se01.psi.ch:8443/srm/managerv2\?SFN=/pnfs/psi.ch/cms/trivcat

source common.sh
cd $GC_SCRATCH
for fi in $FILE_NAMES; do

    #On T3 we can only copy to our own directory
    echo $SRC/$fi $DST/$fi
    newfi=/store/user/$USER/$fi

    #copy the file
    LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH gfal-copy -n1 --force $SRC/$fi $DST/$newfi

    #Add a line to the output file with the filename and number of events
    python $CMSSW_BASE/src/TTH/MEAnalysis/test/getBranches.py root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/$newfi Events | grep " = " >> out.txt 
done
