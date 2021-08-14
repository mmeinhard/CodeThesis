import subprocess
import copy, os
import unittest
import logging
import ROOT

from TTH.Plotting.joosep.sparsinator import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis tests')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        required=True,
    )
    parser.add_argument(
        '--analysis_cfg',
        action="store",
        help="Analysis cfg (eg. MEAnalysis/data/default.cfg)",
        required=False,
        default=os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/default.cfg"
    )
    args = parser.parse_args()

    analysis = analysisFromConfig(args.analysis_cfg)
    file_names = analysis.get_sample(args.sample).file_names
    file_names = [fi.replace("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/", "root://t3se.psi.ch//") for fi in file_names]
    main(analysis, file_names, args.sample, "out.root", 0, 10000, "*")
