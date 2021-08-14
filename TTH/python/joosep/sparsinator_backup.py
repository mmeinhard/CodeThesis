from __future__ import print_function

import ROOT
ROOT.gSystem.Load("libTTHMEAnalysis")

import math

import os
from collections import OrderedDict
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)
    
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample, TRIGGERPATH_MAP
from TTH.Plotting.Datacards.sparse import add_hdict, save_hdict

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import SystematicProcess, CategoryCut
from TTH.CommonClassifier.db import ClassifierDB

from TTH.MEAnalysis.leptonSF import calc_lepton_SF

#prefetch the C++ classes
CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")

#Need to access this to initialize the library (?)
dummy = ROOT.TTH_MEAnalysis.TreeDescription

#From https://gitlab.cern.ch/jpata/tthbb13/blob/FH_systematics/Plotting/Daniel/Helper.py#L7
#Derived by Silvio in a manual fit to semileptonic differential top pt data: CMS-PAS-TOP-17-002
topPTreweight = lambda x,y: math.exp(0.5*((0.0843616-0.000743051*x)+(0.0843616-0.000743051*y)))
topPTreweightUp = lambda x,y: math.exp(0.5*((0.00160296-0.000411375*x)+(0.00160296-0.000411375*y)))
topPTreweightDown = lambda x,y: math.exp(0.5*((0.16712-0.00107473*x)+(0.16712-0.00107473*y)))

#Create a mapping between a string and the C++ systematic enum defined in EventModel.h
syst_pairs = OrderedDict([
    (x+d, ROOT.TTH_MEAnalysis.Systematic.make_id(
        getattr(ROOT.TTH_MEAnalysis.Systematic, x),
        getattr(ROOT.TTH_MEAnalysis.Systematic, d if d != "" else "None")
    ))
    for x in [
        "CMS_scale_j",
        "CMS_res_j",
        #"CMS_scaleSubTotalPileUp_j",
        "CMS_scaleAbsoluteStat_j",
        "CMS_scaleAbsoluteScale_j",
        #"CMS_scaleAbsoluteFlavMap_j",
        "CMS_scaleAbsoluteMPFBias_j",
        "CMS_scaleFragmentation_j",
        "CMS_scaleSinglePionECAL_j",
        "CMS_scaleSinglePionHCAL_j",
        "CMS_scaleFlavorQCD_j",
        "CMS_scaleTimePtEta_j",
        "CMS_scaleRelativeJEREC1_j",
        "CMS_scaleRelativeJEREC2_j",
        "CMS_scaleRelativeJERHF_j",
        "CMS_scaleRelativePtBB_j",
        "CMS_scaleRelativePtEC1_j",
        "CMS_scaleRelativePtEC2_j",
        "CMS_scaleRelativePtHF_j",
        "CMS_scaleRelativeFSR_j",
        "CMS_scaleRelativeStatFSR_j",
        "CMS_scaleRelativeStatEC_j",
        "CMS_scaleRelativeStatHF_j",
        "CMS_scalePileUpDataMC_j",
        "CMS_scalePileUpPtRef_j",
        "CMS_scalePileUpPtBB_j",
        "CMS_scalePileUpPtEC1_j",
        "CMS_scalePileUpPtEC2_j",
        "CMS_scalePileUpPtHF_j",

        #"CMS_btag_cferr1",
        #"CMS_btag_cferr2",
        #"CMS_btag_hf",
        #"CMS_btag_hfstats1",
        #"CMS_btag_hfstats2",
        #"CMS_btag_lf",
        #"CMS_btag_lfstats1",
        #"CMS_btag_lfstats2",

        #"CMS_btag_jesAbsoluteMPFBias",
        #"CMS_btag_jesAbsoluteStat",
        #"CMS_btag_jesAbsoluteScale",
        #"CMS_btag_jesFlavorQCD",
        #"CMS_btag_jesFragmentation",
        #"CMS_btag_jesPileUpDataMC",
        #"CMS_btag_jesPileUpPtBB",
        #"CMS_btag_jesPileUpPtEC1",
        #"CMS_btag_jesPileUpPtEC2",
        #"CMS_btag_jesPileUpPtHF",
        #"CMS_btag_jesPileUpPtRef",
        #"CMS_btag_jesRelativeBal",
        #"CMS_btag_jesRelativeFSR",
        #"CMS_btag_jesRelativeJEREC1",
        #"CMS_btag_jesRelativeJEREC2",   
        #"CMS_btag_jesRelativeJERHF",
        #"CMS_btag_jesRelativePtBB",
        #"CMS_btag_jesRelativePtEC1",
        #"CMS_btag_jesRelativePtEC2",
        #"CMS_btag_jesRelativePtHF",
        #"CMS_btag_jesRelativeStatFSR",
        #"CMS_btag_jesRelativeStatEC",
        #"CMS_btag_jesRelativeStatHF",
        #"CMS_btag_jesSinglePionECAL",
        #"CMS_btag_jesSinglePionHCAL",
        #"CMS_btag_jesTimePtEta",

        "CMS_ttHbb_PDF",
        "CMS_ttHbb_scaleMuR",
        "CMS_ttHbb_scaleMuF",
        "CMS_ttHbb_FSR",
        "CMS_ttHbb_ISR",

        "CMS_ttHbb_scaleME",
        "CMS_pu",
        "gen",

    ]
    for d in ["Up", "Down", ""]
])
syst_pairs["nominal"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.Nominal, ROOT.TTH_MEAnalysis.Systematic.None)
syst_pairs["CMS_btag"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.CMS_btag, ROOT.TTH_MEAnalysis.Systematic.None)

def getNormFactor(sample, thisWeight, direction):
    """
    TEMP This is a ugly workaround for now. Should be replaced with something nicer
    """
    samples = ["ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8", "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8", "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",
               "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8", "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"]
    if sample not in samples:
        print("Not in samples")
        return 1.0

    if thisWeight not in ["CMS_ttHbb_PDF", "CMS_ttHbb_scaleMuF", "CMS_ttHbb_scaleMuR"]:
        print(str(thisWeight)+" Not in uncert")
        return 1.0
    
    if sample == "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Down":
                return 0.97434497243
            elif direction == "Up":
                return 1.04933821577
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.23482672348
            elif direction == "Down":
                return 0.716791546792
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.03007643474
            elif direction == "Down":
                return 0.982795526895
            else:
                return 1.0
    elif sample == "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Up":
                return 1.0
            elif direction == "Down":
                return 1.0
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.0622097077
            elif direction == "Down":
                return 0.940493042843
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.00982040144
            elif direction == "Down":
                return 0.965440040689
            else:
                return 1.0
    elif sample == "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Down":
                return 0.972586489542
            elif direction == "Up":
                return 1.04782945306
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.11349412706
            elif direction == "Down":
                return 0.906413843014
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.02397759634
            elif direction == "Down":
                return 0.979581153425
            else:
                return 1.0
    elif sample == "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Down":
                return 0.973550415696
            elif direction == "Up":
                return 1.0357922454
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.11805385244
            elif direction == "Down":
                return 0.905492462524
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.02218902158
            elif direction == "Down":
                return 0.978701034364
            else:
                return 1.0
    elif sample == "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Down":
                return 0.97899663691
            elif direction == "Up":
                return 1.03925132037
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.12125645383
            elif direction == "Down":
                return 0.907798694898
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.02547310827
            elif direction == "Down":
                return 0.981605523428
            else:
                return 1.0

def vec_from_list(vec_type, src):
    """
    Creates a std::vector<T> from a python list.
    vec_type (ROOT type): vector datatype, ex: std::vector<double>
    src (iterable): python list
    """
    v = vec_type()
    for item in src:
        v.push_back(item)
    return v

def l4p(pt, eta, phi, m):
    v = ROOT.TLorentzVector()
    v.SetPtEtaPhiM(pt, eta, phi, m)
    return v

def logit(x):
    return np.log(x/(1.0 - x))

def lv_p4s(pt, eta, phi, m, btagCSV=-100):
    ret = ROOT.TLorentzVector()
    ret.SetPtEtaPhiM(pt, eta, phi, m)
    ret.btagCSV = btagCSV
    return ret

def pass_METfilter(event, schema):
    ret = event.passMETFilters
    #ret = ret and event.Flag_goodVertices
    #ret = ret and event.Flag_GlobalTightHalo2016Filter
    #ret = ret and event.Flag_HBHENoiseFilter
    #ret = ret and event.Flag_HBHENoiseIsoFilter
    #ret = ret and event.Flag_EcalDeadCellTriggerPrimitiveFilter
    #if schema == "data":
    #    ret = ret and event.Flag_eeBadScFilter
    return ret

def pass_HLT_sl_mu(event):
    pass_hlt = event.HLT_ttH_SL_mu
    return event.is_sl and pass_hlt and len(event.leps_pdgId)>=1 and int(abs(event.leps_pdgId[0])) == 13

def pass_HLT_sl_el(event):
    pass_hlt = event.HLT_ttH_SL_el
    return event.is_sl and pass_hlt and len(event.leps_pdgId)>=1 and int(abs(event.leps_pdgId[0])) == 11

def pass_HLT_dl_mumu(event):
    pass_hlt = (event.HLT_ttH_DL_mumu) or (not event.HLT_ttH_DL_mumu and event.HLT_ttH_SL_mu)
    st = sum(map(abs, event.leps_pdgId))
    return event.is_dl and pass_hlt and st == 26

def pass_HLT_dl_elmu(event):
    pass_hlt = event.HLT_ttH_DL_elmu
    pass_hlt = pass_hlt or (not event.HLT_ttH_DL_elmu and (event.HLT_ttH_SL_el and not event.HLT_ttH_SL_mu))
    pass_hlt = pass_hlt or (not event.HLT_ttH_DL_elmu and (event.HLT_ttH_SL_mu and not event.HLT_ttH_SL_el))
    st = sum(map(abs, event.leps_pdgId))
    return event.is_dl and pass_hlt and st == 24

def pass_HLT_dl_elel(event):
    pass_hlt = event.HLT_ttH_DL_elel or (not event.HLT_ttH_DL_elel and event.HLT_ttH_SL_el)
    st = sum(map(abs, event.leps_pdgId))
    return event.is_dl and pass_hlt and st == 22

def pass_HLT_fh(event):
    pass_hlt = event.HLT_ttH_FH
    return event.is_fh and pass_hlt ## FIXME add: st == ??

def triggerPath(event):
    if event.is_sl and pass_HLT_sl_mu(event):
        return TRIGGERPATH_MAP["m"]
    elif event.is_sl and pass_HLT_sl_el(event):
        return TRIGGERPATH_MAP["e"]
    elif event.is_dl and pass_HLT_dl_mumu(event):
        return TRIGGERPATH_MAP["mm"]
    elif event.is_dl and pass_HLT_dl_elmu(event):
        return TRIGGERPATH_MAP["em"]
    elif event.is_dl and pass_HLT_dl_elel(event):
        return TRIGGERPATH_MAP["ee"]
    return 0

def fillBase(matched_processes, event, syst, schema):
    for proc in matched_processes:
        for (k, histo_out) in proc.outdict_syst.get(syst, {}).items():
            dooverflow = True
            if "_topCandidate" in k or "_higgsCandidate" in k:
                dooverflow = False
            weight = 1.0 
            if schema == "mc" or schema == "mc_syst":
                weight = event.weight_nominal * proc.xs_weight
                if weight <= 0:
                    LOG_MODULE_NAME.debug("negative weight, weight_nominal<=0: gen={0}".format(event.weights.at(syst_pairs["gen"])))
            if histo_out.cut(event):
                histo_out.fill(event, weight, dooverflow)


def fillSystematic(matched_processes, event, systematic_weights, schema):
    #pre-compute the event weights 
    precomputed_weights = [
        (syst_weight, weightfunc(event))
        for (syst_weight, weightfunc) in systematic_weights
    ]

    for (syst_weight, _weight) in precomputed_weights:
        for proc in matched_processes:
            for (k, histo_out) in proc.outdict_syst[syst_weight].items():
                weight = _weight * proc.xs_weight
                if histo_out.cut(event):
                    histo_out.fill(event, weight)

def applyCuts(event, matched_processes):
    #check if this event falls into any category
    any_passes = False
    if not hasattr(event, "cuts"):
        event.cuts = {}
    for proc in matched_processes:
        check_proc = CategoryCut(proc.cuts).cut(event)
        if not check_proc:
            continue
        for cut_name, cut in proc.outdict_cuts.items():
            cut_result = cut.cut(event)
            any_passes = any_passes or cut_result
            event.cuts[cut_name] = cut_result
    return any_passes

class FakeJet:
    def __init__(self, pt, eta, hadronFlavour, csv):
        self._pt = pt
        self._eta = eta
        self._hadronFlavour = hadronFlavour
        self._csv = csv

    def pt(self):
        return self._pt
    
    def eta(self):
        return self._eta
    
    def hadronFlavour(self):
        return self._hadronFlavour
    
    def btag(self, algo):
        return self._csv

 
def createEvent(
    events, syst, schema,
    matched_processes,
    cls_bdt_sl, cls_bdt_dl,
    calculate_bdt,
    sample
    ):
    """
    Creates an event with a specified systematic.
    """
    

    event = events.create_event(syst_pairs[syst])
    if schema.startswith("mc"): 
        event.topPTweight = 1.0
        event.topPTweightUp = 1.0
        event.topPTweightDown = 1.0
        if event.is_sl and event.genTopLep_pt>0 and event.genTopHad_pt>0:
            event.topPTweight = topPTreweight(event.genTopLep_pt, event.genTopHad_pt)
            event.topPTweightUp = topPTreweightUp(event.genTopLep_pt, event.genTopHad_pt)
            event.topPTweightDown = topPTreweightDown(event.genTopLep_pt, event.genTopHad_pt)
    event.leps_pdgId = [x.pdgId for x in event.leptons]
    
    event.triggerPath = triggerPath(event)

    event.btag_LR_4b_2b_btagCSV_logit = logit(event.btag_LR_4b_2b_btagCSV)
    any_passes = applyCuts(event, matched_processes)
   
    #workaround for passall=False systematic migrations
    if any_passes and len(event.jets) == 0:
        LOG_MODULE_NAME.info("Event {0}:{1}:{2} has 0 reconstructed jets, likely a weird systematic migration".format(event.run, event.lumi, event.evt))
        return None
  
    if not any_passes:
        return None
   
    #scaleME should be used only for some samples
    if not "scaleME" in sample.tags:
        event.weights[syst_pairs["CMS_ttHbb_scaleMEDown"]] = 1.0
        event.weights[syst_pairs["CMS_ttHbb_scaleMEUp"]] = 1.0
    else:
        #weight correction factors introduced here so that the scaleME weight would be normalized
        #to 1 in the inclusive phase space.
        #Extracted from the mean of the weight distribution in (is_sl || is_dl) && (numJets>=3 && nBCSVM>=0)
        event.weights[syst_pairs["CMS_ttHbb_scaleMEDown"]] = event.weights[syst_pairs["CMS_ttHbb_scaleMEDown"]]/1.14
        event.weights[syst_pairs["CMS_ttHbb_scaleMEUp"]] = event.weights[syst_pairs["CMS_ttHbb_scaleMEUp"]]/0.87

    event.weight_nominal = 1.0
    if schema == "mc" or schema == "mc_syst":
        event.lepton_weight = 1.0
        event.lepton_weight = calc_lepton_SF(event)
        if syst == "nominal":
            event.lepton_weights_syst = {w: calc_lepton_SF(event, w) for w in [
                "CMS_eff_eUp", "CMS_eff_eDown",
                "CMS_eff_mUp", "CMS_eff_mDown",
                "CMS_effTrigger_eUp", "CMS_effTrigger_eDown",
                "CMS_effTrigger_mUp", "CMS_effTrigger_mDown",
                "CMS_effTrigger_dlUp", "CMS_effTrigger_dlDown",
                #Old ones from 2016 - are combined in 2017 analysis
                #"CMS_effID_eUp", "CMS_effID_eDown",
                #"CMS_effReco_eUp", "CMS_effReco_eDown",
                #"CMS_effID_mUp", "CMS_effID_mDown",
                #"CMS_effIso_mUp", "CMS_effIso_mDown",
                #"CMS_effTracking_mUp", "CMS_effTracking_mDown",
                #"CMS_effTrigger_eeUp", "CMS_effTrigger_eeDown",
                #"CMS_effTrigger_emUp", "CMS_effTrigger_emDown",
                #"CMS_effTrigger_mmUp", "CMS_effTrigger_mmDown",
            ]}

        LOG_MODULE_NAME.debug("pu={0} gen={1} btag={2}".format(
            event.weights.at(syst_pairs["CMS_pu"]),
            event.weights.at(syst_pairs["gen"]),
            event.weights.at(syst_pairs["CMS_ttH_CSV"]))
        )
        event.weight_nominal *= event.weights.at(syst_pairs["CMS_pu"]) * event.weights.at(syst_pairs["gen"]) * event.weights.at(syst_pairs["CMS_btag"])

        #event.weight_nominal *= event.weights.at(syst_pairs["gen"])
   
    ##get MEM from the classifier database
    #ret["common_mem"] = -99
    #if do_classifier_db:
    #    syst_index = int(analysis.config.get(syst, "index"))
    #    db_key = int(event.run), int(event.lumi), int(event.evt), int(syst_index)
    #    if cls_db.data.has_key(db_key):
    #        classifiers = cls_db.get(db_key)
    #        if classifiers.mem_p_sig > 0:
    #            ret["common_mem"] = classifiers.mem_p_sig / (classifiers.mem_p_sig + float(MEM_SF) * classifiers.mem_p_bkg)
    #    else:
    #        ret["common_mem"] = -99
    
    event.common_bdt = 0

    #calculate BDT using the CommonClassifier
    if calculate_bdt:
        if event.is_sl:
            ret_bdt = cls_bdt_sl.GetBDTOutput(
                vec_from_list(CvectorLorentz, [x.lv for x in event.leptons]),
                vec_from_list(CvectorLorentz, [x.lv for x in event.jets]),
                vec_from_list(Cvectordouble, [x.btag for x in event.jets]),
                vec_from_list(CvectorLorentz, [x.lv for x in event.jets + event.loose_jets]),
                vec_from_list(Cvectordouble, [x.btag for x in event.jets + event.loose_jets]),
                l4p(event.met_pt, 0, event.met_phi, 0),
                event.btag_LR_4b_2b_btagCSV
            )
            event.common_bdt = ret_bdt
        elif event.is_dl:
            ret_bdt = cls_bdt_dl.GetBDTOutput(
                vec_from_list(CvectorLorentz, [x.lv for x in event.leptons]),
                vec_from_list(Cvectordouble, [x.charge for x in event.leptons]),
                vec_from_list(CvectorLorentz, [x.lv for x in event.jets]),
                vec_from_list(Cvectordouble, [x.btag for x in event.jets + event.loose_jets]),
                l4p(event.met_pt, 0, event.met_phi, 0),
            )
            event.common_bdt = ret_bdt

    return event

def main(analysis, file_names, sample_name, ofname, skip_events=0, max_events=-1, outfilter=None):
    """Summary
    
    Args:
        analysis (Analysis): The main Analysis object used to configure sparsinator
        file_names (list of string): the PFN of the files to process
        sample_name (string): Name of the current sample
        ofname (string): Name of the file
        skip_events (int, optional): Number of events to skip
        max_events (int, optional): Number of events to process
    
    Returns:
        nothing
    
    Raises:
        Exception: Description
    """

    reCalcBtagSF = analysis.config.getboolean("sparsinator","reCalcBTagSF")
    reCalcBtagSF_type = None
    reCalcBtagSF_file = None

    if reCalcBtagSF:
        reCalcBtagSF_type = analysis.config.get("sparsinator","reCalcBTagSFType")
        reCalcBtagSF_file = analysis.config.get("sparsinator","reCalcBTagSFFile")
        if "$CMSSW_BASE" in reCalcBtagSF_file:
            reCalcBtagSF_file = os.environ["CMSSW_BASE"]+reCalcBtagSF_file.replace("$CMSSW_BASE","")
        LOG_MODULE_NAME.warning("Enables recalculation of b-tagging SF in EventModel")
        LOG_MODULE_NAME.warning("reCalcBTag type: %s", reCalcBtagSF_type)
        LOG_MODULE_NAME.warning("reCalcBTag file: %s", reCalcBtagSF_file)


    #need to import here, not in base, because needs special ROOT libraries
    CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
    Cvectordouble = getattr(ROOT, "std::vector<double>")
    CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")

    # Create pairs of (systematic_name, weight function), which will be used on the
    # nominal event to create reweighted copies of the event. The systematic names
    # here will define the output histograms like
    # ttH/sl/sparse -> nominal event
    # ttH/sl/sparse_CMS_ttH_CSVJESUp -> event with btagWeight with JES up variation
    # ...
    
    systematic_weights = []

    systematics_event = []
    systematics_suffix_list = []

    btag_weights = []

    calculate_bdt = analysis.config.getboolean("sparsinator", "calculate_bdt")
    if calculate_bdt:
        cls_bdt_sl = ROOT.BlrBDTClassifier()
        cls_bdt_dl = ROOT.DLBDTClassifier()
    else:
        cls_bdt_sl = None
        cls_bdt_dl = None

    #Optionally add systematics
    if analysis.config.getboolean("sparsinator", "add_systematics"):
        #Get the list of systematics that modify the event topology
        systematics_event_nosdir = analysis.config.get("systematics", "event").split()
        #map the nice systematics names to a suffix in the ntuple
        for syst_event in systematics_event_nosdir:

            for sdir in ["Up", "Down"]:

                syst_event_sdir = syst_event + sdir
                systematics_event += [syst_event_sdir]
                if analysis.config.has_section(syst_event_sdir):
                    systematics_suffix_list += [(syst_event_sdir, analysis.config.get(syst_event_sdir, "suffix"))]
                else:
                    systematics_suffix_list += [(syst_event_sdir, syst_event_sdir.replace("CMS_scale", "").replace("_j", ""))]

        #systematics with weight
        systematics_weight_nosdir = analysis.config.get("systematics", "weight").split()
        
        ##create b-tagging systematics
        systematics_btag = [s for s in systematics_weight_nosdir if (s.startswith("CMS_btag"))]

        for sdir in ["Up", "Down"]:
           for syst in systematics_btag:
               bweight = "{0}{1}".format(syst, sdir)
               systematic_weights += [
                   (bweight, lambda ev, bweight=bweight, syst_pairs=syst_pairs:
                       ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs[bweight]) * ev.lepton_weight)
               ]
               btag_weights += [bweight]

        systematic_weights += [

                #("CMS_ttH_scaleMEUp", lambda ev, syst_pairs=syst_pairs:
                #    (ev.weights.at(syst_pairs["CMS_pu"]) *
                #    ev.weights.at(syst_pairs["CMS_ttH_CSV"]) *
                #    ev.lepton_weight *
                #    ev.weights.at(syst_pairs["gen"]) *
                #    ev.weights.at(syst_pairs["CMS_ttH_scaleMEUp"]))),
                #("CMS_ttH_scaleMEDown", lambda ev, syst_pairs=syst_pairs:
                #    (ev.weights.at(syst_pairs["CMS_pu"]) *
                #    ev.weights.at(syst_pairs["CMS_ttH_CSV"]) *
                #    ev.lepton_weight *
                #    ev.weights.at(syst_pairs["gen"]) *
                #    ev.weights.at(syst_pairs["CMS_ttH_scaleMEDown"]))
                #),
                ("CMS_ttHbb_PUDown", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_puDown"]) * ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_btag"]) * ev.lepton_weight ),
                ("CMS_ttHbb_PUUp", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_puUp"]) * ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_btag"]) * ev.lepton_weight ),
                #("CMS_topPTUp", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                #("CMS_topPTDown", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                #("unweighted", lambda ev: 1.0),
                #("pu_off", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.weights.at(syst_pairs["gen"]) * ev.lepton_weight),
                #("lep_off", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"])),
                #("btag_off", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) * ev.lepton_weight)
        ]

        systematic_weights += [
            ########################################################################################################################################################
            ("CMS_ttHbb_ISR_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) *
                np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarOther_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) *
                np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) * 
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlus2B_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlusB_2017Up", lambda ev,sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlusBBbar_2017Up", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlusCCbar_2017Up", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_FSR_2017Up", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarOther_2017Up", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlus2B_2017Up", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlusB_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlusBBbar_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlusCCbar_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ###############################################################################################################################################################
            ("CMS_ttHbb_ISR_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarOther_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlus2B_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlusB_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlusBBbar_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlusCCbar_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_FSR_2017Down", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarOther_2017Down", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlus2B_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlusB_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlusBBbar_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlusCCbar_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ###############################################################################################################################################################
            ("CMS_ttHbb_PDF_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFUp"]) *
                getNormFactor(sample_name, "CMS_ttHbb_PDF", "Up"))),
            ("CMS_ttHbb_PDF_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) *
                np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFDown"]) *
                getNormFactor(sample_name, "CMS_ttHbb_PDF", "Down"))),
            #("reversed_PDF_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFUp"]) *
            #    ev.weights.at(syst_pairs["CMS_ttHbb_qgWeight"]) *
            #    getNormFactor(sample_name, "CMS_ttHbb_PDF", "Down"))),
            #("reversed_PDF_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) *
            #    np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFDown"]) *
            #    ev.weights.at(syst_pairs["CMS_ttHbb_qgWeight"]) *
            #    getNormFactor(sample_name, "CMS_ttHbb_PDF", "Up"))),
            ("CMS_ttHbb_scaleMuRUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuRUp"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuR", "Up"))),
            ("CMS_ttHbb_scaleMuRDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) *
                np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuRDown"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuR", "Down"))),
            ("CMS_ttHbb_scaleMuFUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuFUp"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuF", "Up"))),
            ("CMS_ttHbb_scaleMuFDown", lambda ev, sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) *
                np.sign(ev.weights.at(syst_pairs["gen"])) *
                ev.weights.at(syst_pairs["CMS_btag"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuFDown"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuF", "Down"))),           
        ] #Added all systematic weights


        for lep_syst in [
                "CMS_eff_eUp", "CMS_eff_eDown",
                "CMS_eff_mUp", "CMS_eff_mDown",
                "CMS_effTrigger_eUp", "CMS_effTrigger_eDown",
                "CMS_effTrigger_mUp", "CMS_effTrigger_mDown",
                "CMS_effTrigger_dlUp", "CMS_effTrigger_dlDown",
                #"CMS_effID_eUp", "CMS_effID_eDown",
                #"CMS_effReco_eUp", "CMS_effReco_eDown",
                #"CMS_effID_mUp", "CMS_effID_mDown",
                #"CMS_effIso_mUp", "CMS_effIso_mDown",
                #"CMS_effTracking_mUp", "CMS_effTracking_mDown",
                #"CMS_effTrigger_eeUp", "CMS_effTrigger_eeDown",
                #"CMS_effTrigger_emUp", "CMS_effTrigger_emDown",
                #"CMS_effTrigger_mmUp", "CMS_effTrigger_mmDown",
        ]:
            systematic_weights += [
                (lep_syst, lambda ev, syst_pairs=syst_pairs, lep_syst=lep_syst: (
                    ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_btag"]) * ev.lepton_weights_syst[lep_syst]
                ))
            ]

    if len(file_names) == 0:
        raise Exception("No files specified")
    if max_events == 0:
        raise Exception("No events specified")

    sample = analysis.get_sample(sample_name)
    schema = sample.schema
    boosted = sample.boosted
    sample_systematic = False 

    #now we find which processes are matched to have this sample as an input
    #these processes are used to generate histograms
    matched_processes = [p for p in analysis.processes if p.input_name == sample.name]
    #Find the processes for which we have up/down variated samples
    systematics_sample = analysis.config.get("systematics", "sample").split()
    matched_procs_new = []
    for syst_sample in systematics_sample:
        procs_up = analysis.process_lists[analysis.config.get(syst_sample, "process_list_up")]
        procs_down = analysis.process_lists[analysis.config.get(syst_sample, "process_list_down")]
        for matched_proc in matched_processes:
            if matched_proc in procs_up:
                matched_proc_new = SystematicProcess(
                    input_name = matched_proc.input_name,
                    output_name = matched_proc.output_name,
                    cuts = matched_proc.cuts,
                    xs_weight = matched_proc.xs_weight,
                    systematic_name = syst_sample + "Up"
                )
                LOG_MODULE_NAME.info("replacing {0} with {1}".format(matched_proc.full_name, matched_proc_new.full_name))       
                matched_procs_new += [matched_proc_new]
            if matched_proc in procs_down:
                matched_proc_new = SystematicProcess(
                    input_name = matched_proc.input_name,
                    output_name = matched_proc.output_name,
                    cuts = matched_proc.cuts,
                    xs_weight = matched_proc.xs_weight,
                    systematic_name = syst_sample + "Down"
                )
                LOG_MODULE_NAME.info("replacing {0} with {1}".format(matched_proc.full_name, matched_proc_new.full_name))       
                matched_procs_new += [matched_proc_new]
  
    if len(matched_procs_new) > 0:
        if len(matched_procs_new) != len(matched_processes):
            raise Exception("Could not match each process to a systematic replacement!")
        matched_processes = matched_procs_new
        sample_systematic = True

    if len(matched_processes) == 0:
        LOG_MODULE_NAME.error("Could not match any processes to sample, will not generate histograms {0}".format(sample.name))
    for proc in matched_processes:
        LOG_MODULE_NAME.info("process: " + str(proc))
    LOG_MODULE_NAME.info("matched processes: {0}".format(len(matched_processes)))

    do_classifier_db = analysis.config.getboolean("sparsinator", "do_classifier_db")

    if do_classifier_db:
        cls_db = ClassifierDB(filename=sample.classifier_db_path)
    
    #configure systematic scenarios according to MC/Data
    if schema == "mc":
        systematics_event = ["nominal"] + systematics_event
        systematics_weight = [k[0] for k in systematic_weights]
    else:
        systematics_event = ["nominal"]
        systematics_weight = []
    LOG_MODULE_NAME.info("systematics_event: " + str(systematics_event))
    LOG_MODULE_NAME.info("systematics_weight: " + str(systematics_weight))

    all_systematics = systematics_event + systematics_weight
   
    outfile = ROOT.TFile(ofname, "RECREATE")
    outfile.cd()
    
    #pre-create output histograms
    for proc in matched_processes:
        LOG_MODULE_NAME.info("creating outputs for {0}, xsw={1}".format(proc.full_name, proc.xs_weight))
        outdict_syst, outdict_cuts = proc.createOutputs(outfile, analysis, all_systematics, outfilter)
        proc.outdict_syst = outdict_syst
        proc.outdict_cuts = outdict_cuts
    
    nevents = 0

    break_file_loop = False

    tf = None

    #Main loop
    for file_name in file_names:
        if break_file_loop:
            break

        # Check if running on predefined files in configuration and if
        # postprocessing file specified
        file_name_postproc = None
        if sample.file_names_postproc:
            if not (file_name in sample.file_names):
                LOG_MODULE_NAME.error(
                    "Specified postprocessing files, but base input "
                    "file {0} is untracked in configuration, skipping "
                    "use of postprocessing".format(file_name)
                )
            else:
                #fix typo
                fn_base = os.path.basename(file_name).replace("_out.root", "_postproccesing.root")
                fns_postproc = [fn for fn in sample.file_names_postproc if fn_base in fn]
                if len(fns_postproc) != 1:
                    raise Exception("Expected exactly one matching postprocessing file but got {0}".format(fns_postproc))
                file_name_postproc = fns_postproc[0]
                LOG_MODULE_NAME.info("Postprocessing file: {0}".format(file_name_postproc))

        LOG_MODULE_NAME.info("opening {0}".format(file_name))
        tfile = ROOT.TFile.Open(file_name)
        if not tfile:
            raise IOError("Could not open file {0}".format(file_name))
        treemodel = getattr(ROOT.TTH_MEAnalysis, sample.treemodel.split(".")[-1])
        LOG_MODULE_NAME.debug("treemodel {0}".format(treemodel))

        if schema == "mc" or schema == "mc_syst":
            #Create MC-specific event model from tree
            if boosted:
                events = treemodel(
                    tfile,
                    ROOT.TTH_MEAnalysis.SampleDescription(
                        ROOT.TTH_MEAnalysis.SampleDescription.MCBOOSTED
                    )
                )
                if reCalcBtagSF:
                    events.initBCalibration(reCalcBtagSF_file, reCalcBtagSF_type)

            else:
                events = treemodel(
                    tfile,
                    ROOT.TTH_MEAnalysis.SampleDescription(
                        ROOT.TTH_MEAnalysis.SampleDescription.MC
                    )
                )
                if reCalcBtagSF:
                    events.initBCalibration(reCalcBtagSF_file, reCalcBtagSF_type)

        else:
            #Create data-specific event model
            if boosted:
                events = treemodel(
                    tfile,
                    ROOT.TTH_MEAnalysis.SampleDescription(
                        ROOT.TTH_MEAnalysis.SampleDescription.DATABOOSTED
                    )
                )
            else:
                events = treemodel(
                    tfile,
                    ROOT.TTH_MEAnalysis.SampleDescription(
                        ROOT.TTH_MEAnalysis.SampleDescription.DATA
                    )
                )

        tfile_postproc = None
        ttree_postproc = None
        if file_name_postproc:
            LOG_MODULE_NAME.info("opening postprocessing file {0}".format(file_name_postproc))
            tfile_postproc = ROOT.TFile.Open(file_name_postproc)
            ttree_postproc = tfile_postproc.Get("Friends")
            if ttree_postproc.GetEntries() != events.reader.GetEntries(True):
                raise Exception("Expected same number of entries in main tree and postprocessed tree")

        LOG_MODULE_NAME.info("looping over {0} events".format(events.reader.GetEntries(True)))
       
        iEv = 0
        
        #Loop over events using the TTreeReader
        while events.reader.Next():
            if ttree_postproc:
                ttree_postproc.GetEntry(iEv)

            nevents += 1
            iEv += 1

            if skip_events > 0 and nevents < skip_events:
                continue

            if max_events > 0:
                if nevents > (skip_events + max_events):
                    LOG_MODULE_NAME.info("event loop: breaking due to MAX_EVENTS: {0} > {1} + {2}".format(
                        nevents, skip_events, max_events
                    ))
                    break_file_loop = True
                    break

            if nevents % 100 == 0:
                LOG_MODULE_NAME.info("processed {0} events".format(nevents))

            #apply some basic preselection that does not depend on jet systematics
            if not (events.is_sl or events.is_dl):
                continue

            #Loop over systematics that transform the event
            for iSyst, syst in enumerate(systematics_event):
                event = createEvent(
                    events, syst, schema,
                    matched_processes,
                    cls_bdt_sl, cls_bdt_dl,
                    calculate_bdt,
                    sample
                )

                print ("passde the loop 22")

                if event is None:
                    continue
                
                if ttree_postproc:
                    LOG_MODULE_NAME.debug("replacing pu weight {0} with postprocessing {1}".format(
                        event.weights[syst_pairs["CMS_pu"]],
                        ttree_postproc.puWeight
                    ))
                    event.weights[syst_pairs["CMS_pu"]] = ttree_postproc.puWeight
                    w = reduce(
                        lambda x,y: x*y,
                        [ttree_postproc.Jet_btagSF_shape[i] for i in range(ttree_postproc.nJet)],
                        1
                    )
                    event.weights[syst_pairs["CMS_btag"]] = w

                #make sure data event is in golden JSON
                #note: nanoAOD data is already pre-selected with the json specified in multicrab_94X.py
                #if schema == "data" and not event.json:
                #    continue
                
                if not pass_METfilter(event, schema):
                    print("Event {0}:{1}:{2} failed MET filter".format(event.run, event.lumi, event.evt))
                    continue

                event.mll = 0.0

                #SL specific MET cut
                if event.is_sl:
                    if event.met_pt <= 20:
                        continue
                #dilepton specific cuts
                elif event.is_dl:
                    mll = (event.leptons.at(0).lv + event.leptons.at(1).lv).M()
                    event.mll = mll
                    #drell-yan
                    if mll < 20:
                        continue
                    #same sign
                    if math.copysign(1, event.leptons.at(0).pdgId * event.leptons.at(1).pdgId) == 1:
                        continue
                    #same flavour
                    if abs(event.leptons.at(0).pdgId) == abs(event.leptons.at(1).pdgId):
                        if event.met_pt <= 40 or abs(mll - 91) < 15:
                            continue

                fillBase(matched_processes, event, syst, schema)
                #Fill the base histogram
                event.bTagWeight = event.weights[syst_pairs["CMS_btag"]] 
               
                #nominal event, fill also histograms with systematic weights
                if syst == "nominal" and schema == "mc" and not sample_systematic:
                    fillSystematic(matched_processes, event, systematic_weights, schema)

            #end of loop over event systematics
        #end of loop over events
        try:
            tfile.Close()
        except Exception as e:
            print(e)
    #end of loop over file names

    outdict = {}
    for proc in matched_processes:
        for (syst, hists_syst) in proc.outdict_syst.items():
            outdict = add_hdict(outdict, {k: v.hist for (k, v) in hists_syst.items()})
   
    #put underflow and overflow entries into the first and last visible bin
    for k in sorted(outdict.keys()):
        v = outdict[k]
        print(k, v.GetEntries(), v.Integral())
        #b0 = v.GetBinContent(0)
        #e0 = v.GetBinError(0)
        #nb = v.GetNbinsX()
        #bn = v.GetBinContent(nb + 1)
        #en = v.GetBinError(nb + 1)

        #v.SetBinContent(0, 0)
        #v.SetBinContent(nb+1, 0)
        #v.SetBinError(0, 0)
        #v.SetBinError(nb+1, 0)

        #v.SetBinContent(1, v.GetBinContent(1) + b0)
        #v.SetBinError(1, math.sqrt(v.GetBinError(1)**2 + e0**2))
        #
        #v.SetBinContent(nb, v.GetBinContent(nb) + bn)
        #v.SetBinError(nb, math.sqrt(v.GetBinError(nb)**2 + en**2))
    
    
    LOG_MODULE_NAME.info("writing output")
    save_hdict(hdict=outdict, outfile=outfile, )
    

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    logging.basicConfig(level=logging.INFO)
    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
        skip_events = int(os.environ.get("SKIP_EVENTS", -1))
        max_events = int(os.environ.get("MAX_EVENTS", -1))
        analysis = analysisFromConfig(os.environ.get("ANALYSIS_CONFIG",))
    elif os.environ.has_key("DATASETPATH"):
        prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
        skip_events = 0
        max_events = 10000
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default.cfg")
        file_names = analysis.get_sample(sample).file_names
    else:
        #sample = "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8"
        sample = "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8"
        #sample = "SingleMuon"
        skip_events = 0
        max_events = 1000
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default_Boosted.cfg")
        file_names = analysis.get_sample(sample).file_names
        file_names = ["/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_9_4_9/CMSSW_9_4_9/src/TTH/MEAnalysis/python/Loop_ttHTobb_test_3/tree.root"]

    outfilter = os.environ.get("OUTFILTER", None)
    main(analysis, file_names, sample, "out.root", skip_events, max_events, outfilter)
