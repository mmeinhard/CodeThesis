#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

#print out the environment
env

python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/@me_conf@.cfg
mv $GC_SCRATCH/Loop/tree.root out.root

python ~/jlr/code/flattener.py --infile out.root --intree tree \
    --outfile out_flat.root --outtree tree \
    -f jets:njets:pt,eta,phi,mass,btagDeepCSV:10 \
    -f leps:nleps:pt,eta,phi,mass,pdgId:2 \
    -b met_pt -b met_phi -b met_sumEt \
    -b mem_tth_SL_2w2h2t_p -b mem_ttbb_SL_2w2h2t_p \
    -b mem_tth_SL_1w2h2t_p -b mem_ttbb_SL_1w2h2t_p \
    -b mem_tth_SL_0w2h2t_p -b mem_ttbb_SL_0w2h2t_p \
    -b mem_tth_DL_0w2h2t_p -b mem_ttbb_DL_0w2h2t_p \
    -b prob_ttHbb -b prob_ttbb -b JointLikelihoodRatio \
    -b nMatch_wq -b nMatch_hb -b nMatch_tb \
    -b nBDeepCSVM -b numJets \
    -b jlr_top_pt -b jlr_top_eta -b jlr_top_phi -b jlr_top_mass \
    -b jlr_bottom_pt -b jlr_bottom_eta -b jlr_bottom_phi -b jlr_bottom_mass \
    -b jlr_atop_pt -b jlr_atop_eta -b jlr_atop_phi -b jlr_atop_mass \
    -b jlr_abottom_pt -b jlr_abottom_eta -b jlr_abottom_phi -b jlr_abottom_mass

echo $FILE_NAMES > inputs.txt

