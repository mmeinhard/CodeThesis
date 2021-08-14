import os
from collections import OrderedDict
from TTH.MEAnalysis.MEMConfig import MEMConfig
import ROOT
from ROOT import MEM
#import VHbbAnalysis.Heppy.TriggerTableData as trigData
#import VHbbAnalysis.Heppy.TriggerTable as trig
import TTH.MEAnalysis.TriggerTable as trig

# JetID: 0: noID, 1: looseID, 2: tightID, 4: tightLepVeto (alsways 6), 6: tight+tightLepVeto (see. nanoAOD jets_cff.py)
# puID: 0: noWP, 4: looseID, 6: mediumID, 7: tightID
def jet_baseline(jet):
    #Jet baseline selection: tight JetID + loose PU ID
    return (jet.jetId >= 4 and (jet.puId >= 4 or jet.pt > 50))

def jet_baseline_tight(jet):
    return (jet.jetId >= 4 and (jet.puId >= 7 or jet.pt > 50))


# LB: in fact,  mu.tightId should contain all the other cuts
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
# nanoAOD is using CMSSW definiton: https://github.com/cms-sw/cmssw/blob/master/DataFormats/MuonReco/src/MuonSelectors.cc#L854
def mu_baseline_tight(mu):
    return (
        mu.tightId == 1 
    )

def print_mu(mu):
    print "Muon: (pt=%s, eta=%s, tight=%s, dxy=%s, dz=%s, nhits=%s, stat=%s)" % (mu.pt, mu.eta, mu.tightId, mu.dxy , mu.dz, (getattr(mu, "nMuonHits", 0) > 0 or getattr(mu, "nChamberHits", 0) > 0) , mu.nStations)

#Some could be removed...
factorizedJetCorrections = [
    "AbsoluteStat",
    "AbsoluteScale",
    #"AbsoluteFlavMap",
    "AbsoluteMPFBias",
    "Fragmentation",
    "SinglePionECAL",
    "SinglePionHCAL",
    "FlavorQCD",
    "TimePtEta",
    "RelativeJEREC1",
    #"RelativeJEREC2",
    #"RelativeJERHF",
    "RelativePtBB",
    "RelativePtEC1",
    #"RelativePtEC2",
    #"RelativePtHF",
    "RelativeBal",
    "RelativeFSR",
    "RelativeStatFSR",
    "RelativeStatEC",
    #"RelativeStatHF",
    "PileUpDataMC",
    "PileUpPtRef",
    "PileUpPtBB",
    "PileUpPtEC1",
    #"PileUpPtEC2",
    #"PileUpPtHF",
    #"PileUpMuZero",
    #"PileUpEnvelope",
    #"SubTotalPileUp",
    #"SubTotalRelative",
    #"SubTotalPt",
    #"SubTotalScale",
    #"SubTotalAbsolute",
    #"SubTotalMC",
    "Total",
    #"TotalNoFlavor",
    #"TotalNoTime",
    #"TotalNoFlavorNoTime",
    #"FlavorZJet",
    #"FlavorPhotonJet",
    #"FlavorPureGluon",
    #"FlavorPureQuark",
    #"FlavorPureCharm",
    #"FlavorPureBottom",
#    "TimeRunB",
#    "TimeRunC",
#    "TimeRunD",
#    "TimeRunE",
#    "TimeRunF",
#    "TimeRunG",
#    "TimeRunH",
    #CorrelationGroupMPFInSitu",
    #CorrelationGroupIntercalibration",
    #CorrelationGroupbJES",
    #CorrelationGroupFlavor",
    #CorrelationGroupUncorrelated",
    "JER"
]

#factorizedJetCorrections = ["JER","Total"]
#factorizedJetCorrections = ["Total"]
#factorizedJetCorrections = []

def el_baseline_loose(el):
    sca = abs(el.etaSc)
    ret = ( el.eleCutId >= 2 and
            not ( sca >= 1.4442 and
                  sca < 1.5660 )
            and (
                (el.dz < 0.10 and sca <= 1.479) #Barrel
                 or (el.dz < 0.20 and sca > 1.479) #Endcap
            ) 
            and (
                (el.dxy < 0.05 and sca <= 1.479) #Barrel
                 or (el.dxy < 0.1 and sca > 1.479) #Endcap
            )
                 
    )

    return ret

def el_baseline_medium(el):
    sca = abs(el.etaSc)
    ret = ( el.eleCutId >= 3 and
            not ( sca >= 1.4442 and
                  sca < 1.5660 )
            and (
                (el.dz < 0.10 and sca <= 1.479) #Barrel
                 or (el.dz < 0.20 and sca > 1.479) #Endcap
            ) 
            and (
                (el.dxy < 0.05 and sca <= 1.479) #Barrel
                 or (el.dxy < 0.1 and sca > 1.479) #Endcap
            )
    )

    return ret

def el_baseline_tight(el):
    
    # Taken from https://gitlab.cern.ch/ttH/reference/blob/ICHEP18/definitions/ICHEP18.md#22-electron
    sca = abs(el.etaSc)

    ret = ( el.eleCutId >= 4 and #tight ID as per nanoAOD bitmap mapper
            not ( sca >= 1.4442 and
                  sca < 1.5660 )
            and (
                (el.dz < 0.10 and sca <= 1.479) #Barrel
                 or (el.dz < 0.20 and sca > 1.479) #Endcap
            ) 
            and (
                (el.dxy < 0.05 and sca <= 1.479) #Barrel
                 or (el.dxy < 0.1 and sca > 1.479) #Endcap
            )

    )
            
    return ret

def print_el(el):
    print "Electron: (pt=%s, eta=%s, convVeto=%s, etaSc=%s, dEta=%s, dPhi=%s, sieie=%s, HoE=%s, dxy=%s, dz=%s, nhits=%s, eOp=%s VIDID=%s)" % (
        el.pt, el.eta, el.convVeto, abs(el.etaSc), abs(el.DEta),
        abs(el.DPhi), el.sieie, el.hoe, abs(el.dxy),
        abs(el.dz), getattr(el, "eleExpMissingInnerHits", 0),
        getattr(el, "eleooEmooP", 0),
        getattr(el, "eleCutId",0)
    )

class Conf:
    leptons = {
        "mu": {
            "SL": {
                "pt": 29,
                "eta":2.4,
                "iso": 0.15,
                "idcut": mu_baseline_tight,
            },
            "DL": {
                "iso": 0.25,
                "eta": 2.4,
                "idcut": mu_baseline_tight,
            },
            "veto": {
                "pt": 15.0,
                "eta": 2.4,
                "iso": 0.25,
                "idcut": mu_baseline_tight,
            },
            "isotype": "PFIso04_all", #pfRelIso - delta-beta, relIso - rho
        },

        "el": {
            "SL": {
                "pt": 30,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_tight(el),
            },
            "DL": {
                "eta": 2.4,
                "idcut": el_baseline_tight,
            },
            "veto": {
                "pt": 15.0,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_tight(el),
            },
            #Isolation applied directly in el_baseline_tight using combIsoAreaCorr as cutoff
            "isotype": "relIso03", #KS: changed for nanoAOD.
        },
        "DL": {
            "pt_leading": 25,
            "pt_subleading": 15,
        },
        "selection": lambda event: event.is_sl or event.is_dl,
        "force_isFH": False,
    }

    jets = {
        # pt, |eta| thresholds for **leading two jets** (common between sl and dl channel)
        "pt":   30,
        "eta":  2.4,

        # pt, |eta| thresholds for **leading jets** specific to sl channel
        "pt_sl":  30,
        "eta_sl": 2.4,

        # pt, |eta| thresholds for **trailing jets** specific to dl channel
        "pt_dl":  20,
        "eta_dl": 2.4,
        
        # pt threshold for leading jets in fh channel
        "pt_fh": 40,

        # nhard'th jet is used for pt threshold
        "nhard_fh": 6,

        # minimum number of jets to save event in tree
        "minjets_fh": 6,

        #The default b-tagging algorithm (branch name)
        "btagAlgo": "btagDeepCSV",

        #The default b-tagging WP
        "btagWP": "DeepCSVM",

        #The loose b-tag WP for QCD data estimation
        "looseBWP": "CSVL",


        #These working points are evaluated and stored in the trees as nB* - number of jets passing the WP
        #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation94X
        "btagWPs": {
            "CSVL": ("btagCSV", 0.5803),
            "CSVM": ("btagCSV", 0.8838),
            "CSVT": ("btagCSV", 0.9693),

            #Note: these working points are currently NOT correct
            "DeepCSVL": ("btagDeepCSV", 0.1522),
            "DeepCSVM": ("btagDeepCSV", 0.4941),
            "DeepCSVT": ("btagDeepCSV", 0.8001),


            "DeepFlavM": ("btagDeepFlav", 0.3033),

            #Removed CMVA since not supported (at least in the BtagRecommendation94X
        },

        #if btagCSV, untagged/tagged selection for W mass and MEM is done by CSVM cut
        #if btagLR, selection is done by the btag likelihood ratio permutation
        #"untaggedSelection": "btagCMVA",
        "untaggedSelection": "btagLR",

        #how many jets to consider for the btag LR permutations
        "NJetsForBTagLR": 15, #DS

        #base jet selection
        "baseSelection": jet_baseline,
        "tightSelection" : jet_baseline_tight
    }

    boost = {
        "top": {
            #Cuts set by "default"
            "pt":   200,
            "eta":  2.4,
            #"drl": 1.5, #In SL events distance to lepton candidate
            #"btagL": "DeepCSVL",
            #Cuts optained by optimization procedure
            "bdt": 0.32,
            #"mass_inf": 160,
            #"mass_sup": 380,
            #"tau32SD": 0.8,
            #"frec": 0.65,
        },
        "higgs": {
            #Cuts set by "default"
            "pt":   300,
            "eta":  2.4,
            #"msoft": 50,
            #Cuts optained by optimization procedure
            "bbtag": 0.6,
            #bbtag": 0.25,
            #btagSL": 0.5,
            #tau21SD": 0.8,
        },
    }

    trigger = {

        "filter": False,
        #Change to trig.triggerTable for 2017 menu (starting from 92X samples)
        "trigTable": trig.triggerTable,
        "trigTableData": trig.triggerTable,
        "calcFHSF" : False,
        "MergePaths" : ["FH"],
        "TriggerSFFile" : os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/sf3d_out_3DSF_Finalv2_tightCutRunB-CNoPre-D-E-F_all_plusHTplusJet_wPuGenB_binningv2.root",
        "TriggerSFHisto" : "h3SF_tot",
    }

    general = {
        #"passall": False,
        "passall": True,
        "boosted": True,
        "QGLtoDo": {
         #3:[(3,0)] => "evalute qg LR of 3q vs 0q(+3g), considering only light jets, in events with 3 b-jets"
            3:[(3,0),(3,2),(4,0),(4,3),(5,0),(5,4)], 
            4:[(3,0),(3,2),(4,0),(4,3),(5,0)] },
        "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/3Dplots_2017.root",
        #"QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/Histos_QGL_flavour.root",
        "QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/QGL_3dPlot.root",
        "sampleFile": os.environ["CMSSW_BASE"]+"/python/TTH/MEAnalysis/samples.py",
        "BDT_Top": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/BDT_Top.pickle",
        "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_JECV32.pickle",
        #"transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_ttbar.pickle",
        "transferFunctions_htt_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_htt_JECV32.pickle",
        "transferFunctions_higgs_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_higgsAK8_JECV32.pickle",
        #MET filters for 2017 data: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Moriond_2018
        #"METFilterData":["Flag_goodVertices","Flag_globalSuperTightHalo2016Filter","Flag_HBHENoiseFilter","Flag_HBHENoiseIsoFilter",
        #                 "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", 
        #                 "Flag_eeBadScFilter","Flag_ecalBadCalibReducedMINIAODFilter"],
        #"METFilterMC":["Flag_goodVertices","Flag_globalSuperTightHalo2016Filter","Flag_HBHENoiseFilter","Flag_HBHENoiseIsoFilter",
        #                 "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_ecalBadCalibReducedMINIAODFilter"],
        "METFilterData":["Flag_goodVertices","Flag_globalSuperTightHalo2016Filter","Flag_HBHENoiseFilter","Flag_HBHENoiseIsoFilter",
                         "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter",
                         "Flag_eeBadScFilter","Flag_ecalBadCalibFilterV2"],
        "METFilterMC":["Flag_goodVertices","Flag_globalSuperTightHalo2016Filter","Flag_HBHENoiseFilter","Flag_HBHENoiseIsoFilter",
                         "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter","Flag_ecalBadCalibFilterV2"],

        #"transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_sj.pickle",
        "systematics": [
            "nominal",
        ] + [fj+sdir for fj in factorizedJetCorrections for sdir in ["Up", "Down"]],
        "BTagSFFile" : os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/deepCSV_sfs_v2.csv",
        "BTagSystematics" : ["lf", "hf", "hfstats1", "hfstats2", "lfstats1", "lfstats2", "cferr1", "cferr2", "jesAbsoluteMPFBias", "jesAbsoluteScale", "jesAbsoluteStat", "jesFlavorQCD", "jesFragmentation", "jesPileUpDataMC", "jesPileUpPtBB", "jesPileUpPtEC1", "jesPileUpPtEC2", "jesPileUpPtHF", "jesPileUpPtRef", "jesRelativeBal", "jesRelativeFSR", "jesRelativeJEREC1", "jesRelativeJEREC2", "jesRelativeJERHF", "jesRelativePtBB", "jesRelativePtEC1", "jesRelativePtEC2", "jesRelativePtHF", "jesRelativeStatFSR", "jesRelativeStatEC", "jesRelativeStatHF", "jesSinglePionECAL", "jesSinglePionHCAL", "jesTimePtEta"],
        "BTagSystematics_bFlav": ["central", "up_lf", "down_lf", "up_hfstats1", "down_hfstats1", "up_hfstats2", "down_hfstats2"],
        "BTagSystematics_cFlav": ["central", "up_cferr1", "down_cferr1",  "up_cferr2", "down_cferr2"],
        "BTagSystematics_udsgFlav": ["central", "up_hf", "down_hf", "up_lfstats1", "down_lfstats1", "up_lfstats2", "down_lfstats2"],

        #If the list contains:
        # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
        # "reco" - print out the reco-level selected particles
        # "matching" - print out the association between gen and reco objects
        "verbosity": [
            #"subjet",
            "eventboundary", #print run:lumi:event
            #"trigger", #print trigger bits
            #"input", #print input particles
            #"gen", #print out gen-level info
            #"matching", 
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput", #info about particles used for MEM input
            #"commoninput", #print out inputs for CommonClassifier
            #"commonclassifier",
            #"debug",
            #"systematics",
        ],

        #"eventWhitelist": [
        #(1,74414,69315815),
        #]
        #(1,485,468792),
        #(1,485,469227),
        #(1,486,469413),
        #(1,486,469627),
        #(1,487,470571),
        #(1,466,450530),
        #(1,3953,3824601),
        #(1,3953,3824973),
        #(1,3953,3824916),
        #]
    }

    #multiclass = {
    #    "bdtPickleFile": os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/BDT.pickle"
    #}

    #tth_mva = {
    #    "filename": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/tth_bdt.pkl",
    #    "varlist": [
    #        "is_sl",
    #        "is_dl",
    #        "lep0_pt",
    #        "lep0_aeta",
    #        "lep1_pt",
    #        "lep1_aeta",
    #        "jet0_pt",
    #        "jet0_btag",
    #        "jet0_aeta",
    #        "jet1_pt",
    #        "jet1_btag",
    #        "jet1_aeta",
    #        "jet2_pt",
    #        "jet2_btag",
    #        "jet2_aeta",
    #        "mean_bdisc",
    #        "mean_bdisc_btag",
    #        "min_dr_btag",
    #        "mean_dr_btag",
    #        "std_dr_btag",
    #        "momentum_eig0",
    #        "momentum_eig1",
    #        "momentum_eig2",
    #        "fw_h0",
    #        "fw_h1",
    #        "fw_h2",
    #        "aplanarity",
    #        "isotropy",
    #        "numJets",
    #        "nBCSVM",
    #        "Wmass"
    #    ]
    #}

    mem = {

        #Actually run the ME calculation
        #If False, all ME values will be 0
        "calcME": True,
        "n_integration_points_mult": 1.0,
        "factorized_sources": factorizedJetCorrections,
        #compute MEM variations for these sources in the nominal case
        "jet_corrections": ["{0}{1}".format(corr, direction) for corr in factorizedJetCorrections for direction in ["Up", "Down"]],
        #compute MEM from scratch with these variations
        "enabled_systematics": [
            "nominal",
            #"TotalUp",
            #"TotalDown",
        ],

        "weight": 0.10, #k in Psb = Ps/(Ps+k*Pb)

        "blr_cuts": {
            "sl_j4_t2": 20,
            "sl_j4_t3": -20,
            "sl_j4_tge4": -20,

            "sl_j5_t2": 20,
            "sl_j5_t3": -20,
            "sl_j5_tge4": -20,

            "sl_jge6_t2": 20,
            "sl_jge6_t3": -20,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": -20,
            "dl_jge4_tge4": -20,

            ##[CHECK-ME]
            "fh_j9_t4": -20,
            "fh_j8_t3": -20,
            "fh_j8_t4": -20,
            "fh_j7_t4": -20,
            "fh_j7_t3": -20,
            "fh_jge6_t4": -20,
            "fh_jge6_t3": -20,
        },

        #Generic event-dependent selection function applied
        #just before the MEM. If False, MEM is skipped for all hypos
        #note that we set hypothesis-specific cuts below
        "selection": lambda event: (
                ((event.is_sl or event.is_dl) and
                (event.numJets>=4 and event.nBDeepCSVM >= 4))
            #(event.is_fh and event.cat in ["cat7","cat8"]
            #and event.btag_LR_4b_2b > 0.95)
        ),

        "selection_boosted": lambda event: (
                ((event.is_sl or event.is_dl) and
                (len(event.boosted_bjets)>=4))
        ),

        #This configures the MEMs to actually run, the rest will be set to 0
        "methodsToRun": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            "SL_1w2h2t",
            "SL_2w2h2t",
            #"SL_2w2h1t_l",
            #"SL_2w2h1t_h",
            #"SL_2w2h2t_1j",
            "SL_2w2h2t_sj",
            "SL_1w2h2t_sj"                                                                                                                                                                                                                        ,
            "SL_0w2h2t_sj",
            "DL_0w2h2t_sj",
            "SL_2w2h2t_sj_perm_top",
            "SL_2w2h2t_sj_perm_tophiggs",
            "SL_2w2h2t_sj_perm_higgs",
            "SL_1w2h2t_sj_perm_higgs",
            "SL_0w2h2t_sj_perm_higgs",
            "DL_0w2h2t_sj_perm_higgs",
            #"SL_2w2h2t_memLR",
            #"SL_0w2h2t_memLR",
            #"FH_4w2h2t", #8j,4b
            #"FH_3w2h2t", #7j,4b
            #"FH_4w2h1t", #7j,3b & 8j,3b
            #"FH_4w1h2t", #7j,3b & 8j,3b
            #"FH_3w2h1t", #7j,3b & 8j,3b (int. 1 jet)
            #"FH_0w2w2h2t", #all 4b cats
            #"FH_1w1w2h2t", #all 4b cats
            #"FH_0w0w2h2t", #all 4b cats
            #"FH_0w0w2h1t", #all cats
            #"FH_0w0w1h2t"  #all cats
        ],
        # btag LR cuts for FH MEM categories
        "FH_bLR_3b_SR": 0.94,
        "FH_bLR_4b_SR": 0.99,
        "FH_bLR_3b_excl": 1.96,
        "FH_bLR_4b_excl": 0.998,       
        "FH_bLR_3b_CR_lo": 0.60,
        "FH_bLR_3b_CR_hi": 0.94,
        "FH_bLR_4b_CR_lo": 0.80,
        "FH_bLR_4b_CR_hi": 0.99,
    }

    mem_configs = OrderedDict()

CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")

###
### SL_2w2h2t
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t"] = c

###
### SL_2w2h2t Sudakov
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code |= MEM.IntegrandType.Sudakov
Conf.mem_configs["SL_2w2h2t_sudakov"] = c

###
### SL_2w2h2t Recoil
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code |= MEM.IntegrandType.Recoil
Conf.mem_configs["SL_2w2h2t_recoil"] = c

###
### SL_2w2h2t No Tag
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_notag"] = c

###
### SL_2w2h2t No Sym
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_nosym"] = c


###
### SL_2w2h2t_1j
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 3
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code += ROOT.MEM.IntegrandType.AdditionalRadiation
Conf.mem_configs["SL_2w2h2t_1j"] = c

###
### SL_1w2h2t
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 1 and
    ev.numJets == 5
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("1qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_1w2h2t"] = c

###
### SL_2w2h1t_l
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("2w2h1t_l")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h1t_l"] = c

###
### SL_2w2h1t_h
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("2w2h1t_h")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h1t_h"] = c

###
### SL_0w2h2t
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.numJets == 4
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
#c.cfg.int_code = 0
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t"] = c

###
### DL_0w2h2t
###
c = MEMConfig(Conf)
#c.b_quark_candidates = lambda ev: ev.good_jets
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4
    #(len(mcfg.l_quark_candidates(ev)) + len(mcfg.b_quark_candidates(ev))) >= 4
)
c.maxLJets = 4
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
#FIXME: are we sure about these assumptions?
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t"] = c


#######################
#Subjet configurations#
#######################

#SL_2w2h2t_sj
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2 and
    ev.PassedSubjetAnalyzer == True
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj"] = c


#SL_1w2h2t_sj
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 1 and
    ev.PassedSubjetAnalyzer == True
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("1qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_1w2h2t_sj"] = c

#SL_0w2h2t_sj
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and 
    len(mcfg.l_quark_candidates(ev)) == 0 and
    ev.PassedSubjetAnalyzer == True

)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t_sj"] = c

#DL_0w2h2t_sj
c = MEMConfig(Conf)
c.l_quark_candidates = lambda ev: []
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.PassedSubjetAnalyzer == True
)
c.maxLJets = 4
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t_sj"] = c


#SL_2w2h2t_sj_perm_top
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2 and
    ev.PassedSubjetAnalyzer == True and
    ev.hashiggs == 0 and
    ev.hastop == 1
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.HEPTopTagged)
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj_perm_top"] = c

#SL_2w2h2t_sj_perm_higgs
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2 and
    ev.PassedSubjetAnalyzer == True and
    ev.hashiggs == 1 and
    ev.hastop == 0
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.HiggsTagged)
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj_perm_higgs"] = c

#SL_2w2h2t_sj_perm_tophiggs
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2 and
    ev.PassedSubjetAnalyzer == True and
    ev.hashiggs == 1 and
    ev.hastop == 1
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.HiggsTagged)
strat.push_back(MEM.Permutations.HEPTopTagged)
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj_perm_tophiggs"] = c

#SL_1w2h2t_sj_perm_higgs
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 1 and
    ev.PassedSubjetAnalyzer == True and
    ev.hashiggs == 1 and
    ev.hastop == 0
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("1qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.HiggsTagged)
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_1w2h2t_sj_perm_higgs"] = c

#SL_0w2h2t_sj_perm_higgs
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and 
    len(mcfg.l_quark_candidates(ev)) == 0 and
    ev.PassedSubjetAnalyzer == True and
    ev.hashiggs == 1 and
    ev.hastop == 0

)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.HiggsTagged)
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t_sj_perm_higgs"] = c

#DL_0w2h2t_sj_perm_higgs
c = MEMConfig(Conf)
c.l_quark_candidates = lambda ev: []
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.PassedSubjetAnalyzer == True and
    ev.hashiggs == 1 and
    ev.hastop == 0
)
c.maxLJets = 4
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.HiggsTagged)
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t_sj_perm_higgs"] = c


# apply btag LR cuts for FH MEM categories only if using btagLR
# must allow for overlapping 3b and 4b regions (both hypos run)
bLR = False
#if Conf.jets["untaggedSelection"] == "btagLR":
#    bLR = True

# btag LR cuts for FH MEM categories
FH_bLR_3b_SR = Conf.mem["FH_bLR_3b_SR"]
FH_bLR_4b_SR = Conf.mem["FH_bLR_4b_SR"]
FH_bLR_3b_excl = Conf.mem["FH_bLR_3b_excl"]
FH_bLR_4b_excl = Conf.mem["FH_bLR_4b_excl"]
FH_bLR_3b_CR_lo = Conf.mem["FH_bLR_3b_CR_lo"]
FH_bLR_3b_CR_hi = Conf.mem["FH_bLR_3b_CR_hi"]
FH_bLR_4b_CR_lo = Conf.mem["FH_bLR_4b_CR_lo"]
FH_bLR_4b_CR_hi = Conf.mem["FH_bLR_4b_CR_hi"]

###
### FH_4w2h2t #only 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low #DS adds 5th,6th,... btags
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and #although from BTagLRAnalyzer there are max 4 candidates
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( #(len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))>=9 ) #DS do not consider 10 jet events
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry, but then add _l,_h for all missing-q methods
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w2h2t"] = c

###
### FH_3w2h2t #7j,4b & 8j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 ) #run two methods for 8j,4b category
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("3w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_3w2h2t"] = c

###
### FH_4w2h1t #7j,3b, 8j,3b (9j,3b) #do not need _l,_h if not imposing t-tbar symmetry
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    (bLR or len(mcfg.b_quark_candidates(ev)) == 3 ) and
    (not bLR or (ev.btag_LR_4b_2b < FH_bLR_4b_excl and (ev.btag_LR_3b_2b > FH_bLR_3b_SR or 
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) ) ) and
    ( len(mcfg.l_quark_candidates(ev)) >= 4 ) #max 9 jets considered in bLR, but only 5 light q for MEM
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w2h1t"] = c

###
### FH_4w1h2t #7j,3b, 8j,3b (9j,3b as drop 6th l jet) #DS
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    (bLR or len(mcfg.b_quark_candidates(ev)) == 3 ) and
    (not bLR or (ev.btag_LR_4b_2b < FH_bLR_4b_excl and (ev.btag_LR_3b_2b > FH_bLR_3b_SR or 
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) ) ) and
    ( len(mcfg.l_quark_candidates(ev)) == 4 or len(mcfg.l_quark_candidates(ev)) == 5
      or len(mcfg.l_quark_candidates(ev)) == 6 ) #DS
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w1h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w1h2t"] = c

###
### FH_3w2h1t #7j,3b, 8j,3b (int. 1 light jet)
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    (bLR or len(mcfg.b_quark_candidates(ev)) == 3 ) and
    (not bLR or (ev.btag_LR_4b_2b < FH_bLR_4b_excl and (ev.btag_LR_3b_2b > FH_bLR_3b_SR or 
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) ) ) and
    ( len(mcfg.l_quark_candidates(ev)) == 4 or len(mcfg.l_quark_candidates(ev)) == 5 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("3w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_3w2h1t"] = c

###
### FH_0w2w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w2w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w2w2h2t"] = c

###
### FH_1w1w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("1w1w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_1w1w2h2t"] = c

###
### FH_0w0w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w2h2t"] = c

###
### FH_0w0w2h1t #all FH categories: 7j,4b, 8j,4b, 9j,4b, 7j,3b, 8j,3b, 9j,3b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or ev.btag_LR_3b_2b > FH_bLR_3b_SR or
     (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) or
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w2h1t"] = c

###
### FH_0w0w1h2t #all FH categories: 7j,4b, 8j,4b, 9j,4b, 7j,3b, 8j,3b, 9j,3b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or ev.btag_LR_3b_2b > FH_bLR_3b_SR or
     (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) or
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w1h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w1h2t"] = c

import inspect
def print_dict(d):
    s = "(\n"
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        if callable(v) and not isinstance(v, ROOT.TF1):
            v = inspect.getsource(v).strip()
        elif isinstance(v, dict):
            s += print_dict(v)
        s += "  {0}: {1},\n".format(k, v)
    s += ")"
    return s

def conf_to_str(Conf):
    s = "Conf (\n"
    for k, v in sorted(Conf.__dict__.items(), key=lambda x: x[0]):
        s += "{0}: ".format(k)
        if isinstance(v, dict):
            s += print_dict(v) + ",\n"
        elif isinstance(v, ROOT.TF1):
            s += "ROOT.TF1({0}, {1})".format(v.GetName(), v.GetTitle()) + ",\n"
        else:
            s += str(v) + ",\n"
    s += "\n"
    return s
