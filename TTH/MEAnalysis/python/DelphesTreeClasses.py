
class Jet:
    def __init__(self, treeReader, n):
        self.pt = treeReader.Jet.At(n).PT
        self.eta = treeReader.Jet.At(n).Eta
        self.phi = treeReader.Jet.At(n).Phi
        self.mass = treeReader.Jet.At(n).Mass
        self.btag = treeReader.Jet.At(n).BTag
    @staticmethod
    def make_array(input):
        return [Jet(input, i) for i in range(input.Jet.GetEntries())]


class Electron:
    def __init__(self, treeReader, n):
        self.pt = treeReader.Electron.At(n).PT
        self.eta = treeReader.Electron.At(n).Eta
        self.phi = treeReader.Electron.At(n).Phi
        self.charge = treeReader.Electron.At(n).Charge
        self.mass =  0.000510998902
    @staticmethod
    def make_array(input):
        return [Electron(input, i) for i in range(input.Electron.GetEntries())]

 
class Muon:
    def __init__(self, treeReader, n):
        self.pt = treeReader.Muon.At(n).PT
        self.eta = treeReader.Muon.At(n).Eta
        self.phi = treeReader.Muon.At(n).Phi
        self.charge = treeReader.Muon.At(n).Charge
        self.mass = 0.105658389
    @staticmethod
    def make_array(input):
        return [Muon(input, i) for i in range(input.Muon.GetEntries())]


class met:
    def __init__(self, treeReader):
        self.eta = treeReader.MissingET.At(0).Eta
        self.phi = treeReader.MissingET.At(0).Phi
        self.pt = treeReader.MissingET.At(0).MET

class ScalarHT:
    def __init__(self, treeReader):
        self.HT = treeReader.ScalarHT.At(0).HT


class GenParticle:
    def __init__(self, treeReader, n):
        self.pdgId = treeReader.Particle.At(n).PID
        self.pt = treeReader.Particle.At(n).PT
        self.eta = treeReader.Particle.At(n).Eta
        self.phi = treeReader.Particle.At(n).Phi
        self.mass = treeReader.Particle.At(n).Mass
        self.status = treeReader.Particle.At(n).Status
        self.genPartIdxMother = treeReader.Particle.At(n).M1
    @staticmethod
    def make_array(input):
        return [GenParticle(input, i) for i in range(input.Particle.GetEntries())]
       
class FatJet:
    def __init__(self, treeReader, n):
        self.pt = treeReader.FatJet.At(n).PT
        self.eta = treeReader.FatJet.At(n).Eta
        self.phi = treeReader.FatJet.At(n).Phi
        self.mass = treeReader.FatJet.At(n).Mass
        self.Nsub = treeReader.FatJet.At(n).Tau
    @staticmethod
    def make_array(input):
        return [FatJet(input, i) for i in range(input.FatJet.GetEntries())]
 
