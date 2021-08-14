import numpy as np

import matplotlib.pyplot as plt

import matplotlib.pylab as pylab

import sys
import argparse
parser = argparse.ArgumentParser(description='Choose category')
parser.add_argument(
    '--categories',
    action="store",
    help="Sample to process",
    required=True
)

args = parser.parse_args()

# Load data
categories = {}
categories["sl"] = ["pulls_sl_jge6_tge4_mu0", "pulls_sl_jge6_t3_mu0", "pulls_sl_j5_tge4_mu0", "pulls_sl_j5_t3_mu0", "pulls_sl_j4_tge4_mu0", "pulls_sl_j4_t3_mu0", "pulls_sl_jge6_tge4_mu1", "pulls_sl_jge6_t3_mu1", "pulls_sl_j5_tge4_mu1", "pulls_sl_j5_t3_mu1", "pulls_sl_j4_tge4_mu1", "pulls_sl_j4_t3_mu1"]
categories["sl_merged"] = ["pulls_SL_combined_mu0","pulls_SL_combined_mu1"]
categories["sldl"] = ["pulls_sl_jge6_tge4_mu0", "pulls_sl_jge6_t3_mu0", "pulls_sl_j5_tge4_mu0", "pulls_sl_j5_t3_mu0", "pulls_sl_j4_tge4_mu0", "pulls_sl_j4_t3_mu0", "pulls_sl_jge6_tge4_mu1", "pulls_sl_jge6_t3_mu1", "pulls_sl_j5_tge4_mu1", "pulls_sl_j5_t3_mu1", "pulls_sl_j4_tge4_mu1", "pulls_sl_j4_t3_mu1","pulls_dl_jge4_tge4_mu0","pulls_dl_jge4_t3_mu0","pulls_dl_jge4_tge4_mu1","pulls_dl_jge4_t3_mu1"]
categories["dl_merged"] = ["pulls_DL_combined_mu0","pulls_DL_combined_mu1"]
categories["sldl_merged"] = ["pulls_SLDL_combined_mu0","pulls_SLDL_combined_mu1"]
categories["resolved"] = ["pulls_SL_combined_mu0","pulls_SL_combined_mu1","pulls_DL_combined_mu0","pulls_DL_combined_mu1","pulls_SLDL_combined_mu0","pulls_SLDL_combined_mu1"]
categories["boosted"] = ["pulls_dl_jge4_tge4_sj_mu0","pulls_sl_j4_tge4_sj_mu0","pulls_sl_j5_tge4_sj_mu0","pulls_sl_jge6_tge4_sj_mu1","pulls_dl_jge4_tge4_sj_mu1","pulls_sl_j4_tge4_sj_mu1","pulls_sl_j5_tge4_sj_mu1","pulls_sl_jge6_tge4_sj_mu0"]
categories["boosted_merged"] = ["pulls_SL_sj_combined_mu0","pulls_SLDL_sj_combined_mu0","pulls_SL_sj_combined_mu1","pulls_SLDL_sj_combined_mu1"]
categories["BoostedAnalysis"] = ["pulls_BoostedAnalysis_mu0","pulls_BoostedAnalysis_mu1"]
categories["SLDL_combined_unblind"] = ["pulls_SLDL_combined_unblind"]
categories["BoostedAnalysisunblind"] = ["pulls_BoostedAnalysis_unblind"]
categories["allunblind"] = ["pulls_SLDL_combined_unblind","pulls_SL_combined_unblind","pulls_DL_combined_unblind","pulls_BoostedAnalysis_unblind"]
categories["sljetunblind"] = ["pulls_SL_j6_unblind","pulls_SL_j5_unblind","pulls_SL_j4_unblind"]
categories["sltagunblind"] = ["pulls_SL_3tag_combined_unblind","pulls_SL_4tag_combined_unblind"]
categories["boostedonlyunblind"] = ["pulls_SLDL_sj_combined_unblind"]
categories["boostedcombinedunblind"] = ["pulls_BoostedAnalysis_unblind"]
categories["test"] = ["test_normal"]
categories["vars_test"] = ["pulls_SLDL_combined_avgbtagbtag_coarse_mu0","pulls_SLDL_combined_avgdeta_coarse_mu0","pulls_SLDL_combined_avgdetabtag_coarse_mu0","pulls_SLDL_combined_avgbtagbtag_coarse_mu1","pulls_SLDL_combined_avgdeta_coarse_mu1","pulls_SLDL_combined_avgdetabtag_coarse_mu1"]
categories["4tag"] = ["pulls_4tag_mu0","pulls_4tag_mu1"]

for c in categories[args.categories]:
	f  = open("./{}.txt".format(c), "read") 
	print "./{}.txt".format(c)
	fout = open("./{}_out.txt".format(c),"w+")

	startmarker = -1
	for x in f:
		if "name" in x:
			startmarker = 0
			continue
		if startmarker == -1:
			continue
		if "prop_bin" in x:
			continue
		x = x.replace(',', ' ')
		x = x.replace('*', ' ')
		x = x.replace('!', ' ')
		x = str(startmarker) + " " + x
		startmarker += 1

		fout.write(x)

	f.close()
	fout.close()



