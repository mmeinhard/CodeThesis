#!/usr/bin/env python
"""
Run the combine limit setting tool
"""

########################################
# Imports
########################################

import os, sys
import shutil
import datetime
import time
import subprocess
import ROOT
import numpy as np
import logging
import multiprocessing
import json
import copy

LOG_MODULE_NAME = logging.getLogger(__name__)
from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH, GENREFLEX, ROOTSYS, ROOT_INCLUDE_PATH, CMSSW_BASE

def get_limits_asymptotic(fn):
    """
    Returns a length 6 vector with the expected limits and quantiles based on the
    combine root file.
    """
    f = ROOT.TFile(fn)

    #No root file created, fit failed
    if f==None or f.IsZombie():
        lims = [0,0,0,0,0,0]
        quantiles = [0,0,0,0,0,0]
        lims[:] = 99999
        return lims, quantiles
    tt = f.Get("limit")
    if tt==None or tt.IsZombie():
        lims = [0,0,0,0,0,0]
        quantiles = [0,0,0,0,0,0]
        lims[:] = 99999
        return lims, quantiles
    lims = [0,0,0,0,0,0]
    quantiles = [0,0,0,0,0,0]
    for i in range(tt.GetEntries()):
        tt.GetEntry(i)
        lims[i] = tt.limit
        quantiles[i] = tt.quantileExpected
    f.Close()
    return lims, quantiles

def get_limits_mlfit(fn, treename="limit"):
    f = ROOT.TFile(fn)
    tt = f.Get(treename)
    tt.GetEntry(0)
    lim = tt.limit
    tt.GetEntry(3)
    err = tt.limitErr
    return lim, err

def get_bestfit_mlfit_shapes(fn, treename="tree_fit_sb"):
    f = ROOT.TFile(fn)
    tt = f.Get(treename)
    if not tt:
        raise Exception("Could not find file {0}".format(fn))
    tt.GetEntry(0)
    mu = tt.mu
    err = tt.muErr
    errLow = tt.muLoErr
    errHigh = tt.muHiErr
    return mu, err, errLow, errHigh

def limit(
    datacard,
    output_path,
    name_extended="",
    opts=["-M", "Asymptotic"],
    output_format="higgsCombine{process_name}.Asymptotic.mH120.root",
    get_limits=get_limits_asymptotic,
    asimov=True,
    expectSignal=None
    ):

    datacard_path, datacard_name = os.path.split(datacard)
    # Add a timestamp to the name
    process_name = "{0}".format(
        os.path.splitext(datacard_name)[0]
    ) + name_extended

    opts_local = copy.deepcopy(opts) 
    if asimov:
        process_name += "_asimov"
        opts_local += ["-t", "-1"]
    if expectSignal:
        opts_local += ["--expectSignal", str(expectSignal)]

    # Run combine
    combine_command = ["combine", 
                       "-n", process_name,
    ] + opts_local + [datacard_name]
 
    LOG_MODULE_NAME.info("running combine: {0}".format(" ".join(combine_command)))
    
    process = subprocess.Popen(combine_command,
                               stdout=subprocess.PIPE,
                               cwd=datacard_path,
                               env=dict(os.environ, 
                                        PATH=PATH,
                                        LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                        PYTHONPATH=PYTHONPATH,
                                        ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                        ROOTSYS = ROOTSYS,
                                        GENREFLEX = GENREFLEX
                                    )
    )
    
    output, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception("error running combine: {0}".format(stderr))
    LOG_MODULE_NAME.info(output)

    # Put the output file in the correct place..
    # ..root file
    output_rootfile_name = output_format.format(process_name=process_name)
    targetpath = os.path.join(output_path, output_rootfile_name)
    shutil.move(os.path.join(datacard_path, output_rootfile_name),
               targetpath)
    # ..text file
    output_textfile_name = "out_{0}.log".format(process_name)
    of = open(os.path.join(output_path, output_textfile_name), "w")
    of.write(output)
    
    # And extact the limit
    lims, quantiles = get_limits(targetpath)
    LOG_MODULE_NAME.info("lims={0} quantiles={1}".format(lims, quantiles))
    return lims, quantiles
# End of get_limit
    
def signal_injection(datacard, output_path):
    LOG_MODULE_NAME.info("running signal injection on {0}".format(datacard))
    limits = []
    for sig in [0.0, 1.0, 2.0, 3.0]:
        LOG_MODULE_NAME.info("signal injection s={0}".format(sig))
        res = limit(
            datacard,
            output_path,
            name_extended="_sig_{0:.2f}".format(sig).replace(".", "_"),
            opts=["-M", "MaxLikelihoodFit",
            "--expectSignal", str(sig),
            "--rMin", "-20",
            "--rMax", "20",
            "--robustFit", "1",
            #"--robustFit", "1",
            ],
            output_format="higgsCombine{process_name}.MaxLikelihoodFit.mH120.root",
            get_limits=get_limits_mlfit
        )[0]
        LOG_MODULE_NAME.info("mu={0}".format(res))
        limits += [res]
    return limits

def pulls(datacard, output_path, signal_coef=1, asimov=True):

    datacard_path, datacard_name = os.path.split(datacard)
    if signal_coef is None:
        process_name = os.path.splitext(datacard_name)[0]
    else: 
        process_name = os.path.splitext(datacard_name)[0] + "_sig_{0:.2f}".format(signal_coef).replace(".", "_")

    if asimov:
        process_name += "_asimov"
    # Run combine
    combine_command = ["combine", 
                       "-n", process_name,
                       "-M", "MaxLikelihoodFit",
                       datacard_name]
    combine_command += [
        #"--setRobustFitTolerance=0.00001",
        #"--setCrossingTolerance=0.00001",
        "--minimizerStrategy=0", #don't use derivatives in fit
        "--minimizerTolerance=0.0001",
        "--robustFit", "1", #slower
        #"--minos", "all", #faster, but sometimes weird results
        "--saveShapes",
        "--saveWithUncertainties",
        "--rMin", "-20",
        "--rMax", "20",
        "--stepSize", "0.05"
    ]
    if asimov:
        combine_command += [
            "-t", "-1",
        ]
    if not (signal_coef is None):
        combine_command += ["--expectSignal", str(signal_coef)]

    
    LOG_MODULE_NAME.info("running combine: {0}".format(" ".join(combine_command)))
    
    process = subprocess.Popen(combine_command,
                               stdout=subprocess.PIPE,
                               cwd=datacard_path,
                               env=dict(os.environ, 
                                        PATH=PATH,
                                        LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                        PYTHONPATH=PYTHONPATH,
                                        ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                        ROOTSYS = ROOTSYS,
                                        GENREFLEX = GENREFLEX
                                    )
    )
    
    output, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception("error running combine: {0}".format(stderr))
    LOG_MODULE_NAME.info(output)

    diff_cmd = [
        "python",
        os.environ["CMSSW_BASE"] + "/src/TTH/Plotting/test/diffNuisances.py",
        "--format",
        "text",
        "-a",
        #"fitDiagnostics{0}.root".format(process_name),
        "mlfit{0}.root".format(process_name),
        "-g",
        "plots{0}.root".format(process_name)
    ]
    LOG_MODULE_NAME.info("diff command: {0}".format(" ".join(diff_cmd)))
    process = subprocess.Popen(diff_cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=datacard_path,
                               env=dict(os.environ,
                                       CMSSW_BASE=CMSSW_BASE,
                                       PATH=PATH,
                                       LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                       PYTHONPATH=PYTHONPATH,
                                       ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                       ROOTSYS = ROOTSYS,
                                       GENREFLEX = GENREFLEX
                               ),
    )
    
    output, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception("error running combine: {0}".format(stderr))
    return output, "plots{0}.root".format(process_name)

def likelihoodScan(datacard, poi, sig=1):
    datacard_path, datacard_name = os.path.split(datacard)
    process_name = os.path.splitext(datacard_name)[0] + "_poi_{0}".format(poi) + "_sig_{0}".format(sig)
    
    combine_cmd = [
        "combine", datacard_name,
        "-n", process_name,
        "-M", "MultiDimFit",
        "-t", "-1",
        "-P", poi,
        "--point", "100",
        "--algo", "grid",
        "--robustFit", "1",
        "--expectSignal", str(sig)
        #"--setRobustFitTolerance=0.00001",
        #"--setCrossingTolerance=0.00001",
        #"--minimizerStrategy=0",
        #"--minimizerTolerance=0.00001",
    ]
    LOG_MODULE_NAME.info("combine command: {0}".format(" ".join(combine_cmd)))
    
    process = subprocess.Popen(combine_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=datacard_path,
        env=dict(os.environ,
                CMSSW_BASE=CMSSW_BASE,
                PATH=PATH,
                LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                PYTHONPATH=PYTHONPATH,
                ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                ROOTSYS = ROOTSYS,
                GENREFLEX = GENREFLEX
        ),
    )
    output, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception("error running combine: {0}".format(stderr))
   
    scan_cmd = [
        CMSSW_BASE + "/src/CombineHarvester/CombineTools/scripts/plot1DScan.py",
        "higgsCombine{0}.MultiDimFit.mH120.root".format(process_name),
        "--POI", poi,
        "--output", "scan_{0}".format(process_name)
    ]

    process = subprocess.Popen(scan_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=datacard_path,
        env=dict(os.environ,
                CMSSW_BASE=CMSSW_BASE,
                PATH=PATH,
                LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                PYTHONPATH=PYTHONPATH,
                ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                ROOTSYS = ROOTSYS,
                GENREFLEX = GENREFLEX
        ),
    )
    output, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception("error running combine: {0}".format(stderr))
    print output

def likelihoodScanTuple(tup):
    datacard, poi = tup
    return likelihoodScan(datacard, poi)

def mlfit(datacard, freeze_groups=[], saveShapes=False):
    datacard_path, datacard_name = os.path.split(datacard)

    process_name = os.path.splitext(datacard_name)[0]
    if len(freeze_groups) > 0:
        process_name += "_freeze_{0}".format("_".join(freeze_groups))
    
    combine_cmd = [
        "combine", datacard_name,
        "-n", process_name,
        "-M", "MaxLikelihoodFit",
        "--minimizerStrategy=0",
        "--minimizerTolerance=0.000001",
        "--robustFit", "0",
        "--minos", "all",
        "--rMin", "-20",
        "--rMax", "20",
    ]
    if saveShapes:
        combine_cmd += [
            "--saveShapes",
            "--saveWithUncertainties",
        ]
    if len(freeze_groups)>0:
        combine_cmd += ["--freezeNuisanceGroups", ",".join(freeze_groups)]

    LOG_MODULE_NAME.info("combine command: {0}".format(" ".join(combine_cmd)))
    
    process = subprocess.Popen(combine_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=datacard_path,
        env=dict(os.environ,
                CMSSW_BASE=CMSSW_BASE,
                PATH=PATH,
                LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                PYTHONPATH=PYTHONPATH,
                ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                ROOTSYS = ROOTSYS,
                GENREFLEX = GENREFLEX
        ),
    )
    output, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception("error running combine: {0}".format(stderr))
    time.sleep(10)
    mu, err, errLo, errHi = get_bestfit_mlfit_shapes(os.path.join(datacard_path, "mlfit{0}.root".format(process_name)))
    return mu, err, errLo, errHi

def freeze_limits(datacard):

    ret = {}
    lim, err = mlfit(datacard)

    print "total", lim, err
    ret["total"] = (lim, err)

    for group in ["exp", "theory", "mcstat", "jec", "btag"]:
        lim, err = mlfit(datacard, [group])
        print "freeze", group, lim, err
        ret[group] = (lim, err)

    lim, err = mlfit(datacard, ["exp", "theory"])
    ret["stat"] = (lim, err)
    return ret

def significance(datacard, asimov=True):
    datacard_path, datacard_name = os.path.split(datacard)

    process_name = os.path.splitext(datacard_name)[0]
    process_name += "_significance_{0}".format("_".join(freeze_groups))
    if asimov:
        process_name += "_asimov"
 
    combine_cmd = [
        "combine", datacard_name,
        "-n", process_name,
        "-M", "ProfileLikelihood",
    ]
    if asimov:
        combined_cmd += ["-t", "-1", "--expectSignal=1"]

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG
    )
    datacard = sys.argv[1]
    workdir = os.path.dirname(datacard)
    do_ll_scans = True
   
    #pulls(datacard, workdir)
    if do_ll_scans:
        pois = [
           # "CMS_effID_e",
           # "CMS_effID_m",
           # "CMS_effIso_m",
           # "CMS_effReco_e",
           # "CMS_effTracking_m",
           "CMS_pu",
           # "CMS_res_j",
           # "CMS_scaleAbsoluteFlavMap_j",
           # "CMS_scaleAbsoluteMPFBias_j",
           # "CMS_scaleAbsoluteScale_j",
           # "CMS_scaleAbsoluteStat_j",
            "CMS_scaleFlavorQCD_j",
           # "CMS_scaleFragmentation_j",
           # "CMS_scalePileUpDataMC_j",
           # "CMS_scalePileUpPtBB_j",
           # "CMS_scalePileUpPtEC1_j",
           # "CMS_scalePileUpPtEC2_j",
           # "CMS_scalePileUpPtHF_j",
           # "CMS_scalePileUpPtRef_j",
           # "CMS_scaleRelativeFSR_j",
           # "CMS_scaleRelativeJEREC1_j",
           # "CMS_scaleRelativeJEREC2_j",
           # "CMS_scaleRelativeJERHF_j",
           # "CMS_scaleRelativePtBB_j",
           # "CMS_scaleRelativePtEC1_j",
           # "CMS_scaleRelativePtEC2_j",
           # "CMS_scaleRelativePtHF_j",
           # "CMS_scaleRelativeStatEC_j",
           # "CMS_scaleRelativeStatFSR_j",
           # "CMS_scaleRelativeStatHF_j",
           # "CMS_scaleSinglePionECAL_j",
           # "CMS_scaleSinglePionHCAL_j",
           # "CMS_scaleTimePtEta_j",
           "CMS_ttH_CSVcferr1",
           "CMS_ttH_CSVcferr2",
           "CMS_ttH_CSVhf",
           "CMS_ttH_CSVhfstats1",
           "CMS_ttH_CSVhfstats2",
           "CMS_ttH_CSVjes",
           "CMS_ttH_CSVlf",
           "CMS_ttH_CSVlfstats1",
           "CMS_ttH_CSVlfstats2",
           "QCDscale_ttbar",
           "bgnorm_ttbarPlus2B",
           "bgnorm_ttbarPlusB",
           "bgnorm_ttbarPlusBBbar",
           "bgnorm_ttbarPlusCCbar",
           "lumi",
           "pdf_gg",
        ]

        #run log likelihood scan
        #pool = multiprocessing.Pool(10)
        map(likelihoodScanTuple, [(datacard, poi) for poi in pois])
        #pool.close()
