import ROOT
import os
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix

# function to get btag pdfs 
def pdfs(file_names):

    chain = ROOT.TChain("tree")
    for file_name in file_names:
        print "Adding file {0}".format(file_name)
        chain.AddFile(file_name)
    print "Chain contains {0} events".format(chain.GetEntries())

    btaggers = ["btagCSV", "btagDeepCSV", "btagCMVA"]

    # disable branches not needed
    chain.SetBranchStatus("*", 0)
    chain.SetBranchStatus("numJets", 1)
    for b in btaggers:
        chain.SetBranchStatus("jets_" + b, 1)
    chain.SetBranchStatus("jets_pt", 1)
    chain.SetBranchStatus("jets_eta", 1)
    chain.SetBranchStatus("jets_hadronFlavour", 1)
    chain.SetBranchStatus("jets_id", 1)

    # initialize output file
    output = ROOT.TFile("out.root", "RECREATE")

    # initialize histograms
    h = {}
    flavour = ["b", "c", "l"]
    btaggers = ["btagCSV", "btagDeepCSV", "btagCMVA"]
   
    for b in btaggers:
        for f in flavour:
            h[b + "_" + f + "_Bin0__rec"] = ROOT.TH1D(b + "_" + f + "_Bin0__rec", b + "_" + f + "_Bin0__rec", 100, 0, 1)
            h[b + "_" + f + "_Bin1__rec"] = ROOT.TH1D(b + "_" + f + "_Bin1__rec", b + "_" + f + "_Bin1__rec", 100, 0, 1)
            h[b + "_" + f + "_pt_eta"] = ROOT.TH3D(b + "_" + f + "_pt_eta", b + "_" + f + "_pt_eta", 6, 20, 400, 6, 0, 2.4, 20, 0, 1)


    for iEv in range(chain.GetEntries()):

        chain.GetEntry(iEv)


        # loop over jets in event
        for ijet in range(chain.numJets):

            pt = chain.jets_pt[ijet]
            eta = chain.jets_eta[ijet]
            ID = chain.jets_id[ijet]

            if pt>20 and np.abs(eta) < 2.4 and ID>=1:
    
                for b in btaggers:
                    btag = getattr(chain, "jets_" + b)[ijet]

                    # light jets
                    if chain.jets_hadronFlavour[ijet] != 4 and chain.jets_hadronFlavour[ijet] != 5: 
                        h[b + "_" + "l" + "_pt_eta"].Fill(pt, eta, btag)
                        if eta <= 1.0:
                            h[b + "_" + "l" + "_Bin0__rec"].Fill(btag)
                        if eta > 1.0:
                            h[b + "_" + "l" + "_Bin1__rec"].Fill(btag)
                    # c jets
                    if chain.jets_hadronFlavour[ijet] == 4:
                        h[b + "_" + "c" + "_pt_eta"].Fill(pt, eta, btag)
                        if eta <= 1.0:
                            h[b + "_" + "c" + "_Bin0__rec"].Fill(btag)
                        if eta > 1.0:
                            h[b + "_" + "c" + "_Bin1__rec"].Fill(btag)
                    # b jets
                    if chain.jets_hadronFlavour[ijet] == 5:
                        h[b + "_" + "b" + "_pt_eta"].Fill(pt, eta, btag)
                        if eta <= 1.0:
                            h[b + "_" + "b" + "_Bin0__rec"].Fill(btag)
                        if eta > 1.0:
                            h[b + "_" + "b" + "_Bin1__rec"].Fill(btag)
 
    for b in btaggers:
        for f in flavour:

            key = b + "_" + f

            """
            !!! Normalization done in different file, so that hadd can be used for the gc output
            # normalize 1D histograms
            norm = h[key + "_Bin0__rec"].GetEntries()
            h[key +  "_Bin0__rec"].Scale(1/float(norm))
            norm = h[key +  "_Bin1__rec"].GetEntries()
            h[key + "_Bin1__rec"].Scale(1/float(norm))

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
            """
            #h[key +  "_Bin0__rec"].Write()
            #h[key +  "_Bin1__rec"].Write()
            h[key + "_pt_eta"].Write()

    output.Close()

    print "all btag pdf histograms written in File"

if __name__ == "__main__":

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        print file_names
    else:
        file_names = np.loadtxt("/mnt/t3nfs01/data01/shome/creissel/tth/2017/sw/CMSSW_9_4_5_cand1/src/TTH/MEAnalysis/gc/datasets/Apr16/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.txt", usecols = [0], dtype = str, skiprows = 1)
        file_names = file_names[:1]
        # print file_names

    pdfs(file_names)
