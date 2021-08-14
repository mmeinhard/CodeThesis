import logging

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

LOG_MODULE_NAME = logging.getLogger(__name__)

class LeptonAnalyzer(FilterAnalyzer):
    """
    Analyzes leptons and applies single-lepton and di-lepton selection.

    Relies on TTH.MEAnalysis.VHbbTree.EventAnalyzer for inputs.

    Configuration:
    Conf.leptons[channel][cuttype] where channel=mu,ele, cuttype=tight,loose,(+veto)
    the lepton cuts must specify pt, eta and isolation cuts.

    Returns:
    event.good_leptons (list of VHbbTree.selLeptons): contains the leptons that pass the SL XOR DL selection.
        Leptons are ordered by flavour and pt.
    event.is_sl, is_dl (bool): specifies if the event passes SL or DL selection.

    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.printedWarningOnce = False
    def beginLoop(self, setup):
        super(LeptonAnalyzer, self).beginLoop(setup)

    def process(self, event):

        event.mu = event.Muon
        LOG_MODULE_NAME.debug("nanoAOD muons: " + str([(x.pt, x.eta, x.phi, x.tightId) for x in event.mu]))

        event.el = event.Electron
        LOG_MODULE_NAME.debug("nanoAOD electrons: " + str([(x.pt, x.eta, x.phi, x.eleCutId) for x in event.el]))

        for id_type in ["SL", "DL", "veto"]:
            sumleps = []
            for lep_flavour in ["mu", "el"]:

                #get the lepton cuts from the configuration
                lepcuts = self.conf.leptons[lep_flavour][id_type]
                incoll = getattr(event, lep_flavour)
                
                #The isolation type and cut value to be used
                isotype = self.conf.leptons[lep_flavour]["isotype"]
                isocut = lepcuts.get("iso", None)
                
                LOG_MODULE_NAME.debug("before pt,eta: id_type={0} lep_flavour={1} Nleps={2} incoll={3}".format(id_type, lep_flavour, len(incoll), str([[x.pt, x.eta, x.pdgId] for x in incoll])))

                #Filter leptons by pt and eta
                leps = filter(
                    lambda x, lepcuts=lepcuts: (
                        x.pt > lepcuts.get("pt", 0) #pt cut may be optional in case of DL
                        and abs(x.eta) < lepcuts["eta"]
                    ), incoll
                )
                LOG_MODULE_NAME.debug("after pt,eta: id_type={0} lep_flavour={1} Nleps={2} leps={3}".format(id_type, lep_flavour, len(leps), str([[x.pt, x.eta, x.pdgId] for x in leps])))

                #Apply isolation cut
                for lep in leps:
                    lep.iso = getattr(lep, isotype)
                if not isocut is None:

                    #Inverted isolation cut
                    if lepcuts.get("isoinverted", False):
                        leps = filter(
                            lambda x, isotype=isotype, isocut=isocut: abs(getattr(x, isotype)) >= isocut, leps
                        )
                    #Normal isolation cut
                    else:
                        leps = filter(
                            lambda x, isotype=isotype, isocut=isocut: abs(getattr(x, isotype)) < isocut, leps
                        )
                LOG_MODULE_NAME.debug("after iso: id_type={0} lep_flavour={1} Nleps={2} leps={3}".format(id_type, lep_flavour, len(leps), str([[x.pt, x.eta, x.pdgId, x.iso] for x in leps])))
                
                #Apply ID cut 
                leps = filter(lepcuts["idcut"], leps)
                LOG_MODULE_NAME.debug("after ID: id_type={0} lep_flavour={1} Nleps={2} leps={3}".format(id_type, lep_flavour, len(leps), str([[x.pt, x.eta, x.pdgId, x.iso] for x in leps])))

                #add to the vector of all the leptons
                sumleps += leps
                lepname = lep_flavour + "_" + id_type

                setattr(event, lepname, leps)
                setattr(event, "n_"+  lepname, len(leps))
                LOG_MODULE_NAME.debug(lepname + " " + str([(x.pt, x.eta, x.pdgId) for x in leps]))
            #end of lep_flavour loop
            
            setattr(event, "lep_{0}".format(id_type), sumleps)
            setattr(event, "n_lep_{0}".format(id_type), len(sumleps))
            LOG_MODULE_NAME.debug("lep_{0}".format(id_type) + " " + str([(x.pt, x.eta, x.pdgId) for x in sumleps]))
        # end of lepton type loop (SL, DL, veto)
        

        #end of id_type loop
        event.lep_SL = sorted(event.lep_SL, key=lambda x: x.pt, reverse=True)
        LOG_MODULE_NAME.debug("Lep_SL: "+ " " + str([(x.pt, x.eta, x.pdgId) for x in event.lep_SL]))
        event.lep_DL = sorted(event.lep_DL, key=lambda x: x.pt, reverse=True)
        LOG_MODULE_NAME.debug("Lep_DL: "+ " " + str([(x.pt, x.eta, x.pdgId) for x in event.lep_DL]))
        event.lep_veto = sorted(event.lep_veto, key=lambda x: x.pt, reverse=True)
        #Apply two-stage pt cut on DL leptons
        lep_DL_afterpt = []
        for lep in event.lep_DL:
            if len(lep_DL_afterpt) == 0:
                ptcut = self.conf.leptons["DL"]["pt_leading"]
            else:
                ptcut = self.conf.leptons["DL"]["pt_subleading"]
            if lep.pt > ptcut:
                lep_DL_afterpt += [lep]
        event.lep_DL = lep_DL_afterpt
        event.n_lep_DL = len(event.lep_DL)
        LOG_MODULE_NAME.debug("after two-stage DL pt: Nleps={0} leps={1}".format(len(event.lep_DL), str([[x.pt, x.eta, x.pdgId] for x in event.lep_DL])))

        sameSignDL = False
        if event.n_lep_DL == 2:
            sign = lambda x: (1, -1)[x < 0]
            sameSignDL = sign(event.lep_DL[0].pdgId) == sign(event.lep_DL[1].pdgId)
        LOG_MODULE_NAME.debug("Same sign DL veto: %s", sameSignDL)
        
        event.is_sl = (event.n_lep_SL == 1 and event.n_lep_veto == 1)
        event.is_dl = (event.n_lep_DL == 2 and event.n_lep_veto == 2 and not sameSignDL)
        event.is_fh = (event.n_lep_veto == 0)
        if self.conf.leptons["force_isFH"]:
            if not self.printedWarningOnce:
                LOG_MODULE_NAME.warning("Forcing is_fh to True")
                self.printedWarningOnce = True
            event.is_fh = True
        LOG_MODULE_NAME.debug("is_sl={0} is_dl={1} is_fh={2}".format(event.is_sl, event.is_dl, event.is_fh))

        #Calculate di-lepton system momentum
        event.dilepton_p4 = ROOT.TLorentzVector()
        if event.is_sl:
            event.good_leptons = event.lep_SL
            event.veto_leptons = event.lep_veto
        elif event.is_dl:
            event.good_leptons =event.lep_DL
            event.veto_leptons = event.lep_veto
            for lv in [lvec(l) for l in event.good_leptons]:
                event.dilepton_p4 += lv
        elif event.is_fh:
            event.good_leptons = []
            event.veto_leptons = []
        else:
            event.good_leptons = []
            event.veto_leptons = []

        
        event.good_leptons = sorted(event.good_leptons, key=lambda x: x.pt, reverse=True)
        event.veto_leptons = sorted(event.veto_leptons, key=lambda x: x.pt, reverse=True)
       
        #Match good signal leptons to gen-leptons 
        if self.cfg_comp.isMC:
            from PhysicsTools.HeppyCore.utils.deltar import matchObjectCollection
            #matchObjectCollection(event.good_leptons, event.GenLepFromTop, 0.3)
        #apply configuration-dependent selection
        passes = self.conf.leptons["selection"](event)
        if "debug" in self.conf.general["verbosity"]:
            autolog("LeptonAnalyzer selection", passes)
        if event.is_sl and event.is_dl:
            autolog("The event (%s,%s,%s) is both sl and dl" % (
                event.input.run,event.input.lumi,event.input.evt)
            )
            autolog("SL mu")
            for lep in event.mu_SL:
                (self.conf.leptons["mu"]["debug"])(lep)
            autolog("DL mu")
            for lep in event.mu_DL:
                (self.conf.leptons["mu"]["debug"])(lep)
                
            autolog("SL el")
            for lep in event.el_SL:
                (self.conf.leptons["el"]["debug"])(lep)
            autolog("DL el")
            for lep in event.el_DL:
                (self.conf.leptons["el"]["debug"])(lep)
                
            autolog("veto mu")
            for lep in event.mu_veto:
                (self.conf.leptons["mu"]["debug"])(lep)
            autolog("veto el")
            for lep in event.mu_veto:
                (self.conf.leptons["el"]["debug"])(lep)
            passes = False
            autolog("WARNING: Overlapping event")

        return self.conf.general["passall"] or passes
