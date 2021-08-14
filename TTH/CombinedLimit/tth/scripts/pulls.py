

# -*- coding: utf-8 -*-

"""

Created on Thu Mar 30 11:14:34 2017

@author: chrissi

"""

import numpy as np

import matplotlib.pyplot as plt

import matplotlib.pylab as pylab

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
categories["BoostedAnalysisunblind"] = ["pulls_BoostedAnalysis_unblind"]
categories["allunblind"] = ["pulls_SLDL_combined_unblind","pulls_SL_combined_unblind","pulls_DL_combined_unblind","pulls_BoostedAnalysis_unblind"]
categories["sljetunblind"] = ["pulls_SL_j6_unblind","pulls_SL_j5_unblind","pulls_SL_j4_unblind"]
categories["sltagunblind"] = ["pulls_SL_3tag_combined_unblind","pulls_SL_4tag_combined_unblind"]
categories["boostedonlyunblind"] = ["pulls_SLDL_sj_combined_unblind"]
categories["boostedcombinedunblind"] = ["pulls_BoostedAnalysis_unblind"]
categories["test"] = ["test_normal"]
categories["SLDL_combined_unblind"] = ["pulls_SLDL_combined_unblind"]
#categories["vars_test"] = ["SLDL_combined_avgbtagbtag_coarse","SLDL_combined_avgdeta_coarse","SLDL_combined_avgdetabtag_coarse"]
categories["vars_test"] = ["pulls_SLDL_combined_avgbtagbtag_coarse_mu0","pulls_SLDL_combined_avgdeta_coarse_mu0","pulls_SLDL_combined_avgdetabtag_coarse_mu0","pulls_SLDL_combined_avgbtagbtag_coarse_mu1","pulls_SLDL_combined_avgdetabtag_coarse_mu1"]
categories["4tag"] = ["pulls_4tag_mu0","pulls_4tag_mu1"]


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
	data = np.loadtxt("./{}_out.txt".format(c), usecols = (0,2,3,4,5))
	
	names = np.loadtxt("./{}_out.txt".format(c), usecols = [1], dtype = str)
	
	params = {'legend.fontsize': 'x-large', 'axes.labelsize': 'x-large', 'axes.titlesize':'x-large', 'xtick.labelsize':'x-large', 'ytick.labelsize':'x-large'}
	
	pylab.rcParams.update(params)
	
	x = data[:,0]
	b = data[:,1]
	b_err = data[:,2]
	sb = data[:,3]
	sb_err = data[:,4]

	names2 = []
	names3 = []

	for i in names:
		names2.append(i.replace("CMS_",""))
	#	#i = b

	for i in names2:
		names3.append(i.replace("_j",""))
#
	print names3


	#fig, ax = plt.subplots(1,1)
	fig = plt.figure(figsize=(5,15))
	ax = plt.subplot(111)
	plt.subplots_adjust(left=0.94, bottom=0.1, right=0.95, top=0.95, wspace=0, hspace=1)
	#fig = plt.figure()
	#ax.plot([0, 20], [0, 0], ls="-", c=".3")
	#plt.plot(x, , ls = '-', c = ".3")
	ax.errorbar(b, x, xerr=[b_err,b_err], ls='none', color='blue', alpha = 1.0, marker = '.', capsize=2, label = 'B')
	ax.errorbar(sb, x + 0.2, xerr=[sb_err,sb_err], ls='none', color='red', alpha = 1.0, marker = '.', capsize=2, label = 'S+B')
	#plt.xlim([-3,3])
	#ax.ylim([-3.0,3.0])
	ax.set_xlim([-3, 4])
	#ax.set_ylim([0, 5]
	ax.set_xlabel(r'$(\hat{\theta}-\theta_{0})/\Delta\theta$')
	ax.set_yticks(x)
	ax.set_yticklabels(names3, rotation = 'horizontal', fontsize = 10)
	ax.axvline(0, 0, 1, color='black', lw=2, alpha=1.0)
	ax.axvspan(-1, 1, alpha=0.1, color='0.3', label = 'prefit')
	ax.legend(loc = 'upper right', frameon = False, numpoints = 1 )
	plt.grid()
	plt.text(-6.5, 73,
		r"$\mathbf{CMS}$ Work In Progress",
		fontsize=16, ha="left", va="top", fontname="Helvetica"
	)
	plt.text(4, 73,
		"$41.5\ \mathrm{fb}^{-1}\ \mathrm{(13\ TeV)}$",
		fontsize=16, ha="right", va="top", fontname="Helvetica"
	)
	plt.gcf().subplots_adjust(top=0.8)
	#plt.ylabel(r'$\mu_{FIT}$')
	#plt.xlabel(r'$\mu_{INPUT}$')
	#plt.title('Comparison between combine & python results')
	plt.gcf().subplots_adjust(left=0.2)
	fig.savefig("./{}_plot.pdf".format(c), bbox_inches='tight')
	#plt.show()
	
	
	
