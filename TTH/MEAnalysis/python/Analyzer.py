from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec, autolog
import resource
import ROOT
import logging
import os
from copy import deepcopy
from FWCore.PythonUtilities.LumiList import LumiList
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer
LOG_MODULE_NAME = logging.getLogger(__name__)

class FilterAnalyzer(Analyzer):
    """
    A generic analyzer that may filter events.
    Counts events the number of processed and passing events.
    """
    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)
        self.counters.addCounter("processed")

    def process(self, event):
        self.counters.counter("processed").inc(0)

class MemoryAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MemoryAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.logger = logging.getLogger("MemoryAnalyzer")
        self.hpy = None
        self.do_heapy = False 
        if self.do_heapy:
            try:
                from guppy import hpy
                self.hpy = hpy()
                self.hpy.setrelheap()
            except Exception as e:
                logging.error("Could not import guppy, skipping memory logging")

        self.heap_prev = None

    def process(self, event):
        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if event.iEv % 100 == 0:
            autolog("memory usage at event {0}: {1:.2f} MB".format(event.iEv, memory/1024.0))
 
        if not self.hpy is None:
            heap = self.hpy.heap() 
            if not self.heap_prev is None:
                diff = heap - self.heap_prev
                print diff
            self.heap_prev = heap
        return True

class PrefilterAnalyzer(Analyzer):
    """
    Performs a very basic prefiltering of the event before fully
    loading the event from disk into memory.
    NB: Actually we can't use this, since systematics may migrate the event into a different category
    """
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PrefilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
    
    def process(self, event):
        njet = event.input.nJet
        btag_csv = [getattr(event.input, "Jet_btagCSVV2")[nj] for nj in range(njet)]
        #btag_cmva = [getattr(event.input, "Jet_btagCMVA")[nj] for nj in range(njet)]
        btag_csv_m = filter(lambda x, wp=self.conf.jets["btagWPs"]["CSVM"][1]: x>=wp, btag_csv)
        #btag_cmva_m = filter(lambda x, wp=self.conf.jets["btagWPs"]["CMVAM"][1]: x>=wp, btag_cmva)
        if njet < 4 or (len(btag_csv_m) < 1):
            #if not self.conf.general["passall"]:
            return False
        return True

class CounterAnalyzer(FilterAnalyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.counter_name = cfg_ana.counter_name
        super(CounterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    
    def beginLoop(self, setup):
        super(CounterAnalyzer, self).beginLoop(setup)
        self.chist = ROOT.TH1F("CounterAnalyzer_count{0}".format(self.counter_name), "count", 1,0,1)
    
    def process(self, event):
        if event.input.nJet >= 0:
            self.chist.Fill(0)
        else:
            raise Exception("Could not read event")

        return True

class EventIDFilterAnalyzer(FilterAnalyzer):
    """
    Allows only events in a whitelist of (run, lumi, event) to pass.
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventIDFilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.event_whitelist = self.conf.general.get("eventWhitelist", None)

    def beginLoop(self, setup):
        super(EventIDFilterAnalyzer, self).beginLoop(setup)

    def process(self, event):
        
        event.id_triplet = (event.input.run, event.input.luminosityBlock, event.input.event)
        LOG_MODULE_NAME.debug("processing event {0}".format(event.id_triplet))

        passes = True
        if not self.event_whitelist is None:
            passes = False
            if (event.input.run, event.input.luminosityBlock, event.input.event) in self.event_whitelist:
                print "IDFilter", (event.input.run, event.input.luminosityBlock, event.input.event)
                passes = True

        if passes and (
            "eventboundary" in self.conf.general["verbosity"] or
            "debug" in self.conf.general["verbosity"]
            ):
            print "---starting EVENT r:l:e", event.input.run, event.input.luminosityBlock, event.input.event
        return passes


class EventWeightAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventWeightAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.n_gen = cfg_comp.n_gen
        self.xs = cfg_comp.xs

    def beginLoop(self, setup):
        super(EventWeightAnalyzer, self).beginLoop(setup)

    def process(self, event):
        event.weight_xs = self.xs/float(self.n_gen) if self.n_gen > 0 else 1

        return True

class LumiListAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LumiListAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        analysis_conf = self.cfg_ana._analysis_conf
        path = analysis_conf.config.get("general", "json")
        path = path.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])

        self.runranges = analysis_conf.config.get("general", "runs").split("\n")
        self.runranges = [map(int, s.split()[1:]) for s in self.runranges if len(s)>0]
         
        ll = LumiList(path)
        
        self.lls = set(ll.getLumis())
        
    def beginLoop(self, setup):
        super(LumiListAnalyzer, self).beginLoop(setup)

    def process(self, event):
        run_lumi = (event.input.run, event.input.luminosityBlock)
        event.json = run_lumi in self.lls
        
        #LOG_MODULE_NAME.debug("Event %s/%s in JSON: %s",event.input.run, event.input.luminosityBlock, event.json)
        
        event.runrange = -1
        for irunrange, runrange in enumerate(self.runranges):
            if event.input.run >= runrange[0] and event.input.run <= runrange[1]:
                event.runrange = irunrange
                break
            
        return True

class PrimaryVertexAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PrimaryVertexAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(PrimaryVertexAnalyzer, self).beginLoop(setup)

    def process(self, event):
        #Split event number in two
        pvs = event.PV
        if len(pvs) > 0:
            event.primaryVertex = pvs[0]
            event.passPV = (not event.primaryVertex.isFake) and (event.primaryVertex.ndof > 4 and event.primaryVertex.Rho < 2 and abs(event.primaryVertex.z)<=24)
        else:
            event.passPV = False
            print "PrimaryVertexAnalyzer: number of vertices=", (len(pvs))
            #cannot use passAll here because we want to ntuplize the primary vertex, in case it doesn't exist, the
            #code will fail
            return False
        if not self.conf.general["passall"]:
            return event.passPV        
        else:
            return True


class NanoOutputEmulator:
    def __init__(self):
        self.data = {}
        pass

    def fillBranch(self, name, val):
        self.data[name] = val

    def fillEvent(self, event):
        for key, val in self.data.items():
            setattr(event, key, val)

    def branch(self, name, type):
        pass

class PUWeightAnalyzer(Analyzer):
    """
    Recomputes the pileup weight using the nanoAOD postprocessing module.
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PUWeightAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        self.analysis_conf = cfg_ana._analysis_conf

        self.pufile_mc = self.analysis_conf.config.get("puweight", "weightfile_mc")
        self.pufile_data = self.analysis_conf.config.get("puweight", "weightfile_data")
        
        self.pufile_mc = self.pufile_mc.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
        self.pufile_data = self.pufile_data.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])

        LOG_MODULE_NAME.debug("pileup MC file: {0}".format(self.pufile_mc))
        LOG_MODULE_NAME.debug("pileup data file: {0}".format(self.pufile_data))

        #create the nanoAOD pileup weight analyzer
        self.nano_analyzer = puWeightProducer(self.pufile_mc, self.pufile_data, "pu_mc", "pileup", verbose=False, nvtx_var="Pileup_nTrueInt")
        #create a kind of container that fakes the nanoAOD output
        self.out = NanoOutputEmulator()
        self.nano_analyzer.out = self.out

    def beginLoop(self, setup):
        super(PUWeightAnalyzer, self).beginLoop(setup)
        self.nano_analyzer.beginJob()
        self.nano_analyzer.beginFile(None, None, None, self.out)
        
    def process(self, event):

        #Only process MC
        if not self.cfg_comp.isMC:
            return event 

        self.nano_analyzer.analyze(event.input)
        self.out.fillEvent(event)

        return True


class TriggerWeightAnalyzer(Analyzer):
    """
    Computes trigger weight from root files containing the SF
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TriggerWeightAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.calcSF = cfg_ana._conf.trigger["calcFHSF"]
        if self.calcSF:
            sfFile = ROOT.TFile(cfg_ana._conf.trigger["TriggerSFFile"],"READ")
            self.SF = deepcopy(sfFile.Get(cfg_ana._conf.trigger["TriggerSFHisto"])) #only works with deepcopy
                
    def beginLoop(self, setup):
        super(TriggerWeightAnalyzer, self).beginLoop(setup)

    def process(self, event):
        #Only process MC
        if not self.cfg_comp.isMC:
            return event 

        if not self.calcSF:
            event.TriggerFHWeight = 1    
            return True
        else:
            SF = 1
            nominalEvent = event.systResults["nominal"]
            #Make the Analyizer save for runnign with pass all!
            hasCSVHTAttr = hasattr(nominalEvent, "nBCSVM") and hasattr(nominalEvent, "ht30")
            hasGoodJets = hasattr(nominalEvent, "good_jets")
            hasSixJets = False
            if hasGoodJets:
                hasSixJets = len(nominalEvent.good_jets) >= 6
            if not (hasCSVHTAttr and hasGoodJets and hasSixJets):
                event.TriggerFHWeight = 1
                return True
            ht, pt, nBSCM = nominalEvent.ht30, getattr(nominalEvent.good_jets[5], "pt"), nominalEvent.nBCSVM
            _bin = self.SF.FindBin(ht, pt, nBSCM)
            SF = self.SF.GetBinContent(_bin)
            #print ht, pt, nBSCM, _bin, SF
            if SF == 0:
                SF = 1

            event.TriggerFHWeight = SF
            return True

class METFilterAnalyzer(Analyzer):
    """
    Creates combination flag of MET data quality filters defiend in config.
    """
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(METFilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        if cfg_comp.isMC:
            self.METFilterList = self.conf.general["METFilterMC"]
            LOG_MODULE_NAME.debug("Loading MC METFilters")
        else:
            self.METFilterList = self.conf.general["METFilterData"]
            LOG_MODULE_NAME.debug("Loading Data METFilters")

    def beginLoop(self, setup):
        super(METFilterAnalyzer, self).beginLoop(setup)

    def process(self, event):

        passesFilter = False
        for ifilter, _filter in enumerate(self.METFilterList):
            filterVal = getattr(event.input,  _filter)
            if ifilter == 0:
                passesFilter = filterVal
            else:
                passesFilter = passesFilter and filterVal

        event.passMETFilters = passesFilter
        return True
