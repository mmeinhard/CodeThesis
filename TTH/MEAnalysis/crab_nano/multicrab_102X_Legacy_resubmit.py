import sys, re, shutil, os
from copy import deepcopy
import subprocess
import json
import time

from splitLumi import getLumiListInFiles, chunks
from FWCore.PythonUtilities.LumiList import LumiList

#the golden json file for data
#json_file = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"
json_file_2016 = "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
json_file_2017 = "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
json_file_2018 = "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt"

#ttbarJSON_2016 = ["","",""]
ttbarJSON_2017 = [ "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/SplitJSON_TTToHadronic_TuneCP5_PSweights_13TeV_0.json",
                   "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/SplitJSON_TTToHadronic_TuneCP5_PSweights_13TeV_1.json",
                   "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/data/SplitJSON_TTToHadronic_TuneCP5_PSweights_13TeV_2.json",
]

ttbarJSON_2018 = ["FHDownstream/data/crab/SplitJSON_2018v2_1LSperJob_TTToHadronic_TuneCP5_13TeV_0.json",
                  "FHDownstream/data/crab/SplitJSON_2018v2_1LSperJob_TTToHadronic_TuneCP5_13TeV_1.json"]


json_file_2017 = "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/crab_nano/crab_projects/v2/crab_SingleElectron-Run2017D-31Mar2018-v1_v2/results/notFinishedLumis.json"


#Workflows needed for 2017 leptonic analysis:
# -data_leptonic_2017": Runs all 25 datasets (5 Triggers * 5 Runs)
# -leptonic_2017: Runs all MC (except TTFH)
# -hadronic_ttFH_2017: Run TT FH sample (separate because it needs to be split into 3 jobs)
# -testing_2017: Tests data + MC sample



#Each time you call multicrab.py, you choose to submit jobs from one of these workflows
workflows = [
    "data_leptonic_2017",
    "leptonic_2017",
    "leptonic_testing_2017",
    "leptonic_data_testing_2017",
    "data_2016",
    "data_2017",
    "data_2018",
    "hadronic_2016",
    "hadronic_2017",
    "hadronic_2018",
    "hadronic_noMEM_2016",
#    "hadronic_2017",
#    "hadronic_2018",
    "hadronic_ttFH_2017",
    "hadronic_ttFH_2018",
    "hadronic_syst_2017",
    "hadronic_syst_2018",
    "hadronic_trigger_2018",
    "hadronic_trigger_2017",
    "hadronic_trigger_2016",
    "hadronic_testing_2018",
    "hadronic_testing_2017",
    "hadronic_testing_2016",
    "hadronic_data_testing_2018",
    "hadronic_data_testing_2017",
    "hadronic_data_testing_2016",
    "hadronic_baseline_2017",
#    "data", #real data
#    "data_leptonic", #real data, SL and DL only
#    "data_hadronic", #real data, FH only
#    "leptonic", #ttH with SL/DL decays
#    "leptonic_nome", #ttH with SL/DL decays
#    "hadronic", #ttH with FH decays
#    "hadronic_test", #ttH with FH decays
    "hadronic_nome",
#    "hadronic_nome_testing", #ttH with FH decays data + MC
    "hadronic_trigger", #ttH AH dataset and processing for calculating trigger SF
#    "QCD_nome", #QCD samples without MEM
#    "pilot", #ttH sample only, with no MEM
#    "signal", #signal sample with common config
    "testing", #single-lumi jobs, a few samples
#    "testing_withme", #single-lumi jobs, a few samples
#    "allmc_nome", # SL, DL and FH, no matrix element
#    "testall",#Test all samples w/ small nJobs and no ME
#    "testing_hadronic_withme", #single-lumi jobs, a few samples
    "testing_had",
#    "memcheck", #specific MEM jobs that contain lots of hypotheses for validation, many interpretations
#    "memcheck2", #specific MEM jobs that contain lots of hypotheses for validation, JES variations
#    #"memcheck3", #Sudakov/Recoil
#    "training", #specific samples for training ETH DNN
]

import argparse
parser = argparse.ArgumentParser(description='Submits crab jobs')
parser.add_argument('--workflow', action="store", required=True, help="Type of workflow to run", type=str, choices=workflows)
parser.add_argument('--useJSON', action="store", default=None, help="Overwrite json file used", type=str)
parser.add_argument('--tag', action="store", required=True, help="the version tag for this run, e.g. VHBBHeppyV22_tthbbV10_test1")
parser.add_argument('--dataset', action="store", required=False, help="submit only matching datasets (shortname)", default="*")
parser.add_argument('--recovery', action="store", required=False, help="the patand json_filename of the job to recover", default="")#Never tested it. Use with caution
parser.add_argument("--runMiniAOD", action="store_true", default=True, help="If passed script will run from miniAOD and run the nanoAOD step")
parser.add_argument("--selectSamples", action="store", required=False, default=None, nargs="+", help="Pass a list of samples that should be run. Will overwrite default sample list set by workflow")
args = parser.parse_args()

#list of configurations that we are using, should be in TTH/MEAnalysis/python/
me_cfgs = {
    "default": "MEAnalysis_cfg_heppy.py",
    "cMVA": "MEAnalysis_cfg_heppy.py",
    "nome": "cfg_noME.py",
    "nometesting": "cfg_noME_testing.py",
    "leptonic": "cfg_leptonic.py",
    "nome_hadSel" : "cfg_noME_FH.py",
    "hadronic": "cfg_FH.py",
    "hadronic_trigger" : "cfg_FH_val.py",
    "memcheck": "cfg_memcheck.py",
    "memcheck2": "cfg_memcheck2.py",
    "training": "cfg_noME.py",
    "hadronic_2016": "cfg_FH_2016.py",
    "hadronic_noMEM_2016": "cfg_FH_noMEM_2016.py",
    "hadronic_noME_2016" : "cfg_FH_noME_2016.py",
    "hadronic_noME_2017" : "cfg_FH_noME_2017.py",
    "hadronic_2017": "cfg_FH_2017.py",
    "hadronic_2018": "cfg_FH_2018.py",
    "hadronic_trigger_2018" : "cfg_FH_trigger_2018.py",
    "hadronic_trigger_2017" : "cfg_FH_trigger_2017.py",
    "hadronic_trigger_2016" : "cfg_FH_trigger_2016.py",
}

sets_data_MINI = [

    #"/MuonEG/Run2017B-31Mar2018-v1/MINIAOD",
    #"/MuonEG/Run2017C-31Mar2018-v1/MINIAOD",
    #"/MuonEG/Run2017D-31Mar2018-v1/MINIAOD",
    #"/MuonEG/Run2017E-31Mar2018-v1/MINIAOD",
    #"/MuonEG/Run2017F-31Mar2018-v1/MINIAOD",
##
    #"/DoubleMuon/Run2017B-31Mar2018-v1/MINIAOD",
    #"/DoubleMuon/Run2017C-31Mar2018-v1/MINIAOD",
    #"/DoubleMuon/Run2017D-31Mar2018-v1/MINIAOD",
    #"/DoubleMuon/Run2017E-31Mar2018-v1/MINIAOD",
    #"/DoubleMuon/Run2017F-31Mar2018-v1/MINIAOD",
    #
    #"/DoubleEG/Run2017B-31Mar2018-v1/MINIAOD",
    #"/DoubleEG/Run2017C-31Mar2018-v1/MINIAOD",
    #"/DoubleEG/Run2017D-31Mar2018-v1/MINIAOD",
    #"/DoubleEG/Run2017E-31Mar2018-v1/MINIAOD",
    #"/DoubleEG/Run2017F-31Mar2018-v1/MINIAOD",
#
    #"/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD",
    #"/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD",
    "/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD",
    #"/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD",
    #"/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD",
#
    #"/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD",
    #"/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD",
    #"/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD",
    #"/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD",
    #"/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD",


    #"/MuonEG/Run2018A-17Sep2018-v1/MINIAOD",
    #"/MuonEG/Run2018B-17Sep2018-v1/MINIAOD",
    #"/MuonEG/Run2018C-17Sep2018-v1/MINIAOD",
    #"/MuonEG/Run2018D-PromptReco-v2/MINIAOD",
    #
    #"/JetHT/Run2018A-17Sep2018-v1/MINIAOD",
    #"/JetHT/Run2018B-17Sep2018-v1/MINIAOD",
    #"/JetHT/Run2018C-17Sep2018-v1/MINIAOD",
    #"/JetHT/Run2018D-PromptReco-v2/MINIAOD",
    
]

sets_data_NANO = [
    ##################### 2018 ######################
    "/MuonEG/Run2018D-Nano1June2019_ver2-v1/NANOAOD",
    "/MuonEG/Run2018C-Nano1June2019-v1/NANOAOD",
    "/MuonEG/Run2018B-Nano1June2019-v1/NANOAOD",
    "/MuonEG/Run2018A-Nano1June2019-v1/NANOAOD",
    
    "/SingleMuon/Run2018D-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2018C-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2018B-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2018A-Nano1June2019-v1/NANOAOD",
    
    "/JetHT/Run2018D-Nano1June2019_ver2-v1/NANOAOD",
    "/JetHT/Run2018C-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2018B-Nano1June2019-v2/NANOAOD",
    "/JetHT/Run2018A-Nano1June2019-v2/NANOAOD",

    ##################### 2017 ##################a####
    "/SingleMuon/Run2017B-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2017C-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2017D-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2017E-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2017F-Nano1June2019-v1/NANOAOD",
    
    "/JetHT/Run2017B-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2017C-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2017D-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2017E-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2017F-Nano1June2019-v1/NANOAOD",

    "/BTagCSV/Run2017B-Nano1June2019-v1/NANOAOD",
    "/BTagCSV/Run2017C-Nano1June2019-v1/NANOAOD",
    "/BTagCSV/Run2017D-Nano1June2019-v1/NANOAOD",
    "/BTagCSV/Run2017E-Nano1June2019-v1/NANOAOD",
    "/BTagCSV/Run2017F-Nano1June2019-v1/NANOAOD",

    ##################### 2016 ######################
    #"/SingleMuon/Run2016B_ver1-Nano1June2019_ver1-v1/NANOAOD",
    "/SingleMuon/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD",
    "/SingleMuon/Run2016C-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2016D-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2016E-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2016F-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2016G-Nano1June2019-v1/NANOAOD",
    "/SingleMuon/Run2016H-Nano1June2019-v1/NANOAOD",
    
    #"/JetHT/Run2016B_ver1-Nano1June2019_ver1-v1/NANOAOD",
    "/JetHT/Run2016B_ver2-Nano1June2019_ver2-v2/NANOAOD",
    "/JetHT/Run2016C-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2016D-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2016E-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2016F-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2016G-Nano1June2019-v1/NANOAOD",
    "/JetHT/Run2016H-Nano1June2019-v1/NANOAOD",
]

sets_data = sets_data_MINI if args.runMiniAOD else sets_data_NANO

#all available datasets.
datasets = {}
datanames = []
for sd in sets_data:
    name = "-".join(sd.split("/")[1:3])
    datanames += [name]
    datasets[name] = {
        "ds": sd,
        "maxlumis": -1,
        "perjob": 10,
        "runtime": 25, #hours
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script_data.sh',
        "json" : None,
        "isMC" : False,
        "memory" : 2500,
        "isNANOAOD" : (not args.runMiniAOD)
    }


#Add MC datasets from JSON files
import multicrabHelper
datasets.update(
    multicrabHelper.getDatasets(
        mem_cfg = me_cfgs["default"],
        script = "heppy_crab_script.sh",
        filesIdentifier="LegacyRun2_nano"
    )
)


#now we construct the workflows from all the base datasets
##########################################################
####################### Data #############################
##########################################################


workflow_datasets = {}

workflow_datasets["data_leptonic_2017"] = {}
for k in datasets.keys():
    if ("Double" in k or "Single" in k) and "2017" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["default"]
        D["perjob"] = 20
        D["runtime"] = 30
        D["json"] = json_file_2017
        workflow_datasets["data_leptonic_2017"][k] = D


workflow_datasets["data_2016"] = {}
for k in datasets.keys():
    if "JetHT" in k  and "2016" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic_2016"]
        D["perjob"] = 20
        D["runtime"] = 40
        D["json"] = json_file_2016
        workflow_datasets["data_2016"][k] = D


workflow_datasets["data_2017"] = {}
for k in datasets.keys():
    if ("JetHT" in k or "BTagCSV" in k) and "2017" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic_2017"]
        D["perjob"] = 40
        D["runtime"] = 24
        D["json"] = json_file_2017
        workflow_datasets["data_2017"][k] = D

workflow_datasets["data_2018"] = {}
for k in datasets.keys():
    if "JetHT" in k and "2018" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic_2018"]
        D["perjob"] = 10 # 40 for initail submit
        D["runtime"] = 30
        D["json"] = json_file_2018
        workflow_datasets["data_2018"][k] = D
        
##########################################################
#################### MC samples ##########################
##########################################################
fullSamples = []
workflow_datasets["hadronic_2016"] = {}
for k in datasets.keys():
    if "2016" in k:
        if k.replace("_2016","") in [
                "ttHTobb", "ttHToNonbb",
                "TTbar_sl", "TTbar_dl", "TTbar_had",
                "QCD200to300", "QCD300to500", "QCD500to700",
                "QCD700to1000", "QCD1000to1500","QCD1500to2000",
                "QCD2000toInf",
                "TTWQQ","TTZQQ", "ZZ","ZZ_ext", "WW","WW_ext", "WZ","WZ_ext",
                "st_s_lep", "st_s_had", "st_tw", "st_t", "stbar_t", "stbar_tw",
                "WJets_180","ZJets",
                ]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2016"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            ##### TESTING #####
            #D["perjob"] = 10
            #D["maxlumis"] = 8*D["perjob"]
            #D["runtime"] = 2
            ###################
            workflow_datasets["hadronic_2016"][k] = D

workflow_datasets["hadronic_noMEM_2016"] = {}
for k in datasets.keys():
    if "2016" in k:
        if k.replace("_2016","") in [
                "ttHTobb"#, "ttHToNonbb",
                # "TTbar_sl", "TTbar_dl", "TTbar_had",
                # "QCD200to300", "QCD300to500", "QCD500to700",
                # "QCD700to1000", "QCD1000to1500","QCD1500to2000",
                # "QCD2000toInf",
                # "TTWQQ","TTZQQ", "ZZ","ZZ_ext", "WW","WW_ext", "WZ","WZ_ext",
                # "st_s_lep", "st_s_had", "st_tw", "st_t", "stbar_t", "stbar_tw",
                #Add Z and w jets
                ]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["hadronic_noMEM_2016"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            ##### TESTING #####
            D["perjob"] = 100
            #D["maxlumis"] = 8*D["perjob"]
            #D["runtime"] = 2
            ###################
            workflow_datasets["hadronic_noMEM_2016"][k] = D

workflow_datasets["leptonic_2017"] = {}
for k in datasets.keys():
    if "2017" in k:
        if k.replace("_2017","") in [
                "ttHTobb", "ttHToNonbb",
                #"TTbar_sl", "TTbar_dl",
                #"ZZ", "WW", "WZ",
                #"st_s_lep", "st_tw", "st_t", "stbar_t", "stbar_tw", 
                #"TTWQQ","TTWLep","TTZQQ","TTZLep", #Maybe also need TTZQQ_ext?
                #"THQ","THW","TTG",
                #"WJets_lep_0jet","WJets_lep_1jet","WJets_lep_2jet",
                #"ZJets_lep_0jet","ZJets_lep_1jet","ZJets_lep_2jet"
                ]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["default"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            ##### TESTING #####
            #D["perjob"] = 10
            #D["maxlumis"] = 8*D["perjob"]
            #D["runtime"] = 2
            ###################
            workflow_datasets["leptonic_2017"][k] = D

            
workflow_datasets["hadronic_2017"] = {}
for k in datasets.keys():
    if "2017" in k:
        if k.replace("_2017","") in [
                "ttHTobb", "ttHToNonbb",
                "TTbar_sl", "TTbar_dl",
                "QCD200to300", "QCD300to500", "QCD500to700",
                "QCD700to1000", "QCD1000to1500","QCD1500to2000",
                "QCD2000toInf",
                "TTWQQ","TTZQQ", "ZZ", "WW", "WZ",
                "st_s_lep", "st_s_had", "st_tw", "st_t", "stbar_t", "stbar_tw",
                "ZJetsToQQ400", "ZJetsToQQ600", "ZJetsToQQ800",
                "WJetsToQQ600","WJetsToQQ400", "WJetsToQQ800",
                ]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2017"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            ##### TESTING #####
            #D["perjob"] = 10
            #D["maxlumis"] = 8*D["perjob"]
            #D["runtime"] = 2
            ###################
            workflow_datasets["hadronic_2017"][k] = D

workflow_datasets["hadronic_2018"] = {}
for k in datasets.keys():
    if "2018" in k:
        if k.replace("_2018","") in [
                "ttHTobb", "ttHToNonbb",
                "TTbar_sl", "TTbar_dl",
                "QCD200to300", "QCD300to500", "QCD500to700",
                "QCD700to1000", "QCD1000to1500","QCD1500to2000",
                "QCD2000toInf",
                "TTWQQ","TTZQQ", "ZZ", "WW", "WZ",
                "st_s_lep", "st_s_had", "st_tw", "st_t", "stbar_t", "stbar_tw",
                "ZJetsToQQ400", "ZJetsToQQ600", "ZJetsToQQ800",
                "WJetsToQQ600","WJetsToQQ400", "WJetsToQQ800",
                ]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2018"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            ##### TESTING #####
            #D["perjob"] = 10
            #D["maxlumis"] = 8*D["perjob"]
            #D["runtime"] = 2
            ###################
            workflow_datasets["hadronic_2018"][k] = D

##########################################################
############### tt FH split MC samples ###################
##########################################################
# ttbar FH 2016 has only 200 evt/LS with 35 we get < 10k jobs
# at approx same number of events 2018 ttbar FH has per LS with 1 LS per job

workflow_datasets["hadronic_ttFH_2017"] = {}
# 2017: approx 700 evt/LS to get < 8k events per need to run on 10 LS/job resulting in > 10k jobs per task
for k in datasets.keys():
    if k in ["TTbar_had_2017"]:
        for ijson, jsonFile in enumerate(ttbarJSON_2017):
            #if ijson == 0:
            #    continue
            D = deepcopy(datasets[k])
            D["json"] =  os.environ["CMSSW_BASE"]+"/src/TTH/"+jsonFile
            D["mem_cfg"] = me_cfgs["hadronic_2017"]
            D["runtime"] = max(40,D["runtime"])
            ##### TESTING #####
            #D["perjob"] = 1
            #D["maxlumis"] = 1
            ###################
            workflow_datasets["hadronic_ttFH_2017"][k+"_json_"+str(ijson)] = D

workflow_datasets["hadronic_ttFH_2018"] = {}
# 2017: approx 8000 evt/LS we run on 1 LS/job resulting in > 10k jobs per task
for k in datasets.keys():
    if k in ["TTbar_had_2018"]:
        for ijson, jsonFile in enumerate(ttbarJSON_2018):
            #if ijson == 0:
            #    continue
            D = deepcopy(datasets[k])
            D["json"] = os.environ["CMSSW_BASE"]+"/src/TTH/"+jsonFile
            D["mem_cfg"] = me_cfgs["hadronic_2018"]
            D["runtime"] = max(40,D["runtime"])
            ##### TESTING #####
            #D["perjob"] = 1
            #D["maxlumis"] = 1
            ###################
            workflow_datasets["hadronic_ttFH_2018"][k+"_json_"+str(ijson)] = D

##########################################################
################# tt syst MC samples #####################
##########################################################

workflow_datasets["hadronic_syst_2017"] = {}
for k in datasets.keys():
    if "2017" in k and "syst" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2017"])
        D["runtime"] = deepcopy(max(40,D["runtime"]))
        ##### TESTING #####
        #D["perjob"] = 10
        #D["maxlumis"] = 8*D["perjob"]
        #D["runtime"] = 2
        ###################
        workflow_datasets["hadronic_syst_2017"][k] = D

workflow_datasets["hadronic_syst_2018"] = {}
for k in datasets.keys():
    if "2018" in k and "syst" in k:
        D = deepcopy(datasets[k])
        D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2018"])
        D["runtime"] = deepcopy(max(40,D["runtime"]))
        ##### TESTING #####
        #D["perjob"] = 10
        #D["maxlumis"] = 8*D["perjob"]
        #D["runtime"] = 2
        ###################
        workflow_datasets["hadronic_syst_2018"][k] = D

##########################################################
##################### Trigger SF #########################
##########################################################


workflow_datasets["hadronic_trigger_2018"] = {}
for k in datasets.keys():
    #if "SingleMu" in k or k.startswith("TTbar_"):
    if "2018" in k and ("SingleMu" in k or k.replace("_2018","") in ["TTbar_had", "TTbar_sl", "TTbar_dl"]):
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic_trigger_2018"]
        D["runtime"] = deepcopy(max(40,D["runtime"]))
        if not D["isMC"]:
            D["perjob"] = 200
            D["json"] = json_file_2018
        else:
            D["perjob"] = 50
        workflow_datasets["hadronic_trigger_2018"][k] = D

workflow_datasets["hadronic_trigger_2017"] = {}
for k in datasets.keys():
    #if "SingleMu" in k or k.startswith("TTbar_"):
    if "2017" in k and ("SingleMu" in k or k.replace("_2017","") in ["TTbar_had", "TTbar_sl", "TTbar_dl"]):
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic_trigger_2017"]#
        D["runtime"] = deepcopy(max(40,D["runtime"]))
        if not D["isMC"]:
            D["perjob"] = 5#300
            D["json"] = json_file_2017
        else:
            D["perjob"] = 100
        ######### Testing ###########
        # D["perjob"] = 2
        # D["maxlumis"] = 8*D["perjob"]
        # D["runtime"] = 2
        #############################
        workflow_datasets["hadronic_trigger_2017"][k] = D

workflow_datasets["hadronic_trigger_2016"] = {}
for k in datasets.keys():
    #if "SingleMu" in k or k.startswith("TTbar_"):
    if "2016" in k and ("SingleMu" in k or k.replace("_2016","") in ["TTbar_had", "TTbar_sl", "TTbar_dl"]):
        D = deepcopy(datasets[k])
        D["mem_cfg"] = me_cfgs["hadronic_trigger_2016"]
        D["runtime"] = deepcopy(max(40,D["runtime"]))
        if not D["isMC"]:
            D["perjob"] = 5#100
            D["runtime"] = 4
            D["json"] = json_file_2016
        else:
            D["perjob"] = 150
        ######### Testing ###########
        # D["perjob"] = 2
        # D["maxlumis"] = 8*D["perjob"]
        # D["runtime"] = 2
        #############################
        workflow_datasets["hadronic_trigger_2016"][k] = D

##########################################################
################### Dataset Tests ########################
##########################################################

workflow_datasets["hadronic_testing_2016"] = {}
for k in datasets.keys():
    if "2016" in k:
        if k.replace("_2016","") in ["ttHTobb", "ttHToNonbb","TTbar_had", "TTbar_dl",
                                     "st_s_lep", "st_s_had", "st_tw", "st_t", "stbar_t", "stbar_tw"]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2016"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            D["maxlumis"] = 35*D["perjob"]
            ###################
            workflow_datasets["hadronic_testing_2016"][k] = D

workflow_datasets["hadronic_testing_2017"] = {}
for k in datasets.keys():
    if "2017" in k:
        if k.replace("_2017","") in ["ttHTobb"]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["default"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            D["maxlumis"] = 3
	    D["perjob"] = 1
            ###################
            workflow_datasets["hadronic_testing_2017"][k] = D

workflow_datasets["hadronic_testing_2018"] = {}
for k in datasets.keys():
    if "2018" in k:
        if k.replace("_2018","") in ["ttHTobb", "ttHToNonbb","TTbar_had", "TTbar_sl", "TTbar_dl",
                                     "st_s_lep", "st_s_had", "st_tw", "st_t", "stbar_t", "stbar_tw"]:
            D = deepcopy(datasets[k])
            D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2018"])
            D["runtime"] = deepcopy(max(40,D["runtime"]))
            D["maxlumis"] = 35*D["perjob"]
            ###################
            workflow_datasets["hadronic_testing_2018"][k] = D

###################################################################################################

workflow_datasets["hadronic_data_testing_2016"] = {}
for k in datasets.keys():
    if "JetHT" in k  and "2016" in k:
        D = deepcopy(datasets[k])
        D["perjob"] = 1
        D["runtime"] = 24
        D["mem_cfg"] = deepcopy(me_cfgs["hadronic_noME_2016"])
        D["maxlumis"] = 10*D["perjob"]
        D["json"] = json_file_2016
        ###################
        workflow_datasets["hadronic_data_testing_2016"][k] = D

workflow_datasets["hadronic_data_testing_2017"] = {}
for k in datasets.keys():
    if ("JetHT" in k or "BTagCSV" in k) and "2017" in k:
        D = deepcopy(datasets[k])
        D["perjob"] = 1
        D["runtime"] = 1
        D["mem_cfg"] = deepcopy(me_cfgs["hadronic_noME_2017"])
        D["maxlumis"] = 10*D["perjob"]
        D["json"] = json_file_2017
        ###################
        workflow_datasets["hadronic_data_testing_2017"][k] = D

workflow_datasets["hadronic_data_testing_2018"] = {}
for k in datasets.keys():
    if "JetHT" in k and "2018" in k:
        D = deepcopy(datasets[k])
        D["perjob"] = 1
        D["runtime"] = 1
        D["mem_cfg"] = deepcopy(me_cfgs["hadronic_2018"])
        D["maxlumis"] = 10*D["perjob"]
        D["json"] = json_file_2018
        ###################
        workflow_datasets["hadronic_data_testing_2018"][k] = D

###################################################################################################
workflow_datasets["hadronic_baseline_2017"] = {}
for k in datasets.keys():
    if (#(("JetHT" in k or "BTagCSV" in k) and "2017" in k) or
        k.replace("_2017","") in [#"ttHTobb", "ttHToNonbb","TTbar_had", "TTbar_sl", "TTbar_dl",
                                  #"st_s_lep", "st_s_had", "st_tw", 
            #"TTbar_had",
            "st_t", "stbar_t",
            #"stbar_tw"
        ]
        ):
        D = deepcopy(datasets[k])
        D["memory"] = 2500
        D["perjob"] = 150# int(10*D["perjob"])
        #D["maxlumis"] = 10*D["perjob"]
        #if "ttHTobb" in k or "ttHToNonbb" in k or "TTbar_had" in k:
        #    D["perjob"] = 10*D["perjob"]
        D["mem_cfg"] = deepcopy(me_cfgs["hadronic_noME_2017"])
        
        if "JetHT" in k or "BTagCSV" in k:
            D["json"] = json_file_2017
        ###################
        workflow_datasets["hadronic_baseline_2017"][k] = D


###################################################################################################
#LEPTONIC TESTS
workflow_datasets["leptonic_testing_2017"] = {}
for k in datasets.keys():
    if "2017" in k:
        if k.replace("_2017","") in ["ttHTobb","DoubleEG"]:
            D = deepcopy(datasets[k])
            D["maxlumis"] = 3
            D["perjob"] = 1
            if not D["isMC"]:
                D["maxlumis"] = 5
                D["perjob"] = 1
                D["json"] = json_file
            D["runtime"] = 2
            D["mem_cfg"] = deepcopy(me_cfgs["default"])
            workflow_datasets["leptonic_testing_2017"][k] = D


workflow_datasets["leptonic_data_testing_2017"] = {}
for k in datasets.keys():
    if ("SingleElectron-Run2017D" in k) and "2017" in k:
        D = deepcopy(datasets[k])
        D["perjob"] = 1
        D["runtime"] = 1
        D["mem_cfg"] = deepcopy(me_cfgs["default"])
        D["maxlumis"] = 3*D["perjob"]
        D["json"] = json_file_2017
        ###################
        workflow_datasets["leptonic_data_testing_2017"][k] = D




####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
##################################################################################################
# Overwrite JSON file
if args.useJSON is not None:
    print "Will overwrite json in all dataset with",args.useJSON
    raw_input("Press enter to continue. Else crtl+c")
    for ds in workflow_datasets[args.workflow]:
        workflow_datasets[args.workflow][ds]["json"] = args.useJSON

#Now select a set of datasets
sel_datasets = workflow_datasets[args.workflow]


if args.selectSamples is not None:
    sel_datasets_ = {}
    runDatasets = []
    for sample in args.selectSamples:
        for sel_dataset in sel_datasets.keys():
            if sample in sel_dataset:
                runDatasets.append(sel_dataset)
                break
    if not runDatasets:
        raise RuntimeError("Something went wrong with the --selectSample arguments. No samples were selected.")
    for ds in runDatasets:
        sel_datasets_[ds] = sel_datasets[ds]

    sel_datasets = sel_datasets_
        

print json.dumps(sel_datasets, sort_keys=True,
                 indent=4, separators=(',', ': '))
if "2018" in args.workflow:
    era = "102Xv1"
elif "2017" in args.workflow:
    era = "94Xv2"
else:
    era = "80X"
    
print "Will use era=%s for nanoPostprocessing step"%era

raw_input("Press ret to start")
if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import getUsernameFromSiteDB

    def submit(config):
        res = crabCommand('submit', config = config)
        with open(config.General.workArea + "/crab_" + config.General.requestName + "/crab_config.py", "w") as fi:
            fi.write(config.pythonise_())

    from CRABClient.UserUtilities import config
    config = config()
    if args.recovery:
	submitname = args.recovery.split("/")[1].split(".json")[0]
    else:
	submitname = args.tag

    config.General.workArea = 'crab_projects/' + submitname
    config.General.transferLogs = True

    #Disable overflow to prevent buggy site T2_US_UCSD
    #config.section_("Debug")
    #config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'heppy_crab_fake_pset.py'

    print "--------------------"
    import os
    tarArgs = "python `find $CMSSW_BASE/src -name python | perl -pe s#$CMSSW_BASE/## `"
    if "hadronic" in args.workflow:
        tarArgs += " src/TTH/FHDownstream/nTupleProcessing"
    print "tar czf python.tar.gz --directory $CMSSW_BASE "+tarArgs
    os.system("tar czf python.tar.gz --directory $CMSSW_BASE "+tarArgs)
    print "tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root"
    os.system("tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root")
    # if not "testing" in args.workflow:
    #     os.system("make -sf $CMSSW_BASE/src/TTH/Makefile get_hashes")
    #     os.system("echo '\n\n{0}\n-------------' >> $CMSSW_BASE/src/TTH/logfile.md".format(submitname))
    #     os.system("cat $CMSSW_BASE/src/TTH/hash >> $CMSSW_BASE/src/TTH/logfile.md")
    print "--------------------"
    nanoTools_dir = os.environ.get("CMSSW_BASE") + "/src/PhysicsTools/NanoAODTools"
    nano_dir = os.environ.get("CMSSW_BASE") + "/src/PhysicsTools/NanoAOD"
    tth_data_dir = os.environ.get("CMSSW_BASE") + "/src/TTH/MEAnalysis/data"

    config.JobType.inputFiles = [
        'hash',
        'analyze_log.py',
        'FrameworkJobReport.xml',
        'env.sh',
        'post.sh',
        'heppy_crab_script.py',
        'mem_crab_script.py',
        'heppy_crab_functions.py',
        'python.tar.gz',
        'data.tar.gz',
        'MEAnalysis_heppy.py',
        #nanoTools_dir + '/scripts/nano_postproc.py',
        #nanoTools_dir + '/python/postprocessing/modules/jme/jecUncertainties.py'
    ]

    config.Data.inputDBS = 'global'

    
    config.Data.splitting = 'LumiBased'
    #config.Data.splitting = 'FileBased'
    config.Data.publication = False
    config.Data.ignoreLocality = False
    config.Data.allowNonValidInputDataset = True
    
    #config.Site.whitelist = [""]
    config.Site.blacklist = [
        "T2_UK_London_IC" # Added 17.10.19 - All/most jobs fail bc reaching max  wallclocktime
    ]

    config.Site.storageSite = "T3_CH_PSI"

    #loop over samples
    for sample in sel_datasets.keys():       
        if not args.dataset=="*" and not args.dataset in sample:
	    continue
	if args.recovery and not sample in args.recovery:
	    continue
        if not args.recovery and sel_datasets[sample]["json"] != "":
            print "Setting json for Dataset:",sample
            config.Data.lumiMask = sel_datasets[sample]["json"]
        else:
            config.Data.lumiMask = args.recovery
        if "st_t_2018" in sample:
            print "WARNING: Switching to FileBased splitting for sample %s"%sample
            answer = raw_input("Type yes if this is intended! ")
            if answer.lower() != "yes":
                print "Skipping"
                continue
            config.Data.splitting = 'FileBased'


        for thisSample in ["st_t_", "stbar_t_", "ttH", "TTbar_had"]:
            if thisSample in sample:
                print "Setting ignoreLocality to True for",sample
                config.Site.whitelist = ["T2_CH_*","T2_AT_*","T2_DE_*","T2_FR_*","T2_UK_*","T2_US_*","T2_IT_*","T2_BE_*","T1_*"]
                config.Data.ignoreLocality = True
        

        config.JobType.maxMemoryMB = sel_datasets[sample]["memory"]

        print 'submitting ' + sample, sel_datasets[sample]

        mem_cfg = sel_datasets[sample]["mem_cfg"]
        config.JobType.scriptExe = sel_datasets[sample]["script"]

        config.JobType.allowUndistributedCMSSW = True
        dataset = sel_datasets[sample]["ds"]
        nlumis = sel_datasets[sample]["maxlumis"]
        perjob = sel_datasets[sample]["perjob"]
        runtime_min = int(sel_datasets[sample].get("runtime_min", sel_datasets[sample]["runtime"]*60))

        config.JobType.maxJobRuntimeMin = runtime_min
        if args.recovery:
	    config.General.requestName = submitname
	else:
	    config.General.requestName = sample + "_" + submitname
        config.Data.inputDataset = dataset
        config.Data.unitsPerJob = perjob
        config.Data.totalUnits = nlumis
        config.Data.outputDatasetTag = submitname
        try:
            config.Data.outLFNDirBase = '/store/user/{0}/tth/'.format(getUsernameFromSiteDB()) + submitname
        except Exception as e:
            config.Data.outLFNDirBase = '/store/user/{0}/tth/'.format(os.environ["USER"]) + submitname

        config.JobType.scriptArgs = ['ME_CONF={0}'.format(mem_cfg)]
        if "BTagCSV" in sample:
            config.JobType.scriptArgs.append('DataSetName=BTagCSV')
        if "JetHT" in sample:
            config.JobType.scriptArgs.append('DataSetName=JetHT')
        if "ttH" in sample:
            config.JobType.scriptArgs.append('DataSetName=ttH')
        isNanoAOD = sel_datasets[sample]["isNANOAOD"]
        if not isinstance(isNanoAOD, bool):
            raise TypeError("isNANOAOD not bool")

        if isNanoAOD:
            config.JobType.scriptArgs.append('nano=nostep1')
        config.JobType.scriptArgs.append('era=%s'%era)
        print  config.JobType.scriptArgs

        try:
            submit(config)
        except Exception as e:
            print "==============================================="
            print "==== EXCEPTION : =============================="
            print e
            print " ================ SKIPPING ===================="
            print "==============================================="
