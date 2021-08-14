import os
from importlib import import_module
import sys

import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from TTH.MEAnalysis.samples_base import getSitePrefix

from TTH.MEAnalysis.nano_config import NanoConfig


def main(outdir = "./", _input = None, asFriend = True, _era = "94Xv2", runAll = False, skipEvents=None, maxEvents=None, isMC=True, subfolderClone=False):
    if _input is None:
        infiles = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    else:
        infiles = map(getSitePrefix, _input)

    if runAll:
        nano_cfg = NanoConfig(_era, jec = isMC, btag=isMC, pu=isMC)
    else:
        nano_cfg = NanoConfig(_era, btag=isMC, pu=isMC)
    for inf in infiles:
        tf = ROOT.TFile.Open(inf)
#        if not tf.Get("Events"):
#            raise Exception("Couldn't find TTree 'Events' in file, is it a nanoAOD file? Currently, the PostProcessor doesn't know how to read the tree from a subfolder.")

    eventRange = None
    if skipEvents>=0 and maxEvents>=0:
        eventRange = xrange(skipEvents, skipEvents + maxEvents)

    p=PostProcessor(
        outdir, infiles,
        cut=nano_cfg.cuts, branchsel=nano_cfg.branchsel, modules=nano_cfg.modules,
        compression="LZMA:9", friend=asFriend, postfix="_postprocessed",
        jsonInput=None, noOut=False, justcount=False,
        #needs a patch to NanoAODTools
        #treename="nanoAOD/Events", eventRange=eventRange
    )
    for module in p.modules:
        module.treename = "nanoAOD/Events"
    p.run()

    #One more workaround for the tree name problem
    if subfolderClone:
        filePrefix = infiles[0].split(".root")[0]
        rIn = ROOT.TFile("{0}_postprocessed.root".format(filePrefix),"UPDATE")
        t = rIn.Get("Events")
        rIn.mkdir("nanoAOD")
        rIn.cd("nanoAOD")
        tNew = t.CloneTree(-1,"fast")
        tNew.Write()

        
if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Wrapper for running the nanoAOD postprocessor with the tthbb definition for CRAB'
    )
    argumentparser.add_argument(
        "--input",
        action = "store",
        help = "Inputfiles for postprocessing (separated by whitespace). Default: Get names for environment - FILE_NAMES",
        nargs='+',
        type=str,
        default = None
    )
    argumentparser.add_argument(
        "--outputdir",
        action = "store",
        help = "Ouput dir of the postprocessed file. Default: ./",
        type = str,
        default = "./",
    )
    argumentparser.add_argument(
        "--skipEvents",
        action = "store",
        help = "Number of events to skip",
        type = int,
        default = 0,
    )
    argumentparser.add_argument(
        "--maxEvents",
        action = "store",
        help = "Number of events to process",
        type = int,
        default = -1,
    )

    argumentparser.add_argument(
        "--era",
        action = "store",
        help = "Era. Defailt: 94Xv1",
        choices = ["80X", "92X", "94Xv1", "94Xv2"],
        type = str,
        default = "94Xv2",
    )
    
    argumentparser.add_argument(
        "--noFriend",
        action = "store_false",
        help = "Disables friend option in nanoAOD postprocessor",
    )
    argumentparser.add_argument(
        "--runAllModules",
        action = "store_true",
        help = "Disables friend option in nanoAOD postprocessor",
    )
    argumentparser.add_argument(
        "--isData",
        action = "store_true",
        help = "Disables all postprocessor modules",
    )
    argumentparser.add_argument(
        "--subfolderClone",
        action = "store_true",
        help = "Create clone of Events tree in subfolder",
    )




    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    main(args.outputdir, args.input, args.noFriend, args.era, args.runAllModules, args.skipEvents, args.maxEvents, isMC = not args.isData, subfolderClone = args.subfolderClone)
