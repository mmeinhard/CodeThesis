import nanoTreeClasses
import nanoTreeGenClasses
import logging

LOG_MODULE_NAME = logging.getLogger(__name__)


from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.errorsPrinted = False
    def process(self, event):
        event.lumi = getattr(event.input, "luminosityBlock", None)
    	event.evt = long(getattr(event.input, "event", None))
        #event.json = getattr(event.input, "json", None)
        #event.json_silver = getattr(event.input, "json_silver", None)

        event.Flag_ele32DoubleL1ToSingleL1 = getattr(event.input, "Flag_ele32DoubleL1ToSingleL1", None)

        event.Electron = nanoTreeClasses.Electron.make_array(event.input, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(event.input, MC = True)

        event.met = nanoTreeClasses.met.make_obj(event.input, MC = True)
        event.Jet = nanoTreeClasses.Jet.make_array(event.input, MC = True)
        event.ttCls = getattr(event.input, "genTtbarId", None)%100
        #event.heavyFlavourCategory = getattr(event.input, "heavyFlavourCategory", None)

        event.PV = nanoTreeClasses.PV.make_array(event.input)
        #event.pileUpVertex_z = pileUpVertex_z.make_array(event.input)        
        event.Pileup_nPU = getattr(event.input, "Pileup_nPU", None)
        event.Pileup_nTrueInt = getattr(event.input, "Pileup_nTrueInt", None)
        event.nPVs = getattr(event.input, "PV_npvs", None)
        #event.bx = getattr(event.input, "bx", None)
        #event.rho = getattr(event.input, "rho", None)

        event.GenJet = nanoTreeGenClasses.GenJet.make_array(event.input)
        #event.genHiggsDecayMode = getattr(event.input, "genHiggsDecayMode", None)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(event.input)
        event.GenLepFromTop = nanoTreeGenClasses.GenLepFromTop.make_array(event.GenParticle)
    	event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
    	event.GenLepFromTau = nanoTreeGenClasses.GenLepFromTau.make_array(event.GenParticle)
    	event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
    	event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
    	event.GenTaus = nanoTreeGenClasses.GenTaus.make_array(event.GenParticle)
    	event.GenLep = nanoTreeGenClasses.GenLep.make_array(event.GenParticle)
    	event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
    	event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
    	event.GenNuFromTop = nanoTreeGenClasses.GenNuFromTop.make_array(event.GenParticle)
    	event.GenNu = nanoTreeGenClasses.GenNu.make_array(event.GenParticle)
    	event.GenNuFromTau = nanoTreeGenClasses.GenNuFromTau.make_array(event.GenParticle)
    	event.GenGluonFromTop = nanoTreeGenClasses.GenGluonFromTop.make_array(event.GenParticle)
    	event.GenGluonFromB = nanoTreeGenClasses.GenGluonFromB.make_array(event.GenParticle)
    	nanoTreeGenClasses.Jet_addmc(event.Jet,event.GenJet)
        

        event.PSWeight_ISR_Down = 1.0
        event.PSWeight_FSR_Down = 1.0 
        event.PSWeight_ISR_Up = 1.0
        event.PSWeight_FSR_Up = 1.0
        
        try: 
            getattr(event.input, "nPSWeight")
        except Exception:
            LOG_MODULE_NAME.debug("No PSWeights")
        else:
            if getattr(event.input, "nPSWeight") == 4:
                event.PSWeight_ISR_Down = getattr(event.input, "PSWeight")[0]
                event.PSWeight_FSR_Down = getattr(event.input, "PSWeight")[1]
                event.PSWeight_ISR_Up = getattr(event.input, "PSWeight")[2]
                event.PSWeight_FSR_Up = getattr(event.input, "PSWeight")[3]
        try:
            getattr(event.input, "nLHEScaleWeight")
        except Exception:
            event.LHEScaleWeights = [nanoTreeClasses.LHEScaleWeight(None, -1, 1.0)]
        else:
            event.LHEScaleWeights = nanoTreeClasses.LHEScaleWeight.make_array(event.input)
        try:
            getattr(event.input, "nLHEPdfWeight")
        except Exception:
            event.LHEPDFWeights = [nanoTreeClasses.LHEPdfWeight(None, -1, 1.0)]
        else:
            event.LHEPDFWeights = nanoTreeClasses.LHEPdfWeight.make_array(event.input)
        try:
            getattr(event.input, "nLHEReweightingWeight")
        except Exception:
            event.LHEReweightingWeights = [nanoTreeClasses.LHEReweightingWeight(None, -1, 1.0)]
        else:
            event.LHEReweightingWeights = nanoTreeClasses.LHEReweightingWeight.make_array(event.input)

            
            
        try:
            getattr(event.input, "LHE_Njets")
        except Exception:
            if not self.errorsPrinted:
                LOG_MODULE_NAME.error("LHE* variables are missing setting all to None")
                self.errorsPrinted = True
            event.LHEScaleWeight = nanoTreeClasses.LHEScaleWeight(event.input, 1, devVal = -1)
            event.LHEPdfWeight = nanoTreeClasses.LHEPdfWeight(event.input, 1, devVal = -1)
            event.LHE_Njets = None
            event.LHE_Nb = None
            event.LHE_Nc = None
            event.LHE_Nglu = None
            event.LHE_Nuds = None
            event.LHE_Vpt = None 
            event.LHE_HT = None
        else:
            event.LHEScaleWeight = nanoTreeClasses.LHEScaleWeight.make_array(event.input)
            event.LHEPdfWeight = nanoTreeClasses.LHEPdfWeight.make_array(event.input)
            event.LHE_Njets = getattr(event.input, "LHE_Njets", None)
            event.LHE_Nb = getattr(event.input, "LHE_Nb", None)
            event.LHE_Nc = getattr(event.input, "LHE_Nc", None)
            event.LHE_Nglu = getattr(event.input, "LHE_Nglu", None)
            event.LHE_Nuds = getattr(event.input, "LHE_Nuds", None)
            event.LHE_Vpt = getattr(event.input, "LHE_Vpt", None)
            event.LHE_HT = getattr(event.input, "LHE_HT", None)

        
        event.puWeight = getattr(event.input, "puWeight", None)
        event.puWeightUp = getattr(event.input, "puWeightUp", None)
        event.puWeightDown = getattr(event.input, "puWeightDown", None)
        event.L1PrefiringWeight = getattr(event.input, "L1PreFiringWeight_Nom", None)
        event.L1PrefiringWeightUp = getattr(event.input, "L1PreFiringWeight_Up", None)
        event.L1PrefiringWeightDown = getattr(event.input, "L1PreFiringWeight_Dn", None)
        #event.L1PrefiringWeight = getattr(event.input, "L1PrefireWeight", None)
        #event.L1PrefiringWeightUp = getattr(event.input, "L1PrefireWeight_Up", None)
        #event.L1PrefiringWeightDown = getattr(event.input, "L1PrefireWeight_Down", None)

        #event.triggerEmulationWeight = getattr(event.input, "triggerEmulationWeight", None)
        #event.btagWeightCSV_down_jesPileUpPtBB = getattr(event.input, "btagWeightCSV_down_jesPileUpPtBB", None)
        #event.btagWeightCSV_down_jesFlavorQCD = getattr(event.input, "btagWeightCSV_down_jesFlavorQCD", None)
        #event.btagWeightCSV_down_jesAbsoluteScale = getattr(event.input, "btagWeightCSV_down_jesAbsoluteScale", None)
        #event.btagWeightCSV_down_jesPileUpPtRef = getattr(event.input, "btagWeightCSV_down_jesPileUpPtRef", None)
        #event.btagWeightCSV_down_jesRelativeFSR = getattr(event.input, "btagWeightCSV_down_jesRelativeFSR", None)
        #event.btagWeightCSV_down_jesTimePtEta = getattr(event.input, "btagWeightCSV_down_jesTimePtEta", None)
        #event.btagWeightCSV_down_hf = getattr(event.input, "btagWeightCSV_down_hf", None)
        #event.btagWeightCSV_down_cferr1 = getattr(event.input, "btagWeightCSV_down_cferr1", None)
        #event.btagWeightCMVAV2_up_hf = getattr(event.input, "btagWeightCMVAV2_up_hf", None)
        #event.btagWeightCMVAV2_down_hfstats2 = getattr(event.input, "btagWeightCMVAV2_down_hfstats2", None)
        #event.btagWeightCSV_down_cferr2 = getattr(event.input, "btagWeightCSV_down_cferr2", None)
        #event.btagWeightCSV_down_jes = getattr(event.input, "btagWeightCSV_down_jes", None)
        #event.btagWeightCSV_down_jesAbsoluteMPFBias = getattr(event.input, "btagWeightCSV_down_jesAbsoluteMPFBias", None)
        #event.btagWeightCSV_down_lf = getattr(event.input, "btagWeightCSV_down_lf", None)
        #event.btagWeightCSV_down_jesPilenanoTreeGenClassesUpPtEC1 = getattr(event.input, "btagWeightCSV_down_jesPileUpPtEC1", None)
        #event.btagWeightCMVAV2_down_hfstats1 = getattr(event.input, "btagWeightCMVAV2_down_hfstats1", None)
        #event.btagWeightCSV_up_lf = getattr(event.input, "btagWeightCSV_up_lf", None)
        #event.btagWeightCMVAV2 = getattr(event.input, "btagWeightCMVAV2", None)
        #event.btagWeightCSV_down_lfstats2 = getattr(event.input, "btagWeightCSV_down_lfstats2", None)
        #event.btagWeightCSV_up_jesPileUpPtRef = getattr(event.input, "btagWeightCSV_up_jesPileUpPtRef", None)
        #event.btagWeightCSV_down_lfstats1 = getattr(event.input, "btagWeightCSV_down_lfstats1", None)
        #evenself.mass = GenParticle[n].masst.btagWeightCSV_up_jesFlavorQCD = getattr(event.input, "btagWeightCSV_up_jesFlavorQCD", None)
        #event.btagWeightCSV_down_jesPileUpDataMC = getattr(event.input, "btagWeightCSV_down_jesPileUpDataMC", None)
        #event.btagWeightCSV_up_lfstats1 = getattr(event.input, "btagWeightCSV_up_lfstats1", None)
        #event.btagWeightCMVAV2_down_lf = getattr(event.input, "btagWeightCMVAV2_down_lf", None)
        #event.btagWeightCSV_up_lfstats2 = getattr(event.input, "btagWeightCSV_up_lfstats2", None)
        #event.btagWeightCSV = getattr(event.input, "btagWeightCSV", None)
        #event.btagWeightCSV_up_cferr2 = getattr(event.input, "btagWeightCSV_up_cferr2", None)
        #event.btagWeightCSV_up_jesAbsoluteMPFBias = getattr(event.input, "btagWeightCSV_up_jesAbsoluteMPFBias", None)
        #event.btagWeightCSV_up_jesSinglePionECAL = getattr(event.input, "btagWeightCSV_up_jesSinglePionECAL", None)
        #event.btagWeightCSV_up_cferr1 = getattr(event.input, "btagWeightCSV_up_cferr1", None)
        #event.btagWeightCSV_up_jesPileUpPtBB = getattr(event.input, "btagWeightCSV_up_jesPileUpPtBB", None)
        #event.btagWeightCMVAV2_down_hf = getattr(event.input, "btagWeightCMVAV2_down_hf", None)
        #event.btagWeightCMVAV2_up_lfstats2 = getattr(event.input, "btagWeightCMVAV2_up_lfstats2", None)
        #event.btagWeightCMVAV2_up_hfstats2 = getattr(event.input, "btagWeightCMVAV2_up_hfstats2", None)
        #event.btagWeightCMVAV2_up_hfstats1 = getattr(event.input, "btagWeightCMVAV2_up_hfstats1", None)
        #event.btagWeightCSV_up_jesAbsoluteScale = getattr(event.input, "btagWeightCSV_up_jesAbsoluteScale", None)
        #event.btagWeightCMVAV2_up_lfstats1 = getattr(event.input, "btagWeightCMVAV2_up_lfstats1", None)
        #event.btagWeightCMVAV2_down_cferr2 = getattr(event.input, "btagWeightCMVAV2_down_cferr2", None)
        #event.btagWeightCSV_up_hf = getattr(event.input, "btagWeightCSV_up_hf", None)
        #event.btagWeightCSV_up_jesPileUpPtEC1 = getattr(event.input, "btagWeightCSV_up_jesPileUpPtEC1", None)
        #event.btagWeightCMVAV2_down_cferr1 = getattr(event.input, "btagWeightCMVAV2_down_cferr1", None)
        #event.btagWeightCSV_up_jesRelativeFSR = getattr(event.input, "btagWeightCSV_up_jesRelativeFSR", None)
        #event.btagWeightCSV_up_jesTimePtEta = getattr(event.input, "btagWeightCSV_up_jesTimePtEta", None)
        #event.btagWeightCSV_up_jes = getattr(event.input, "btagWeightCSV_up_jes", None)
        #event.btagWeightCMVAV2_up_jes = getattr(event.input, "btagWeightCMVAV2_up_jes", None)
        #event.btagWeightCSV_down_jesSinglePionECAL = getattr(event.input, "btagWeightCSV_down_jesSinglePionECAL", None)
        #event.btagWeightCMVAV2_up_lf = getattr(event.input, "btagWeightCMVAV2_up_lf", None)
        #event.btagWeightCSV_down_hfstats2 = getattr(event.input, "btagWeightCSV_down_hfstats2", None)
        #event.btagWeightCSV_up_jesPileUpDataMC = getattr(event.input, "btagWeightCSV_up_jesPileUpDataMC", None)
        #event.btagWeightCSV_down_hfstats1 = getattr(event.input, "btagWeightCSV_down_hfstats1", None)
        #event.btagWeightCSV_down_jesSinglePionHCAL = getattr(event.input, "btagWeightCSV_down_jesSinglePionHCAL", None)
        #event.btagWeightCMVAV2_up_cferr1 = getattr(event.input, "btagWeightCMVAV2_up_cferr1", None)
        #event.btagWeightCMVAV2_up_cferr2 = getattr(event.input, "btagWeightCMVAV2_up_cferr2", None)
        #event.btagWeightCMVAV2_down_lfstats1 = getattr(event.input, "btagWeightCMVAV2_down_lfstats1", None)
        #event.btagWeightCMVAV2_down_lfstats2 = getattr(event.input, "btagWeightCMVAV2_down_lfstats2", None)
        #event.btagWeightCSV_up_hfstats2 = getattr(event.input, "btagWeightCSV_up_hfstats2", None)
        #event.btagWeightCSV_up_hfstats1 = getattr(event.input, "btagWeightCSV_up_hfstats1", None)
        #event.btagWeightCMVAV2_down_jes = getattr(event.input, "btagWeightCMVAV2_down_jes", None)
        #event.btagWeightCSV_up_jesSinglePionHCAL = getattr(event.input, "btagWeightCSV_up_jesSinglePionHCAL", None)
