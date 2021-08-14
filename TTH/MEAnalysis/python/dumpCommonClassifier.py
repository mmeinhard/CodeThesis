import ROOT
import sys, os, json, math, copy
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from PhysicsTools.HeppyCore.statistics.tree import Tree
import numpy as np

class Jet:
    def __init__(self, *args, **kwargs):
        self.pt = kwargs.get("pt")
        self.eta = kwargs.get("eta")
        self.phi = kwargs.get("phi")
        self.mass = kwargs.get("mass")
        self.corr = kwargs.get("corr")
        self.corr_JER = kwargs.get("corr_JER")
        for v in jet_corrections:
            for ud in ["Up","Down"]:
                setattr(self,"{a}{b}".format(a = v,b = ud),kwargs.get("{}{}".format(v,ud)))

        self.csv = kwargs.get("csv")
        self.deepcsv = kwargs.get("deepcsv")
        self.cmva = kwargs.get("cmva")
        self.corrections = kwargs.get("corrections")


    def correct(self, correction):

        dic =  {}
        dic["pt"] = self.pt
        dic["eta"] = self.eta
        dic["phi"] = self.phi
        dic["mass"] = self.mass
        dic["csv"] = self.csv
        dic["deepcsv"] = self.deepcsv
        dic["cmva"] = self.cmva
        dic["corr"] = self.corr
        dic["corr_JER"] = self.corr_JER

        for v in jet_corrections:
            for ud in ["Up","Down"]:
                dic["{a}{b}".format(a = v,b = ud)] = getattr(self,"{a}{b}".format(a = v,b = ud))

        return Jet(**dic)
           

jet_corrections = [
    "AbsoluteStat",
    "AbsoluteScale",
    "AbsoluteMPFBias",
    "Fragmentation",
    "SinglePionECAL",
    "SinglePionHCAL",
    "FlavorQCD",
    "TimePtEta",
    "RelativeJEREC1",
    "RelativePtBB",
    "RelativePtEC1",
    "RelativeBal",
    "RelativeFSR",
    "RelativeStatFSR",
    "RelativeStatEC",
    "PileUpDataMC",
    "PileUpPtRef",
    "PileUpPtBB",
    "PileUpPtEC1",
    "Total",
    "JER"
        ]

class Scenario:
    def __init__(self, *args, **kwargs):
        self.jets = kwargs.get("jets")
        self.leps_p4 = kwargs.get("leps_p4")
        self.leps_charge = kwargs.get("leps_charge")
        self.met_pt = kwargs.get("met_pt")
        self.met_phi = kwargs.get("met_phi")
        self.systematic_index = kwargs.get("systematic_index")

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample_name = get_prefix_sample(os.environ["DATASETPATH"])
        an_name, analysis = analysisFromConfig(os.environ.get("ANALYSIS_CONFIG"))
    else:
        #file_names = ["/mnt/t3nfs01/data01/shome/mameinha/tth/data/marchsamples.root"]
        file_names = map(getSitePrefix, [
            "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/april16_v1/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/april16_v1/200416_133203/0000/tree_81.root"
        ])
        #prefix = ""
        #sample_name = "SingleMuon"
        #analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default_Boosted.cfg")

    #sample = analysis.get_sample(sample_name)

    ch = ROOT.TChain("tree")
    for fi in file_names:
        ch.AddFile(fi)

    outfile = ROOT.TFile('out.root', 'recreate')
    tree = Tree('tree', 'MEM tree')
    tree.var('systematic', type=int)
    tree.var('njets', type=int)
    max_jets = 10
    for v in ["jet_pt", "jet_eta", "jet_phi", "jet_mass", "jet_csv", "jet_deepcsv", "jet_cmva"]:
        tree.vector(v, "njets", maxlen=max_jets, type=float, storageType="F")

    for v in ["jet_type"]:
        tree.vector(v, "njets", maxlen=max_jets, type=int, storageType="I")

    for v in ["jet_corr"]:
        tree.vector(v, "njets", maxlen=max_jets, type=float, storageType="F")

    for v in ["jet_corr_JER"]:
        tree.vector(v, "njets", maxlen=max_jets, type=float, storageType="F")

    for v in jet_corrections:
        for ud in ["Up","Down"]:
            tree.vector("jet_{}{}".format(v,ud), "njets", maxlen=max_jets, type=float, storageType="F")
    
    max_leps = 2
    tree.var('nleps', type=int)
    for v in ["lep_pt", "lep_eta", "lep_phi", "lep_mass", "lep_charge"]:
        tree.vector(v, "nleps", maxlen=max_leps, type=float, storageType="F")
    
    tree.var('met_pt', type=float, storageType="F")
    tree.var('met_phi', type=float, storageType="F")
    
    tree.var('hypothesis', type=int, storageType="I")
   
    for v in ["event", "run", "lumi"]:
        tree.var(v, type=int, storageType="L")

    for iEv, ev in enumerate(ch):
        #print iEv
        #if iEv > 1000:
        #    break
        accept = (ev.is_sl and ev.njets >= 4 and (ev.nBDeepCSVM >= 4))
        accept = accept or (ev.is_dl and ev.njets >= 4 and (ev.nBDeepCSVM >= 4))

        if not accept:
            continue
        hypo = -1

        print iEv, ev.evt2

        leps_p4 = []
        leps_charge = []
        for ilep in range(ev.nleps)[:max_leps]:
            p4 = [
                ev.leps_pt[ilep],
                ev.leps_eta[ilep],
                ev.leps_phi[ilep],
                ev.leps_mass[ilep]
            ]
            leps_p4 += [p4]
            #Minus sign because in pdg particles are positive and antiparticle negative
            leps_charge += [math.copysign(1, -ev.leps_pdgId[ilep])]
 
        jets = []

        for ijet in range(ev.njets)[:max_jets]:

            dic =  {}
            dic["pt"] = ev.jets_pt[ijet]
            dic["eta"] = ev.jets_eta[ijet]
            dic["phi"] = ev.jets_phi[ijet]
            dic["mass"] = ev.jets_mass[ijet]
            dic["csv"] = ev.jets_btagCSV[ijet]
            dic["deepcsv"] = ev.jets_btagDeepCSV[ijet]
            dic["cmva"] = ev.jets_btagCMVA[ijet]
            dic["corr"] = ev.jets_corr[ijet] if hasattr(ev,"jet_corr") else 1.0
            dic["corr_JER"] = ev.jets_corr_JER[ijet] if hasattr(ev,"jet_corr_JER") else 1.0

            for v in jet_corrections:
                for ud in ["Up","Down"]:
                    #print hasattr(ev,"jets_pt_corr_{a}{b}".format(a = v,b = ud)), v, "jets_corr_{a}{b}".format(a = v,b = ud)
                    dic["{a}{b}".format(a = v,b = ud)] = getattr(ev,"jets_pt_corr_{a}{b}".format(a = v,b = ud))[ijet]/getattr(ev,"jets_pt")[ijet] if hasattr(ev,"jets_pt_corr_{a}{b}".format(a = v,b = ud)) else 1.0

            jets += [Jet(**dic)]

        for ijet in range(ev.nloose_jets)[:max_jets-ev.njets]:

            dic =  {}
            dic["pt"] = ev.loose_jets_pt[ijet]
            dic["eta"] = ev.loose_jets_eta[ijet]
            dic["phi"] = ev.loose_jets_phi[ijet]
            dic["mass"] = ev.loose_jets_mass[ijet]
            dic["csv"] = ev.loose_jets_btagCSV[ijet]
            dic["deepcsv"] = ev.loose_jets_btagDeepCSV[ijet]
            dic["cmva"] = ev.loose_jets_btagCMVA[ijet]
            dic["corr"] = ev.loose_jets_corr[ijet] if hasattr(ev,"loose_jet_corr") else 1.0
            dic["corr_JER"] = ev.loose_jets_corr_JER[ijet] if hasattr(ev,"loose_jet_corr_JER") else 1.0

            #for v in jet_corrections:
            #    for ud in ["Up","Down"]:
            #        dic["{a}{b}".format(a = v,b = ud)] = getattr(ev,"loose_jets_pt_corr_{a}{b}".format(a = v,b = ud))[ijet]/getattr(ev,"loose_jets_pt_corr_{a}{b}".format(a = v,b = ud))[ijet] if hasattr(ev,"loose_jets_corr_{a}{b}".format(a = v,b = ud)) else 1 

            jets += [Jet(**dic)]

        jets = jets[0:max_jets]

        scenarios = []
        #for isf in range(len(jets[0].corrections)):
        #    scenario = Scenario(
        #        jets = [j.correct(j.corrections[isf]) for j in jets],
        #        leps_p4 = leps_p4,
        #        leps_charge = leps_charge,
        #        met_pt = ev.met_pt,
        #        met_phi = ev.met_phi,
        #        systematic_index = isf
        #    )
        #    scenarios += [scenario]

        scenario = Scenario(
                jets = [j for j in jets],
                leps_p4 = leps_p4,
                leps_charge = leps_charge,
                met_pt = ev.met_pt,
                met_phi = ev.met_phi,
                systematic_index = 0
            )

        scenarios += [scenario]

        for scenario in scenarios:
            tree.fill('njets', len(scenario.jets))
            tree.vfill('jet_pt', [x.pt for x in scenario.jets])
            tree.vfill('jet_eta', [x.eta for x in scenario.jets])
            tree.vfill('jet_phi', [x.phi for x in scenario.jets])
            tree.vfill('jet_mass', [x.mass for x in scenario.jets])
            tree.vfill('jet_csv', [x.csv for x in scenario.jets])
            tree.vfill('jet_deepcsv', [x.deepcsv for x in scenario.jets])
            tree.vfill('jet_cmva', [x.cmva for x in scenario.jets])
            tree.vfill('jet_corr', [x.corr for x in scenario.jets])
            tree.vfill('jet_corr_JER', [x.corr_JER for x in scenario.jets])
            for unc in jet_corrections:
                for ud in ["Up","Down"]:
                    tree.vfill('jet_{}{}'.format(unc,ud), [getattr(x,"{}{}".format(unc,ud)) for x in scenario.jets])

            tree.fill('nleps', len(scenario.leps_p4))
            tree.vfill('lep_pt', [x[0] for x in scenario.leps_p4])
            tree.vfill('lep_eta', [x[1] for x in scenario.leps_p4])
            tree.vfill('lep_phi', [x[2] for x in scenario.leps_p4])
            tree.vfill('lep_mass', [x[3] for x in scenario.leps_p4])
            tree.vfill('lep_charge', scenario.leps_charge)
            
            tree.fill('met_pt', scenario.met_pt)
            tree.fill('met_phi', scenario.met_phi)
            
            tree.fill('event', ev.evt2)
            tree.fill('run', ev.run)
            tree.fill('lumi', ev.lumi)
            
            tree.fill('systematic', scenario.systematic_index)
            tree.fill('hypothesis', hypo)
            
            tree.tree.Fill()
    
    outfile.Write()
