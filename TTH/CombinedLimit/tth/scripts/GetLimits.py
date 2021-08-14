


# -*- coding: utf-8 -*-

"""

@author: maren

"""

import numpy as np

import matplotlib.pyplot as plt

import matplotlib.pylab as pylab

import ROOT

# Load data
categories = {}
categories["sl"] = ["sl_jge6_tge4", "sl_jge6_t3", "sl_j5_tge4", "sl_j5_t3", "sl_j4_tge4", "sl_j4_t3"]
categories["sl_merged"] = ["SL_combined"]
categories["sldl"] = ["sl_jge6_tge4", "sl_jge6_t3", "sl_j5_tge4", "sl_j5_t3", "sl_j4_tge4", "sl_j4_t3","dl_jge4_tge4","dl_jge4_t3",]
categories["dl_merged"] = ["DL_combined"]
categories["sldl_merged"] = ["SLDL_combined"]
categories["sldl_unblind"] = ["SL_combined_unblind","DL_combined_unblind"]
categories["resolved"] = ["SL_combined","DL_combined","SLDL_combined"]
categories["boosted"] = ["dl_jge4_tge4_sj","sl_j4_tge4_sj","sl_j5_tge4_sj","sl_jge6_tge4_sj"]
categories["boosted_v2"] = ["dl_jge4_tge4_sj_only","sl_j4_tge4_sj_only","sl_j5_tge4_sj_only","sl_jge6_tge4_sj_only"]
categories["boosted_merged"] = ["BoostedAnalysis"]
categories["boosted_merged_unblind"] = ["BoostedAnalysis_unblind"]
categories["vars_test"] = ["SLDL_combined_avgbtagbtag_coarse","SLDL_combined_avgdeta_coarse","SLDL_combined_avgdetabtag_coarse"]
categories["sldl_merged_unblind"] = ["SLDL_combined_unblind"]
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

for c in categories[args.categories]:
	if "unblind" in c:
	    f = ROOT.TFile.Open("higgsCombine_{}.AsymptoticLimits.mH120.root".format(c), "READ")
	else:
            f = ROOT.TFile.Open("higgsCombine_{}_mu0.AsymptoticLimits.mH120.root".format(c), "READ")
	ttree = f.Get("limit")
	values  = []
	for event in ttree:
		#print "...."
		values.append(event.limit)
		#print values

	print c, round(values[5],2), "$^{-" ,round(values[5]-values[1],2), "}_{+", round(values[3]-values[5],2),"}$"

	f.Close()

