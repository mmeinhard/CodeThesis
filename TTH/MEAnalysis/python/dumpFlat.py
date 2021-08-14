import ROOT
import sys
import numpy as np
from PhysicsTools.HeppyCore.statistics.tree import Tree
import rootpy
import rootpy.root2hdf5
import time
from TTH.MEAnalysis.samples_base import getSitePrefix
import os

class FlattenCommand(object):
    def __init__(self, name, dtype=int):
        self.name = name
        self.dtype = dtype

    def createBranch(self, tree):
        tree.var(self.name, the_type=self.dtype)
    
    def fillValue(self, tree, event):
        pass

class ScalarFlattenCommand(FlattenCommand):
    def __init__(self, name, dtype=int):
        super(ScalarFlattenCommand, self).__init__(name, dtype)

    def fillValue(self, tree, event):
        tree.fill(self.name, getattr(event, self.name))

class VectorFlattenCommand(FlattenCommand):
    def __init__(self, name, max_length, default=0, dtype=int):
        super(VectorFlattenCommand, self).__init__(name, dtype)
        self.max_length = max_length
        self.default = 0
    
    def createBranch(self, tree):
        for ivar in range(self.max_length):
            tree.var("{0}{1}".format(self.name, ivar), the_type=self.dtype)

    def fillValue(self, tree, event):
        vec = getattr(event, self.name)
        for ivar in range(self.max_length):
            tree.fill("{0}{1}".format(self.name, ivar), vec[ivar] if len(vec)>ivar else self.default)

def produce_syst(cmd, systs):
    ret = [cmd]
    for syst in systs:
        for sdir in ["Up", "Down"]:
            ret += [ScalarFlattenCommand(
                cmd.name + "_" + syst + sdir,
                dtype=cmd.dtype
            )]
    return ret
def produce_syst_multi(commands, systs):
    ret = []
    for cmd in commands:
        ret += produce_syst(cmd, systs)
    return ret

if __name__ == "__main__":
    #input file
    file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    tt = ROOT.TChain("tree")
    for fi in file_names:
        tt.AddFile(fi)
    
    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis')
    parser.add_argument(
        '--systematics',
        action="store_true",
        help="Add systematics to output",
    )
    parser.add_argument(
        '--schema',
        action="store",
        help="Type of data being processed",
        choices=["data", "mc"],
        required=True
    )
    args = parser.parse_args(sys.argv[1:])

    if args.systematics:
        systematics = ["Total", "JER"]
    else:
        systematics = []
    max_entries = 0

    max_jets = 3
    branches_to_copy = [
        ScalarFlattenCommand("njets", dtype=int),
        VectorFlattenCommand("jets_pt", max_jets, dtype=float),
        VectorFlattenCommand("jets_eta", max_jets, dtype=float),
        VectorFlattenCommand("jets_phi", max_jets, dtype=float),
        VectorFlattenCommand("jets_btagCSV", max_jets, dtype=float),
        VectorFlattenCommand("jets_btagCMVA", max_jets, dtype=float),
    ] + produce_syst_multi([
        ScalarFlattenCommand("numJets", dtype=int),
        ScalarFlattenCommand("nBCSVM", dtype=int),
        ],
    systematics)
    if args.schema == "mc":
        branches_to_copy += [
            VectorFlattenCommand("jets_corr", max_jets, dtype=float),
            VectorFlattenCommand("jets_corr_TotalUp", max_jets, dtype=float),
            VectorFlattenCommand("jets_corr_TotalDown", max_jets, dtype=float),
            VectorFlattenCommand("jets_corr_JER", max_jets, dtype=float),
            VectorFlattenCommand("jets_corr_JERUp", max_jets, dtype=float),
            VectorFlattenCommand("jets_corr_JERDown", max_jets, dtype=float),
        ]

    #Create the root file
    outfile = ROOT.TFile("out.root", "RECREATE")
    outfile.cd()
    tree = Tree('tree', 'Flat tree')
    for br in branches_to_copy:
        br.createBranch(tree)
    
    tprev = time.time()
    print("Looping over {0} entries".format(tt.GetEntries()))
    for iEvent, event in enumerate(tt):
        
        if max_entries>0 and iEvent >= max_entries:
            break
        
        for br in branches_to_copy:
            br.fillValue(tree, event) 
        tree.tree.Fill()
        if iEvent%1000 == 0:
            dt = time.time() - tprev
            print("event={0}, dt={1:.2f} {2:.4f}".format(iEvent, dt, float(iEvent)/float(tt.GetEntries())))
            tprev = time.time()

    outfile.Write()
    outfile.Close()
    
    #Convert the root file to HDF5
    print("converting to HDF5")
    rootpy.root2hdf5.root2hdf5("out.root", "out.h5")
