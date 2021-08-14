import sys

from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.MEAnalysis.MEAnalysis_heppy import main as tth_main

_file = sys.argv[1]

import argparse
parser = argparse.ArgumentParser(description='Runs nanoAOD postprocessing')
parser.add_argument(
    '--testFH',
    action="store_true",
    help="Set if file is mc",
    required=False,
)
args = parser.parse_args(sys.argv[2:])
if args.testFH:
    cfgPath = "MEAnalysis/test/config_test_FH.cfg"
    nEv = 14
else:
    cfgPath = "MEAnalysis/test/config_test.cfg"
    nEv = 50
an = analysisFromConfig(cfgPath)


tth_main(an, schema="mc", output_name="Output_ttH", files=_file, loglevel="DEBUG", numEvents=nEv)
