import sys, logging, os
from TTH.MEAnalysis.nano_postproc import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser(description='Runs nanoAOD postprocessing')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        required=False,
        default="ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8"
    )
    parser.add_argument(
        '--analysis_cfg',
        action="store",
        help="Analysis cfg (eg. MEAnalysis/data/default.cfg)",
        required=False,
        default=os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/default.cfg"
    )
    parser.add_argument(
        '--testFile',
        action="store",
        help="File to test",
        required=False,
        default=None
    )
    parser.add_argument(
        '--isMC',
        action="store_true",
        help="Set if file is mc",
        required=False,
    )
    args = parser.parse_args(sys.argv[1:])

    if args.testFile is not None:
        files = [args.testFile]
        main(outdir="./", _input=files, asFriend = False, runAll=True, isMC = args.isMC)
    else:
        analysis = analysisFromConfig(args.analysis_cfg)

        samples = {
            sample.name: sample for sample in analysis.samples
        }
        sample = samples[args.sample] 

        files = sample.file_names_step1[:1]

    
        #Read official nanoAOD file
        if args.sample == "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8":
            files = ["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/18C1BD10-B842-E811-87AA-6CC2173D6B10.root"]
        main(outdir="./", _input=files)

