import ROOT
import sys, os
from TTH.MEAnalysis.samples_base import getSitePrefix

datatypes = sys.argv[2:]
print datatypes

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
tt.SetBranchStatus("ttCls", True)
tt.SetBranchStatus("btagWeight*", True)
tt.SetBranchStatus("puWeight*", True)
tt.SetBranchStatus("changes_jet_category*", True)

if "mem" in datatypes:
    tt.SetBranchStatus("mem_*", True)
    tt.SetBranchStatus("nMatch*", True)
    tt.SetBranchStatus("nGen*", True)
    tt.SetBranchStatus("gen*", True)
    tt.SetBranchStatus("Gen*", True)#
    tt.SetBranchStatus("btag_LR_*", True)
    tt.SetBranchStatus("tth_rho_*", True)
    tt.SetBranchStatus("met_*", True)


if "kinematics" in datatypes:
    tt.SetBranchStatus("jets_*", True)
    tt.SetBranchStatus("njets", True)
    tt.SetBranchStatus("leps_pt*", True)
    tt.SetBranchStatus("leps_eta*", True)
    tt.SetBranchStatus("leps_pdgId*", True)
    tt.SetBranchStatus("nleps", True)
    tt.SetBranchStatus("Wmass*", True)
    tt.SetBranchStatus("qg_LR*", True)
    tt.SetBranchStatus("*mass*", True)
    tt.SetBranchStatus("ht*", True)
    tt.SetBranchStatus("nPVs", True)
    tt.SetBranchStatus("qg*", True)
    tt.SetBranchStatus("*gen*", True)
    
#tt.SetBranchStatus("*topCand*", True)
if "trigger" in datatypes:
    tt.SetBranchStatus("HLT_ttH*", True)
    tt.SetBranchStatus("HLT_BIT_HLT_PFHT*", True)
    tt.SetBranchStatus("HLT_BIT_HLT_Iso*", True)
    tt.SetBranchStatus("HLT_BIT_HLT_Ele*", True)
    tt.SetBranchStatus("trigger*", True)
    tt.SetBranchStatus("tr*", True)

if "alltrigger" in datatypes:
    tt.SetBranchStatus("HLT_*", True)

of = ROOT.TFile(ofname, "RECREATE")
of.cd()
#tt.CopyTree("(is_sl && ((numJets>=6 && nBCSVM>=2) || (numJets>=4 && nBCSVM>=3) || (numJets==5 && nBCSVM>=2))) || (is_dl && (numJets>=3 && nBCSVM >=2)) || (is_fh && (numJets>=4 && nBCSVM>=3))")
#tt.CopyTree("(is_sl && numJets>=4 && nBCSVM>=2) || (is_dl && numJets>=4 && nBCSVM>=2)")
#tt.CopyTree("(is_sl && numJets>=6)")
#tt.CopyTree("(is_sl || is_dl || is_fh)")


#tt.CopyTree("is_fh && HLT_ttH_FH")
tt.CopyTree("is_sl == 0 && is_dl == 0 && ht30 > 250 && nBCSVM >= 1 && numJets>= 5 && (HLT_BIT_HLT_PFHT430_SixPFJet40 || HLT_BIT_HLT_PFHT380_SixPFJet32)")
of.Write()
of.Close()
