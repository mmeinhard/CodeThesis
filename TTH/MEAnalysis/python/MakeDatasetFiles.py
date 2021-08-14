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
das_client = "/cvmfs/cms.cern.ch/common/das_client"
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
    parser.add_argument('--prefix', action="store", help="Prefix to add to filename", default="")
    parser.add_argument('--doLumis', action="store_true", help="Get the lumi-sections")
    args = parser.parse_args()
    
    version = args.version
    dsnm = args.name
    
    # Create directory for version under output_base
    outdir = os.path.join(output_base, version)
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    ########################################
    # Get List of Datasets
    ########################################
    
    #no specified input dataset list
    if not args.datasetfile:
        cmds = [ 
            das_client, 
            "--format=json",
            "--limit=0",
            '--query=dataset dataset=/{2}/*{0}*/USER instance={1}'.format(version, args.instance, dsnm)
        ]
        if args.debug:
            print " ".join(cmds)
        datasets_json = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read()
        if args.debug:
            print datasets_json
        
        datasets_di = json.loads(datasets_json)
        datasets = [
            d["dataset"][0]["name"] for d in datasets_di["data"]
        ]
        
        print "Got {0} datasets".format(len(datasets))
        
        ds_list = []
        for dataset in datasets:
            print dataset
            ds_list += [dataset]
    else:
        datasets = filter(
            lambda x: len(x)>0 and not x.startswith("#"),
            map(lambda x: x.strip(),
                open(args.datasetfile).readlines()
            )
        )
    ########################################
    # And add .txt for each of them
    ########################################
    
    samples_processed = []
    for ds in datasets:
    
        print "Doing", ds
        
        # Extract sample
        # Example:
        # /TTTo2L2Nu_13TeV-powheg/jpata-VHBBHeppyV21_tthbbV6_TTTo2L2Nu_13TeV-powheg__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1-827a43512a0ceecb1e2aee5987443e5a/USER
        # Yields:
        # sample = TTTo2L2Nu_13TeV-powheg
        sample  = "_".join(ds.split("/")[1:3])
        sample_short  = ds.split("/")[1]
        
        ofile_fn = os.path.join(outdir, sample_short + ".txt")
        if sample_short in samples_processed:
            print "opening existing file"
            ofile = open(ofile_fn, "a")
        else:
            print "opening new file"
            ofile = open(ofile_fn, "w")
            ofile.write("[{0}]\n".format(sample_short))
        

        files_json = subprocess.Popen([
            "{0} --query='file dataset={1} instance={2}' --format=json --limit={3} --threshold=600".format(
            das_client, ds, args.instance, args.limit)
            ], stdout=subprocess.PIPE, shell=True
        ).stdout.read()
        files_di = json.loads(files_json)
       
        
        try:
            print "Got {0} files".format(len(files_di['data']))
        except Exception as e:
            print "Could not parse 'data' in output json"
            print files_di
            raise e
       
        #Create dict of filename -> run -> lumis
        if args.doLumis:
            files_run_lumi_json = subprocess.Popen([
                "{0} --query='file,run,lumi dataset={1} instance={2}' --format=json --limit={3} --threshold=600".format(
                das_client, ds, args.instance, args.limit)
                ], stdout=subprocess.PIPE, shell=True
            ).stdout.read()
            files_run_lumi = json.loads(files_run_lumi_json)
            
            lumis_dict = {}
            for fi in files_run_lumi["data"]:
                fn = fi["file"][0]["name"]
               
                if not lumis_dict.has_key(fn):
                    lumis_dict[fn] = {}
                for run, lumis in zip(fi["run"], fi["lumi"]):
                    run_num = run["run_number"]
                    if not lumis_dict[fn].has_key(run_num):
                        lumis_dict[fn][run_num] = []
                    lumis_dict[fn][run_num] += lumis["number"]

        lumis = []
        for ifile, fi in enumerate(files_di['data']):
            name = None
            try:
                name = fi["file"][0]["name"]
            except Exception as e:
                print "Could not parse file name", fi
                name = None
            
            if name:
                try:
                    nevents = fi["file"][0]["nevents"]
                except Exception as e:
                    print "Could not parse nevents", fi["file"][0]
                    nevents = 0
                if args.doLumis:
                    if lumis_dict.has_key(name):
                        tmp_lumis = LumiList(runsAndLumis = lumis_dict[name])
                        lumis += [tmp_lumis]
                    else:
                        if nevents > 0:
                            raise Exception("file {0} has no associated lumis (events={1})".format(name, nevents))
                        else:
                            print "file {0} has no associated lumis (events={1})".format(name, nevents)
                ofile.write("{0} = {1}\n".format(args.prefix + name, nevents))
            #merge lumi files

        if args.doLumis:
            #merge lumi files
            total_lumis = LumiList()
            lumi_fn = ofile_fn.replace(".txt", ".json")
            if sample_short in samples_processed:
                total_lumis = LumiList(filename = lumi_fn)
                print "opened existing lumi file", len(total_lumis)
            for i in range(len(lumis)):
                total_lumis = total_lumis + lumis[i]
            total_lumis.writeJSON(fileName=lumi_fn)
            #end loop over files

            #write per-file lumi dictionary 
            with open(ofile_fn.replace(".txt", "_lumi_per_file.json"), "w") as fi:
                fi.write(json.dumps(lumis_dict, indent=2))

        ofile.close()
        samples_processed += [sample_short]
        #sleep so as to not overload the DAS server
        time.sleep(60)
        
