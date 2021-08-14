source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`

#to get the rq exe and all python libs (except ROOT and our CMSSW code) from anaconda
#export PATH=/swshare/anaconda/bin/:$PATH
#export PYTHONPATH=/mnt/t3nfs01/data01/shome/jpata/.local/lib/python2.7/site-packages:${CMSSW_BASE}/python:/cvmfs/cms.cern.ch/slc6_amd64_gcc630/lcg/root/6.10.08/lib:$PYTHONPATH
export PYTHONPATH=/mnt/t3nfs01/data01/shome/creissel/.local/lib/python2.7/site-packages:${CMSSW_BASE}/python:$PYTHONPATH
