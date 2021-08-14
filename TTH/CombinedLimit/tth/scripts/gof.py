#!/usr/bin/env python

########################################
# Imports
########################################

import math
import argparse
import ROOT



ROOT.gROOT.SetBatch(ROOT.kTRUE)

def plot(output):

    f0 = ROOT.TFile.Open("higgsCombine_BoostedAnalysis_unblind.GoodnessOfFit.mH120.observed.root", "READ")
    ttree = f0.Get("limit")
    medium  = []
    for event in ttree:
        #print "...."
        medium.append(event.limit)
    f0.Close()

    f = ROOT.TFile.Open("higgsCombine_BoostedAnalysis_unblind.GoodnessOfFit.mH120.toys.root", "READ")
    ttree2 = f.Get("limit")
    values = []
    for event in ttree:
        #print "...."
        values.append(event.limit)
    f.Close()

    h = ROOT.TH1F("","",50,min(0, min(values)*0.9),max(values)*1.1)
    for v in values:
        h.Fill(v)

    
    print medium
    print values

    c = ROOT.TCanvas("aerg","",800,800)
    c.SetLeftMargin(0.16)
    
    W = 600
    H = 600
    H_ref = 600
    W_ref = 600
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref    
    
    c.SetLeftMargin(0.16)
    c.SetRightMargin(0.1)
    c.SetTopMargin(T/H)
    c.SetBottomMargin(B/H)
    
    #ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetOptStat(0)
    #ROOT.TGaxis.SetMaxDigits(3)    pad1.SetGrid() 

    h.Scale(1/300.)
    h.Draw()

    
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetXaxis().SetNdivisions(505)
    h.GetXaxis().SetTitleOffset(1)
    h.GetYaxis().SetTitleOffset(1)
    h.GetXaxis().SetTitle("test statistics")
    ROOT.gPad.SetTicks()
    
    


    x = ROOT.TLine(medium[0],0,medium[0],h.GetMaximum()*1.2)
    x.SetLineColor(ROOT.kRed)
    x.Draw()

    c.SaveAs("./GoodnessofFit_{}.png".format(output))
    c.SaveAs("./GoodnessofFit_{}.pdf".format(output))


    h.GetXaxis().SetRangeUser(medium[0],max(values)+5)
    print "Integral:", h.Integral()



if __name__ == "__main__":

    
    parser = argparse.ArgumentParser(description = 'Plot gof')
    
    parser.add_argument('--outputname', '-o', help = 'name of output plot', required = True)
    
    args = parser.parse_args()
    plot(args.outputname)
