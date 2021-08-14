import ROOT
import numpy as np

class TriggerSFComputer(object):
    def __init__(self):
        pass

    def getSF(self, leptons_pt, leptons_eta):
        return 0.0

    def clip_pt_eta(self, lep_pt, lep_eta):
        if lep_pt < self.min_pt:
            lep_pt = self.min_pt
        elif lep_pt >= self.max_pt:
            lep_pt = self.max_pt

        if lep_eta < self.min_eta:
            lep_eta = self.min_eta
        elif lep_eta >= self.max_eta:
            lep_eta = self.max_eta
        return lep_pt, lep_eta

class ElectronTriggerSFComputer(TriggerSFComputer):
    def __init__(self, sf_file, histo_name):
        super(ElectronTriggerSFComputer, self).__init__()
        self.tf = ROOT.TFile.Open(sf_file)
        self.histo = self.tf.Get(histo_name)
    

        #use overflow bin for pt out of bounds
        self.min_pt = self.histo.GetXaxis().GetBinLowEdge(1)
        self.max_pt = self.histo.GetXaxis().GetBinLowEdge(self.histo.GetNbinsX() + 1)
        
        self.min_eta = self.histo.GetYaxis().GetBinLowEdge(1)
        self.max_eta = self.histo.GetYaxis().GetBinLowEdge(self.histo.GetNbinsY())
        
        print "ElectronSF {0} pt".format(histo_name), self.min_pt, self.max_pt
        print "ElectronSF {0} eta".format(histo_name), self.min_eta, self.max_eta
    
    def getSF(self, leptons_pt, leptons_eta):
        lep_pt = leptons_pt[0]
        lep_eta = leptons_eta[0]

        lep_pt, lep_eta = self.clip_pt_eta(lep_pt, lep_eta)
       
        ibin = self.histo.FindBin(lep_pt, lep_eta)
        return self.histo.GetBinContent(ibin), self.histo.GetBinError(ibin)


if __name__ == "__main__":
    sf = ElectronTriggerSFComputer("data/TriggerSF_Run2016All_v1.root", "Ele27_WPTight_Gsf")
    
    for pt in np.arange(0, 200, 10):
        print pt, sf.getSF([pt], [2.2])
    
    for eta in np.arange(-3.0, 3.0, 0.2):
        print eta, sf.getSF([40], [eta])
