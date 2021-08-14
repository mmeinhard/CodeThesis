import logging
import numpy as np

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import *

LOG_MODULE_NAME = logging.getLogger(__name__)

class BtagWeightAnalyzer(FilterAnalyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BtagWeightAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.boosted = self.cfg_ana.boosted
        SFFile = cfg_ana._conf.general["BTagSFFile"]
        ROOT.gSystem.Load('libCondFormatsBTauObjects') 
        ROOT.gSystem.Load('libCondToolsBTau')

        self.bTagSyst = cfg_ana._conf.general["BTagSystematics"]
        LOG_MODULE_NAME.debug("B-tag systematics: %s",self.bTagSyst)
        self.bTagSyst_bFlav = cfg_ana._conf.general["BTagSystematics_bFlav"]
        LOG_MODULE_NAME.debug("B -- B-tag systematics: %s",self.bTagSyst_bFlav)
        self.bTagSyst_cFlav = cfg_ana._conf.general["BTagSystematics_cFlav"]
        LOG_MODULE_NAME.debug("C -- B-tag systematics: %s",self.bTagSyst_cFlav )
        self.bTagSyst_udsgFlav = cfg_ana._conf.general["BTagSystematics_udsgFlav"]
        LOG_MODULE_NAME.debug("UDSG -- B-tag systematics: %s",self.bTagSyst_udsgFlav)

        
        self.v_sys = getattr(ROOT, 'vector<string>')()
        for syst in self.bTagSyst:
            self.v_sys.push_back('up_'+syst)
            self.v_sys.push_back('down_'+syst)
        LOG_MODULE_NAME.info("Loading b-tag systematics from %s",SFFile)
        self.calib = ROOT.BTagCalibration('deepcsv', SFFile)
        self.reader = ROOT.BTagCalibrationReader(3, "central", self.v_sys)

        self.reader.load(self.calib, 0, "iterativefit")# 0: BTagEntry::FLAV_B
        self.reader.load(self.calib, 1, "iterativefit")# 1: BTagEntry::FLAV_C
        self.reader.load(self.calib, 2, "iterativefit")# 2: BTagEntry::FLAV_UDSG

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)
        
    def process(self, event):

        if self.boosted == False:
            jets = event.systResults["nominal"].good_jets
        elif self.boosted == True and event.systResults["nominal"].passes_subjet:
            bla = event.systResults["nominal"].htt_subjets_b + event.systResults["nominal"].htt_subjets_W
            jets = event.systResults["nominal"].boosted_bjets + event.systResults["nominal"].boosted_ljets
        elif self.boosted == True and event.systResults["nominal"].passes_subjet == False:
            return False

        if self.cfg_comp.isMC:

            
            for syst in ["central"] + self.bTagSyst:
                for sdir in ["up", "down"]:
                    if syst == "central" and sdir == "up":
                        thisSyst = "central"
                    elif syst == "central" and sdir == "down":
                        continue
                    else:
                        thisSyst = sdir+"_"+syst

                    if self.boosted == False:
                        varName = "btagSF_shape"
                    elif self.boosted == True:
                        varName = "btagSFboosted_shape"
                    if syst != "central":
                        varName = varName+"_"+syst+"_"+sdir

                    if self.boosted == False:
                        varNameEv = "btagWeight_shape"
                    elif self.boosted == True:
                        varNameEv = "btagWeightboosted_shape"
                    if syst != "central":
                        varNameEv = varNameEv+"_"+syst+"_"+sdir
                        
                    evCorrection = 1.0
                    for iJet, jet in enumerate(jets):
                        jetSyst = thisSyst
                        if jet.hadronFlavour == 0:
                            if not (jetSyst in self.bTagSyst_udsgFlav or "jes" in jetSyst):
                                jetSyst = "central"
                            BTagEntry = 2
                        elif jet.hadronFlavour == 5:
                            if not (jetSyst in self.bTagSyst_bFlav or "jes" in jetSyst):
                                jetSyst = "central"
                            BTagEntry = 0
                        elif jet.hadronFlavour == 4:
                            if not (jetSyst in self.bTagSyst_cFlav):
                                jetSyst = "central"
                            BTagEntry = 1
                        else:
                            LOG_MODULE_NAME.error("Found a jet with invalid Flavour")
                            raise RuntimeError
                        #print "Jet",iJet,"flav:",jet.hadronFlavour,"("+str(BTagEntry)+")"+"|eta|",abs(jet.eta),"pt",jet.pt,"DeepCSV",jet.btagDeepCSV,
                        if self.boosted == False:
                            thisJetCorr = self.reader.eval_auto_bounds(jetSyst, BTagEntry, abs(jet.eta), jet.pt, jet.btagDeepCSV)
                        elif self.boosted == True: #btag is DeepCSV for subjets
                            thisJetCorr = self.reader.eval_auto_bounds(jetSyst, BTagEntry, abs(jet.eta), jet.pt, jet.btag)
                        #print "corr",thisJetCorr,"(",jetSyst,")"
                        setattr(jet, varName, thisJetCorr)
                        evCorrection *= thisJetCorr
                        
                    setattr(event, varNameEv, evCorrection)
                    LOG_MODULE_NAME.debug("Set %s to %s",varNameEv, evCorrection)

        return True