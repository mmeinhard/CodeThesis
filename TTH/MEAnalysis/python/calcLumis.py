"""
We want the Lumi of our data.

Use the BRILCALC tool [1]
which currently only runs on lxplus. 

Prerequisite:
Install brilcalc for your lxplus account following the instructions at
[1].

What this script does:
- create a temporary directory
- gather all the json files for which we want the lumi calculated
- add a script to be executed on lxplus
- scp the temp directory to lxplus
- remote execute the script
- and copy back the output
- and display the lumis

[1] http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html#brilcalc]

"""

import os
import sys
import shutil
import getpass
import subprocess

def calculate_lumi(
    lxplus_username,
    dataset_name,
    processes,
    dataset_base,
    tmpdir_name
    ):


    print "This program will SSH to lxplus several times and requires previous setup, please see the documentation of calcLumis.py"

    # Prepare a new and empty temp directory
    if os.path.isdir(tmpdir_name):
        shutil.rmtree(tmpdir_name)
    os.mkdir(tmpdir_name)

    # Copy all the json files there
    for process in processes:
        shutil.copy(
            os.path.join(os.environ["CMSSW_BASE"], dataset_base, dataset_name, process + ".json"),
            tmpdir_name)
    #golden JSON
    shutil.copy(
        os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/crab_vhbb/json.txt",
        tmpdir_name + "/golden.json"
    )

    for process in processes:
        os.system("compareJSON.py --and {0}/golden.json {0}/{1}.json {0}/{1}_ingolden.json\n".format(tmpdir_name, process))

    # Now build the shell script
    out = open(os.path.join(tmpdir_name, "runme.sh"), "w")
    out.write("export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH\n")
    for process in processes + ["golden"] + ["{0}_ingolden".format(proc) for proc in processes]:
        out.write('brilcalc lumi -b "STABLE BEAMS" --normtag=/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json -i {0}.json -u /pb -o {0}.out\n'.format(process))
    out.close()

    # scp to lxplus
    scp_command = ["scp", "-o", "PreferredAuthentications=password", "-o", "PubkeyAuthentication=no", "-r", tmpdir_name, lxplus_username + "@lxplus.cern.ch:"]
    print subprocess.Popen(scp_command, stdout=subprocess.PIPE).communicate()[0]

    # remote execute
    print "Next command is remote execute - this may take a while"
    run_command = ["ssh", "-o", "PreferredAuthentications=password", "-o", "PubkeyAuthentication=no", lxplus_username + "@lxplus.cern.ch", "cd {0}; bash runme.sh".format(tmpdir_name)]
    print subprocess.Popen(run_command, stdout=subprocess.PIPE).communicate()[0]

    # get back the output
    scp_back_command = ["scp", "-v", "-o", "PreferredAuthentications=password", "-o", "PubkeyAuthentication=no", "-r", lxplus_username + "@lxplus.cern.ch:"+tmpdir_name, tmpdir_name+"_OUT"]
    print subprocess.Popen(scp_back_command, stdout=subprocess.PIPE).communicate()[0]

    # and analyze it
    for process in processes + ["golden"]:
        inf = open(os.path.join(tmpdir_name+"_OUT", process + ".out"), "r")
        
        # Look for:
        # #Summary:
        # #nfill,nrun,nls,ncms,totdelivered(/pb),totrecorded(/pb)
        # #66,269,101502,101495,12165.673,11629.565
        # and extract the totrecorded
        while True:
            line1 = inf.readline()
            if "Summary" in line1:
                line2 = inf.readline()
                line3 = inf.readline().strip()
                print "'{0}': {1},".format(process,line3.split(",")[-1])
                break

if __name__ == "__main__":
    
    # Translate t3 user to lxplus user
    lxplus_users = { "gregor" : "gregor",
                     "jpata"  : "jpata" }

    lxplus_username = lxplus_users[getpass.getuser()]
    dataset_name = "Sep20_data"

    processes = [
        "SingleMuon",
        "SingleElectron",
        "MuonEG",
        "DoubleEG",
        "DoubleMuon",
    ]

    dataset_base = os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/gc/datasets/"
    tmpdir_name = "./LUMICALC_TEMP"
    calculate_lumi(
        lxplus_username,
        dataset_name,
        processes,
        dataset_base,
        tmpdir_name
    )
            
