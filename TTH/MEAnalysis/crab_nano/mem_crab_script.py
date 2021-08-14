#!/usr/bin/env python
import os, time, sys, re, imp
import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg
cfg.Analyzer.nosubdir=True
import PSet
args = sys.argv
if "--test" in sys.argv:
    import PSet_test as PSet

if "--isMC" in sys.argv:
    isMC = True
elif "--isData" in sys.argv:
    isMC = False
else:
    print "No MC flag in scirpt --> falling back to isMC = True"
    isMC = True

    
import copy
import json
from PhysicsTools.HeppyCore.framework.looper import Looper
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

import heppy_crab_functions as fn

skipNano = False
if "nano=nostep1" in args or "--nostep1" in args:
    skipNano = True
    print(8*"=","Skipping nano part",8*"=")

dumpfile = open("dump.txt", "a") #append mode

dumpfile.write(PSet.process.dumpPython())
dumpfile.write("\n")

t0 = time.time()
print "ARGV:",sys.argv

crabFiles=copy.deepcopy(PSet.process.source.fileNames) # For some reason this ens up as the pfn value after calling inputFiles() with deepcopy if works
crabFiles_pfn = inputFiles()

lumidict = runsAndLumis()
    
os.getcwd()
### tthbb13 code
if not "--nostep2" in args:
    print "Running tth code"

    if not os.path.isfile("Output/nanoAOD_postprocessed.root"):
         raise Exception("Step 1 failed! Output/nanoAOD_postprocessed.root does not exist")
    
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    from TTH.MEAnalysis.MEAnalysis_heppy import main as tth_main
    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str
    #Set config names for analysis and MEM
    an_conf_name = None
    me_conf_name = None
    if "AN_CFG" in os.environ and os.environ["AN_CFG"]:
        an_conf_name = os.environ["AN_CFG"]
    else:
        an_conf_name = os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default_Boosted.cfg"
        me_conf_name = "MEAnalysis_cfg_heppy.py"
        for arg in sys.argv:
            if arg.startswith("ME_CONF="):
                me_conf_name = arg.split("=")[1]
            if arg.startswith("AN_CFG="):
                an_conf_name = arg.split("=")[1]

    sampleNameFromArg = None
    for arg in sys.argv:
        if arg.startswith("DataSetName="):
            sampleNameFromArg = arg.split("=")[1]
            print "Found sampleName in arguments: {0}".format(sampleNameFromArg)
    
    #Make Analysis object and set mem config if changed
    an = analysisFromConfig(an_conf_name)
    if me_conf_name is not None:
        an.mem_python_config = "$CMSSW_BASE/src/TTH/MEAnalysis/python/" + me_conf_name
        
    print "I'm using ",an_conf_name, " and ", an.mem_python_config
    mem_python_conf = tth_main(
        an,
        schema="mc" if isMC else "data",
        output_name="Output_tth",
        #files=os.getcwd()+"/Output/nanoAOD_postprocessed.root"
        files="Output/nanoAOD_postprocessed.root",
        sampleName = sampleNameFromArg
    )
    #dumpfile.write(conf_to_str(mem_python_conf))
    #dumpfile.write("\n")
    tfm = ROOT.TFile("Output_tth/tree.root") #print events
    if not tfm or tfm.IsZombie():
        raise Exception("Error occurred in processing step2")
    ttm = tfm.Get("tree")
    print "step2 tree={0}".format(ttm.GetEntries())
    tfm.Close()
    print "timeto_doMEM ",(time.time()-t0)

#Now we need to copy both the vhbb and tth outputs to the same file
inf1 = ROOT.TFile("Output/nanoAOD_postprocessed.root")
inf2 = ROOT.TFile("Output_tth/tree.root")
tof = ROOT.TFile("tree.root", "RECREATE")
nano_dir = tof.mkdir("nanoAOD")

fn.copyTo(inf1, nano_dir)
fn.copyTo(inf2, tof)
tof.Close()

assert(fn.getEntries("Output/nanoAOD_postprocessed.root", "Events") == fn.getEntries("tree.root", "nanoAOD/Events"))
assert(fn.getEntries("Output_tth/tree.root", "tree") == fn.getEntries("tree.root", "tree"))

#Now write the FWKJobReport
report=open('./FrameworkJobReport.xml', 'w+')
report.write(fn.getFJR(lumidict, crabFiles, crabFiles_pfn, "tree.root", inputNano = skipNano))
#report.write(fn.getFJR({}, crabFiles, crabFiles_pfn, "tree.root"))
report.close()
print "timeto_totalJob ",(time.time()-t0)
dumpfile.close()
