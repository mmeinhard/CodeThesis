import ROOT
import sys, os, json
import math
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

def main(sample, file_names):
    
    ch = ROOT.TChain("tree")
    for fi in file_names:
        ch.AddFile(getSitePrefix(fi))
    
    for ev in ch:

        #apply semileptonic fully matched selection
        if not (ev.is_sl and ev.numJets==6 and ev.nBCSVM==4 and ev.nMatch_wq_btag==2 and ev.nMatch_tb_btag==2):
            continue

        #for background, choose tt+bb, 2b, b
        if "ttjets" in sample.tags:
            if not (ev.ttCls >= 50):
                continue
        #for signal, choose fully matched events
        elif "tth" in sample.tags:
            if not (ev.nMatch_hb_btag == 2):
                continue
    
        jets_p4 = []
        jets_btag = []
        jets_csv = []
        jets_matchFlag = []
        jets_hadronFlavour = []
        for ijet in range(ev.numJets):
            p4 = [
                ev.jets_pt[ijet],
                ev.jets_eta[ijet],
                ev.jets_phi[ijet],
                ev.jets_mass[ijet]
            ]
            jets_p4 += [p4]
            jets_btag += [ev.jets_btagFlag[ijet]]
            jets_csv += [ev.jets_btagCSV[ijet]]
            jets_hadronFlavour += [ev.jets_hadronFlavour[ijet]]
            jets_matchFlag += [ev.jets_matchFlag[ijet]]
        
        leps_p4 = []
        leps_charge = []
        for ilep in range(ev.nleps):
            p4 = [
                ev.leps_pt[ilep],
                ev.leps_eta[ilep],
                ev.leps_phi[ilep],
                ev.leps_mass[ilep]
            ]
            leps_p4 += [p4]
            leps_charge += [math.copysign(1, ev.leps_pdgId[ilep])]
    
        event = {
            "input": {
                "selectedJetsP4": jets_p4,
                "selectedJetsBTag": jets_btag,
                "selectedJetsCSV": jets_csv,
                "selectedJetsMatchFlag": jets_matchFlag,
                "selectedJetsHadronFlavour": jets_hadronFlavour,
    
                "selectedLeptonsP4": leps_p4,
                "selectedLeptonsCharge": leps_charge,
    
                "metP4": [ev.met_pt, ev.met_phi],
                "evt": ev.evt,
                "run": ev.run,
                "lumi": ev.lumi,
                "numJets": ev.numJets,
                "nBCSVM": ev.nBCSVM,
                "ttCls": ev.ttCls,
    #            "nBCMVAM": ev.nBCMVAM,
    #            "btag_LR_4b_2b_btagCSV": ev.btag_LR_4b_2b_btagCSV,
    #            "btag_LR_4b_2b_btagCMVA": ev.btag_LR_4b_2b_btagCMVA,
                
                "nMatch_wq": ev.nMatch_wq_btag,
                "nMatch_tb": ev.nMatch_tb_btag,
                "nMatch_hb": ev.nMatch_hb_btag,
                "nMatch_wq_btag": ev.nMatch_wq_btag,
                "nMatch_tb_btag": ev.nMatch_tb_btag,
                "nMatch_hb_btag": ev.nMatch_hb_btag,
    
                "mem_tth_SL_2w2h2t_p": ev.mem_tth_SL_2w2h2t_p,
                "mem_ttbb_SL_2w2h2t_p": ev.mem_ttbb_SL_2w2h2t_p,
            }
        }
        print json.dumps(event)

if __name__ == "__main__":
    analysis_cfg = analysisFromConfig(sys.argv[1])

    prefix, sample_name = get_prefix_sample(os.environ["DATASETPATH"])
    file_names = os.environ["FILE_NAMES"].split()
    sample = analysis_cfg.get_sample(sample_name)
    
    main(sample, file_names)
