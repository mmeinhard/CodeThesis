#!/usr/bin/env python
########################################
# Imports
########################################

import os
import sys
import pdb
import json
import subprocess
import time
import ROOT

from FWCore.PythonUtilities.LumiList import LumiList

########################################
# Initialize
########################################

#/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_5/external/slc6_amd64_gcc530/bin/das_client.py
#das_client = os.path.join(
#    os.environ["CMSSW_RELEASE_BASE"],
#    "external",
#    os.environ["SCRAM_ARCH"],
#    "bin",
#    "das_client.py"
#)
#das_client = "/cvmfs/cms.cern.ch/common/das_client"

das_client = "dasgoclient"

output_base = os.path.join(
    os.environ["CMSSW_BASE"],
    "src/TTH/MEAnalysis/gc/datasets/",
)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Prepares dataset lists from DAS')
    parser.add_argument('--version', action="store", help="DAS pattern to search, also the output directory")
    parser.add_argument('--datasetfile', action="store", help="Input file with datasets")
    parser.add_argument('--instance', action="store", help="DBS instance", default="prod/phys03")
    parser.add_argument('--limit', action="store", help="max files per dataset", default=0)
    parser.add_argument('--debug', action="store", help="debug mode", default=False)
    parser.add_argument('--name', action="store", help="search only this dataset", default="*")
    parser.add_argument('--prefix', action="store", help="Prefix to add to filename", default="root://cmsxrootd.fnal.gov//")
    args = parser.parse_args()

    version = args.version
    dsnm = args.name
    prefix = args.prefix

    # Create directory for version under output_base
    outdir = os.path.join(output_base, version)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    ########################################
    # Get List of Datasets
    ########################################

    #no specified input dataset list
    if not args.datasetfile:
        #cmds = [ 
        #    das_client, 
        #    "--format=json",
        #    "--limit=0",
        #    '--query=dataset dataset=/{2}/*{0}*/USER instance={1}'.format(version, args.instance, dsnm)
        #]
	print '-query=file dataset=/{1}/*{0}*/NANOAODSIM'.format(version, dsnm)
        cmds = [
            das_client,
            '-query=file dataset=/{1}/*{0}*/NANOAODSIM'.format(version, dsnm),
            '-json'
        ]

        if args.debug:
            print " ".join(cmds)
        datasets_json = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read()
        if args.debug:
            print datasets_json
            print type(datasets_json)

        dataset = open(outdir + "/" + dsnm + ".txt", "w")
        print "Creating dataset file: ", outdir + dsnm + ".txt"
        print ("[" + dsnm + "]")
        dataset.write("[" + dsnm + "]\n")


        datasets_di = json.loads(datasets_json)

        datasets = [
            datasets_di[i][u'file'][0][u'name'] for i in range(len(datasets_di))
        ]

        print "Got {0} datasets".format(len(datasets))
        
        ds_list = []
        for da in datasets:
            print da
            ds_list += [da]

        for f in ds_list:

            rootfile = prefix + f
            print rootfile

            # get number of entries
            rf = ROOT.TFile.Open(rootfile)
            tree = rf.Get("Events")
            nevt = tree.GetEntries()

            print prefix + f + " = %i" % nevt
            dataset.write(prefix + f + " = %i\n" % nevt)

            rf.Close()

        dataset.close()



