#!/bin/bash

time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GC6dc0a1d23ed9/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8  --prefix TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/ --parallelize multiprocessing --outfile out_1.root
time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GC6dc0a1d23ed9/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8  --prefix TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/ --parallelize multiprocessing --outfile out_2.root
time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GCbdfada609bd5/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8 --prefix ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/ --parallelize multiprocessing --outfile out_3.root
time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GC8c011fd1269b/SingleElectron --prefix SingleElectron/ --parallelize multiprocessing --outfile out_4.root
time python python/reduction.py --files_path /pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/meanalysis/GC8c011fd1269b/SingleMuon --prefix SingleMuon/ --parallelize multiprocessing --outfile out_5.root
