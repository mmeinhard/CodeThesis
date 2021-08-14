#!/usr/bin/env python
import os, time, sys, re, imp, glob
import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg
cfg.Analyzer.nosubdir=True
import PSet


args = sys.argv
if "--test" in sys.argv:
    import PSet_test as PSet

print PSet.__dict__["process"].dumpPython()


if "--isMC" in sys.argv:
    isMC = True
elif "--isData" in sys.argv:
    isMC = False
else:
    print "No MC flag in script --> falling back to isMC = True"
    isMC = True

import copy
import json

#Create the NanoAOD postprocessing configuration
from TTH.MEAnalysis.nano_config import NanoConfig
#TODO: Make the era sys.argv so it is set depending on the sample
eraID = None
for arg in args:
    if arg.startswith("era"):
        eraID = arg.split("=")[1]
        print "Using era ID:",eraID
if eraID is None:
    raise RuntimeError("No eraID passed")

runID = None
if not isMC:
    # Parser to get the run from the file name
    # File name should be something like: /store/data/Run2016B_ver2/JetHT/NANOAOD/Nano1June2019_ver2-v2/70000/1E95D5D9-967E-9842-9FF2-DD6F064D775A.root
    print "I'm in data so lets figure out the run"
    onefile = PSet.process.source.fileNames[0]
    print "Using file", onefile
    lfile = onefile.split("/")
    runID = lfile[lfile.index("data")+1]
    print "runID (first step) =", runID
    runID = runID.replace("2016","")
    runID = runID.replace("2017","")
    runID = runID.replace("2018","")
    print "runID (second step) =", runID
    runID = runID[len("Run")]
    print "runID (third step) =", runID
    
nanoCFG = NanoConfig(eraID, jec=True, pu=isMC, btag=False, isData=(not isMC), run = runID)

import heppy_crab_functions as fn

dumpfile = open("dump.txt", "w") #new file created here

dumpfile.write(PSet.process.dumpPython())
dumpfile.write("\n")

t0 = time.time()
print "ARGV:",sys.argv

skipNano = False
if "nano=nostep1" in args or "--nostep1" in args:
    skipNano = True
    print(8*"=","Skipping nano part",8*"=")

os.system("mkdir Output")

if not skipNano:
    #Load necessary variables from PSet:
    crabFiles=PSet.process.source.fileNames
    crabFiles_pfn = copy.deepcopy(PSet.process.source.fileNames)

    #Try first if PSet has skipEvents
    try:
        PSet.process.source.skipEvents.value()
    except AttributeError:
        crabnfirst = 0
    else:
        print "Reading skipEvents from PSet"
        crabnfirst = int(PSet.process.source.skipEvents.value())

    crabMaxEvents = PSet.process.maxEvents.input.value()


    print crabFiles
    fn.convertLFN(crabFiles,crabFiles_pfn)
    print "-------------------------",crabFiles_pfn


    #Setting lumis in file
    lumisToProcess = None
    VLuminosityBlockRange = None
    lumidict = {}
    lumiJSON = 'joblumis.json'

    if hasattr(PSet.process.source, "lumisToProcess"):
        lumisToProcess = PSet.process.source.lumisToProcess
        VLuminosityBlockRange = PSet.process.source.lumisToProcess
        lumidict = fn.getLumisProcessed(lumisToProcess)
        fn.makeLumiJSON(lumisToProcess, lumiJSON)


    ### nanoAOD code
    #Building cmsDriver.py command
    #cmsRun handles LFN files. So we give it those
    if len(crabFiles.value()) == 1:
        filename = crabFiles.value()[0]
    else:
        filename = ""
        for infile in crabFiles.value():
            filename += infile+','
        filename = filename[:-1] #remove tailing ,
    driverCommand = "cmsDriver.py {0} --fileout=Output/nanoAOD.root --no_exec -s NANO --filein {1} -n {2}" .format("runConfig",filename, crabMaxEvents)
    if VLuminosityBlockRange is not None and lumidict != {}:
        driverCommand = "{0}  --lumiToProcess={1}".format(driverCommand, lumiJSON)
    if isMC:
        conditions = nanoCFG.conditionsMC
        era = nanoCFG.eraMC
        datatier = "NANOAODSIM"
        eventcontent = "NANOAODSIM"
        driverCommand = "{0} --eventcontent {1} --datatier {2} --mc --conditions {3} --era {4} --customise_commands=\"process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))\"".format(driverCommand, eventcontent, datatier, conditions, era)
    else:
        conditions = nanoCFG.conditionsData
        era = nanoCFG.eraData
        eventcontent = "NANOAOD"
        driverCommand = "{0} --eventcontent {1} --datatier {1} --data --conditions {2} --era {3} --customise_commands=\"process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))\"".format(driverCommand, eventcontent, conditions, era)

    print "Running cmsDriver command:"
    print driverCommand

    #Run cmsDriver
    os.system(driverCommand+" &> Output/cmsDriver.log")

    os.system("cat Output/cmsDriver.log")
    #os.system("ulimit -u unlimited")

    #Modfiy the config for multiple input files
    dir_ = os.getcwd()
    configfile=dir_+"/runConfig_NANO.py"

    #Run cmsRun with the modified config file
    runstring="{0} {1} >& {2}/Output/cmsRun.log".format("cmsRun",configfile,dir_)
    print "Running cmsRun: {0}".format(runstring)
    ret=os.system(runstring)

    print "available dirs:", os.listdir("/srv/.")
    print "current dir: ", os.getcwd()

    print "cmsRun finished with errorcode: ",ret
    if ret != 0:
        raise Exception("cmsRun returned none 0 return value")


    tf = ROOT.TFile("Output/nanoAOD.root")
    if not tf or tf.IsZombie():
        raise Exception("Error occurred in processing step1")
    tt = tf.Get("Events")
    print "step1 tree={0}".format(tt.GetEntries())
    tf.Close()

    print "timeto_donanoAOD ",(time.time()-t0)
else:
    print 70*"*"
    print 70*"*"
    print 30*"*","skipping NANOAOD production"
    print 70*"*"
    print 70*"*"
t1 = time.time()

### Run nanoAOD postprocessing
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis


outdir = "Output"
if skipNano:
    infiles = inputFiles() #Use the inputdataset as input for postprocessing -> Check if DS is really nanoAOD?
else:
    infiles = ["Output/nanoAOD.root"] #Use nanoAOD output as input for postprocessing
cuts = nanoCFG.cuts
branchsel = nanoCFG.branchsel
json = nanoCFG.json
if isMC:
    json = None
modules = nanoCFG.modules

if skipNano:
    thisJSON = runsAndLumis()
else:
    thisJSON = json
print(thisJSON)
if isinstance(thisJSON, dict):
    if not thisJSON.keys():
        thisJSON = None
print "Starting postprocessor:"
print "  Input file:", infiles
p=PostProcessor(
    outputDir=outdir,
    inputFiles=infiles,
    cut=cuts,
    branchsel=branchsel,
    modules=modules,
    compression="LZMA:9",
    postfix="_postprocessed",
    jsonInput= thisJSON,
    provenance=True,
    fwkJobReport=True,
    #haddFileName="Output/nanoAOD_postprocessed.root"
)
p.run()
print 50*"-"
os.system("ls Output/*.root")
print 50*"-"



"""
Merge postprocessed files. Only necessary if nano step was skipped since running nanoAOD always results in single file
"""
if skipNano:
    """
    Found some problems with hadd that failed for no reason with c++ bs. Added some code 
    that loops over a few permuations you can hadd the files (makes no sense but okay). 
    
    Number of permuations can be set with the nPerm2Try. It will always first try the 
    inversion of the original order. 
    """
    nanoOutputFiles = sorted(glob.glob("Output/*.root"))
    print "Found Output files: \n",nanoOutputFiles
    inv_nanoOutputFiles = sorted(nanoOutputFiles, reverse=True)
    print inv_nanoOutputFiles
    import itertools
    otherPerms = [list(x) for x in list(itertools.permutations(nanoOutputFiles)) if (list(x) != nanoOutputFiles and list(x) != inv_nanoOutputFiles)]
    haddCommand = "hadd Output/nanoAOD_postprocessed.root "+" ".join(nanoOutputFiles)
    print "Running:",haddCommand
    ret = os.system(haddCommand)
    if ret != 0:
        nPerm2Try = 2 # Inversion + 1 
        print 50*"!"
        print "HADD failed woth error code: %s. Will run %s permutations (starting with the inversion)"%(ret, nPerm2Try)
        print 50*"!"
        allPerms = [inv_nanoOutputFiles]+otherPerms
        print allPerms
        for iPerm, perm in enumerate(allPerms):
            rmCommand = "rm Output/nanoAOD_postprocessed.root"
            print "Running:",rmCommand
            os.system(rmCommand)
            print "Trying permuation %s"%iPerm,perm
            haddCommand = "hadd Output/nanoAOD_postprocessed.root "+" ".join(perm)
            print "Running:",haddCommand
            ret = os.system(haddCommand)
            if ret == 0:
                print "This one worked :D"
                break
            elif ret != 0 and iPerm+1 < nPerm2Try:
                print "This one also failed Trying next" 
                continue
            else:
                print "This was the last try.... :("
                exit(ret)
    if ret != 0:
        print "All permutations failes"
        exit(ret)


            
#os.system("hadd Output/nanoAOD_postprocessed.root Output/*.root")
print "timeto_donanoAODpostprocessing", (time.time() - t1)
### run tthbb13 code separately
tf = ROOT.TFile("Output/nanoAOD_postprocessed.root")
if not tf or tf.IsZombie():
    raise Exception("Error occurred in processing step1")
tt = tf.Get("Events")
print "step1.5 tree={0}".format(tt.GetEntries())
tf.Close()
#Write the FWKJobReport after the mem step

print "timeto_FirstHalf ",(time.time()-t0)
dumpfile.close() #will reopen in append mode later
