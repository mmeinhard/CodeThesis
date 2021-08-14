import sys

from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.MEAnalysis.MEAnalysis_heppy import main as tth_main

_file = sys.argv[1]

an = analysisFromConfig("MEAnalysis/test/config_test.cfg")
tth_main(an, schema="data", output_name="Output_data", files=_file, loglevel="DEBUG")
