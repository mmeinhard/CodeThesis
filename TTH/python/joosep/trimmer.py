# -*- coding: utf-8 -*-
"""
@author: christina reissel
"""

import numpy as np
import ROOT as r
import rootpy
from rootpy.tree import Tree, TreeChain
from rootpy.io import root_open
import time
import os

blacklist_files = [
]

# Function to create histograms
def process(file_names, output_file): 

# file_names (list of strings): list of the file names to be opened
# skip_events (int): index of the first event (0-based) to be processed
# max_events (int): number of events to be processed
# variables (list of strings): names of variables from root file that are considered
# output_file (string): name/ path of output file







    for b in blacklist_files:
        if b in files:
            files.remove(b)
    
    files = ' '.join(file_names)
    os.system('hadd -f tree.root ' + files)

    chain = TreeChain("tree", "tree.root")

    # Output file
    output = root_open(output_file, 'recreate')

    # prepare branches
    tree = Tree("tree")

    pass_dl_mumu = "HLT_ttH_DL_mumu || (!HLT_ttH_DL_mumu && HLT_ttH_SL_mu)"
    pass_dl_elmu = "HLT_ttH_DL_elmu || (!HLT_ttH_DL_elmu && (HLT_ttH_SL_el && !HLT_ttH_SL_mu)) || (!HLT_ttH_DL_elmu && (HLT_ttH_SL_mu && !HLT_ttH_SL_el))"
    pass_dl_elel = "HLT_ttH_DL_elel || (!HLT_ttH_DL_elel && HLT_ttH_SL_el)"


    #Also contains nominal
    pass_resolved_string_up = "( (numJets >= 4 && nBDeepCSVM >= 2) || (numJets_AbsoluteMPFBiasUp >= 4 && nBDeepCSVM_AbsoluteMPFBiasUp>= 2) || (numJets_AbsoluteStatUp >= 4 && nBDeepCSVM_AbsoluteStatUp >= 2) || (numJets_AbsoluteScaleUp >= 4 && nBDeepCSVM_AbsoluteScaleUp >= 2) || (numJets_FlavorQCDUp >= 4 && nBDeepCSVM_FlavorQCDUp >= 2) || (numJets_FragmentationUp >= 4 && nBDeepCSVM_FragmentationUp >= 2) || (numJets_PileUpDataMCUp >= 4 && nBDeepCSVM_PileUpDataMCUp >= 2) || (numJets_PileUpPtBBUp >= 4 && nBDeepCSVM_PileUpPtBBUp >= 2) || (numJets_PileUpPtEC1Up >= 4 && nBDeepCSVM_PileUpPtEC1Up >= 2) || (numJets_PileUpPtRefUp >= 4 && nBDeepCSVM_PileUpPtRefUp >= 2) || (numJets_RelativeBalUp >= 4 && nBDeepCSVM_RelativeBalUp >= 2) || (numJets_RelativeFSRUp >= 4 && nBDeepCSVM_RelativeFSRUp >= 2) || (numJets_RelativeJEREC1Up >= 4 && nBDeepCSVM_RelativeJEREC1Up >= 2) || (numJets_RelativePtBBUp >= 4 && nBDeepCSVM_RelativePtBBUp >= 2) || (numJets_RelativePtEC1Up >= 4 && nBDeepCSVM_RelativePtEC1Up >= 2) || (numJets_RelativeStatFSRUp >= 4 && nBDeepCSVM_RelativeStatFSRUp >= 2) || (numJets_RelativeStatECUp >= 4 && nBDeepCSVM_RelativeStatECUp >= 2) || (numJets_SinglePionECALUp >= 4 && nBDeepCSVM_SinglePionECALUp >= 2) || (numJets_SinglePionHCALUp >= 4 && nBDeepCSVM_SinglePionHCALUp >= 2) || (numJets_TimePtEtaUp >= 4 && nBDeepCSVM_TimePtEtaUp >= 2)) "

    pass_boosted_string_up = "(boosted == 1 || boosted_AbsoluteMPFBiasUp  == 1 || boosted_AbsoluteStatUp  == 1 || boosted_AbsoluteScaleUp  == 1 || boosted_FlavorQCDUp  == 1 || boosted_FragmentationUp  == 1 || boosted_PileUpDataMCUp  == 1 || boosted_PileUpPtBBUp  == 1 || boosted_PileUpPtEC1Up  == 1 || boosted_PileUpPtRefUp  == 1 || boosted_RelativeBalUp  == 1 || boosted_RelativeFSRUp  == 1 || boosted_RelativeJEREC1Up  == 1 || boosted_RelativePtBBUp  == 1 || boosted_RelativePtEC1Up  == 1 || boosted_RelativeStatFSRUp  == 1 || boosted_RelativeStatECUp  == 1 || boosted_SinglePionECALUp  == 1 || boosted_SinglePionHCALUp  == 1 || boosted_TimePtEtaUp  == 1)"


    pass_resolved_string_down = "( (numJets_AbsoluteMPFBiasDown >= 4 && nBDeepCSVM_AbsoluteMPFBiasDown>= 2) || (numJets_AbsoluteStatDown >= 4 && nBDeepCSVM_AbsoluteStatDown >= 2) || (numJets_AbsoluteScaleDown >= 4 && nBDeepCSVM_AbsoluteScaleDown >= 2) || (numJets_FlavorQCDDown >= 4 && nBDeepCSVM_FlavorQCDDown >= 2) || (numJets_FragmentationDown >= 4 && nBDeepCSVM_FragmentationDown >= 2) || (numJets_PileUpDataMCDown >= 4 && nBDeepCSVM_PileUpDataMCDown >= 2) || (numJets_PileUpPtBBDown >= 4 && nBDeepCSVM_PileUpPtBBDown >= 2) || (numJets_PileUpPtEC1Down >= 4 && nBDeepCSVM_PileUpPtEC1Down >= 2) || (numJets_PileUpPtRefDown >= 4 && nBDeepCSVM_PileUpPtRefDown >= 2) || (numJets_RelativeBalDown >= 4 && nBDeepCSVM_RelativeBalDown >= 2) || (numJets_RelativeFSRDown >= 4 && nBDeepCSVM_RelativeFSRDown >= 2) || (numJets_RelativeJEREC1Down >= 4 && nBDeepCSVM_RelativeJEREC1Down >= 2) || (numJets_RelativePtBBDown >= 4 && nBDeepCSVM_RelativePtBBDown >= 2) || (numJets_RelativePtEC1Down >= 4 && nBDeepCSVM_RelativePtEC1Down >= 2) || (numJets_RelativeStatFSRDown >= 4 && nBDeepCSVM_RelativeStatFSRDown >= 2) || (numJets_RelativeStatECDown >= 4 && nBDeepCSVM_RelativeStatECDown >= 2) || (numJets_SinglePionECALDown >= 4 && nBDeepCSVM_SinglePionECALDown >= 2) || (numJets_SinglePionHCALDown >= 4 && nBDeepCSVM_SinglePionHCALDown >= 2) || (numJets_TimePtEtaDown >= 4 && nBDeepCSVM_TimePtEtaDown >= 2) ) "

    pass_boosted_string_down = "(boosted_AbsoluteMPFBiasDown  == 1 || boosted_AbsoluteStatDown  == 1 || boosted_AbsoluteScaleDown  == 1 || boosted_FlavorQCDDown  == 1 || boosted_FragmentationDown  == 1 || boosted_PileUpDataMCDown  == 1 || boosted_PileUpPtBBDown  == 1 || boosted_PileUpPtEC1Down  == 1 || boosted_PileUpPtRefDown  == 1 || boosted_RelativeBalDown == 1 || boosted_RelativeFSRDown  == 1 || boosted_RelativeJEREC1Down  == 1 || boosted_RelativePtBBDown  == 1 || boosted_RelativePtEC1Down  == 1 || boosted_RelativeStatFSRDown  == 1 || boosted_RelativeStatECDown  == 1 || boosted_SinglePionECALDown  == 1 || boosted_SinglePionHCALDown  == 1 || boosted_TimePtEtaDown  == 1)"



  

    from rootpy.tree import Cut
    cut_trigger_sl = Cut()
    #cut_sl = Cut( 'is_sl && (HLT_ttH_SL_mu || HLT_ttH_SL_el) && numJets>=4 && nBDeepCSVM>=2')
    cut_sl = Cut( 'is_sl && (HLT_ttH_SL_mu || HLT_ttH_SL_el)')
    #dlstring = "("+pass_dl_mumu+"||"+pass_dl_elmu+"||"+pass_dl_elel+") && is_dl && numJets>=2 && nBDeepCSVM>=1"
    dlstring = "("+pass_dl_mumu+"||"+pass_dl_elmu+"||"+pass_dl_elel+") && is_dl"
    #print dlstring
    #cut_dl = Cut( 'is_dl && numJets>=2 && nBDeepCSVM>=1')
    cut_dl = Cut(dlstring)
    #cut_boosted_sl = Cut('is_sl && (HLT_ttH_SL_mu || HLT_ttH_SL_el) && n_boosted_bjets>=2')
    cut_boosted_sl = Cut('is_sl && (HLT_ttH_SL_mu || HLT_ttH_SL_el)')
    #dlstring_boosted = "("+pass_dl_mumu+"||"+pass_dl_elmu+"||"+pass_dl_elel+") && is_dl && n_boosted_bjets>=2"
    dlstring_boosted = "("+pass_dl_mumu+"||"+pass_dl_elmu+"||"+pass_dl_elel+") && is_dl"
    #cut_boosted_dl = Cut('is_dl && len(boosted_bjets)>=4')
    cut_boosted_dl = Cut(dlstring_boosted)

    cut_resolved_up = Cut(pass_resolved_string_up)
    cut_boosted_up = Cut(pass_boosted_string_up)
    cut_resolved_down = Cut(pass_resolved_string_down)
    cut_boosted_down = Cut(pass_boosted_string_down)

    
    cut_lepton = (cut_sl | cut_dl | cut_boosted_sl | cut_boosted_dl)
    cut_jets = (cut_resolved_up | cut_boosted_up | cut_resolved_down | cut_boosted_down)

    cut = (cut_lepton and cut_jets)

    chain.copy_tree(cut)

    # Save tree
    output.Write("",r.TFile.kOverwrite)	
    output.Close()
    print 'Trimmer sucessfully finished'

    return

##### Main
if __name__ == "__main__":

    ##### Settings

    import os
    if os.environ.get("FILE_NAMES") is not None:
        file_names = os.environ["FILE_NAMES"].split()
    else:
        signal_file_1 = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v3/GCa3f2dae85dfe/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/job_41_out.root"
        signal_file_2 = 'root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/creissel/tth/Mar27/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Mar27/190327_085009/0000/tree_100.root'
        background_file = 'root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Aug02/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/Aug02/190802_081104/0000/tree_34.root '
        file_names = [signal_file_1]

    output_file = 'out.root'

    process(file_names, output_file)
