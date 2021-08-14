import subprocess
import copy, os
import logging
import ROOT
import fnmatch
import sys
from TTH.MEAnalysis.MEAnalysis_heppy import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

def launch_test_MEAnalysis(analysis, sample, **kwargs):
    output_name = "Loop_{0}".format(sample)
    main(analysis, sample_name=sample, firstEvent=0, output_name = output_name, **kwargs)
    return output_name

def test_MEAnalysis(insample="*", infile=None, **kwargs):
    analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/config_FH.cfg")
    for sample in analysis.samples:
        if insample == sample.name:
            logging.info("Running on sample {0}".format(sample.name))
            out = launch_test_MEAnalysis(analysis, sample.name, numEvents=analysis.config.getint(sample.name, "test_events"), files=[infile])
            
            tf = ROOT.TFile(out + "/tree.root")
            tt = tf.Get("tree")
            if not tt:
                raise Exception("Could not find tree in output")
            logging.info("produced {0} entries".format(tt.GetEntries()))
            
            tf.Close()
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis tests')
    parser.add_argument(
        '--sample',
        action="store",
        help="Samples to process, glob pattern",
        required=False,
        default="*"
    )
    parser.add_argument(
        '--file',
        action="store",
        help="Input vhbb file",
        required=False,
        default=None
    )
    args = parser.parse_args(sys.argv[1:])
    test_MEAnalysis(args.sample,args.file)
