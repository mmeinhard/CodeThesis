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

def main(filenames):
    filenames_pref = map(getSitePrefix, filenames)
    tree_list = ROOT.TList()

    #keep tfiles open for the duration of the merge
    tfiles = []
    for infn, lfn in zip(filenames_pref, filenames):
        tf = ROOT.TFile.Open(infn)
        tfiles += [tf]

        run_tree = tf.Get("Runs")
        if not run_tree:
            run_tree = tf.Get("nanoAOD/Runs")

        event_tree = tf.Get("Events")
        if not event_tree:
            event_tree = tf.Get("nanoAOD/Events")

        sumwnom = 0
        sumwnomw = 0
        sumwx = 0
        sumwxw = 0
        sumgen = 0

        for event in event_tree :
            #counter += 1

            sumwnom += event.LHEScaleWeight[4]
            sumwnomw += event.genWeight * event.LHEScaleWeight[4]
            sumwx += event.LHEScaleWeight[1]
            sumwxw += event.genWeight * event.LHEScaleWeight[1]
            sumgen += event.genWeight


    print sumwnom, sumwx, sumwnom/sumwx, sumwx/sumwnom
    print sumgen, sumwnom, sumwx, sumwx/sumgen, sumgen/sumwx
    print sumwnomw, sumwxw, sumwnomw/sumwxw, sumwxw/sumwnomw

if __name__ == "__main__":
    filenames = sys.argv[1:]
    print main(filenames)
