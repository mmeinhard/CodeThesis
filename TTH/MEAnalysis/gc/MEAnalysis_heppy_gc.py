#!/usr/bin/env python

#Need to enable ROOT batch mode to prevent it from importing libXpm, which may cause a crash
import ROOT
ROOT.gROOT.SetBatch(True)

import os
#pickle and transfer function classes to load transfer functions
import cPickle as pickle
#to prevent pickle import error
#== CMSSW:    File "MEAnalysis_heppy.py", line 33, in <module>
#== CMSSW:      conf.tf_matrix = pickle.load(pi_file)
#== CMSSW:    File "/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd4/lib/ROOT.py", line 353, in _importhook
#== CMSSW:      return _orig_ihook( name, glbls, lcls, fromlist, level )
#== CMSSW:  ImportError: No module named TFClasses
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
sys.modules["TFClasses"] = TFClasses

from TTH.MEAnalysis.MEAnalysis_heppy import main
import FWCore.ParameterSet.Config as cms
from TTH.MEAnalysis.samples_base import getSitePrefix
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
import TTH.MEAnalysis.counts as counts
import logging

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    an = analysisFromConfig(sys.argv[1])
    firstEvent = int(os.environ["SKIP_EVENTS"])
    nEvents = int(os.environ["MAX_EVENTS"])
    fns = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    dataset = os.environ["DATASETPATH"].split("__")[-1]

    main(an, sample_name=dataset, firstEvent=firstEvent, numEvents=nEvents, output_name="Loop", files=fns)
