

# -*- coding: utf-8 -*-

"""

@author: maren

"""

import math

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
categories["sldl_unblind"] = ["SL_combined_unblind","DL_combined_unblind"]
categories["sldl_merged"] = ["SLDL_combined"]
categories["sldl_merged_unblind"] = ["SLDL_combined_unblind"]
categories["resolved"] = ["SL_combined","DL_combined","SLDL_combined"]
categories["boosted"] = ["dl_jge4_tge4_sj","sl_j4_tge4_sj","sl_j5_tge4_sj","sl_jge6_tge4_sj"]
categories["boosted_merged"] = ["SL_sj_combined","SLDL_sj_combined"]
categories["BoostedAnalysis"] = ["BoostedAnalysis"]
categories["BoostedAnalysis"] = ["BoostedAnalysis_unblind"]

import sys
import argparse
parser = argparse.ArgumentParser(description='Choose category')
# either stasyst or all
parser.add_argument(
    '--type',
    action="store",
    help="Type of unceratinty",
    required=True
)
parser.add_argument(
    '--category',
    action="store",
    help="SL, DL or SLDL or something for boosted which I will add later",
    required=True
)

args = parser.parse_args()




fnofreeze = ROOT.TFile.Open("higgsCombine_{}.FitDiagnostics.mH120.root".format(args.category), "READ")
fallfreeze = ROOT.TFile.Open("higgsCombine_{}_freezeAll.FitDiagnostics.mH120.root".format(args.category), "READ")
ttreenofreeze = fnofreeze.Get("limit")
ttreeallfreeze = fallfreeze.Get("limit")
valuesfreezeint = []
valuesnofreezeint = []
valuesfreeze = []  # Nominal / Up / Down
valuesnofreeze = []
for event in ttreeallfreeze:
	valuesfreezeint.append(event.limit)
for event in ttreenofreeze:
	valuesnofreezeint.append(event.limit)
valuesfreeze.append(valuesfreezeint[0])
valuesfreeze.append(valuesfreezeint[2]-valuesfreezeint[0])
valuesfreeze.append(valuesfreezeint[0]-valuesfreezeint[1])
valuesnofreeze.append(valuesnofreezeint[0])
valuesnofreeze.append(valuesnofreezeint[2]-valuesnofreezeint[0])
valuesnofreeze.append(valuesnofreezeint[0]-valuesnofreezeint[1])
if abs(valuesfreeze[0] - valuesnofreeze[0])  > 0:
	print "Problem somewhere!"
print "total error : - ", round(valuesnofreeze[2],2), " / + ", round(valuesnofreeze[1],2)
print "stat error : - ", round(valuesfreeze[2],2), " / + ", round(valuesfreeze[1],2)
systerrorup = math.sqrt(valuesnofreeze[1]*valuesnofreeze[1]-valuesfreeze[1]*valuesfreeze[1]) 
systerrordown = math.sqrt(valuesnofreeze[2]*valuesnofreeze[2]-valuesfreeze[2]*valuesfreeze[2]) 
print "syst error : - ", round(systerrordown,2), " / + ", round(systerrorup,2)

if "Boosted" in args.category:
    doboosted = True
else:
    doboosted = False

if args.type == "all":
	fexp = ROOT.TFile.Open("higgsCombine_{}_exp.FitDiagnostics.mH120.root".format(args.category), "READ")
	ftheory = ROOT.TFile.Open("higgsCombine_{}_theory.FitDiagnostics.mH120.root".format(args.category), "READ")
	fbtag = ROOT.TFile.Open("higgsCombine_{}_btag.FitDiagnostics.mH120.root".format(args.category), "READ")
	fjec = ROOT.TFile.Open("higgsCombine_{}_jec.FitDiagnostics.mH120.root".format(args.category), "READ")
	fmisc = ROOT.TFile.Open("higgsCombine_{}_bgnorm.FitDiagnostics.mH120.root".format(args.category), "READ")
	fisrfsr = ROOT.TFile.Open("higgsCombine_{}_isrfsr.FitDiagnostics.mH120.root".format(args.category), "READ")
	fhdampue = ROOT.TFile.Open("higgsCombine_{}_hdampue.FitDiagnostics.mH120.root".format(args.category), "READ")
	fpdf = ROOT.TFile.Open("higgsCombine_{}_pdf.FitDiagnostics.mH120.root".format(args.category), "READ")
	fscale = ROOT.TFile.Open("higgsCombine_{}_scale.FitDiagnostics.mH120.root".format(args.category), "READ")
	fstats = ROOT.TFile.Open("higgsCombine_{}_autoMCStats.FitDiagnostics.mH120.root".format(args.category), "READ")
	fbgnorm = ROOT.TFile.Open("higgsCombine_{}_bgnorm.FitDiagnostics.mH120.root".format(args.category), "READ")
	if doboosted:
	    fboosted = ROOT.TFile.Open("higgsCombine_{}_boosted.FitDiagnostics.mH120.root".format(args.category), "READ")
	ttreeexp = fexp.Get("limit")
	ttreetheory = ftheory.Get("limit")
	ttreebtag = fbtag.Get("limit")
	ttreejec = fjec.Get("limit")
	ttreemisc = fmisc.Get("limit")
	ttreeisrfsr = fisrfsr.Get("limit")
	ttreehdampue = fhdampue.Get("limit")
	ttreepdf = fpdf.Get("limit")
	ttreescale = fscale.Get("limit")
	ttreestats = fstats.Get("limit")	
	ttreebgnorm = fbgnorm.Get("limit")
	if doboosted:
            ttreeboosted = fboosted.Get("limit")
	valuesexpint = []
	valuestheoryint = []
	valuesbtagint = []
	valuesjecint = []
	valuesmiscint = []
	valuesisrfsrint = []
	valueshdampueint = []
	valuespdfint = []
	valuesscaleint = []
	valuesstatsint = []
	valuesbgnormint = []
	valuesboostedint = []
	#valuesexp = []
	#valuestheory = []
	#valuesbtag = []
	#valuesjec = []
	#valuesmisc = []
	#valuesisrfsr = []
	#valueshdampue = []
	#valuespdf = []
	#valuesscale = []
	for event in ttreeexp:
		valuesexpint.append(event.limit)
	for event in ttreetheory:
		valuestheoryint.append(event.limit)
	for event in ttreebtag:
		valuesbtagint.append(event.limit)
	for event in ttreejec:
		valuesjecint.append(event.limit)
	for event in ttreemisc:
		valuesmiscint.append(event.limit)
	for event in ttreeisrfsr:
		valuesisrfsrint.append(event.limit)
	for event in ttreehdampue:
		valueshdampueint.append(event.limit)
	for event in ttreepdf:
		valuespdfint.append(event.limit)
	for event in ttreescale:
		valuesscaleint.append(event.limit)
	for event in ttreestats:
		valuesstatsint.append(event.limit)
	for event in ttreebgnorm:
		valuesbgnormint.append(event.limit)
	if doboosted:
	    for event in ttreeboosted:
		valuesboostedint.append(event.limit)

	unc = ["exp","btag","jec","misc","stats","theory","isrfsr","hdampue","pdf","scale","bgnorm","boosted"]

	if not doboosted:
	    unc.remove("boosted")

	values = {}
	valuesint = {}
	valuesint["exp"] = valuesexpint
	valuesint["theory"] = valuestheoryint
	valuesint["btag"] = valuesbtagint
	valuesint["jec"] = valuesjecint
	valuesint["misc"] = valuesmiscint
	valuesint["isrfsr"] = valuesisrfsrint
	valuesint["hdampue"] = valueshdampueint
	valuesint["pdf"] = valuespdfint
	valuesint["scale"] = valuesscaleint
	valuesint["stats"] = valuesstatsint
	valuesint["bgnorm"] = valuesbgnormint
	if doboosted:
	    valuesint["boosted"] = valuesboostedint

	for i in unc:
		values[i] = []
		values[i].append(valuesint[i][0])
		values[i].append(valuesint[i][2]-valuesint[i][0])
		values[i].append(valuesint[i][0]-valuesint[i][1])


	for i in unc:
		print i, values[i][1], valuesfreeze[1]
		systerrorup = math.sqrt(values[i][1]*values[i][1]-valuesfreeze[1]*valuesfreeze[1]) 
		systerrordown = math.sqrt(values[i][2]*values[i][2]-valuesfreeze[2]*valuesfreeze[2]) 

		print i, " / - ", round(systerrordown,2), " : + ", round(systerrorup,2)#c, values[i][1], valuesfreeze[2]



	fexp.Close()
	ftheory.Close()
	fbtag.Close()
	fjec.Close()
	fmisc.Close()
	fisrfsr.Close()
	fhdampue.Close()
	fpdf.Close()
	fscale.Close()
	fstats.Close()
	fbgnorm.Close()
	if doboosted:
	    fboosted.Close()

fnofreeze.Close()
fallfreeze.Close()



