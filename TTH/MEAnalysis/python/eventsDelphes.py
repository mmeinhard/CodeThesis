# Copyright (C) 2014 Colin Bernet
# https://github.com/cbernet/heppy/blob/master/LICENSE

#from ROOT import TFile
import ROOT

class Events(object):
    '''Event list from a tree in a root file.
    '''
    def __init__(self, filename, treename, options=None):

        """
        self.file = ROOT.TFile(filename[0])

        if self.file.IsZombie():
            raise ValueError('file {fnam} does not exist'.format(fnam=filename))
        self.tree = self.file.Get(treename)
        if self.tree == None: # is None would not work
            raise ValueError('tree {tree} does not exist in file {fnam}'.format(
                tree = treename,
                fnam = filename
                ))
        self.treeReader = ROOT.ExRootTreeReader(self.tree)
        """

        self.files = filename
        self.tree_name = treename
        self.chain = ROOT.TChain(self.tree_name)
        
        # Add all input files, which need to be opened, to the chain
        for f in self.files:
            print ("Adding tree {0}".format(f))
            ret = self.chain.AddFile(f, 0)
            if ret == 0:
                raise IOError("Could not openn file {0}".format(f))
        self.treeReader = ROOT.ExRootTreeReader(self.chain)

        self.Event = self.treeReader.UseBranch("Event")
        self.Particle = self.treeReader.UseBranch("Particle")
        self.Jet = self.treeReader.UseBranch("Jet")
        self.FatJet = self.treeReader.UseBranch("FatJet")
        self.Electron = self.treeReader.UseBranch("Electron")
        self.Muon = self.treeReader.UseBranch("Muon")
        self.MissingET = self.treeReader.UseBranch("MissingET")
        self.ScalarHT = self.treeReader.UseBranch("ScalarHT")

    def size(self):
        return self.treeReader.GetEntries()

    def __getitem__(self, iEv):
        '''navigate to event iEv.'''
        self.treeReader.ReadEntry(iEv)
        return self

    def __iter__(self):
        print "in Delphes event"
        return iter(self.treeReader)

    def __len__(self):
        return int(self.treeReader.GetEntries())

