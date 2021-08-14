import TTH.MEAnalysis.config as cfg
import os
from copy import copy
from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator
from TTH.MEAnalysis.MEMAnalyzer import MEMPermutation
from TTH.MEAnalysis.vhbb_utils import *

#Defines the output TTree branch structures
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *

import numpy as np

import logging

LOG_MODULE_NAME = logging.getLogger(__name__)


#Override the default fillCoreVariables and declareCoreVariables in heppy,
#as otherwise they would mess with some variables like puWeight etc
def fillCoreVariables(self, tr, event, isMC):
    pass

def declareCoreVariables(self, tr, isMC):
    pass

def getBTagSystematicNames(sysList , prefix):
    """
    Function to build internal names of the b-tag scalefactors calculated in BtagweightsAnalyzer

    Args:
    -----
    sysList (list(str)) : Intended to be list from MEAnalysis_cfg_heppy.py
    prefix (str) : Prefix of the variable - Options: btagSF_shape (jets), btagWeight_shape (event)
                   Must correspond to names defined in BtagweightsAnalyzer __init__
    """
    retList = [prefix] #nominal SF names as prefix
    for syst in sysList:
        for sdir in ["up","down"]:
            retList.append("{0}_{1}_{2}".format(prefix, syst, sdir))

    return retList

AutoFillTreeProducer.declareCoreVariables = declareCoreVariables 
AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

def makeGlobalVariable(vtype, systematic="nominal", mcOnly=False):

    #LOG_MODULE_NAME.info("Making global variable {0}, for systematic {1}".format(vtype, systematic))
    name = vtype[0] #name of variable
    typ = vtype[1] #type of variable
    hlp = vtype[2] #help string

    #if only 3 supplied, assume variable can be accessed from tree using name
    if len(vtype) == 3:
        func = lambda ev, systematic=systematic, name=name: \
            getattr(ev.systResults[systematic], name, -9999)

    #if 4 supplied, access variable using name from systematic tree
    elif len(vtype) == 4:

        #If 4th element is string, just use that as an accessor
        if isinstance(vtype[3], str):
            func = lambda ev, systematic=systematic, name=vtype[3]: \
                getattr(ev.systResults[systematic], name, -9999)
        #Otherwise it's a function
        else:
            func = vtype[3]

    syst_suffix = "_" + systematic
    if systematic == "nominal":
        syst_suffix = ""

    return NTupleVariable(
        name + syst_suffix, func, type=typ, help=hlp, mcOnly=mcOnly
    )

lepton_sf_kind = [
    "SF_HLT_RunD4p2",
    "SF_HLT_RunD4p3",
    "SF_IdCutLoose",
    "SF_IdCutTight",
    "SF_IdMVALoose",
    "SF_IdMVATight",
    "SF_IsoLoose",
    "SF_IsoTight",
    "SF_trk_eta",
]

lepton_sf_kind_err = [x.replace("SF", "SFerr") for x in lepton_sf_kind]

#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("etaSc", lambda x : getattr(x, "etaSc", -99)),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    NTupleVariable("iso", lambda x : x.iso),
    #NTupleVariable("ele_mva_id", lambda x : x.eleMVAIdSpring15Trig),
    NTupleVariable("mu_id", lambda x : 1*getattr(x, "looseIdPOG", 0) + 2*getattr(x, "tightId", 0)),
] + [NTupleVariable(sf, lambda x, sf=sf : getattr(x, sf, -1.0))
    for sf in lepton_sf_kind + lepton_sf_kind_err
])

p4type = NTupleObjectType("p4Type", variables = [
    NTupleVariable("pt", lambda x : x.Pt()),
    NTupleVariable("eta", lambda x : x.Eta()),
    NTupleVariable("phi", lambda x : x.Phi()),
    NTupleVariable("mass", lambda x : x.M()),
])

kinType = NTupleObjectType("kinType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("btag", lambda x : x.btag),
    #NTupleVariable("partonFlavour", lambda x : x.partonFlavour, type=int, mcOnly=True),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int, mcOnly=True),
    NTupleVariable("btagSF_shape", lambda x : getattr(x, "btagSF_shape", 1.0), mcOnly=True),
])

LHE_weights_type = NTupleObjectType("LHE_type", variables = [
    #NTupleVariable("id", lambda x : x.id),
    NTupleVariable("wgt", lambda x : x.wgt),
])

#Specifies what to save for leptons
pvType = NTupleObjectType("pvType", variables = [
    NTupleVariable("z", lambda x : x.z),
    NTupleVariable("rho", lambda x : x.Rho),
    NTupleVariable("ndof", lambda x : x.ndof),
    NTupleVariable("isFake", lambda x : x.isFake),
])

quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
])

genTopType = NTupleObjectType("genTopType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("decayMode", lambda x : x.decayMode),
])



perm_vars = [
    NTupleVariable("perm_{0}".format(i), lambda x : getattr(x, "perm_{0}".format(i)))
    for i in range(MEMPermutation.MAXOBJECTS)
]
memPermType = NTupleObjectType("memPermType", variables = [
    NTupleVariable("idx", lambda x : x.idx, type=int),
    NTupleVariable("p_mean", lambda x : x.p_mean),
    NTupleVariable("p_std", lambda x : x.p_std),
    NTupleVariable("p_tf_mean", lambda x : x.p_tf_mean),
    NTupleVariable("p_tf_std", lambda x : x.p_tf_std),
    NTupleVariable("p_me_mean", lambda x : x.p_me_mean),
    NTupleVariable("p_me_std", lambda x : x.p_me_std),
] + perm_vars)

arrayType = NTupleObjectType("arrayType", variables = [ #generic vector variable
    NTupleVariable("", lambda x : x),
])


def getTreeProducer(conf):
    factorized_dw_vars = [
        NTupleVariable("dw_" + fc, lambda x,fc=fc : getattr(x, "dw", {}).get(fc, 0.0), type=float)
        for fc in conf.mem["jet_corrections"]
    ]
    
    variated_vars = [
        NTupleVariable("var_" + fc, lambda x,i=i : x.variated.at(i) if x.variated.size()>i else 0.0, type=float)
        for (i, fc) in enumerate(conf.mem["jet_corrections"])
    ]
    
    memType_nominal = NTupleObjectType("memType", variables = [
        NTupleVariable("p", lambda x : x.p),
        NTupleVariable("p_err", lambda x : x.p_err),
        #NTupleVariable("chi2", lambda x : x.chi2),
        NTupleVariable("time", lambda x : x.time),
        #NTupleVariable("error_code", lambda x : x.error_code, type=int),
        #NTupleVariable("efficiency", lambda x : x.efficiency),
        NTupleVariable("nperm", lambda x : x.num_perm, type=int),
    ])# + factorized_dw_vars + variated_vars) MM - removed to save space
    
    memType_syst = NTupleObjectType("memType", variables = [
        NTupleVariable("p", lambda x : x.p),
        NTupleVariable("p_err", lambda x : x.p_err),
        #NTupleVariable("chi2", lambda x : x.chi2),
        #NTupleVariable("time", lambda x : x.time),
        #NTupleVariable("error_code", lambda x : x.error_code, type=int),
        #NTupleVariable("efficiency", lambda x : x.efficiency),
        #NTupleVariable("nperm", lambda x : x.num_perm, type=int),
    ])
   
    #create jet up/down variations
    corrs = [NTupleVariable(
        "pt_corr_"+c,
        lambda x,c="pt_corr_"+c : getattr(x, c),
        mcOnly=True,
        type=float,
    ) for c in conf.mem["jet_corrections"]
    ]
    corrs_phi = [NTupleVariable(
        "phi_corr_"+c,
        lambda x,c="pt_corr_"+c : getattr(x, c),
        mcOnly=True,
        type=float,
    ) for c in conf.mem["jet_corrections"]
    ]

    metType = NTupleObjectType("metType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("px", lambda x : x.px),
    NTupleVariable("py", lambda x : x.py),
    NTupleVariable("sumEt", lambda x : x.sumEt),
    NTupleVariable("genPt", lambda x : x.genPt, mcOnly=True),
    NTupleVariable("genPhi", lambda x : x.genPhi, mcOnly=True),
    ] + corrs + corrs_phi)


    corrssj1 = [NTupleVariable(
            "sj1pt_corr_"+c,
            lambda x,c="sj1pt_corr_"+c : getattr(x, c),
            mcOnly=True,
            type=float,
        ) for c in conf.mem["jet_corrections"]
    ]

    corrssj2 = [NTupleVariable(
            "sj2pt_corr_"+c,
            lambda x,c="sj2pt_corr_"+c : getattr(x, c),
            mcOnly=True,
            type=float,
        ) for c in conf.mem["jet_corrections"]
    ]

    corrssj3 = [NTupleVariable(
            "sj3pt_corr_"+c,
            lambda x,c="sj3pt_corr_"+c : getattr(x, c),
            mcOnly=True,
            type=float,
        ) for c in conf.mem["jet_corrections"]
    ]



    #Specifies what to save for jets
    jetType = NTupleObjectType("jetType", variables = [
        NTupleVariable("pt", lambda x : x.pt),
        NTupleVariable("eta", lambda x : x.eta),
        NTupleVariable("phi", lambda x : x.phi),
        NTupleVariable("mass", lambda x : x.mass),
        NTupleVariable("id", lambda x : x.jetId),  
        NTupleVariable("qgl", lambda x : x.qgl),
        NTupleVariable("btagCSV", lambda x : x.btagCSV),
        NTupleVariable("btagDeepCSV", lambda x : x.btagDeepCSV),
        NTupleVariable("btagDeepFlav", lambda x : x.btagDeepFlav),
        NTupleVariable("btagCMVA", lambda x : x.btagCMVA),
        #NTupleVariable("btagCMVA_log", lambda x : getattr(x, "btagCMVA_log", -20), help="log-transformed btagCMVA"),
        NTupleVariable("btagFlag", lambda x : getattr(x, "btagFlag", -1), help="Jet was considered to be a b in MEM according to the algo"),
        NTupleVariable("nVertexTracks", lambda x : x.nVertexTracks),
        NTupleVariable("VertexFlightDistance", lambda x : x.VertexFlightDistance),
        NTupleVariable("VertexErrorFD", lambda x : x.VertexErrorFD),
        NTupleVariable("rawPt", lambda x : x.rawPt),
        NTupleVariable("qg_sf", lambda x : getattr(x,"qg_sf",1.), type=float, mcOnly=True),
        NTupleVariable("partonFlavour", lambda x : x.partonFlavour, type=int, mcOnly=True),
        NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int, mcOnly=True),
        NTupleVariable("matchFlag",
            lambda x : getattr(x, "tth_match_label_numeric", -1),
            type=int,
            mcOnly=True,
            help="0 - matched to light quark from W, 1 - matched to b form top, 2 - matched to b from higgs"
        ),
        NTupleVariable("matchBfromHadT", lambda x : getattr(x, "tth_match_label_bfromhadt", -1), type=int, mcOnly=True),
        NTupleVariable("mcPt", lambda x : x.mcPt, mcOnly=True),
        NTupleVariable("mcEta", lambda x : x.mcEta, mcOnly=True),
        NTupleVariable("mcPhi", lambda x : x.mcPhi, mcOnly=True),
        NTupleVariable("mcM", lambda x : x.mcM, mcOnly=True),
        NTupleVariable("mcMatchIdx", lambda x : x.mcMatchIdx, mcOnly=True),
        #NTupleVariable("mcNumBHadrons", lambda x : x.genjet.numBHadrons if hasattr(x, "genjet") else -1, mcOnly=True),
        #NTupleVariable("mcNumCHadrons", lambda x : x.genjet.numCHadrons if hasattr(x, "genjet") else -1, mcOnly=True),
        NTupleVariable("corr_JEC", lambda x : x.corr, mcOnly=True),
        NTupleVariable("corr_JER", lambda x : x.corr_JER, mcOnly=True),
        #Some SF for sync
        NTupleVariable("corr_JEC_Up", lambda x : x.pt_corr_TotalUp/x.pt, mcOnly=True),
        NTupleVariable("corr_JEC_Down", lambda x : x.pt_corr_TotalDown/x.pt, mcOnly=True),
        NTupleVariable("corr_JEC_PileUpDataMC_Down", lambda x : x.pt_corr_PileUpDataMCDown/x.pt, mcOnly=True),
        NTupleVariable("corr_JEC_RelativeFSR_Up", lambda x : x.pt_corr_RelativeFSRUp/x.pt, mcOnly=True),
        NTupleVariable("btagSF_shape", lambda x : getattr(x, "btagSF_shape", 1.0), mcOnly=True),
        NTupleVariable("puId", lambda x : x.puId),
        NTupleVariable("CSVrank", lambda x : getattr(x, "CSVrank", -99), type=int),
        NTupleVariable("CSVindex", lambda x : getattr(x, "CSVindex", -99), type=int),
        NTupleVariable("DeepCSVrank", lambda x : getattr(x, "DeepCSVrank", -99), type=int),
        NTupleVariable("DeepCSVindex", lambda x : getattr(x, "DeepCSVindex", -99), type=int),
        NTupleVariable("dRmax", lambda x : getattr(x, "dRmax", -99), type=float),
        NTupleVariable("dRmin", lambda x : getattr(x, "dRmin", -99), type=float),
        NTupleVariable("dRave", lambda x : getattr(x, "dRave", -99), type=float),
    ] + corrs)

    topCandidateType = NTupleObjectType("topCandidateType", variables = [
        NTupleVariable("subjetIDPassed", lambda x: x.subjetIDPassed ),
        NTupleVariable("fRec", lambda x: x.fRec ),
        NTupleVariable("Ropt", lambda x: x.Ropt ),
        NTupleVariable("RoptCalc", lambda x: x.RoptCalc ),
        NTupleVariable("ptForRoptCalc", lambda x: x.ptForRoptCalc ),
        NTupleVariable("pt", lambda x: x.pt ),
        NTupleVariable("eta", lambda x: x.eta ),
        NTupleVariable("phi", lambda x: x.phi ),
        NTupleVariable("mass", lambda x: x.mass ),
        NTupleVariable("sj1pt", lambda x: x.sj1pt ),
        NTupleVariable("sj1eta", lambda x: x.sj1eta ),
        NTupleVariable("sj1phi", lambda x: x.sj1phi ),
        NTupleVariable("sj1mass", lambda x: x.sj1mass ),
        NTupleVariable("sj1btag", lambda x: x.sj1btag ),
        NTupleVariable("sj1corr", lambda x: x.sj1corr ),
        NTupleVariable("sj1corr_JER", lambda x: x.sj1corr_JER ),
        NTupleVariable("sj2pt", lambda x: x.sj2pt ),
        NTupleVariable("sj2eta", lambda x: x.sj2eta ),
        NTupleVariable("sj2phi", lambda x: x.sj2phi ),
        NTupleVariable("sj2mass", lambda x: x.sj2mass ),
        NTupleVariable("sj2btag", lambda x: x.sj2btag ),
        NTupleVariable("sj2corr", lambda x: x.sj2corr ),
        NTupleVariable("sj2corr_JER", lambda x: x.sj2corr_JER ),
        NTupleVariable("sj3pt", lambda x: x.sj3pt ),
        NTupleVariable("sj3eta", lambda x: x.sj3eta ),
        NTupleVariable("sj3phi", lambda x: x.sj3phi ),
        NTupleVariable("sj3mass", lambda x: x.sj3mass ),
        NTupleVariable("sj3btag", lambda x: x.sj3btag ),
        NTupleVariable("sj3corr", lambda x: x.sj3corr ),
        NTupleVariable("sj3corr_JER", lambda x: x.sj3corr_JER ),
        NTupleVariable("tau1SD", lambda x: x.tau1SD ),   # Copied from matched fat jet
        NTupleVariable("tau2SD", lambda x: x.tau2SD ),   # Copied from matched fat jet
        NTupleVariable("tau3SD", lambda x: x.tau3SD ),   # Copied from matched fat jet
        #NTupleVariable("bbtag", lambda x: x.bbtag ), # Copied from matched fat jet
        NTupleVariable("tau32SD", lambda x: x.tau32SD ), # Calculated
        #NTupleVariable("n_subjettiness_groomed", lambda x: x.n_subjettiness_groomed ), # Calculated
        NTupleVariable("delRopt", lambda x: x.delRopt ),             # Calculated
        NTupleVariable("genTopHad_dr", lambda x: getattr(x, "genTopHad_dr", -1), help="DeltaR to the closest hadronic gen top" ),
        NTupleVariable("genTopHad_index", lambda x: getattr(x, "genTopHad_index", -1), type=int, help="Index of the matched genTopHad" ),
        NTupleVariable("dr_lepton", lambda x: getattr(x, "delR_lepton", -1), help="deltaR to closest selection lepton"),
    ]  + corrssj1 + corrssj2 + corrssj3)

    higgsCandidateType = NTupleObjectType("higgsCandidateType", variables = [
        NTupleVariable("subjetIDPassed", lambda x: x.subjetIDPassed ),
        NTupleVariable("pt", lambda x: x.pt ),
        NTupleVariable("eta", lambda x: x.eta ),
        NTupleVariable("phi", lambda x: x.phi ),
        NTupleVariable("mass", lambda x: x.mass ),
        NTupleVariable("tau1", lambda x: x.tau1 ),
        NTupleVariable("tau2", lambda x: x.tau2 ),
        NTupleVariable("tau3", lambda x: x.tau3 ),    
        NTupleVariable("tau1SD", lambda x: x.tau1SD ),
        NTupleVariable("tau2SD", lambda x: x.tau2SD ),
        NTupleVariable("tau3SD", lambda x: x.tau3SD ),
        NTupleVariable("bbtag", lambda x: x.bbtag ),
        NTupleVariable("area", lambda x: x.area ),
        NTupleVariable("ptSD", lambda x: x.ptSD ),
        NTupleVariable("etaSD", lambda x: x.etaSD ),
        NTupleVariable("phiSD", lambda x: x.phiSD ),
        NTupleVariable("massSD", lambda x: x.massSD ),

        NTupleVariable("sj1pt",   lambda x: x.sj1pt ),
        NTupleVariable("sj1eta",  lambda x: x.sj1eta ),
        NTupleVariable("sj1phi",  lambda x: x.sj1phi ),
        NTupleVariable("sj1mass", lambda x: x.sj1mass ),
        NTupleVariable("sj1btag", lambda x: x.sj1btag ),
        NTupleVariable("sj1corr", lambda x: x.sj1corr ),
        NTupleVariable("sj1corr_JER", lambda x: x.sj1corr_JER ),
        NTupleVariable("sj2pt",   lambda x: x.sj2pt ),
        NTupleVariable("sj2eta",  lambda x: x.sj2eta ),
        NTupleVariable("sj2phi",  lambda x: x.sj2phi ),
        NTupleVariable("sj2mass", lambda x: x.sj2mass ),
        NTupleVariable("sj2btag", lambda x: x.sj2btag ),
        NTupleVariable("sj2corr", lambda x: x.sj2corr ),
        NTupleVariable("sj2corr_JER", lambda x: x.sj2corr_JER ),

        NTupleVariable("tau21", lambda x: x.tau21 ),
        #NTupleVariable("tau21SD", lambda x: x.tau21SD ),
        NTupleVariable("dr_top", lambda x: getattr(x, "dr_top", -1), help="deltaR to the best HTT candidate"),
        NTupleVariable("dr_genHiggs", lambda x: getattr(x, "dr_genHiggs", -1), help="deltaR to gen higgs"),
        NTupleVariable("dr_genTop", lambda x: getattr(x, "dr_genTop", -1), help="deltaR to closest gen top"),
    ])


    higgsCandidateAK8Type = NTupleObjectType("higgsCandidateAK8Type", variables = [
        NTupleVariable("pt", lambda x: x.pt ),
        NTupleVariable("eta", lambda x: x.eta ),
        NTupleVariable("phi", lambda x: x.phi ),
        NTupleVariable("mass", lambda x: x.mass ),
        NTupleVariable("tau1", lambda x: x.tau1 ),
        NTupleVariable("tau2", lambda x: x.tau2 ),
        NTupleVariable("tau3", lambda x: x.tau3 ),
        NTupleVariable("tau21", lambda x: x.tau21 ),
        NTupleVariable("bbtag", lambda x: x.bbtag ),
        NTupleVariable("area", lambda x: x.area ),
        NTupleVariable("msoftdrop", lambda x: x.msoftdrop ),

        NTupleVariable("sj1pt",   lambda x: x.sj1pt ),
        NTupleVariable("sj1eta",  lambda x: x.sj1eta ),
        NTupleVariable("sj1phi",  lambda x: x.sj1phi ),
        NTupleVariable("sj1mass", lambda x: x.sj1mass ),
        NTupleVariable("sj1btag", lambda x: x.sj1btag ),
        NTupleVariable("sj1corr", lambda x: x.sj1corr ),
        NTupleVariable("sj1corr_JER", lambda x: x.sj1corr_JER ),
        NTupleVariable("sj2pt",   lambda x: x.sj2pt ),
        NTupleVariable("sj2eta",  lambda x: x.sj2eta ),
        NTupleVariable("sj2phi",  lambda x: x.sj2phi ),
        NTupleVariable("sj2mass", lambda x: x.sj2mass ),
        NTupleVariable("sj2btag", lambda x: x.sj2btag ),
        NTupleVariable("sj2corr", lambda x: x.sj2corr ),
        NTupleVariable("sj2corr_JER", lambda x: x.sj2corr_JER ),

        NTupleVariable("n_subjettiness", lambda x: x.tau2/x.tau1 if x.tau1 > 0 else -1 ),
        NTupleVariable("dr_top", lambda x: getattr(x, "dr_top", -1), help="deltaR to the best HTT candidate"),
        NTupleVariable("dr_genHiggs", lambda x: getattr(x, "dr_genHiggs", -1), help="deltaR to gen higgs"),
        NTupleVariable("dr_genTop", lambda x: getattr(x, "dr_genTop", -1), help="deltaR to closest gen top"),
    ] + corrssj1 + corrssj2)

    FatjetCA15Type = NTupleObjectType("FatjetCA15Type", variables = [
        NTupleVariable("pt", lambda x: x.pt ),
        NTupleVariable("eta", lambda x: x.eta ),
        NTupleVariable("phi", lambda x: x.phi ),
        NTupleVariable("mass", lambda x: x.mass ),
        NTupleVariable("tau1", lambda x: x.tau1 ),
        NTupleVariable("tau2", lambda x: x.tau2 ),
        NTupleVariable("tau3", lambda x: x.tau3 ),
        NTupleVariable("bbtag", lambda x: x.bbtag ),
    ])

    #Create the output TTree writer
    #Here we define all the variables that we want to save in the output TTree
    treeProducer = cfg.Analyzer(
        class_object = AutoFillTreeProducer,
        defaultFloatType = "F",
        verbose = False,
        vectorTree = True,
        globalVariables = [
            NTupleVariable(
               "nGenBHiggs", lambda ev: len(getattr(ev, "b_quarks_h_nominal", [])),
               type=int,
               help="Number of generated b from higgs", mcOnly=True
            ),

            NTupleVariable(
               "nGenBTop", lambda ev: len(getattr(ev, "b_quarks_t_nominal", [])),
               type=int,
               help="Number of generated b from top", mcOnly=True
            ),

            NTupleVariable(
               "nGenQW", lambda ev: len(getattr(ev, "l_quarks_w_nominal", [])),
               type=int,
               help="Number of generated quarks from W", mcOnly=True
            ),
            
            NTupleVariable(
               "passPV", lambda ev: getattr(ev, "passPV", -1),
               type=int,
               help="First PV passes selection"
            ),

            NTupleVariable(
               "triggerDecision", lambda ev: getattr(ev, "triggerDecision", -1),
               type=int,
               help="Trigger selection"
            ),
            NTupleVariable(
               "triggerBitmask", lambda ev: getattr(ev, "triggerBitmask", -1),
               type=int,
               help="Bitmask of trigger decisions"
            ),
            NTupleVariable(
               "is_sl", lambda ev: ev.is_sl,
               type=int,
               help="is single-leptonic"
            ),
            NTupleVariable(
               "is_dl", lambda ev: ev.is_dl,
               type=int,
               help="is di-leptonic"
            ),
            NTupleVariable(
               "is_fh", lambda ev: ev.is_fh,
               type=int,
               help="is fully hadronic"
            ),
            #NTupleVariable("ht40", lambda ev: getattr(ev, "ht40", -9999), type=float, help="ht considering only jets with pT>40"),
            #NTupleVariable("csv1", lambda ev: getattr(ev, "csv1", -9999), type=float, help="highest jet csv value"),
            #NTupleVariable("csv2", lambda ev: getattr(ev, "csv2", -9999), type=float, help="2nd highest jet csv value"),
            NTupleVariable("run", lambda ev: ev.input.run, type=int),
            NTupleVariable("lumi", lambda ev: ev.input.luminosityBlock, type=int),
            NTupleVariable("evt1", lambda ev: int(math.floor(ev.input.event / 1000000000.0)), type=int),
            NTupleVariable("evt2", lambda ev: ev.input.event - int(math.floor(ev.input.event / 1000000000.0)) * 1000000000, type=int),
            NTupleVariable("evt", lambda ev: ev.input.event),
            NTupleVariable("evt_more", lambda ev: round(ev.input.event)),
            NTupleVariable("Flag_ele32DoubleL1ToSingleL1", lambda ev: ev.input.Flag_ele32DoubleL1ToSingleL1, type=int),


        ],
        globalObjects = {
           "MET" : NTupleObject("met", metType, help="Reconstructed MET"),
           #"MET_gen_nominal" : NTupleObject("met_gen", metType, help="Generated MET", mcOnly=True),
           #"MET_jetcorr_nominal" : NTupleObject("met_jetcorr", metType, help="Reconstructed MET, corrected to gen-level jets"),
           #"MET_tt_nominal" : NTupleObject("met_ttbar_gen", metType, help="Generated MET from nu(top)"),
           "primaryVertex" : NTupleObject("pv", pvType, help="First PV"),
           "dilepton_p4" : NTupleObject("ll", p4type, help="Dilepton system"),
           #"jlr_top" : NTupleObject("jlr_top", p4type, help="Top quark from the JLR calculation", mcOnly=True),
           #"jlr_atop" : NTupleObject("jlr_atop", p4type, help="Antitop quark from the JLR calculation", mcOnly=True),
           #"jlr_bottom" : NTupleObject("jlr_bottom", p4type, help="bottom quark from the JLR calculation", mcOnly=True),
           #"jlr_abottom" : NTupleObject("jlr_abottom", p4type, help="Antibottom quark from the JLR calculation", mcOnly=True),
        },
        collections = {
        #standard dumping of objects
        #These are collections which are not variated
            #"b_quarks_gen_nominal" : NTupleCollection("b_quarks_gen", quarkType, 5, help="generated b quarks", mcOnly=True),
            #"l_quarks_gen_nominal" : NTupleCollection("l_quarks_gen", quarkType, 3, help="generated light quarks", mcOnly=True),
            "b_quarks_t_nominal" : NTupleCollection("GenBFromTop", quarkType, 3, help="generated b quarks from top", mcOnly=True),
            "b_quarks_h_nominal" : NTupleCollection("GenBFromHiggs", quarkType, 3, help="generated b quarks from higgs", mcOnly=True),
            "l_quarks_w_nominal" : NTupleCollection("GenQFromW", quarkType, 5, help="generated light quarks from W", mcOnly=True),
            "GenHiggsBoson" : NTupleCollection("genHiggs", quarkType, 2, help="Generated Higgs boson", mcOnly=True),
            "genTopLep" : NTupleCollection("genTopLep", genTopType, 2, help="Generated top quark (leptonic)", mcOnly=True),
            "genTopHad" : NTupleCollection("genTopHad", genTopType, 2, help="Generated top quark (hadronic)", mcOnly=True),
            "GenLep" : NTupleCollection("GenLep", quarkType, 2, help="Generated leptons", mcOnly=True),
            "LHEScaleWeights" : NTupleCollection("LHEScaleWeights", LHE_weights_type, 9,
                                                 help="muR/muF weights: Down/Down, Down/Nom, Down/Up, Nom/Down, Nom/Nom, Nom/Up, Up/Down, Up/Nom, Up/Up", mcOnly=True),
            "LHEPDFWeights" : NTupleCollection("LHEPDFWeights", LHE_weights_type, 150,
                                               help="LHE weights pdf: PDFSet depending on nanoAOD settings --> check PhysicsTools/NanoAOD/python/nano_cff.py", mcOnly=True),
            "LHEReweightingWeights" : NTupleCollection("LHEReweightingWeights", LHE_weights_type, 100,
                                                 help="LHEWeight for reweiging the sample- E.g. for tH samples.", mcOnly=True),


            "good_jets_nominal" : NTupleCollection("jets", jetType, 16, help="Selected resolved jets, pt ordered"),
            "good_leptons_nominal" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),
            
            "loose_jets_nominal" : NTupleCollection("loose_jets", jetType, 6, help="Additional jets with 20<pt<30"),

        }
    )
    
    #add HLT bits to final tree
    trignames = []
    triggerlist = list(conf.trigger["trigTable"].items()) + list(conf.trigger["trigTableData"].items())
    triggerlist = filter(lambda x: not ":" in x[0], triggerlist) # remove ds specific trigger configurations
    for pathname, trigs in triggerlist:
        #add trigger path (combination of trigger)
        _pathname = "_".join(["HLT", pathname])
        if not _pathname in trignames and "ttH" in _pathname: #Only save path with ttH in name 
            trignames += [_pathname]

        #add individual trigger bits
        for tn in trigs:
            #strip the star
            tn = "HLT_BIT_" + tn
            if not tn in trignames:
                trignames += [tn]
                
    for mergedPath in conf.trigger["MergePaths"]:
        _pathname = "HLT_ttH_"+mergedPath
        if not _pathname in trignames:
            trignames += [_pathname]
            
    for trig in trignames:
        if trig.startswith("HLT_BIT_"):
            trig_ = trig[len("HLT_BIT_"):] #Bit is saved w/o "HLT_BIT_" in the beginning
            treeProducer.globalVariables += [NTupleVariable(
                trig, lambda ev, name=trig_: getattr(ev, name, -1), type=int, mcOnly=False
            )]
        else:
            treeProducer.globalVariables += [NTupleVariable(
                trig, lambda ev, name=trig: getattr(ev, name, -1), type=int, mcOnly=False
            )]
        
    if conf.general["boosted"] == True:
        treeProducer.globalVariables += [NTupleVariable(
            "n_bjets",
            lambda ev: getattr(ev, "n_bjets_nominal", -1),
            help="Number of selected bjets in event"
        )]
    
        treeProducer.globalVariables += [NTupleVariable(
           "n_ljets",
           lambda ev: getattr(ev, "n_ljets_nominal", -1),
           help="Number of selected ljets in event"
        )]
    
        #treeProducer.globalVariables += [NTupleVariable(
        #   "n_boosted_bjets",
        #   lambda ev: getattr(ev, "n_boosted_bjets_nominal", -1),
        #   help="Number of selected bjets in subjet-modified bjet list"
        #)]
    
        #treeProducer.globalVariables += [NTupleVariable(
        #   "n_boosted_ljets",
        #   lambda ev: getattr(ev, "n_boosted_ljets_nominal", -1),
        #   help="Number of selected ljets in subjet-modified ljet list"
        #)]

        treeProducer.globalVariables += [NTupleVariable(
           "n_boosted_allljets",
           lambda ev: getattr(ev, "n_boosted_allljets_nominal", -1),
           help="Number of selected ljets in subjet-modified ljet list, including additional FSR + ISR jets"
        )]

        treeProducer.globalVariables += [NTupleVariable(
           "n_excluded_bjets",
           lambda ev: getattr(ev, "n_excluded_bjets_nominal", -1),
           help="Number of excluded bjets: reco resolved b-jets that match a subjet in the HTT-candidate"
        )]  

        treeProducer.globalVariables += [NTupleVariable(
           "n_excluded_ljets",
           lambda ev: getattr(ev, "n_excluded_ljets_nominal", -1),
           help="Number of excluded ljets: "
        )]

        #treeProducer.globalVariables += [NTupleVariable(
        #   "boosted",
        #   lambda ev: getattr(ev, "boosted_nominal", -1),
        #   help="Passed subjet analyzer"
        #)]

        #treeProducer.collections.update({"FatjetCA15" : NTupleCollection("fatjets", FatjetCA15Type, 4, help="Ungroomed CA 1.5 fat jets")})
        treeProducer.collections.update({"topCandidate_nominal": NTupleCollection("topCandidate" , topCandidateType, 4, help="Boosted Top candidates")})
        treeProducer.collections.update({"higgsCandidate_nominal": NTupleCollection("higgsCandidate", higgsCandidateAK8Type, 4, help="Boosted Higgs candidates")})

        treeProducer.collections.update({"boosted_bjets_nominal": NTupleCollection("boosted_bjets", kinType, 4, help="Boosted b jets")})
        treeProducer.collections.update({"boosted_ljets_nominal": NTupleCollection("boosted_ljets", kinType, 4, help="Boosted l jets")})      
        
        for systematic in conf.general["systematics"]:

            #scalar variables that have systematic variations
            for vtype in [
                ("n_boosted_bjets",               float,      "Number of selected bjets in subjet-modified bjet list"),
                ("n_boosted_ljets",               float,      "Number of selected ljets in subjet-modified bjet list"),
                ("boosted",               float,      "Passed subjet analyzer"),
            ]:
                is_mc_only = False
    
                #only define the nominal values for data
                if systematic != "nominal":
                    is_mc_only = True
    
                treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic, mcOnly=is_mc_only)]
        #end of loop over syst variables 
    #MET filter flags added in VHBB
    #According to https://gitlab.cern.ch/ttH/reference/blob/master/definitions/Moriond17.md#42-met-filters
    metfilter_flags = [
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_CSCTightHaloFilter",
        "Flag_CSCTightHaloTrkMuUnvetoFilter",
        "Flag_CSCTightHalo2015Filter",
        "Flag_globalTightHalo2016Filter",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_HcalStripHaloFilter",
        "Flag_hcalLaserEventFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_EcalDeadCellBoundaryEnergyFilter",
        "Flag_ecalBadCalibFilter",
        "Flag_goodVertices",
        "Flag_eeBadScFilter",
        "Flag_ecalLaserCorrFilter",
        "Flag_trkPOGFilters",
        "Flag_chargedHadronTrackResolutionFilter",
        "Flag_muonBadTrackFilter",
        "Flag_BadChargedCandidateFilter",
        "Flag_BadPFMuonFilter",
        "Flag_BadChargedCandidateSummer16Filter",
        "Flag_BadPFMuonSummer16Filter",
        "Flag_trkPOG_manystripclus53X",
        "Flag_trkPOG_toomanystripclus53X",
        "Flag_trkPOG_logErrorTooManyClusters",
        "Flag_METFilters",
        "Flag_ecalBadCalibFilterV2",
    ]
    for metfilter in metfilter_flags:
        treeProducer.globalVariables += [NTupleVariable(
            metfilter, lambda ev, name=metfilter: getattr(ev.input, name, -1), type=int, mcOnly=False
        )]
    
    treeProducer.globalVariables += [NTupleVariable(
        "passMETFilters", lambda ev, name="passMETFilters": getattr(ev, "passMETFilters", -1), type=int, mcOnly=False
        )]
                                                                    
       
    #Add systematically variated quantities
    for systematic in conf.general["systematics"]:

        #scalar variables that have systematic variations
        for vtype in [
            ("Wmass",               float,      "Best reconstructed W candidate mass"),
            #("mbb_closest",          float,      "Mass of geometrically closest bb pair"),
            #("mjjmin",               float,      "Minimus mass of all jet pairs"),
            #("min_dr_btag",          float,      "DR between closest b tags"),
            #("mass_drpair_btag",     float,      "Mass of closest b tag pair"),
            #("mass_drpair_untag",    float,      "Mass of closest jet pair"),
            #("centralitymass",       float,      "HT over invariant mass of all jets"),
            ("cat",                 int,        "ME category", "catn"),
            ("cat_btag",            int,        "ME category (b-tag)", "cat_btag_n"),
            ("cat_gen",             int,        "top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)", "cat_gen_n"),
            #("fh_region",           int,        "FH region for QCD estimation"), #DS
            #("btag_lr_4b",          float,      "4b, N-4 light, probability, 3D binning"),
            #("btag_lr_3b",          float,      "3b, N-3 light, probability, 3D binning"),
            #("btag_lr_2b",          float,      "2b, N-2 Nlight probability, 3D binning"),
            #("btag_lr_1b",          float,      "1b, N-1 Nlight probability, 3D binning"),
            #("btag_lr_0b",          float,      "0b, N   Nlight probability, 3D binning"),
            #("btag_LR_4b_2b_btagCMVA_log",   float,      ""),
            #("btag_LR_4b_2b_btagCMVA",        float,      "4b vs 2b b-tag likelihood ratio using the cMVA tagger"),
            ("btag_LR_4b_2b_btagCSV",        float,      "4b vs 2b b-tag likelihood ratio using the CSV tagger"),
            ("btag_LR_4b_2b_btagDeepCSV",        float,      "4b vs 2b b-tag likelihood ratio using the DeepCSV tagger"),
            #("htt_mass",        float,      "HEPTopTagger candidate mass"),
            #("htt_frec",        float,      "HEPTopTagger candidate mass"),
            #("higgs_mass",      float,      "Higgs candidate mass"),
            #("btag_LR_4b_3b_btagCMVA_log",   float,      ""),
            #("btag_LR_4b_3b_btagCMVA",       float,      ""),
            ("btag_LR_4b_3b_btagCSV",        float,      ""),
            ("btag_LR_4b_3b_btagDeepCSV",        float,      ""),
            #("btag_LR_3b_2b_btagCMVA_log",   float,      ""),
            #("btag_LR_3b_2b_btagCMVA",       float,      ""),
            ("btag_LR_3b_2b_btagCSV",        float,      ""),
            ("btag_LR_3b_2b_btagDeepCSV",        float,      ""),
            #("btag_LR_geq2b_leq1b_btagCMVA_log",   float,   ""),
            #("btag_LR_geq2b_leq1b_btagCMVA",       float,   ""),
            ("btag_LR_geq2b_leq1b_btagCSV",        float,   ""),
            ("btag_LR_geq2b_leq1b_btagDeepCSV",        float,   ""),
            #("qg_LR_4b_flavour_3q_0q", float,      ""),
            #("qg_LR_4b_flavour_3q_2q", float,      ""),
            #("qg_LR_4b_flavour_4q_0q", float,      ""),
            #("qg_LR_4b_flavour_4q_3q", float,      ""),
            #("qg_LR_4b_flavour_5q_0q", float,      ""),
            #("qg_LR_3b_flavour_3q_0q", float,      ""),
            #("qg_LR_3b_flavour_3q_2q", float,      ""),
            #("qg_LR_3b_flavour_4q_0q", float,      ""),
            #("qg_LR_3b_flavour_4q_3q", float,      ""),
            #("qg_LR_3b_flavour_5q_0q", float,      ""),
            #("qg_LR_3b_flavour_5q_4q", float,      ""),

            #("nBCSVM",              int,      "Number of good jets that pass the CSV Medium WP"),
            #("nBCSVT",              int,      "Number of good jets that pass the DeepCSV Tight WP"),
            #("nBCSVL",              int,      "Number of good jets that pass the DeepCSV Loose WP"),
            ("nBDeepCSVM",          int,      "Number of good jets that pass the DeepCSV Medium WP"),
            ("nBDeepFlavM",          int,      "Number of good jets that pass the DeepFlavour Medium WP"),
            #("nCSVv2IVFM",              int,      ""),                
            #("nBCMVAM",             int,      "Number of good jets that pass cMVAv2 Medium WP"),
            ("numJets",             int,        "Total number of good jets that pass jet ID"),
            ("ht",                  float,      ""),
            ("changes_jet_category",int,        "Jet category changed on systematic"),
            #("ht30",                float,      ""),
        ]:

            is_mc_only = False

            #only define the nominal values for data
            if systematic != "nominal":
                is_mc_only = True

            treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic, mcOnly=is_mc_only)]
        #end of loop over syst variables 
        
        syst_suffix = "_" + systematic
        syst_suffix2 = syst_suffix
        if systematic == "nominal":
            syst_suffix2 = ""
       
        #treeProducer.collections.update({"Detaj"+syst_suffix : NTupleCollection("Detaj"+syst_suffix2, arrayType, 15, help="Average deltaEta to (N+1)th closest jet", mcOnly=is_mc_only)})
        #add nominal and systematically variated final MEM ratios
        #these are simple scalars already
        for hypo in conf.mem["methodsToRun"]:
            treeProducer.globalVariables.append(
                NTupleVariable(
                    "mem_" + hypo + "_p" + syst_suffix2,
                    lambda ev, s="mem_" + hypo + "_p" + syst_suffix: getattr(ev, s, 0.0),
                    mcOnly = False,
                ),
            )
    #add full MEM output struct for nominal and the systematic case where we
    #explicitly recomputed the MEM
    for systematic in conf.general["systematics"]:
        syst_suffix = "_" + systematic
        syst_suffix2 = syst_suffix
        memType = memType_syst
        if systematic == "nominal":
            syst_suffix2 = ""
            memType = memType_nominal
            #Run only in the nominal case
            for hypo in conf.mem["methodsToRun"]:
                for proc in ["tth", "ttbb"]:
                    name = "mem_{0}_{1}".format(proc, hypo) 
                    treeProducer.globalObjects.update({
                        name + syst_suffix: NTupleObject(
                            name + syst_suffix2, memType ,
                            help="MEM result for proc={0} hypo={1} syst={2}".format(proc, hypo, systematic),
                            mcOnly = False if systematic == "nominal" else True
                        ),
                    })

    #bTagSFEvVars = []
    ## Has to be hardcoded getattr(ev, variable) seems not to work if variable is set in a for loop
    #bTagSFEvVars.append(("btagWeight_shape", float, "Event b-tag SF", lambda ev: getattr(ev, "btagWeight_shape")))
    #bTagSFEvVars.append(("btagWeight_shape_lf_up", float, "Event b-tag SF lf_up", lambda ev: getattr(ev, "btagWeight_shape_lf_up")))
    #bTagSFEvVars.append(("btagWeight_shape_lf_down", float, "Event b-tag SF lf_down", lambda ev: getattr(ev, "btagWeight_shape_lf_down")))
    #bTagSFEvVars.append(("btagWeight_shape_hf_up", float, "Event b-tag SF hf_up", lambda ev: getattr(ev, "btagWeight_shape_hf_up")))
    #bTagSFEvVars.append(("btagWeight_shape_hf_down", float, "Event b-tag SF hf_down", lambda ev: getattr(ev, "btagWeight_shape_hf_down")))
    #bTagSFEvVars.append(("btagWeight_shape_hfstats1_up", float, "Event b-tag SF hfstats1_up", lambda ev: getattr(ev, "btagWeight_shape_hfstats1_up")))
    #bTagSFEvVars.append(("btagWeight_shape_hfstats1_down", float, "Event b-tag SF hfstats1_down", lambda ev: getattr(ev, "btagWeight_shape_hfstats1_down")))
    #bTagSFEvVars.append(("btagWeight_shape_hfstats2_up", float, "Event b-tag SF hfstats2_up", lambda ev: getattr(ev, "btagWeight_shape_hfstats2_up")))
    #bTagSFEvVars.append(("btagWeight_shape_hfstats2_down", float, "Event b-tag SF hfstats2_down", lambda ev: getattr(ev, "btagWeight_shape_hfstats2_down")))
    #bTagSFEvVars.append(("btagWeight_shape_lfstats1_up", float, "Event b-tag SF lfstats1_up", lambda ev: getattr(ev, "btagWeight_shape_lfstats1_up")))
    #bTagSFEvVars.append(("btagWeight_shape_lfstats1_down", float, "Event b-tag SF lfstats1_down", lambda ev: getattr(ev, "btagWeight_shape_lfstats1_down")))
    #bTagSFEvVars.append(("btagWeight_shape_lfstats2_up", float, "Event b-tag SF lfstats2_up", lambda ev: getattr(ev, "btagWeight_shape_lfstats2_up")))
    #bTagSFEvVars.append(("btagWeight_shape_lfstats2_down", float, "Event b-tag SF lfstats2_down", lambda ev: getattr(ev, "btagWeight_shape_lfstats2_down")))
    #bTagSFEvVars.append(("btagWeight_shape_cferr1_up", float, "Event b-tag SF cferr1_up", lambda ev: getattr(ev, "btagWeight_shape_cferr1_up")))
    #bTagSFEvVars.append(("btagWeight_shape_cferr1_down", float, "Event b-tag SF cferr1_down", lambda ev: getattr(ev, "btagWeight_shape_cferr1_down")))
    #bTagSFEvVars.append(("btagWeight_shape_cferr2_up", float, "Event b-tag SF cferr2_up", lambda ev: getattr(ev, "btagWeight_shape_cferr2_up")))
    #bTagSFEvVars.append(("btagWeight_shape_cferr2_down", float, "Event b-tag SF cferr2_down", lambda ev: getattr(ev, "btagWeight_shape_cferr2_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesAbsoluteMPFBias_up", float, "Event b-tag SF jesAbsoluteMPFBias_up", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteMPFBias_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesAbsoluteMPFBias_down", float, "Event b-tag SF jesAbsoluteMPFBias_down", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteMPFBias_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesAbsoluteScale_up", float, "Event b-tag SF jesAbsoluteScale_up", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteScale_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesAbsoluteScale_down", float, "Event b-tag SF jesAbsoluteScale_down", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteScale_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesAbsoluteStat_up", float, "Event b-tag SF jesAbsoluteStat_up", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteStat_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesAbsoluteStat_down", float, "Event b-tag SF jesAbsoluteStat_down", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteStat_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesFlavorQCD_up", float, "Event b-tag SF jesFlavorQCD_up", lambda ev: getattr(ev, "btagWeight_shape_jesFlavorQCD_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesFlavorQCD_down", float, "Event b-tag SF jesFlavorQCD_down", lambda ev: getattr(ev, "btagWeight_shape_jesFlavorQCD_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesFragmentation_up", float, "Event b-tag SF jesFragmentation_up", lambda ev: getattr(ev, "btagWeight_shape_jesFragmentation_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesFragmentation_down", float, "Event b-tag SF jesFragmentation_down", lambda ev: getattr(ev, "btagWeight_shape_jesFragmentation_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpDataMC_up", float, "Event b-tag SF jesPileUpDataMC_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpDataMC_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpDataMC_down", float, "Event b-tag SF jesPileUpDataMC_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpDataMC_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtBB_up", float, "Event b-tag SF jesPileUpPtBB_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtBB_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtBB_down", float, "Event b-tag SF jesPileUpPtBB_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtBB_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtEC1_up", float, "Event b-tag SF jesPileUpPtEC1_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC1_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtEC1_down", float, "Event b-tag SF jesPileUpPtEC1_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC1_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtEC2_up", float, "Event b-tag SF jesPileUpPtEC2_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC2_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtEC2_down", float, "Event b-tag SF jesPileUpPtEC2_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC2_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtHF_up", float, "Event b-tag SF jesPileUpPtHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtHF_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtHF_down", float, "Event b-tag SF jesPileUpPtHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtHF_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtRef_up", float, "Event b-tag SF jesPileUpPtRef_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtRef_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesPileUpPtRef_down", float, "Event b-tag SF jesPileUpPtRef_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtRef_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeBal_up", float, "Event b-tag SF jesRelativeBal_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeBal_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeBal_down", float, "Event b-tag SF jesRelativeBal_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeBal_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeFSR_up", float, "Event b-tag SF jesRelativeFSR_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeFSR_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeFSR_down", float, "Event b-tag SF jesRelativeFSR_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeFSR_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeJEREC1_up", float, "Event b-tag SF jesRelativeJEREC1_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC1_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeJEREC1_down", float, "Event b-tag SF jesRelativeJEREC1_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC1_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeJEREC2_up", float, "Event b-tag SF jesRelativeJEREC2_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC2_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeJEREC2_down", float, "Event b-tag SF jesRelativeJEREC2_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC2_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeJERHF_up", float, "Event b-tag SF jesRelativeJERHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJERHF_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeJERHF_down", float, "Event b-tag SF jesRelativeJERHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJERHF_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtBB_up", float, "Event b-tag SF jesRelativePtBB_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtBB_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtBB_down", float, "Event b-tag SF jesRelativePtBB_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtBB_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtEC1_up", float, "Event b-tag SF jesRelativePtEC1_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC1_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtEC1_down", float, "Event b-tag SF jesRelativePtEC1_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC1_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtEC2_up", float, "Event b-tag SF jesRelativePtEC2_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC2_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtEC2_down", float, "Event b-tag SF jesRelativePtEC2_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC2_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtHF_up", float, "Event b-tag SF jesRelativePtHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtHF_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativePtHF_down", float, "Event b-tag SF jesRelativePtHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtHF_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeStatFSR_up", float, "Event b-tag SF jesRelativeStatFSR_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatFSR_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeStatFSR_down", float, "Event b-tag SF jesRelativeStatFSR_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatFSR_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeStatEC_up", float, "Event b-tag SF jesRelativeStatEC_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatEC_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeStatEC_down", float, "Event b-tag SF jesRelativeStatEC_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatEC_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeStatHF_up", float, "Event b-tag SF jesRelativeStatHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatHF_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesRelativeStatHF_down", float, "Event b-tag SF jesRelativeStatHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatHF_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesSinglePionECAL_up", float, "Event b-tag SF jesSinglePionECAL_up", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionECAL_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesSinglePionECAL_down", float, "Event b-tag SF jesSinglePionECAL_down", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionECAL_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesSinglePionHCAL_up", float, "Event b-tag SF jesSinglePionHCAL_up", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionHCAL_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesSinglePionHCAL_down", float, "Event b-tag SF jesSinglePionHCAL_down", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionHCAL_down")))
    #bTagSFEvVars.append(("btagWeight_shape_jesTimePtEta_up", float, "Event b-tag SF jesTimePtEta_up", lambda ev: getattr(ev, "btagWeight_shape_jesTimePtEta_up")))
    #bTagSFEvVars.append(("btagWeight_shape_jesTimePtEta_down", float, "Event b-tag SF jesTimePtEta_down", lambda ev: getattr(ev, "btagWeight_shape_jesTimePtEta_down")))
        
    #bTagSFEvVarsboosted = []
    ## Has to be hardcoded getattr(ev, variable) seems not to work if variable is set in a for loop
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape", float, "Event b-tag SF", lambda ev: getattr(ev, "btagWeight_shape")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_lf_up", float, "Event b-tag SF lf_up", lambda ev: getattr(ev, "btagWeight_shape_lf_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_lf_down", float, "Event b-tag SF lf_down", lambda ev: getattr(ev, "btagWeight_shape_lf_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_hf_up", float, "Event b-tag SF hf_up", lambda ev: getattr(ev, "btagWeight_shape_hf_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_hf_down", float, "Event b-tag SF hf_down", lambda ev: getattr(ev, "btagWeight_shape_hf_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_hfstats1_up", float, "Event b-tag SF hfstats1_up", lambda ev: getattr(ev, "btagWeight_shape_hfstats1_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_hfstats1_down", float, "Event b-tag SF hfstats1_down", lambda ev: getattr(ev, "btagWeight_shape_hfstats1_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_hfstats2_up", float, "Event b-tag SF hfstats2_up", lambda ev: getattr(ev, "btagWeight_shape_hfstats2_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_hfstats2_down", float, "Event b-tag SF hfstats2_down", lambda ev: getattr(ev, "btagWeight_shape_hfstats2_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_lfstats1_up", float, "Event b-tag SF lfstats1_up", lambda ev: getattr(ev, "btagWeight_shape_lfstats1_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_lfstats1_down", float, "Event b-tag SF lfstats1_down", lambda ev: getattr(ev, "btagWeight_shape_lfstats1_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_lfstats2_up", float, "Event b-tag SF lfstats2_up", lambda ev: getattr(ev, "btagWeight_shape_lfstats2_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_lfstats2_down", float, "Event b-tag SF lfstats2_down", lambda ev: getattr(ev, "btagWeight_shape_lfstats2_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_cferr1_up", float, "Event b-tag SF cferr1_up", lambda ev: getattr(ev, "btagWeight_shape_cferr1_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_cferr1_down", float, "Event b-tag SF cferr1_down", lambda ev: getattr(ev, "btagWeight_shape_cferr1_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_cferr2_up", float, "Event b-tag SF cferr2_up", lambda ev: getattr(ev, "btagWeight_shape_cferr2_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_cferr2_down", float, "Event b-tag SF cferr2_down", lambda ev: getattr(ev, "btagWeight_shape_cferr2_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesAbsoluteMPFBias_up", float, "Event b-tag SF jesAbsoluteMPFBias_up", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteMPFBias_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesAbsoluteMPFBias_down", float, "Event b-tag SF jesAbsoluteMPFBias_down", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteMPFBias_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesAbsoluteScale_up", float, "Event b-tag SF jesAbsoluteScale_up", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteScale_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesAbsoluteScale_down", float, "Event b-tag SF jesAbsoluteScale_down", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteScale_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesAbsoluteStat_up", float, "Event b-tag SF jesAbsoluteStat_up", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteStat_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesAbsoluteStat_down", float, "Event b-tag SF jesAbsoluteStat_down", lambda ev: getattr(ev, "btagWeight_shape_jesAbsoluteStat_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesFlavorQCD_up", float, "Event b-tag SF jesFlavorQCD_up", lambda ev: getattr(ev, "btagWeight_shape_jesFlavorQCD_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesFlavorQCD_down", float, "Event b-tag SF jesFlavorQCD_down", lambda ev: getattr(ev, "btagWeight_shape_jesFlavorQCD_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesFragmentation_up", float, "Event b-tag SF jesFragmentation_up", lambda ev: getattr(ev, "btagWeight_shape_jesFragmentation_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesFragmentation_down", float, "Event b-tag SF jesFragmentation_down", lambda ev: getattr(ev, "btagWeight_shape_jesFragmentation_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpDataMC_up", float, "Event b-tag SF jesPileUpDataMC_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpDataMC_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpDataMC_down", float, "Event b-tag SF jesPileUpDataMC_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpDataMC_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtBB_up", float, "Event b-tag SF jesPileUpPtBB_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtBB_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtBB_down", float, "Event b-tag SF jesPileUpPtBB_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtBB_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtEC1_up", float, "Event b-tag SF jesPileUpPtEC1_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC1_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtEC1_down", float, "Event b-tag SF jesPileUpPtEC1_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC1_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtEC2_up", float, "Event b-tag SF jesPileUpPtEC2_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC2_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtEC2_down", float, "Event b-tag SF jesPileUpPtEC2_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtEC2_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtHF_up", float, "Event b-tag SF jesPileUpPtHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtHF_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtHF_down", float, "Event b-tag SF jesPileUpPtHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtHF_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtRef_up", float, "Event b-tag SF jesPileUpPtRef_up", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtRef_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesPileUpPtRef_down", float, "Event b-tag SF jesPileUpPtRef_down", lambda ev: getattr(ev, "btagWeight_shape_jesPileUpPtRef_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeBal_up", float, "Event b-tag SF jesRelativeBal_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeBal_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeBal_down", float, "Event b-tag SF jesRelativeBal_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeBal_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeFSR_up", float, "Event b-tag SF jesRelativeFSR_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeFSR_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeFSR_down", float, "Event b-tag SF jesRelativeFSR_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeFSR_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeJEREC1_up", float, "Event b-tag SF jesRelativeJEREC1_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC1_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeJEREC1_down", float, "Event b-tag SF jesRelativeJEREC1_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC1_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeJEREC2_up", float, "Event b-tag SF jesRelativeJEREC2_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC2_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeJEREC2_down", float, "Event b-tag SF jesRelativeJEREC2_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJEREC2_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeJERHF_up", float, "Event b-tag SF jesRelativeJERHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJERHF_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeJERHF_down", float, "Event b-tag SF jesRelativeJERHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeJERHF_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtBB_up", float, "Event b-tag SF jesRelativePtBB_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtBB_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtBB_down", float, "Event b-tag SF jesRelativePtBB_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtBB_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtEC1_up", float, "Event b-tag SF jesRelativePtEC1_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC1_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtEC1_down", float, "Event b-tag SF jesRelativePtEC1_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC1_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtEC2_up", float, "Event b-tag SF jesRelativePtEC2_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC2_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtEC2_down", float, "Event b-tag SF jesRelativePtEC2_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtEC2_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtHF_up", float, "Event b-tag SF jesRelativePtHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtHF_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativePtHF_down", float, "Event b-tag SF jesRelativePtHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativePtHF_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeStatFSR_up", float, "Event b-tag SF jesRelativeStatFSR_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatFSR_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeStatFSR_down", float, "Event b-tag SF jesRelativeStatFSR_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatFSR_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeStatEC_up", float, "Event b-tag SF jesRelativeStatEC_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatEC_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeStatEC_down", float, "Event b-tag SF jesRelativeStatEC_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatEC_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeStatHF_up", float, "Event b-tag SF jesRelativeStatHF_up", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatHF_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesRelativeStatHF_down", float, "Event b-tag SF jesRelativeStatHF_down", lambda ev: getattr(ev, "btagWeight_shape_jesRelativeStatHF_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesSinglePionECAL_up", float, "Event b-tag SF jesSinglePionECAL_up", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionECAL_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesSinglePionECAL_down", float, "Event b-tag SF jesSinglePionECAL_down", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionECAL_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesSinglePionHCAL_up", float, "Event b-tag SF jesSinglePionHCAL_up", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionHCAL_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesSinglePionHCAL_down", float, "Event b-tag SF jesSinglePionHCAL_down", lambda ev: getattr(ev, "btagWeight_shape_jesSinglePionHCAL_down")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesTimePtEta_up", float, "Event b-tag SF jesTimePtEta_up", lambda ev: getattr(ev, "btagWeight_shape_jesTimePtEta_up")))
    #bTagSFEvVarsboosted.append(("btagWeightboosted_shape_jesTimePtEta_down", float, "Event b-tag SF jesTimePtEta_down", lambda ev: getattr(ev, "btagWeight_shape_jesTimePtEta_down")))


    #MC-only global variables
    for vtype in [
        ("nMatch_wq",               int,    ""),
        ("nMatch_wq_btag",          int,    ""),
        ("nMatch_tb",               int,    ""),
        ("nMatch_tb_btag",          int,    ""),
        ("nMatch_hb",               int,    ""),
        ("nMatch_hb_btag",          int,    ""),
        ("ttCls",                   int,    "ttbar classification from GenHFHadronMatcher"),
        ("genHiggsDecayMode",       int,    ""),
        ("qgWeight",                float,  ""),

        ("Pileup_nTrueInt",         float,  ""),
        ("Pileup_nPU",              int,  ""),

        ("puWeight",                float,  "pileup weight"),
        ("puWeightUp",              float,    ""),
        ("puWeightDown",            float,    ""),
        
        ("L1PrefireWeight",                float,  "L1Prefiring Weight", lambda ev: ev.L1PrefiringWeight),    
        ("L1PrefireWeight_Up",              float,    "", lambda ev: ev.L1PrefiringWeightUp),    
        ("L1PrefireWeight_Down",            float,    "", lambda ev: ev.L1PrefiringWeightDown),

        ("genWeight",            float,    "Generator weight", lambda ev: ev.input.genWeight),

        #("btagWeight",            float,    "per event btag weight", lambda ev: ev.btagSF),
        #("btagWeightUp",            float,    "", lambda ev: ev.btagSF_up),
        #("btagWeightDown",            float,    "", lambda ev: ev.btagSF_down),

        #("btagWeight_shape",            float,    "per event btag weight (shape)", lambda ev: ev.btagSF_shape),
        #("btagWeight_shapeJESUp",            float,    "", lambda ev: ev.btagSF_shape_up_jes),
        #("btagWeight_shapeJESDown",            float,    "", lambda ev: ev.btagSF_shape_down_jes),
        #("btagWeight_shapeLFUp",            float,    "", lambda ev: ev.btagSF_shape_up_lf),
        #("btagWeight_shapeLFDown",            float,    "", lambda ev: ev.btagSF_shape_down_lf),
        #("btagWeight_shapeHFUp",            float,    "", lambda ev: ev.btagSF_shape_up_hf),
        #("btagWeight_shapeHFDown",            float,    "", lambda ev: ev.btagSF_shape_down_hf),
        #("btagWeight_shapeHFSTATS1Up",            float,    "", lambda ev: ev.btagSF_shape_up_hfstats1),
        #("btagWeight_shapeHFSTATS1Down",            float,    "", lambda ev: ev.btagSF_shape_down_hfstats1),
        #("btagWeight_shapeHFSTATS2Up",            float,    "", lambda ev: ev.btagSF_shape_up_hfstats2),
        #("btagWeight_shapeHFSTATS2Down",            float,    "", lambda ev: ev.btagSF_shape_down_hfstats2),
        #("btagWeight_shapeLFSTATS1Up",            float,    "", lambda ev: ev.btagSF_shape_up_lfstats1),
        #("btagWeight_shapeLFSTATS1Down",            float,    "", lambda ev: ev.btagSF_shape_down_lfstats1),
        #("btagWeight_shapeLFSTATS2Up",            float,    "", lambda ev: ev.btagSF_shape_up_lfstats2),
        #("btagWeight_shapeLFSTATS2Down",            float,    "", lambda ev: ev.btagSF_shape_down_lfstats2),
        #("btagWeight_shapeCFERR1Up",            float,    "", lambda ev: ev.btagSF_shape_up_cferr1),
        #("btagWeight_shapeCFERR1Down",            float,    "", lambda ev: ev.btagSF_shape_down_cferr1),
        #("btagWeight_shapeCFERR2Up",            float,    "", lambda ev: ev.btagSF_shape_up_cferr2),
        #("btagWeight_shapeCFERR2Down",            float,    "", lambda ev: ev.btagSF_shape_down_cferr2),

        #("prob_ttHbb",            float,    "squared matrix element for hypo ttHbb", lambda ev: ev.prob_ttHbb),
        #("prob_ttbb",            float,    "squared matrix element for hypo ttbb", lambda ev: ev.prob_ttbb),
        #("JointLikelihoodRatio",            float,    "joint likelihood ratio", lambda ev: ev.jointlikelihood),

        ("tth_rho_px_gen",  float,  ""),
        ("tth_rho_py_gen",  float,  ""),
        ("tth_rho_px_reco",  float,  ""),
        ("tth_rho_py_reco",  float,  ""),

        ("PSWeight_ISR_Down", float, "ISR Down weight (not avail in all samples)", lambda ev: ev.PSWeight_ISR_Down),
        ("PSWeight_ISR_Up", float, "ISR Up weight (not avail in all samples)", lambda ev: ev.PSWeight_ISR_Up),
        ("PSWeight_FSR_Down", float, "FSR Down weight (not avail in all samples)", lambda ev: ev.PSWeight_FSR_Down),
        ("PSWeight_FSR_Up", float, "FSR Up weight (not avail in all samples)", lambda ev: ev.PSWeight_FSR_Up),

    ]:#+bTagSFEvVars:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=True)]


    if conf.general["boosted"] == True:
        for vtype in [
            ("nMatch_q_htt",            int,    "number of light quarks matched to HEPTopTagger subjets"),
            ("nMatch_b_htt",            int,    "number of b-quarks matched to HEPTopTagger subjets"),
            ("nMatch_b_higgs",          int,    "number of b-quarks matched to HiggsTagger subjets"),

            #Btag weights for HTT subjets
            #("btagWeight_HTTV2Subjets",            float,    "per event btag weight", lambda ev: getattr(ev, "btagSF_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_Up",            float,    "", lambda ev: getattr(ev, "btagSF_up_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_Down",            float,    "", lambda ev: getattr(ev, "btagSF_down_HTTSubjet", -1)),

            #("btagWeight_HTTV2Subjets_shape",            float,    "per event btag weight (shape)", lambda ev: getattr(ev, "btagSF_shape_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeJESUp",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_jes_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeJESDown",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_jes_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeLFUp",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_lf_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeLFDown",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_lf_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeHFUp",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_hf_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeHFDown",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_hf_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeHFSTATS1Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_hfstats1_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeHFSTATS1Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_hfstats1_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeHFSTATS2Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_hfstats2_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeHFSTATS2Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_hfstats2_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeLFSTATS1Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_lfstats1_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeLFSTATS1Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_lfstats1_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeLFSTATS2Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_lfstats2_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeLFSTATS2Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_lfstats2_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeCFERR1Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_cferr1_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeCFERR1Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_cferr1_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeCFERR2Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_cferr2_HTTSubjet", -1)),
            #("btagWeight_HTTV2Subjets_shapeCFERR2Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_cferr2", -1)),

            ###Btag weights for AK8 subjets
            #("btagWeight_AK8Subjets",            float,    "per event btag weight", lambda ev: getattr(ev, "btagSF_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_Up",            float,    "", lambda ev: getattr(ev, "btagSF_up_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_Down",            float,    "", lambda ev: getattr(ev, "btagSF_down_AK8Subjet", -1)),

            #("btagWeight_AK8Subjets_shape",            float,    "per event btag weight (shape)", lambda ev: getattr(ev, "btagSF_shape_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeJESUp",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_jes_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeJESDown",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_jes_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeLFUp",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_lf_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeLFDown",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_lf_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeHFUp",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_hf_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeHFDown",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_hf_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeHFSTATS1Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_hfstats1_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeHFSTATS1Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_hfstats1_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeHFSTATS2Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_hfstats2_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeHFSTATS2Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_hfstats2_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeLFSTATS1Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_lfstats1_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeLFSTATS1Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_lfstats1_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeLFSTATS2Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_lfstats2_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeLFSTATS2Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_lfstats2_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeCFERR1Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_cferr1_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeCFERR1Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_cferr1_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeCFERR2Up",            float,    "", lambda ev: getattr(ev, "btagSF_shape_up_cferr2_AK8Subjet", -1)),
            #("btagWeight_AK8Subjets_shapeCFERR2Down",            float,    "", lambda ev: getattr(ev, "btagSF_shape_down_cferr2", -1)),

        ]:#+bTagSFEvVarsboosted:
            treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=True)]
   
    #for bweight in bweights:
    #    treeProducer.globalVariables += [
    #        makeGlobalVariable((bweight, float, ""), "nominal", mcOnly=True)
    #    ]

    #Variables in both MC and data
    for vtype in [
        ("rho",                     float,  ""),
        ("json",                    int,  ""),
        ("runrange",                int,  "integer index of the run range (A-F)"),
        ("nPVs",                    float,  ""),
    ]:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=False)]
    return treeProducer
