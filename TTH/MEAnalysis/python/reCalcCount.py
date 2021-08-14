#!/usr/bin/env python
"""Recalculates the number fo weighted gen events from the nanoAOD tree"""
import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix
import logging
import os
import math

LOG_MODULE_NAME = logging.getLogger(__name__)

def main(filenames, ofname, debug=False):
    """
    Get the necessary weight from the nanoAOD file and calulates the the number of genevents with
    Sum of 1 * puWeight * sign(genWeight)
    """
    filenames_pref = map(getSitePrefix, filenames)
    if os.path.isfile(ofname):
        LOG_MODULE_NAME.info("opening existing file {0}".format(ofname))
        of = ROOT.TFile(ofname, "UPDATE")
    else:
        LOG_MODULE_NAME.info("creating new file {0}".format(ofname))
        of = ROOT.TFile(ofname, "RECREATE")
    tree_list = ROOT.TList()

    #keep tfiles open for the duration of the merge
    #tfiles = []
    
    hGen = ROOT.TH1F("hGen","hGen",1,0,1)
    hGenWeighted = ROOT.TH1F("hGenWeighted","hGenWeighted",1,0,1)
    hGenWeightednoPU = ROOT.TH1F("hGenWeightednoPU","hGenWeightednoPU",1,0,1)
    hGenFullWeighted = ROOT.TH1F("hGenFullWeighted","hGenFullWeighted",1,0,1)
    hGenFullWeightednoPU = ROOT.TH1F("hGenFullWeightednoPU","hGenFullWeightednoPU",1,0,1)
    for infn, lfn in zip(filenames_pref, filenames):
        LOG_MODULE_NAME.info("processing {0}".format(infn))
        tf = ROOT.TFile.Open(infn)
        #tfiles += [tf]

        #run_tree = tf.Get("Runs")
        #if not run_tree:
        #    run_tree = tf.Get("nanoAOD/Runs")

        evt_tree = tf.Get("Events")
        if not evt_tree:
            evt_tree = tf.Get("nanoAOD/Events")

        for iEv in range(evt_tree.GetEntries()):
            if iEv%10000 == 0 and iEv != 0:
                 LOG_MODULE_NAME.info("Processed events: {0}".format(iEv))
            evt_tree.GetEvent(iEv)
            nWeighted = 1 * evt_tree.puWeight * math.copysign(1.0, evt_tree.genWeight)
            nWeightednoPU = 1 * math.copysign(1.0, evt_tree.genWeight)
            nFullWeighted = 1 * evt_tree.puWeight * evt_tree.genWeight
            nFullWeightednoPU = 1 * evt_tree.genWeight
            hGen.Fill(0, 1)
            hGenWeighted.Fill(0, nWeighted)
            hGenFullWeighted.Fill(0, nFullWeighted)
            hGenWeightednoPU.Fill(0, nWeightednoPU)
            hGenFullWeightednoPU.Fill(0, nFullWeightednoPU)
        
        #tree_list.Add(run_tree)

    of.cd()
    #out_tree = ROOT.TTree.MergeTrees(tree_list)    
    LOG_MODULE_NAME.info("saving output")
    #out_tree.Write()
    hGen.Write()
    hGenWeighted.Write()
    hGenFullWeighted.Write()
    hGenWeightednoPU.Write()
    hGenFullWeightednoPU.Write()
    
    if debug:
        LOG_MODULE_NAME.debug("Recalculated Values:")
        LOG_MODULE_NAME.debug("hGen : {0}".format(hGen.GetBinContent(1)))
        LOG_MODULE_NAME.debug("hGenWeighted : {0}".format(hGenWeighted.GetBinContent(1)))
        LOG_MODULE_NAME.debug("hGenFullWeighted : {0}".format(hGenFullWeighted.GetBinContent(1)))
        LOG_MODULE_NAME.debug("hGenWeightednoPU : {0}".format(hGenWeightednoPU.GetBinContent(1)))
        LOG_MODULE_NAME.debug("hGenFullWeightednoPU : {0}".format(hGenFullWeightednoPU.GetBinContent(1)))
        LOG_MODULE_NAME.debug("nanoAOD Values:")
        #countw = 0
        #countgen = 0
        #for ient in range(out_tree.GetEntries()):
        #    out_tree.GetEntry(ient)
        #    countw += out_tree.genEventSumw
        #    countgen += out_tree.genEventCount
        #LOG_MODULE_NAME.debug("genEventCount : {0}".format(countgen))
        #LOG_MODULE_NAME.debug("genEventCount : {0}".format(countw))
    
    
    of.Close()
    return ofname

if __name__ == "__main__":
    loglevel = 20
    logging.basicConfig(stream=sys.stdout, level=loglevel)
    filenames = sys.argv[2:]
    ofname = sys.argv[1]
    logging.info("Files to process: {0}".format(len(filenames)))
    logging.info("Outputfilename: "+ofname)
    debug = False
    if loglevel < 20:
        debug = True
    
    print main(filenames, ofname, debug)
