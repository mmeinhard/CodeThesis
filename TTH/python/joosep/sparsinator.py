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
from TTH.Plotting.Datacards.MiscClasses import convertBtagSystNames, PUWeightProducer

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import SystematicProcess, CategoryCut
from TTH.CommonClassifier.db import ClassifierDB

from TTH.MEAnalysis.leptonSF import calc_lepton_SF

#prefetch the C++ classes
CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")

#Need to access this to initialize the library (?)
dummy = ROOT.TTH_MEAnalysis.TreeDescription


#Create a mapping between a string and the C++ systematic enum defined in EventModel.h
syst_pairs = OrderedDict([
    (x+d, ROOT.TTH_MEAnalysis.Systematic.make_id(
        getattr(ROOT.TTH_MEAnalysis.Systematic, x),
        getattr(ROOT.TTH_MEAnalysis.Systematic, d if d != "" else "None")
    ))
    for x in [
        "CMS_scale_j",
        "CMS_res_j",

        "CMS_scaleAbsoluteMPFBias_j",
        "CMS_scaleAbsoluteStat_j",
        "CMS_scaleAbsoluteScale_j",
        "CMS_scaleFlavorQCD_j",
        "CMS_scaleFragmentation_j",
        "CMS_scalePileUpDataMC_j",
        "CMS_scalePileUpPtBB_j",
        "CMS_scalePileUpPtEC1_j",
        #"CMS_scalePileUpPtEC2_j",
        #"CMS_scalePileUpPtHF_j",
        "CMS_scalePileUpPtRef_j",
        "CMS_scaleRelativeBal_j",
        "CMS_scaleRelativeFSR_j",
        "CMS_scaleRelativeJEREC1_j",
        #"CMS_scaleRelativeJEREC2_j",    
        #"CMS_scaleRelativeJERHF_j",
        "CMS_scaleRelativePtBB_j",
        "CMS_scaleRelativePtEC1_j",
        #"CMS_scaleRelativePtEC2_j",
        #"CMS_scaleRelativePtHF_j",
        "CMS_scaleRelativeStatFSR_j",
        "CMS_scaleRelativeStatEC_j",
        #"CMS_scaleRelativeStatHF_j",
        "CMS_scaleSinglePionECAL_j",
        "CMS_scaleSinglePionHCAL_j",
        "CMS_scaleTimePtEta_j",
            
        "CMS_btag_cferr1",
        "CMS_btag_cferr2",
        "CMS_btag_hf",
        "CMS_btag_hfstats1",
        "CMS_btag_hfstats2",
        "CMS_btag_lf",
        "CMS_btag_lfstats1",
        "CMS_btag_lfstats2",

        "CMS_btag_boosted_cferr1",
        "CMS_btag_boosted_cferr2",
        "CMS_btag_boosted_hf",
        "CMS_btag_boosted_hfstats1",
        "CMS_btag_boosted_hfstats2",
        "CMS_btag_boosted_lf",
        "CMS_btag_boosted_lfstats1",
        "CMS_btag_boosted_lfstats2",
	
        "CMS_btag_jesAbsoluteMPFBias",
        "CMS_btag_jesAbsoluteStat",
        "CMS_btag_jesAbsoluteScale",
        "CMS_btag_jesFlavorQCD",
        "CMS_btag_jesFragmentation",
        "CMS_btag_jesPileUpDataMC",
        "CMS_btag_jesPileUpPtBB",
        "CMS_btag_jesPileUpPtEC1",
        #"CMS_btag_jesPileUpPtEC2",
        #"CMS_btag_jesPileUpPtHF",
        "CMS_btag_jesPileUpPtRef",
        "CMS_btag_jesRelativeBal",
        "CMS_btag_jesRelativeFSR",
        "CMS_btag_jesRelativeJEREC1",
        #"CMS_btag_jesRelativeJEREC2",   
        #"CMS_btag_jesRelativeJERHF",
        "CMS_btag_jesRelativePtBB",
        "CMS_btag_jesRelativePtEC1",
        #"CMS_btag_jesRelativePtEC2",
        #"CMS_btag_jesRelativePtHF",
        "CMS_btag_jesRelativeStatFSR",
        "CMS_btag_jesRelativeStatEC",
        #"CMS_btag_jesRelativeStatHF",
        "CMS_btag_jesSinglePionECAL",
        "CMS_btag_jesSinglePionHCAL",
        "CMS_btag_jesTimePtEta",

        "CMS_btag_boosted_jesAbsoluteMPFBias",
        "CMS_btag_boosted_jesAbsoluteStat",
        "CMS_btag_boosted_jesAbsoluteScale",
        "CMS_btag_boosted_jesFlavorQCD",
        "CMS_btag_boosted_jesFragmentation",
        "CMS_btag_boosted_jesPileUpDataMC",
        "CMS_btag_boosted_jesPileUpPtBB",
        "CMS_btag_boosted_jesPileUpPtEC1",
        "CMS_btag_boosted_jesPileUpPtRef",
        "CMS_btag_boosted_jesRelativeBal",
        "CMS_btag_boosted_jesRelativeFSR",
        "CMS_btag_boosted_jesRelativeJEREC1",
        "CMS_btag_boosted_jesRelativePtBB",
        "CMS_btag_boosted_jesRelativePtEC1",
        "CMS_btag_boosted_jesRelativeStatFSR",
        "CMS_btag_boosted_jesRelativeStatEC",
        "CMS_btag_boosted_jesSinglePionECAL",
        "CMS_btag_boosted_jesSinglePionHCAL",
        "CMS_btag_boosted_jesTimePtEta",

        "CMS_ttHbb_PDF",
        "CMS_ttHbb_scaleMuR",
        "CMS_ttHbb_scaleMuF",
        "CMS_ttHbb_FSR",
        "CMS_ttHbb_ISR",

        "CMS_ttHbb_scaleME",
        "CMS_pu",
        "CMS_L1Prefiring",
        "gen",


    ]
    for d in ["Up", "Down", ""]
])
syst_pairs["nominal"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.Nominal, ROOT.TTH_MEAnalysis.Systematic.None)
syst_pairs["CMS_btag"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.CMS_btag, ROOT.TTH_MEAnalysis.Systematic.None)
syst_pairs["CMS_btag_boosted"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.CMS_btag_boosted, ROOT.TTH_MEAnalysis.Systematic.None)

#Normalisation for btagging SFs needed for events with large number of jets, see:
#https://hypernews.cern.ch/HyperNews/CMS/get/btag/1582/2.html

bTagNormFile = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/BtaggingPatches.root")

hists = {}
hists["hist_patches_sl_tth"] = bTagNormFile.Get("distr_sl_without_tth")
hists["hist_patches_sl_ttbb"] = bTagNormFile.Get("distr_sl_without_ttbb")
hists["hist_patches_sl_ttcc"] = bTagNormFile.Get("distr_sl_without_ttcc")
hists["hist_patches_sl_ttlight"] = bTagNormFile.Get("distr_sl_without_ttlight")
hists["hist_patches_dl_tth"] = bTagNormFile.Get("distr_dl_without_tth")
hists["hist_patches_dl_ttbb"] = bTagNormFile.Get("distr_dl_without_ttbb")
hists["hist_patches_dl_ttcc"] = bTagNormFile.Get("distr_dl_without_ttcc")
hists["hist_patches_dl_ttlight"] = bTagNormFile.Get("distr_dl_without_ttlight")




def getBoostedSyst(obj, pt, var, sample):
    if obj == "top":
        if var == "Up":
            val = 0.982+0.059
        elif var == "Down":
            val = 0.982-0.059
    elif obj == "higgs":
        if "TTTo" in sample:
            if pt < 350:
                if var == "Up":
                    val = 0.922+0.027
                elif var == "Down":
                    val = 0.922-0.027
            elif pt < 430:
                if var == "Up":
                    val = 0.967+0.057
                elif var == "Down":
                    val = 0.967-0.056
            else:
                if var == "Up":
                    val = 0.902+0.083
                elif var == "Down":
                    val = 0.902-0.081 
        else:
            if pt < 350:
                if var == "Up":
                    val = 0.93+0.04
                elif var == "Down":
                    val = 0.93-0.03 
            else:
                if var == "Up":
                    val = 0.9+0.08 
                elif var == "Down":
                    val = 0.9-0.04 

    return val


def getNormFactor(sample, thisWeight, direction):
    """
    TEMP This is a ugly workaround for now. Should be replaced with something nicer
    """
    samples = ["ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8", "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8", "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",
               "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8", "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"]
    if sample not in samples:
        #print("Not in samples")
        return 1.0

    if thisWeight not in ["CMS_ttHbb_PDF", "CMS_ttHbb_scaleMuF", "CMS_ttHbb_scaleMuR"]:
        print(str(thisWeight)+" Not in uncert")
        return 1.0

    #Using weights derived by KIT. Should be reproducible with:
    # Sum of (nominal weight (=1)) / Sum of (variated weight)
    if sample == "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Down":
                return 0.952142528529
            elif direction == "Up":
                return 1.05290660498
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.22389593243
            elif direction == "Down":
                return 0.708343635374
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.01889904914
            elif direction == "Down":
                return 0.975553045386
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
                return 0.963487965832
            elif direction == "Up":
                return 1.03937416398
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.11033714669
            elif direction == "Down":
                return 0.903494257282
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.01920161897
            elif direction == "Down":
                return 0.976070081989
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
                return 1.11031625998
            elif direction == "Down":
                return 0.903517748772
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.01931803718
            elif direction == "Down":
                return 0.975962412462
            else:
                return 1.0
    elif sample == "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8":
        if thisWeight == "CMS_ttHbb_PDF":
            if direction == "Down":
                return 0.963535841988
            elif direction == "Up":
                return 1.03934150512
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuR":
            if direction == "Up":
                return 1.11039099843
            elif direction == "Down":
                return 0.903431252427
            else:
                return 1.0
        elif thisWeight == "CMS_ttHbb_scaleMuF":
            if direction == "Up":
                return 1.01936686545
            elif direction == "Down":
                return 0.975914225836
            else:
                return 1.0


def calcPatch(ht, njets, category, procs):
    hist = hists["hist_patches_{}_{}".format(category,procs)]
    if ht < 50:
        ht = 51
    if ht > 1500:
        ht = 1499
    b = hist.FindBin(ht, njets)
    w = hist.GetBinContent(b)
    return w



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

def Get_DeltaR_two_objects(obj1, obj2):


    pi = math.pi

    del_phi = abs( obj1.lv.Phi() - obj2.lv.Phi() )
    if del_phi > pi: del_phi = 2*pi - del_phi

    delR = pow( pow(obj1.lv.Eta()-obj2.lv.Eta(),2) + pow(del_phi,2) , 0.5 )

    return delR

def getJESName(systemticName, prefix = "jes"):
    """
    Function for extracting the JES systemtics form the systemtics name
    
    Args:
    -----
    systemticName (str) : Name of a systemtics (the jes name will be extracted from this string)
    prefix (str) : The prefix that is used. Use ["scale", "jes"] (first for event systemics second for b-tag syst)
    """
    parts = systemticName.split("_")
    isJESSyst = False
    indexJESPart = -1
    for ipart, part in enumerate(parts):
        if prefix in part:
            isJESSyst = True
            indexJESPart = ipart
    if not isJESSyst or parts[indexJESPart].replace(prefix, "") == "":
        return None
    else:
        postfix = ""
        if prefix == "scale":
            postfix = "Down" if systemticName.endswith("Down") else "Up"
            #postfix = "Up" if systemticName.endswith("Up") else ""
            
        return parts[indexJESPart].replace(prefix, "")+postfix

def fillBase(matched_processes, event, syst, schema, addSystematics = None):
    for iproc, proc in enumerate(matched_processes):
        iHisto = 0
        for (k, histo_out) in proc.outdict_syst.get(syst, {}).items():
            dooverflow = True
            if "_topCandidate" in k or "_higgsCandidate" in k:
                dooverflow = False
            weight = 1.0 
            if schema == "mc" or schema == "mc_syst":
                useNominalBTagWeight = True
                weight = event.weight_nominal * proc.xs_weight
                #### !!! Adding jes b.tag weights to corresponding systemtics !!! ####
                if addSystematics is not None and syst != "nominal":
                    eventJESSyst = getJESName(syst, "scale")                    
                    if eventJESSyst is not None:
                        if "_sj_" in k:
                            newlist = [m for m in addSystematics if "boosted" in m]
                        else:
                            newlist = [m for m in addSystematics if not "boosted" in m]
                        for addsyst in newlist:
                            JESSysName = getJESName(addsyst)
                            if JESSysName is not None:
                                if JESSysName == eventJESSyst:
                                    if iproc == 0 and iHisto == 0:
                                        LOG_MODULE_NAME.debug("Found matching b-tag systematic %s - Weight %s,%s (nominal %s), %s", syst, addsyst, addSystematics[addsyst](event), event.weights[syst_pairs["CMS_btag"]],k)
                                    weight *= addSystematics[addsyst](event)
                                    useNominalBTagWeight = False
                                    break
                if useNominalBTagWeight:
                    if iproc == 0 and iHisto == 0:
                        LOG_MODULE_NAME.debug("Adding nominal b-tag weights (systematic %s)", syst)
                    if "_sj_" in k:
                        weight *= event.weight_btag_nominal_boosted
                    else:
                        weight *= event.weight_btag_nominal
                if weight <= 0:
                    LOG_MODULE_NAME.debug("negative weight, weight_nominal<=0: gen={0}".format(event.weights.at(syst_pairs["gen"])))
            if schema == "data":
                weight = event.weight_nominal
            if histo_out.cut(event):
                #Boosted SF
                if event.boosted == 1 and "_sj_" in k and not "data" in schema:
                    if len(event.topCandidate) > 0:
                        weight*= 0.982                        
                    if len(event.higgsCandidate) > 0:
                        if event.higgsCandidate.at(0).lv.Pt() < 350:
                            if "TTTo" in sample:
                                weight *= 0.922
                            else:
                                weight *= 0.93
                        elif event.higgsCandidate.at(0).lv.Pt() < 430:
                            if "TTTo" in sample:
                                weight *= 0.967
                            else:
                                weight *= 0.9
                        elif event.higgsCandidate.at(0).lv.Pt() > 430:
                            if "TTTo" in sample:
                                weight *= 0.902
                            else:
                                weight *= 0.9
 

                #print ("histo, event.weight_nominal, proc.xs_weight =", histo_out.cut_name[0], event.weight_nominal, proc.xs_weight) #DS temp
                histo_out.fill(event, weight)
                #print (k, weight, proc.xs_weight)
                #if "sl_j4_t3" in k:
                #print (k, event.evt)
                #histo_out.hist.Draw("")
                #raw_input("")
                #exit()
            iHisto += 1



def fillSystematic(matched_processes, event, systematic_weights, schema):
    #pre-compute the event weights 
    precomputed_weights = [
        (syst_weight, weightfunc(event))
        for (syst_weight, weightfunc) in systematic_weights
    ]

    d = dict(precomputed_weights)

    for (syst_weight, _weight) in precomputed_weights:
        #if "hf" in syst_weight and not "boosted" in syst_weight and event.boosted == 1 :
        #    print (syst_weight, abs(_weight-event.weight_btag_nominal), _weight, event.weight_btag_nominal)
        #if "hf" in syst_weight and  "boosted" in syst_weight and event.boosted == 1 :
        #    print (syst_weight, abs(_weight-event.weight_btag_nominal_boosted), _weight, event.weight_btag_nominal_boosted)
        for proc in matched_processes:
            for (k, histo_out) in proc.outdict_syst[syst_weight].items():
                interweight = _weight
                if event.boosted == 1 and "_sj_" in k and "btag" in syst_weight and not "btag_boosted" in syst_weight:
                    index = syst_weight.find('btag_') + 5
                    boosted_chain =  syst_weight[:index] + 'boosted_' + syst_weight[index:]
                    interweight = d[boosted_chain]
                #Apply boosted weights to non-boosted systematics
                if event.boosted == 1 and "_sj_" in k and not "effHiggs" in k and not "effTop" in k:
                    if len(event.topCandidate) > 0:
                        interweight*= 0.982                        
                    if len(event.higgsCandidate) > 0:
                        if event.higgsCandidate.at(0).lv.Pt() < 350:
                            if "TTTo" in sample:
                                interweight *= 0.922
                            else:
                                interweight *= 0.93
                        elif event.higgsCandidate.at(0).lv.Pt() < 430:
                            if "TTTo" in sample:
                                interweight *= 0.967
                            else:
                                interweight *= 0.9
                        elif event.higgsCandidate.at(0).lv.Pt() > 430:
                            if "TTTo" in sample:
                                interweight *= 0.902
                            else:
                                interweight *= 0.9
                #Apply top boosted weight for HiggsEfficiency
                if event.boosted == 1 and "_sj_" in k and "effHiggs" in k:
                    if len(event.topCandidate) > 0:
                        interweight*= 0.982      
                #Apply higgs boosted weight for TopEfficiency                  
                if event.boosted == 1 and "_sj_" in k and "effTop" in k:                     
                    if len(event.higgsCandidate) > 0:
                        if event.higgsCandidate.at(0).lv.Pt() < 350:
                            if "TTTo" in sample:
                                interweight *= 0.922
                            else:
                                interweight *= 0.93
                        elif event.higgsCandidate.at(0).lv.Pt() < 430:
                            if "TTTo" in sample:
                                interweight *= 0.967
                            else:
                                interweight *= 0.9
                        elif event.higgsCandidate.at(0).lv.Pt() > 430:
                            if "TTTo" in sample:
                                interweight *= 0.902
                            else:
                                interweight *= 0.9
                if event.boosted == 1 and "_sj_" in k and not "_btag" in k:
                    try:
			corrfactor = event.weight_btag_nominal_boosted/event.weight_btag_nominal
                    except:
			corrfactor =  event.weight_btag_nominal_boosted
		    interweight*=corrfactor
                if schema == "data":
                    weight = interweight
                else:
                    weight = interweight * proc.xs_weight
                if histo_out.cut(event):
                    histo_out.fill(event, weight)


def applyCuts(event, matched_processes):
    #check if this event falls into any category
    any_passes = False
    if not hasattr(event, "cuts"):
        event.cuts = {}
    for proc in matched_processes:
        check_proc = CategoryCut(proc.cuts).cut(event)
        #print (proc, check_proc)
        if not check_proc:
            continue
        for cut_name, cut in proc.outdict_cuts.items():
            cut_result = cut.cut(event)
            #print (cut_name, cut_result)
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
    sample, 
    sample_name
    ):
    """
    Creates an event with a specified systematic.
    """
    

    event = events.create_event(syst_pairs[syst.replace("_2017","")])

    #event.evt = event.evt1 * 1000000000 + event.evt2
    try:
        evta = str(int(event.evt))
        evta4last = evta[:-4]
        evtb = str(int(event.evt2))
        evtb4last = evtb[-4:]
        evt = evta4last + evtb4last
        event.event= long(evt) 
    except:
        #evta = event.evt1
        #evtb = event.evt2
        #event.event = evta + evtb
        event.event = 1
        #print ("....", evta, evtb, event.event)
    #print (event.event, evta, evtb, event.evt, event.evt2)

    if event.is_sl:
        event.cats = "sl"
    elif event.is_dl:
        event.cats = "dl"
    else:
        event.cats = None

    if "ttH" in sample_name:
        event.pr = "tth"
    elif "TTTo" in sample_name:
        if event.ttCls >= 51:
            event.pr = "ttbb"
        elif event.ttCls >= 41 and event.ttCls <= 45:
            event.pr = "ttcc"
        elif event.ttCls == 0:
            event.pr = "ttlight"
    else:
        event.pr = "ttlight"

    event.HT = 0
    for jet in event.jets:
        event.HT += jet.lv.Pt()

    #Needed just for quick test

    #mins = []
    #dist = 10
    #for jet in event.jets:
    #    for jet2 in event.jets:
    #        if jet is not jet2:
    #            m = Get_DeltaR_two_objects(jet, jet2)
    #            if m < dist:
    #                dist = m
    #                mins = [jet,jet2]

    #if len(mins) > 1:
    #    J1 = ROOT.TLorentzVector()
    #    J1.SetPtEtaPhiM(mins[0].lv.Pt(), mins[0].lv.Eta(), mins[0].lv.Phi(), mins[0].lv.M())
    #    J2 = ROOT.TLorentzVector()
    #    J2.SetPtEtaPhiM(mins[1].lv.Pt(), mins[1].lv.Eta(), mins[1].lv.Phi(), mins[1].lv.M())
    #    J3 = ROOT.TLorentzVector()
    #    J3 = J1 + J2

    #    event.minpt = J3.Pt()
    #else:
    #    event.minpt = 0

    mins7 = []
    dist7 = 10
    for jet in event.jets:
        for jet2 in event.jets:
            if jet is not jet2:
                m = Get_DeltaR_two_objects(jet, jet2)
                if m < dist7 and jet.btagDeepCSV > 0.4941 and jet2.btagDeepCSV > 0.4941:
                    dist7 = m
                    mins7 = [jet,jet2]

    if len(mins7) > 1:
        J1 = ROOT.TLorentzVector()
        J1.SetPtEtaPhiM(mins7[0].lv.Pt(), mins7[0].lv.Eta(), mins7[0].lv.Phi(), mins7[0].lv.M())
        J2 = ROOT.TLorentzVector()
        J2.SetPtEtaPhiM(mins7[1].lv.Pt(), mins7[1].lv.Eta(), mins7[1].lv.Phi(), mins7[1].lv.M())
        J3 = ROOT.TLorentzVector()
        J3 = J1 + J2

        event.minmass = J3.M()
    else:
        event.minmass = 0



    #sum1 = 0
    #for jet in event.jets:
    #    sum1 += jet.lv.Pt()

    #try:
    #    if len(event.jets) > 0:
    #        event.avgpt = sum1 / (len(event.jets))
    #    else:
    #        event.avgpt = 0
    #except:
    #    event.avgpt = 0

    sum2 = 0
    count2 = 0
    for jet in event.jets:
        if jet.btagDeepCSV > 0.4941:
            sum2 += jet.lv.M()
            count2 += 1

    if count2 > 0:
        event.avgmassbtag = sum2 / count2
    else:
        event.avgmassbtag = 0

    event.weight_mass = 1
    #if event.avgmassbtag > 2.5 and  event.avgmassbtag <= 5:
    #    event.weight_mass = 0.735
    #elif event.avgmassbtag > 5 and  event.avgmassbtag <= 7.5:
    #    event.weight_mass = 0.829
    #elif event.avgmassbtag > 7.5 and  event.avgmassbtag <= 10:
    #    event.weight_mass = 0.974
    #elif event.avgmassbtag > 10 and  event.avgmassbtag <= 12.5:
    #    event.weight_mass = 1.060
    #elif event.avgmassbtag > 12.5 and  event.avgmassbtag <= 15:
    #    event.weight_mass = 1.122
    #elif event.avgmassbtag > 15 and  event.avgmassbtag <= 17.5:
    #    event.weight_mass = 1.167
    #elif event.avgmassbtag > 17.5 and  event.avgmassbtag <= 20:
    #    event.weight_mass = 1.212
    #elif event.avgmassbtag > 20 and  event.avgmassbtag <= 22.5:
    #    event.weight_mass = 1.245
    #elif event.avgmassbtag > 22.5 and  event.avgmassbtag <= 25:
    #    event.weight_mass = 1.205
    #elif event.avgmassbtag > 25 and  event.avgmassbtag <= 27.5:
    #    event.weight_mass = 1.172
    #elif event.avgmassbtag > 27.5 and  event.avgmassbtag <= 30:
    #    event.weight_mass = 1.142
    #elif event.avgmassbtag > 30:
    #    event.weight_mass = 1.091

    #print (event.weight_mass)

    #sum8 = 0
    #count8 = 0
    #for jet in event.jets:
    #    if jet.btagDeepCSV < 0.4941:
    #        sum8 += jet.lv.M()
    #        count8 += 1

    #if count8 > 0:
    #    event.avgmassnonbtag = sum8 / count8 
    #else:
    #    event.avgmassnonbtag = 0

    #sum9 = 0
    #count9 = 0
    #for jet in event.jets:
    #    sum9 += jet.lv.M()
    #    count9 += 1

    #if count9 > 0:
    #    event.avgjetmass = sum9 / count9 
    #else:
    #    event.avgjetmass = 0


    #if event.is_sl:
    #    mins2 = []
    #    dist2 = 10
    #    for jet in event.jets:
    #        m = Get_DeltaR_two_objects(jet, event.leptons.at(0))
    #        if m < dist2:
    #            dist2 = m
    #            mins2 = [jet]

    #    J1 = ROOT.TLorentzVector()
    #    J1.SetPtEtaPhiM(mins[0].lv.Pt(), mins[0].lv.Eta(), mins[0].lv.Phi(), mins[0].lv.M())
    #    J2 = ROOT.TLorentzVector()
    #    J2.SetPtEtaPhiM(event.leptons.at(0).lv.Pt(), event.leptons.at(0).lv.Eta(), event.leptons.at(0).lv.Phi(), event.leptons.at(0).lv.M())
    #    J3 = ROOT.TLorentzVector()
    #    J3 = J1 + J2

    #    event.massjetlep = J3.M()

    sum3 = 0
    for jet in event.jets:
        sum3 += jet.btagDeepCSV

    if len(event.jets) > 0:
        event.avgbtag = sum3 / (len(event.jets))
    else:
        event.avgbtag = 0

    sum4 = 0
    count4 = 0
    for jet in event.jets:
        if jet.btagDeepCSV > 0.4941:
            sum4 += jet.btagDeepCSV
            count4 += 1

    if count4 > 0:
        event.avgbtagbtag = sum4 / count4
    else:
        event.avgbtagbtag = 0


    sum5 = 0
    count5 = 0

    for jet in event.jets:
        for jet2 in event.jets:
            if jet is not jet2:
                m = abs(jet.lv.Eta()-jet2.lv.Eta())
                sum5 += m
                count5 += 1


    if count5 > 0:
        event.avgdeta = sum5 / count5
    else:
        event.avgdeta = 0

    sum6 = 0
    count6 = 0

    for jet in event.jets:
        for jet2 in event.jets:
            if jet is not jet2:
                if jet.btagDeepCSV > 0.4941 and jet2.btagDeepCSV > 0.4941:
                    m = abs(jet.lv.Eta()-jet2.lv.Eta())
                    sum6 += m
                    count6 += 1


    if count6 > 0:
        event.avgdetabtag = sum6 / count6
    else:
        event.avgdetabtag = 0

    #sum5 = 0
    #count5 = 0


    #for jet in event.jets:
    #    for jet2 in event.jets:
    #        if jet is not jet2:
    #            m = Get_DeltaR_two_objects(jet,jet2)
    #            sum5 += m
    #            count5 += 1


    #if count5 > 0:
    #    event.avgdr = sum5 / count5
    #else:
    #    event.avgdr = 0

    #sum6 = 0
    #count6 = 0

    #for jet in event.jets:
    #    for jet2 in event.jets:
    #        if jet is not jet2:
    #            if jet.btagDeepCSV > 0.4941 and jet2.btagDeepCSV > 0.4941:
    #                m = Get_DeltaR_two_objects(jet,jet2)
    #                sum6 += m
    #                count6 += 1


    #if count6 > 0:
    #    event.avgdrbtag = sum6 / count6
    #else:
    #    event.avgdrbtag = 0

    #sum10 = 0
    #count10 = 0
    #for jet in event.jets:
    #    for jet2 in event.jets:
    #        if jet is not jet2:
    #            if jet.btagDeepCSV > 0.4941:
    #                m = Get_DeltaR_two_objects(jet,jet2)
    #                sum10 += m
    #                count10 += 1
#
#
    #if count10 > 0:
    #    event.avgdrbtagjet = sum10 / count10
    #else:
    #    event.avgdrbtagjet = 0
    #
    
    

    #END OF THAT BLOCK



    #print (event.is_sl, event.is_dl, event.is_fh, event.pr, event.cats, event.HT)


    event.leps_pdgId = [x.pdgId for x in event.leptons]
    
    event.triggerPath = triggerPath(event)

    event.btag_LR_4b_2b_btagCSV_logit = logit(event.btag_LR_4b_2b_btagCSV)


    any_passes = applyCuts(event, matched_processes)
   
    #workaround for passall=False systematic migrations
    if any_passes and len(event.jets) == 0:
        LOG_MODULE_NAME.info("Event {0}:{1}:{2} has 0 reconstructed jets, likely a weird systematic migration".format(event.run, event.lumi, event.event))
        return None
  
    if not any_passes:
        return None
    #else:
    #    print (event.evt, event.evt1, event.evt2)
   
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




        #event.weight_nominal *= event.weights.at(syst_pairs["gen"])

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
    LOG_MODULE_NAME.info("Option from config: reCalcBTagSF - %s",reCalcBtagSF)
    doBtagPatches = analysis.config.getboolean("sparsinator","doBTagPatches")
    LOG_MODULE_NAME.info("Option from config: doBtagPatches - %s",doBtagPatches)
    doCRCorr = analysis.config.getboolean("sparsinator","doCRCorr")
    LOG_MODULE_NAME.info("Option from config: doCRCorr - %s",doCRCorr)
    useJESbTagWeights= analysis.config.getboolean("sparsinator","useJESbTagWeights")
    LOG_MODULE_NAME.info("Option from config: useJESbTagWeights - %s",useJESbTagWeights)
    addJESbTagTemples = analysis.config.getboolean("sparsinator","addJESbTagTemples")
    LOG_MODULE_NAME.info("Option from config: addJESbTagTemples - %s",addJESbTagTemples)
    reCalcPUWeight = analysis.config.getboolean("sparsinator","reCalcPUWeight")    
    LOG_MODULE_NAME.info("Option from config: reCalcPUWeight - %s [Era %s]", reCalcPUWeight)
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


    sample = analysis.get_sample(sample_name)



    #Get normalization weights for PDF, muR, muF scale uncertainties - not used at the moment
    #normmuFup = sample.normmuFup
    #normmuFdown = sample.normmuFdown
    #normmuRup = sample.normmuRup
    #normmuRdown = sample.normmuRdown


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
        
        ########################################################################################################################################################
        #### Systematics with weight --> Starting with standalone b-tag systemtics
        systematics_weight_nosdir = analysis.config.get("systematics", "weight").split()
        ##create b-tagging systematics
        if addJESbTagTemples:
            systematics_btag = [s for s in systematics_weight_nosdir if (s.startswith("CMS_btag"))]
        else:
            systematics_btag = [s for s in systematics_weight_nosdir if (s.startswith("CMS_btag") and not "jes" in s)]

        for sdir in ["Up", "Down"]:
            for syst in systematics_btag:
                bweight = "{0}{1}".format(syst, sdir)
                index = bweight.find('btag_') + 5
                bweight_boosted = bweight[:index] + 'boosted_' + bweight[index:]



                systematic_weights += [
                    (bweight, lambda ev, bweight=bweight, syst_pairs=syst_pairs: (ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                                                                                  ev.weights.at(syst_pairs[bweight.replace("_2017","")]) *
                                                                                  calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                                                                                  ev.lepton_weight * event.weights.at(syst_pairs["CMS_L1Prefiring"])))
                ]
                systematic_weights += [
                    (bweight_boosted, lambda ev, bweight=bweight, bweight_boosted=bweight_boosted, syst_pairs=syst_pairs: (ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                                                                                  ev.weights.at(syst_pairs[bweight_boosted.replace("_2017","")]) *
                                                                                  calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                                                                                  ev.lepton_weight * event.weights.at(syst_pairs["CMS_L1Prefiring"])))
                ]
                btag_weights += [bweight]
                btag_weights += [bweight_boosted]

        ########################################################################################################################################################
        #### JES b-tagging systematics have to handled separately --> Apply btag_jes* systematic weight to the histograms taken from the tree with propagated JES
        systematics_btag_jes = [s for s in systematics_weight_nosdir if (s.startswith("CMS_btag") and "jes" in s)]
        btag_jes_systemtics = None
        if useJESbTagWeights:
            btag_jes_systemtics = {}
            for sdir in ["Up", "Down"]:
                for syst in systematics_btag_jes:
                    bweight = "{0}{1}".format(syst, sdir)
                    index = bweight.find('btag_') + 5
                    bweight_boosted = bweight[:index] + 'boosted_' + bweight[index:]


                    btag_jes_systemtics[bweight] = lambda ev, bweight=bweight, syst_pairs=syst_pairs: (ev.weights.at(syst_pairs[bweight]) *
                                                                                                       calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) 
                    )
                    btag_jes_systemtics[bweight_boosted] = lambda ev, bweight=bweight, bweight_boosted=bweight_boosted, syst_pairs=syst_pairs: (ev.weights.at(syst_pairs[bweight_boosted]) *
                                                                                                       calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr)
                    )
                    btag_weights += [bweight]


        systematic_weights += [

            #("CMS_ttHbb_scaleMEUp", lambda ev, syst_pairs=syst_pairs:
            #    (ev.weights.at(syst_pairs["CMS_pu"]) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) *
            #    ev.lepton_weight *
            #    np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_ttHbb_scaleMEUp"]))),
            #("CMS_ttHbb_scaleMEDown", lambda ev, syst_pairs=syst_pairs:
            #    (ev.weights.at(syst_pairs["CMS_pu"]) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) *
            #    ev.lepton_weight *
            #    np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_ttHbb_scaleMEDown"]))
            #),
            ("CMS_ttHbb_L1PreFiringUp", lambda ev, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight*
                ev.weights.at(syst_pairs["CMS_L1PrefiringUp"]))),
            ("CMS_ttHbb_L1PreFiringDown", lambda ev, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight *
                ev.weights.at(syst_pairs["CMS_L1PrefiringDown"]))),
            ("CMS_ttHbb_PUDown", lambda ev, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_puDown"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_L1Prefiring"]))),
            ("CMS_ttHbb_PUUp", lambda ev, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_puUp"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_L1Prefiring"]))),
            #("CMS_topPTUp", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) * ev.weights.at(syst_pairs["CMS_btag"]) * ev.lepton_weight ),
            #("CMS_topPTDown", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) * ev.weights.at(syst_pairs["CMS_btag"]) * ev.lepton_weight ),
            #("unweighted", lambda ev: 1.0),#
            #("btagNorm_off", lambda ev, syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * ev.lepton_weight *
            #    (get_CRCorr(ev, "mc") if doCRCorr else 1.0))),
            #("pu_off", lambda ev, syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    np.sign(ev.weights.at(syst_pairs["gen"])) * ev.lepton_weight *
            #    (get_CRCorr(ev, "mc") if doCRCorr else 1.0))),
            #("lep_off", lambda ev, syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    (get_CRCorr(ev, "mc") if doCRCorr else 1.0))),
            #("btag_off", lambda ev, syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.lepton_weight * (get_CRCorr(ev, "mc") if doCRCorr else 1.0))),
            #("trig_off", lambda ev, syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) * ev.lepton_weight *
            #    (get_CRCorr(ev, "mc") if doCRCorr else 1.0))),
            #("CRCorr_off", lambda ev, syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    ev.lepton_weight)),
        ]

         #Add all the other stupid weights
        systematic_weights += [
            ########################################################################################################################################################
            ("CMS_ttHbb_ISRUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarOtherUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlus2BUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlusBUp", lambda ev,sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlusBBbarUp", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_ISR_ttbarPlusCCbarUp", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRUp"]))),
            ("CMS_ttHbb_FSRUp", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarOtherUp", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlus2BUp", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlusBUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlusBBbarUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ("CMS_ttHbb_FSR_ttbarPlusCCbarUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRUp"]))),
            ###############################################################################################################################################################
            ("CMS_ttHbb_ISRDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarOtherDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlus2BDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlusBDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlusBBbarDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_ISR_ttbarPlusCCbarDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_ISRDown"]))),
            ("CMS_ttHbb_FSRDown", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarOtherDown", lambda ev,sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlus2BDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlusBDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlusBBbarDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ("CMS_ttHbb_FSR_ttbarPlusCCbarDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_FSRDown"]))),
            ###############################################################################################################################################################
            ("CMS_ttHbb_PDFUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFUp"]) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                getNormFactor(sample_name, "CMS_ttHbb_PDF", "Up"))),
            ("CMS_ttHbb_PDFDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFDown"]) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                getNormFactor(sample_name, "CMS_ttHbb_PDF", "Down"))),
            #("reversed_PDF_2017Up", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFUp"]) *
            #    (get_CRCorr(ev, "mc") if doCRCorr else 1.0) *
            #    getNormFactor(sample_name, "CMS_ttHbb_PDF", "Down"))),
            #("reversed_PDF_2017Down", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
            #    ev.weights.at(syst_pairs["CMS_pu"]) * np.sign(ev.weights.at(syst_pairs["gen"])) *
            #    ev.weights.at(syst_pairs["CMS_btag"]) * bTagWeightNorm.getSF(ev.numJets) *
            #    ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_PDFDown"]) *
            #    (get_CRCorr(ev, "mc") if doCRCorr else 1.0) *
            #    getNormFactor(sample_name, "CMS_ttHbb_PDF", "Up"))),
            ("CMS_ttHbb_scaleMuRUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuRUp"]) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuR", "Up"))),
            ("CMS_ttHbb_scaleMuRDown", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuRDown"]) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuR", "Down"))),
            ("CMS_ttHbb_scaleMuFUp", lambda ev, sample_name=sample_name,syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuFUp"]) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuF", "Up"))),
            ("CMS_ttHbb_scaleMuFDown", lambda ev, sample_name=sample_name, syst_pairs=syst_pairs: (
                ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["gen"]) *
                ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) *
                ev.lepton_weight * ev.weights.at(syst_pairs["CMS_ttHbb_scaleMuFDown"]) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) *
                getNormFactor(sample_name, "CMS_ttHbb_scaleMuF", "Down"))),        
            
        ]



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
                    ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr)* 
                    ev.lepton_weights_syst[lep_syst] * event.weights.at(syst_pairs["CMS_L1Prefiring"])
                ))
            ]

        #Boosted uncertainties
        systematic_weights += [
                ("CMS_effTopUp", lambda ev, syst_pairs=syst_pairs, sample_name=sample_name: (
                    ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) * 
                    ev.lepton_weight*(getBoostedSyst("top",0, "Up", sample_name) if len(ev.topCandidate) > 0 else 1.0)
                )),
                ("CMS_effTopDown", lambda ev, syst_pairs=syst_pairs, sample_name=sample_name: (
                    ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) * 
                    ev.lepton_weight*(getBoostedSyst("top",0, "Down", sample_name) if len(ev.topCandidate) > 0 else 1.0)
                )),
                ("CMS_effHiggsUp", lambda ev, syst_pairs=syst_pairs, sample_name=sample_name: (
                    ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) * 
                    ev.lepton_weight*(getBoostedSyst("higgs",ev.higgsCandidate.at(0).lv.Pt(), "Up", sample_name) if len(ev.higgsCandidate) > 0 else 1.0)
                )),
                ("CMS_effHiggsDown", lambda ev, syst_pairs=syst_pairs, sample_name=sample_name: (
                    ev.weights.at(syst_pairs["gen"]) * ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_btag"]) * calcPatch(ev.HT,ev.numJets,ev.cats,ev.pr) * ev.weights.at(syst_pairs["CMS_L1Prefiring"]) * 
                    ev.lepton_weight*(getBoostedSyst("higgs",ev.higgsCandidate.at(0).lv.Pt(), "Down", sample_name) if len(ev.higgsCandidate) > 0 else 1.0)
                )),
            ]


    if len(file_names) == 0:
        raise Exception("No files specified")
    if max_events == 0:
        raise Exception("No events specified")

    #sample = analysis.get_sample(sample_name)
    schema = sample.schema
    boosted = sample.boosted
    sample_systematic = False

    puWeight = None
    if reCalcPUWeight == True and schema == "mc":
        pufile_data = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/pileup_Cert_294927-306462_13TeV_PromptReco_Collisions17_withVar.root" % os.environ['CMSSW_BASE']
        puWeight = PUWeightProducer(file_names, pufile_data)

 

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

    eventnums = []

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


            if nevents % 100 == 0 and schema == "mc":
                LOG_MODULE_NAME.info("processed {0} events".format(nevents))

            if nevents % 10000 == 0 and schema != "mc":
                LOG_MODULE_NAME.info("processed {0} events".format(nevents))

            #apply some basic preselection that does not depend on jet systematics
            if not (events.is_sl or events.is_dl):
                continue

            #Loop over systematics that transform the event
            for iSyst, syst in enumerate(systematics_event):
                event = createEvent(
                    events, syst, schema,
                    matched_processes,
                    sample,
                    sample_name
                )
                
                if event is None:
                    continue


                if puWeight is not None and schema is "mc":
                    thisEventPuWeights = puWeight.getWeight(event.Pileup_nTrueInt)
                    event.weights[syst_pairs["CMS_pu"]], event.weights[syst_pairs["CMS_puUp"]], event.weights[syst_pairs["CMS_puDown"]] =  thisEventPuWeights

                
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


                if schema == "mc" or schema == "mc_syst":
                    event.lepton_weight = 1.0
                    event.lepton_weight = calc_lepton_SF(event) #Lepton_weight also includes trigger weight in SL/DL
                    if syst == "nominal":
                        event.lepton_weights_syst = {w: calc_lepton_SF(event, w) for w in [
                            "CMS_eff_eUp", "CMS_eff_eDown",
                            "CMS_eff_mUp", "CMS_eff_mDown",
                            "CMS_effTrigger_eUp", "CMS_effTrigger_eDown",
                            "CMS_effTrigger_mUp", "CMS_effTrigger_mDown",
                            "CMS_effTrigger_dlUp", "CMS_effTrigger_dlDown",
                        ]}

                        #print (event.lepton_weight, event.lepton_weights_syst)
            

                    #if syst == "nominal":
                    #    print("{0}: pu={1} gen={2}(actual val = {3}) btag={4} btagNorm={5} L1Prefiring={6} leptonweight={7} boosted btag={8}".format(
                    #        syst,
                    #        event.weights.at(syst_pairs["CMS_pu"]),
                    #        np.sign(event.weights.at(syst_pairs["gen"])),
                    #        event.weights.at(syst_pairs["gen"]),
                    #        event.weights.at(syst_pairs["CMS_btag"]),
                    #        bTagNormNom,
                    #        event.weights.at(syst_pairs["CMS_L1Prefiring"]),
                    #        event.lepton_weight,
                    #        event.weights.at(syst_pairs["CMS_btag_boosted"])
                    #        #event.event
                    #        )
                    #    )


                    patch =  calcPatch(event.HT,event.numJets,event.cats,event.pr)
                

                    ######### CAREFUL REMOVE WEIGHT MASS!!!!!!!!
                    event.weight_nominal *= (event.weights.at(syst_pairs["CMS_pu"]) * event.weights.at(syst_pairs["gen"]) * event.lepton_weight *
                                                         event.weights.at(syst_pairs["CMS_L1Prefiring"])) * event.weight_mass

            
            
                    event.weight_btag_nominal = event.weights.at(syst_pairs["CMS_btag"]) * patch
                    #print (event.weight_btag_nominal)

                    event.weight_btag_nominal_boosted = event.weights.at(syst_pairs["CMS_btag_boosted"]) * patch


                #make sure data event is in golden JSON
                #note: nanoAOD data is already pre-selected with the json specified in multicrab_94X.py
                #if schema == "data" and not event.json:
                #    continue
                
                if not pass_METfilter(event, schema):
                    LOG_MODULE_NAME.debug("Event {0}:{1}:{2} failed MET filter".format(event.run, event.lumi, event.event))
                    continue

                event.mll = 0.0

                #print (event.evt)

                if event.passPV == 0:
                    continue

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

                if not event.event in eventnums:
                    eventnums.append(event.event)

                fillBase(matched_processes, event, syst, schema, addSystematics = btag_jes_systemtics)
                #Fill the base histogram
                #event.bTagWeight = event.weights[syst_pairs["CMS_btag"]] 

                #print (event.met_pt)
               
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
    outdict2 = {}
    outdict2["sl_jge4_tge3"] = eventnums
    import json
    #with open('numbers.json', 'w') as fp:
    #    json.dump(outdict2, fp)
    
    for proc in matched_processes:
        for (syst, hists_syst) in proc.outdict_syst.items():
            dictinint = {k:v for k,v in hists_syst.items() if (not (not "_sj_" in k and ("effHiggs" in k or "effTop" in k)))}
            dictinint2 =  {k:v for k,v in dictinint.items() if (not "btag_boosted" in k)}
            dictin =  {k:v for k,v in dictinint2.items() if (not "btag_jes" in k)}
            outdict = add_hdict(outdict, {k: v.hist for (k, v) in dictin.items()})
   
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

    print("running over {}".format(max_events-skip_events))
    
    
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
        max_events = -1
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default_Boosted.cfg")
        file_names = analysis.get_sample(sample).file_names
    else:
        #sample = "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8"
        sample = "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8"
        #sample = "QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8"
        #sample = "WW_TuneCP5_13TeV-pythia8"
        #sample = "TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8"
        #sample = "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8"
        #sample = "SingleMuon"
        #sample = "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8"
        #sample = "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8"
        #sample = "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"
        #skip_events = 764
        skip_events = 0
        max_events = 200
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default_Boosted.cfg")
        #file_names = analysis.get_sample(sample).file_names
        #file_names = ["/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/Plotting/python/tthbbwork/DifferentChecks/out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v1/SingleMuon/data_v1/191125_173644/0000/tree_168.root"]
        file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/withunboostedflag/TTH_Boosted_v3/GC2b974a4ba058/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/job_299_out.root"]
        #file_names = ["/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/python/Loop_ttHTobb_test/tree.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/april16_v1/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/april16_v1/200416_133203/0000/tree_81.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/april16_v1/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/april16_v1/200416_133634/0001/tree_1857.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/withunboostedflag/TTH_Boosted_v3/GC3eef8bd0a488/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/job_13_out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/may15_v1/SingleMuon/may15_v1/200515_162756/0000/tree_340.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v3/GC2a1f5531dfaa/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/job_12_out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v3/GCf8c94f9cb8a3/WW_TuneCP5_13TeV-pythia8/job_1_out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/ttH-v2/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/ttH-v2/191122_171829/0000/tree_83.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v1/GC5dc7ce893526/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/job_329_out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v1/GC6d6f8332dcbc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/job_88_out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v1/GC5dc7ce893526/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/job_20_out.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_37.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_47.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_38.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_33.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_35.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_48.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_34.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_49.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_50.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_51.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_54.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_56.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_57.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_58.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_13.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_15.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_61.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_62.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_64.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_65.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_66.root","root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_69.root"]
        #file_names = ["/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/python/Loop_ttHTobb_test_6/tree.root"]
        #file_names = ["/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/TTH/MEAnalysis/python/Loop_data_test/tree.root"]
        #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_62.root"]
	    #file_names = ["root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_37.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_47.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_38.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_33.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_35.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_48.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_34.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_49.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_50.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_51.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_54.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_56.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_57.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_58.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_13.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_15.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_61.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_62.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_64.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_65.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_66.root", "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/data_v7/SingleMuon/data_v7/191210_122718/0000/tree_69.root"]

    LOG_MODULE_NAME.info("running over {}".format(max_events-skip_events))
    outfilter = os.environ.get("OUTFILTER", None)
    main(analysis, file_names, sample, "out.root", skip_events, max_events, outfilter)

