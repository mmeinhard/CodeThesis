import ROOT
import sys, os
from TTH.MEAnalysis.samples_base import getSitePrefix

datatypes = sys.argv[2:]
print datatypes

minimalTriggers = False

ofname = sys.argv[1]
tt = ROOT.TChain("tree")
for fi in os.environ["FILE_NAMES"].split():
    print "adding", fi
    fn = getSitePrefix(fi)
    tf = ROOT.TFile.Open(fn)
    if not tf or tf.IsZombie():
        raise Exception("Could not open file: {0}".format(fn))
    tf.Close() 
    tt.AddFile(fn)


tt.SetBranchStatus("*", False)
if "all" in datatypes:
    tt.SetBranchStatus("*", True)
    
tt.SetBranchStatus("is_*", True)
tt.SetBranchStatus("numJets*", True)
tt.SetBranchStatus("nB*", True)
tt.SetBranchStatus("n*", True)
tt.SetBranchStatus("ttCls", True)
tt.SetBranchStatus("run", True)
tt.SetBranchStatus("lumi", True)
tt.SetBranchStatus("evt", True)
tt.SetBranchStatus("*eight*", True)
tt.SetBranchStatus("btagWeight*", True)
tt.SetBranchStatus("puWeight*", True)
tt.SetBranchStatus("jets_*", True)
tt.SetBranchStatus("njets", True)
tt.SetBranchStatus("leps_pt*", True)
tt.SetBranchStatus("leps_eta*", True)
tt.SetBranchStatus("leps_pdgId*", True)
tt.SetBranchStatus("leps_iso*", True)
tt.SetBranchStatus("nleps", True)
tt.SetBranchStatus("Wmass*", True)
tt.SetBranchStatus("qg_LR*", True)
tt.SetBranchStatus("*mass*", True)
tt.SetBranchStatus("ht*", True)
tt.SetBranchStatus("nPVs", True)
tt.SetBranchStatus("qg*", True)
tt.SetBranchStatus("*gen*", True)
    
tt.SetBranchStatus("HLT_ttH*", True)
if minimalTriggers:
    pass
else:
    tt.SetBranchStatus("HLT_BIT_HLT_*", True)
tt.SetBranchStatus("HLT_BIT_HLT_Iso*", True)
tt.SetBranchStatus("trigger*", True)
tt.SetBranchStatus("tr*", True)

of = ROOT.TFile(ofname, "RECREATE")
of.cd()
tt.CopyTree("(HLT_BIT_HLT_IsoMu27) && is_sl && abs(leps_pdgId[0]) == 13 && nBCSVM >= 1 && numJets >= 4 && ht30 > 300")
of.Write()
of.Close()
