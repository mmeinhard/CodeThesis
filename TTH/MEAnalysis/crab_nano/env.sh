#!/bin/bash
echo "heppy_crab_script_pre.sh"

tar xvzf python.tar.gz --directory $CMSSW_BASE
tar xzf data.tar.gz --directory $CMSSW_BASE/src/TTH/MEAnalysis
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
cp -r lib/slc*/* $CMSSW_BASE/lib/slc*
cp -r lib/slc*/.* $CMSSW_BASE/lib/slc*
echo "AFTER COPY content of $CMSSW_BASE/lib/slc*"

cp -r interface/* $CMSSW_BASE/interface/
echo "AFTER COPY content of $CMSSW_BASE/interface"

cp -r src/* $CMSSW_BASE/src/
echo "AFTER COPY content of $CMSSW_BASE/src"

#look for the file in the current folder which contains the proxy string, but is not this file
#FIXME: better way to discover the proxy
PROXYFILE=`grep "BEGIN CERTIFICATE" * | perl -pe 's/:.*//'  | grep -v "env.sh" | tail -n 1`
export X509_USER_PROXY=$PWD/$PROXYFILE
echo Found Proxy in: $X509_USER_PROXY
MD5SUM=`cat python.tar.gz heppy_config.py | md5sum | awk '{print $1}'`

cat <<EOF > fakeprov.txt
Processing History:
 HEPPY '' '"CMSSW_X_y_Z"' [1]  ($MD5SUM)
EOF

cat <<EOF > $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump
#!/bin/sh
cat fakeprov.txt
EOF

chmod +x $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump

# Update library path
# Needed so recompiled modules are found
export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/gsl/2.2.1/lib:$LD_LIBRARY_PATH 
cd $CMSSW_BASE
eval `scram runtime -sh`
cd -
echo "LD LIBRARY PATH IS"
echo $LD_LIBRARY_PATH

export ROOT_INCLUDE_PATH=.:./src:/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/gsl/2.2.1/include:$ROOT_INCLUDE_PATH

echo "tth_hashes"
cat hash
