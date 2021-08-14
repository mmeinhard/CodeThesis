#when updating this file, don't forget to update also .gitlab-ci.yml
export SCRAM_ARCH=slc6_amd64_gcc630

cmsrel CMSSW_9_4_9
cd CMSSW_9_4_9/src/
eval `scramv1 runtime -sh`
cmsenv 
git cms-init

git cms-merge-topic mmeinhard:BoostedNanoAOD


git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
#If need some additional patches on nanoAOD-tools, do this:
#cd PhysicsTools/NanoAODTools
#git remote add korbinian-nanoTools https://github.com/kschweiger/nanoAOD-tools.git
#git fetch korbinian-nanoTools
cd $CMSSW_BASE/src

#get the TTH code
git clone ssh://git@gitlab.cern.ch:7999/Zurich_ttH/tthbb13.git TTH --branch SwitchNanoAOD
cd $CMSSW_BASE/src/TTH

git submodule update --init --recursive

#get DNN training code
git clone ssh://git@gitlab.cern.ch:7999/chreisse/TTH_massfit.git DNN

cd $CMSSW_BASE/src

#FIXME: combine is not yet 80X?
#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit --branch 74x-root6
#after scram b clean, these need to be copied again
cp -R TTH/MEIntegratorStandalone/libs/* ../lib/$SCRAM_ARCH/
scram setup lhapdf
scram setup TTH/MEIntegratorStandalone/deps/gsl.xml




