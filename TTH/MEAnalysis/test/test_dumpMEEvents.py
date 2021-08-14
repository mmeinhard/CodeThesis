import sys, logging, os

from TTH.MEAnalysis.dumpMEEvents import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig


def test_dumpMEEvents(sample_name, analysis_cfg_path):
    analysis = analysisFromConfig(analysis_cfg_path)
    sample = analysis.get_sample(sample_name)
    files = sample.file_names[:sample.debug_max_files]

    return main(sample, files)

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
    args = parser.parse_args(sys.argv[1:])
    test_dumpMEEvents(args.sample, args.analysis_cfg)
