import ROOT
import logging
import pickle
from copy import deepcopy

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer


LOG_MODULE_NAME = logging.getLogger(__name__)


def convertBtagSystNames(CMSName, direction):
    if CMSName == "CMS_btag_cferr1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_cferr2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_hf":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_hfstats1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_hfstats2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_lf":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_lfstats1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_lfstats2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesAbsoluteMPFBias":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesAbsoluteScale":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesAbsoluteStat":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesFlavorQCD":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesFragmentation":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesPileUpDataMC":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesPileUpPtBB":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesPileUpPtEC1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesPileUpPtEC2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesPileUpPtHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesPileUpPtRef":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeBal":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeFSR":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeJEREC1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeJEREC2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeJERHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativePtBB":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativePtEC1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativePtEC2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativePtHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeStatFSR":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeStatEC":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesRelativeStatHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesSinglePionECAL":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesSinglePionHCAL":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_jesTimePtEta":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_cferr1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_cferr2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_hf":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_hfstats1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_hfstats2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_lf":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_lfstats1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_lfstats2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesAbsoluteMPFBias":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesAbsoluteScale":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesAbsoluteStat":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesFlavorQCD":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesFragmentation":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesPileUpDataMC":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesPileUpPtBB":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesPileUpPtEC1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesPileUpPtEC2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesPileUpPtHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesPileUpPtRef":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeBal":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeFSR":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeJEREC1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeJEREC2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeJERHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativePtBB":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativePtEC1":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativePtEC2":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativePtHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeStatFSR":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeStatEC":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesRelativeStatHF":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesSinglePionECAL":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesSinglePionHCAL":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    elif CMSName == "CMS_btag_boosted_jesTimePtEta":
        return "hWeight_"+direction.lower()+"_"+CMSName.split("CMS_btag_")[1]
    
    else:
        LOG_MODULE_NAME.error("Could not convert CMS btagging systamatics name - %s%s.",CMSName,direction)
        exit()



class BTagNormalization(object):
    def __init__(self, fileName, hname = "hWeight_nom_central"):
        self.hName = hname
        self.fileName = fileName
        if fileName is not None:
            self.rFile= ROOT.TFile(fileName, "READ")
            self.weightHisto = self.rFile.Get(hname)
        
    def getSF(self, nJets):
        if self.fileName is None:
            return 1.0
        thisBin = -1
        SF = -1
        #print self.weightHisto, self.hName
        if nJets <= 12:
            SF = self.weightHisto.GetBinContent(self.weightHisto.FindBin(nJets))
        else:
            LOG_MODULE_NAME.warning("nJets is %s! Will set SF to 1", nJets)
            SF = 1.0

        if SF == -1:
            LOG_MODULE_NAME.warning("SF is -1! Will set it back to 1")

        return SF


class TriggerSFCalculator(object):
    def __init__(self, fileName, histoName = "h3SF_tot_mod"):
        self.rFile = ROOT.TFile(fileName, "READ")
        self.SFHisto = self.rFile.Get(histoName)

    def getSF(self, ht, pt, nBCSVM, sys = 0):
        if sys not in [0, 1, -1]:
           LOG_MODULE_NAME.warning("Sys variable is not in [0, 1, -1]. Setting it to 0")
           sys = 0
        _bin = self.SFHisto.FindBin(ht, pt, nBCSVM)
        SF = self.SFHisto.GetBinContent(_bin)
        SFErr = self.SFHisto.GetBinError(_bin)
        if SF == 0:
            SF = 1
        return SF + (sys * SFErr)
        
class PUWeightProducer:
    """
    Based on NanoAODTools puWeightProducer. Reimplementation on auto method
    """
    def __init__(self, fileList, targetfile, targethist="pileup", name="puWeight", norm=True,verbose=False,nvtx_var="Pileup_nTrueInt",doSysVar=True):
        LOG_MODULE_NAME.debug("Passed file: %s", targetfile)
        self.targeth = self.loadHisto(targetfile,targethist)
        self.targeth_plus = self.loadHisto(targetfile,targethist+"_plus")
        self.targeth_minus = self.loadHisto(targetfile,targethist+"_minus")

    # self.myh=self.targeth.Clone("autoPU")
    # self.myh.Reset()
        
        self.name = name
        self.norm = norm
        self.verbose = verbose
        self.nvtxVar = nvtx_var
        self.doSysVar = True
        self.fixLargeWeights = False
        LOG_MODULE_NAME.info("Calculating MC histo for PU weight - nFiles = %s", len(fileList)) 
        self.myh = self.getFileDist(fileList, self.nvtxVar, self.targeth, "autoPU2")

        ROOT.gSystem.Load("libPhysicsToolsNanoAODTools")
        dummy = ROOT.WeightCalculatorFromHistogram

        
        #Make histograms for getting the weight
        self._worker = ROOT.WeightCalculatorFromHistogram(self.myh,self.targeth,self.norm,self.fixLargeWeights,self.verbose)
        self._worker_plus = ROOT.WeightCalculatorFromHistogram(self.myh,self.targeth_plus,self.norm,self.fixLargeWeights,self.verbose)
        self._worker_minus = ROOT.WeightCalculatorFromHistogram(self.myh,self.targeth_minus,self.norm,self.fixLargeWeights,self.verbose)
        
    def loadHisto(self,filename,hname):
        tf = ROOT.TFile.Open(filename)
        hist = tf.Get(hname)
        hist.SetDirectory(None)
        tf.Close()
        return hist

    @staticmethod
    def getFileDist(files, variable, baseHisto, hName):
        """
        Had problem with TTree:Project. This worked. No Idea why.
        """
        ROOT.gROOT.cd()
        baseHisto = baseHisto.Clone(hName+"Base")
        baseHisto.Reset()
        histos = []
        LOG_MODULE_NAME.info("Projection histo %s from %s files", variable, len(files))
        for iFile,f in enumerate(files):
            _rFile = ROOT.TFile.Open(f)            
            _reHisto = baseHisto.Clone(hName+"_"+str(iFile))
            _rFile.Get("tree").Project(hName+"_"+str(iFile), variable)
            histos.append(deepcopy(_reHisto))

        for i in range(1, len(histos)):
            histos[0].Add(histos[i])

        return deepcopy(histos[0])


    def getWeight(self, nvtx):
        nvtx = int(nvtx)
        weight = self._worker.getWeight(nvtx) if nvtx < self.myh.GetNbinsX() else 1
        weight_plus = self._worker_plus.getWeight(nvtx) if nvtx < self.myh.GetNbinsX() else 1
        weight_minus = self._worker_minus.getWeight(nvtx) if nvtx < self.myh.GetNbinsX() else 1
        return weight, weight_plus, weight_minus
