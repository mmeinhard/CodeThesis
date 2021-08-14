#!/bin/bash

exitCode=$1
#cat log

if [ $exitCode -eq 0 ]; then
echo "command succeeded"
else
cat log | python analyze_log.py
exitCode=$?
errorType=""
exitMessage=`tail -n500 | grep -A5 -B5 -i error`
cat << EOF > FrameworkJobReport.xml
<FrameworkJobReport>
<FrameworkError ExitStatus="$exitCode" Type="$errorType" >
<![CDATA[
$exitMessage
]]>
</FrameworkError>
</FrameworkJobReport>
EOF
fi

cat FrameworkJobReport.xml
echo "======================= CMSRUN CONFIG =========================="
head -n 50 runConfig_NANO.py
echo "======================== CMSRUN LOG ============================"
head -n 300 Output/cmsRun.log 
echo "=== SNIP ==="
tail -n 300 Output/cmsRun.log 
echo "====================== END CMSRUN LOG =========================="
