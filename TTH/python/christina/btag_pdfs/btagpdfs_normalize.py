import ROOT
import os
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix
from rootpy.io import root_open

# function to get btag pdfs 
def normalize(rootfile):

    file = ROOT.TFile(rootfile, "READ")

    # initialize output file
    output = ROOT.TFile("3Dplots_2017.root", "RECREATE")

    # initialize histograms
    h = {}
    flavour = ["b", "c", "l"]
    btaggers = ["btagCSV", "btagDeepCSV", "btagCMVA"]
   
    for b in btaggers:
        for f in flavour:

            key = b + "_" + f
            h[key + "_pt_eta"] = file.Get(key + "_pt_eta")

            # normalize 3D histogram
            nbinX = h[key + "_pt_eta"].GetNbinsX()
            nbinY = h[key + "_pt_eta"].GetNbinsY()
            nbinZ = h[key + "_pt_eta"].GetNbinsZ()

            for i in range(nbinX+2):
                for j in range(nbinY+2):

                    s =  h[key + "_pt_eta"].ProjectionZ("projz", i, i, j, j).Integral()
                    for k in range(0, nbinZ + 2):
                        Bin = h[key + "_pt_eta"].GetBinContent(i,j,k)
                        if s > 0:
                            h[key + "_pt_eta"].SetBinContent(i,j,k, float(Bin)/float(s))

            h[key + "_pt_eta"].Write()

    output.Close()

    print "all btag pdf histograms written in File"

if __name__ == "__main__":

    normalize("/mnt/t3nfs01/data01/shome/creissel/tth/2017/gc/btagpdf/GCad486ee0dc0d/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/3Dplots_2017.root")
