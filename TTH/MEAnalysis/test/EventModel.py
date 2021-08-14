import ROOT
from collections import OrderedDict
ROOT.gSystem.Load("libTTHMEAnalysis")

tf = ROOT.TFile("../job_0_tree.root")
tree = ROOT.TTH_MEAnalysis.TreeDescription(tf, ROOT.TTH_MEAnalysis.SampleDescription(ROOT.TTH_MEAnalysis.SampleDescription.MC))

syst_pairs = OrderedDict([
    (x+d, ROOT.TTH_MEAnalysis.Systematic.make_id(getattr(ROOT.TTH_MEAnalysis.Systematic, x), getattr(ROOT.TTH_MEAnalysis.Systematic, d)))
    for x in [
        "CMS_scale_j",
        "CMS_res_j",
        "CMS_SubTotalPileUp_j",
        "CMS_AbsoluteStat_j",
        "CMS_AbsoluteScale_j",
        "CMS_AbsoluteFlavMap_j",
        "CMS_AbsoluteMPFBias_j",
        "CMS_Fragmentation_j",
        "CMS_SinglePionECAL_j",
        "CMS_SinglePionHCAL_j",
        "CMS_FlavorQCD_j",
        "CMS_TimePtEta_j",
        "CMS_RelativeJEREC1_j",
        "CMS_RelativeJEREC2_j",
        "CMS_RelativeJERHF_j",
        "CMS_RelativePtBB_j",
        "CMS_RelativePtEC1_j",
        "CMS_RelativePtEC2_j",
        "CMS_RelativePtHF_j",
        "CMS_RelativeFSR_j",
        "CMS_RelativeStatFSR_j",
        "CMS_RelativeStatEC_j",
        "CMS_RelativeStatHF_j",
        "CMS_PileUpDataMC_j",
        "CMS_PileUpPtRef_j",
        "CMS_PileUpPtBB_j",
        "CMS_PileUpPtEC1_j",
        "CMS_PileUpPtEC2_j",
        "CMS_PileUpPtHF_j",
    ]
    for d in ["Up", "Down"]
])

iEv = 0
while tree.reader.Next():
    events = {}
    events["nominal"] = tree.create_event()
    for k in syst_pairs.keys():
        event_var = tree.create_event(syst_pairs[k])
        events[k] = event_var

    iEv += 1

print iEv