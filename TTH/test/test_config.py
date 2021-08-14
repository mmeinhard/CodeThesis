from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

import unittest
import os
import logging


class TestAnalysisConfig(unittest.TestCase):

    def test_config_creation(self):
        path = os.path.join([os.environ["CMSSW_BASE"], "MEAnalysis/data/default.cfg"])
        cfg = analysisFromConfig(path)
        self.assertTrue(len(cfg.samples) > 0)
        self.assertTrue(len(cfg.categories) > 0)
        self.assertTrue(len(cfg.groups) > 0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
