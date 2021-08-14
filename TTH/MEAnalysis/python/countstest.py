#!/usr/bin/env python
"""
Retrieves the number of generated MC events from the input files and saves it
into an output file.
In nanoAOD, this number is stored in a separate TTree "Runs", which can simply
be added up from all the input files.
"""
import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix
import logging
import os

LOG_MODULE_NAME = logging.getLogger(__name__)

def main(filenames, ofname):
    """
    Retrieves counts from input files and saves to output file.

    Args:
        filenames (list of strings): Input ROOT file names
        ofname (string): Output ROOT file name, will be created
    
    Returns:
        Output file name
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
    tfiles = []
    for infn, lfn in zip(filenames_pref, filenames):
        LOG_MODULE_NAME.info("processing {0}".format(infn))
        tf = ROOT.TFile.Open(infn)
        tfiles += [tf]

        run_tree = tf.Get("Runs")
        if not run_tree:
            run_tree = tf.Get("nanoAOD/Runs")

        event_tree = tf.Get("Events")
        if not event_tree:
            event_tree = tf.Get("nanoAOD/Events")


        tree_list.Add(run_tree)

    of.cd()
    out_tree = ROOT.TTree.MergeTrees(tree_list)
    LOG_MODULE_NAME.info("saving output")
    out_tree.Write()
    of.Close()
    return ofname

if __name__ == "__main__":
    filenames = sys.argv[2:]
    ofname = sys.argv[1]
    print main(filenames, ofname)
