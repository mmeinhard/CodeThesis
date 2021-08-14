#!/bin/bash
export DATASETPATH="Feb6_leptonic_nome__TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"
export FILE_NAMES="/store/user/jpata/tth/Feb6_leptonic_nome/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Feb6_leptonic_nome/170206_161748/0000/tree_43.root /store/user/jpata/tth/Feb6_leptonic_nome/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Feb6_leptonic_nome/170206_161748/0000/tree_430.root /store/user/jpata/tth/Feb6_leptonic_nome/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Feb6_leptonic_nome/170206_161748/0000/tree_431.root /store/user/jpata/tth/Feb6_leptonic_nome/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Feb6_leptonic_nome/170206_161748/0000/tree_432.root"
export MAX_EVENTS=20000
export SKIP_EVENTS=4637
python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py ${CMSSW_BASE}/src/TTH/MEAnalysis/data/default.cfg
