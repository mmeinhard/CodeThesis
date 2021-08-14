import nanoTreeClasses

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):
        event.lumi = getattr(event.input, "luminosityBlock", None)
        event.evt = getattr(event.input, "event", None)

        event.Electron = nanoTreeClasses.Electron.make_array(event.input)
        event.Muon = nanoTreeClasses.Muon.make_array(event.input)
        event.Jet = nanoTreeClasses.Jet.make_array(event.input)
        event.PV = nanoTreeClasses.PV.make_array(event.input)
        event.met = nanoTreeClasses.met.make_obj(event.input)
        """
        event.met_shifted_UnclusteredEnUp = met_shifted_UnclusteredEnUp.make_obj(event.input)
        event.met_shifted_UnclusteredEnDown = met_shifted_UnclusteredEnDown.make_obj(event.input)
        event.met_shifted_JetResUp = met_shifted_JetResUp.make_obj(event.input)
        event.met_shifted_JetResDown = met_shifted_JetResDown.make_obj(event.input)
        event.met_shifted_JetEnUp = met_shifted_JetEnUp.make_obj(event.input)
        event.met_shifted_JetEnDown = met_shifted_JetEnDown.make_obj(event.input)
        event.met_shifted_MuonEnUp = met_shifted_MuonEnUp.make_obj(event.input)
        event.met_shifted_MuonEnDown = met_shifted_MuonEnDown.make_obj(event.input)
        event.met_shifted_ElectronEnUp = met_shifted_ElectronEnUp.make_obj(event.input)
        event.met_shifted_ElectronEnDown = met_shifted_ElectronEnDown.make_obj(event.input)
        event.met_shifted_TauEnUp = met_shifted_TauEnUp.make_obj(event.input)
        eveEnt.met_shifted_TauEnDown = met_shifted_TauEnDown.make_obj(event.input)
        """
        #event.json = getattr(event.input, "json", None)
        #event.json_silver = getattr(event.input, "json_silver", None)
        event.nPVs = getattr(event.input, "PV_npvs")
        #event.bx = getattr(event.input, "bx", None)
        #event.rho = getattr(event.input, "rho", None)
