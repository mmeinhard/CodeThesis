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
tt.SetBranchStatus("passPV*", True)
if "mem" in datatypes:
    tt.SetBranchStatus("mem_*", True)
    tt.SetBranchStatus("nMatch*", True)
    tt.SetBranchStatus("nGen*", True)
    tt.SetBranchStatus("gen*", True)
    tt.SetBranchStatus("Gen*", True)
    tt.SetBranchStatus("btag_LR_4b_2b*", True)
    tt.SetBranchStatus("ttCls", True)
    tt.SetBranchStatus("tth_rho_*", True)
    tt.SetBranchStatus("met_*", True)
    tt.SetBranchStatus("btagWeight*", True)
    tt.SetBranchStatus("puWeight*", True)
    tt.SetBranchStatus("changes_jet_category*", True)

if "kinematics" in datatypes:
    tt.SetBranchStatus("jets_pt*", True)
    tt.SetBranchStatus("jets_eta*", True)
    tt.SetBranchStatus("jets_btagCSV*", True)
    tt.SetBranchStatus("njets", True)
    tt.SetBranchStatus("leps_pt*", True)
    tt.SetBranchStatus("leps_eta*", True)
    tt.SetBranchStatus("leps_pdgId*", True)
    tt.SetBranchStatus("nleps", True)
    tt.SetBranchStatus("Wmass", True)
    tt.SetBranchStatus("HLT*", True)
    tt.SetBranchStatus("nPVs*", True)

tt.SetBranchStatus("run", True)
tt.SetBranchStatus("lumi", True)
tt.SetBranchStatus("evt", True)
tt.SetBranchStatus("json", True)
#tt.SetBranchStatus("cat", True)
#tt.SetBranchStatus("ht", True)
#tt.SetBranchStatus("isotropy", True)
#tt.SetBranchStatus("sphericity", True)
#tt.SetBranchStatus("C", True)
#tt.SetBranchStatus("D", True)
#tt.SetBranchStatus("aplanarity", True)
#tt.SetBranchStatus("leps_*", True)
#tt.SetBranchStatus("jets_*", True)
#tt.SetBranchStatus("btagWeight*", True)
#tt.SetBranchStatus("puWeight*", True)
#tt.SetBranchStatus("HLT*", True)
#tt.SetBranchStatus("trigger*", True)
#tt.SetBranchStatus("common*", True)
#tt.SetBranchStatus("mean*", True)
#tt.SetBranchStatus("std*", True)
#tt.SetBranchStatus("momentum*", True)
#tt.SetBranchStatus("weight_xs", True)

of = ROOT.TFile(ofname, "RECREATE")
of.cd()
#tt.CopyTree("1")
#tt.CopyTree("(is_sl && numJets>=4 && nBCSVM>=2) || (numJets>=4 && nBCSVM>=3) || (numJets==5 && nBCSVM>=2))) || (is_dl && (numJets>=3 && nBCSVM >=2)) || (is_fh && (numJets>=4 && nBCSVM>=3))")
tt.CopyTree("(is_sl && numJets>=4 && nBCSVM>=2) || (is_dl && numJets>=4 && nBCSVM>=2)")
#tt.CopyTree("(is_sl || is_dl)")
of.Write()
of.Close()
