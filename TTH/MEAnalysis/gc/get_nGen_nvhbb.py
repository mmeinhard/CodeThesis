#!/usr/bin/env python
from TTH.MEAnalysis.ParHadd import par_hadd
import ROOT
import glob
import sys
import os, fnmatch

filenames = {
   #"datasets/JoosepFeb_nosyst_v1/JetHT_dsalerno-JoosepFeb_nosyst_v1-a91b745a2333df3c1dcf2cedb60be78c.txt",
   #"datasets/JoosepFeb_nosyst_v1/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_dsalerno-JoosepFeb_nosyst_v1-ad34c5d555175199a164e56760d04270.txt",
   #QCD300_ext1 (v2) files included in v1 txt file above
   "datasets/JoosepFeb_nosyst_v1/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_dsalerno-JoosepFeb_nosyst_v1-ad34c5d555175199a164e56760d04270.txt",
   #done"datasets/JoosepFeb_nosyst_v1/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_dsalerno-JoosepFeb_nosyst_v1-ad34c5d555175199a164e56760d04270.txt",
   #"datasets/JoosepFeb_nosyst_v1/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_dsalerno-JoosepFeb_nosyst_v1-ad34c5d555175199a164e56760d04270.txt",
   #"datasets/JoosepFeb_nosyst_v1/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_dsalerno-JoosepFeb_nosyst_v1-ad34c5d555175199a164e56760d04270.txt",
   #"datasets/JoosepFeb_nosyst_v1/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_dsalerno-JoosepFeb_nosyst_v1-ad34c5d555175199a164e56760d04270.txt",
   #"datasets/JoosepFeb_nosyst_v1/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8_dsalerno-JoosepFeb_nosyst_v1-bcaebf0a02c198095baf78b8701e80aa.txt",
   #"datasets/JoosepFeb_nosyst_v2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_dsalerno-JoosepFeb_nosyst_v2-8db24930f7b7d32a444074088a119384.txt",
}

#prefix = "root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat"
prefix = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/"

print "sample nvhbb nGen %"
for fname in filenames:
    nGen = 0
    nvhbb = 0
    sample = fname.split("/")[2].split("_dsalerno")[0]
    #print sample
    f = open(fname)
    lines = f.readlines()
    for l in lines:
        if not (l.find('.root')>0):
            continue
        rootfile = l.split()[0]
        longfile = prefix+rootfile
        #print longfile
        try:
            file_ = ROOT.TFile.Open(longfile)
        except:
            print "cannot open file",rootfile
            continue
        if not file_ or file_.IsZombie():
            print "zombie file",rootfile
            continue
        count_gen = file_.Get("vhbb/Count")
        count_vhbb = file_.Get("CounterAnalyzer_count")
        #print l
        #print type( count_gen)
        #print type( count_vhbb)
        try:
            nGen += count_gen.GetBinContent(1)
            nvhbb += count_vhbb.GetBinContent(1)
        except:
            print "missing histogram",rootfile

    print sample,nvhbb,nGen,(100.0*nvhbb/nGen)
