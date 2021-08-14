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
    pass_resolved_string_up = "(numJets >= 4 && nBDeepCSVM >= 2)"

    pass_boosted_string_up = "(boosted == 1 )"


  

  

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
    
    cut_lepton = (cut_sl | cut_dl | cut_boosted_sl | cut_boosted_dl)
    cut_jets = (cut_resolved_up | cut_boosted_up)

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
