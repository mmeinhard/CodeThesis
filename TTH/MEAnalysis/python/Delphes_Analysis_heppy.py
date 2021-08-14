import math
import ROOT
ROOT.gROOT.SetBatch(True)

DELPHES_PATH="/mnt/t3nfs01/data01/shome/algomez/work/Generation/Delphes/"

ROOT.gROOT.ProcessLine('.include {0}'.format(DELPHES_PATH))
ROOT.gROOT.ProcessLine('.include {0}/classes/'.format(DELPHES_PATH))
ROOT.gROOT.ProcessLine('.include {0}/external/'.format(DELPHES_PATH))
ROOT.gInterpreter.Declare('#include "{0}/classes/DelphesClasses.h"'.format(DELPHES_PATH))
ROOT.gInterpreter.Declare('#include "{0}/external/ExRootAnalysis/ExRootTreeReader.h"'.format(DELPHES_PATH))
ROOT.gSystem.Load(DELPHES_PATH+"/libDelphes.so")

#ROOT.gInterpreter.AddIncludePath("/mnt/t3nfs01/data01/shome/algomez/work/Generation/Delphes/external/ExRootAnalysis/ExRootTreeReader.h")
#ROOT.gSystem.Load("libFWCoreFWLite.so")
#ROOT.gSystem.Load("libTTHCommonClassifier.so")
#ROOT.gSystem.Load("libTTHGenLevel.so")
#import ROOT.HepMC
import sys, os, pickle
import logging
import numpy as np

#fastjet setup
#ROOT.gSystem.Load("libfastjet")
#ROOT.gInterpreter.ProcessLine('#include "fastjet/ClusterSequence.hh"')
#ROOT.gInterpreter.ProcessLine("fastjet::ClusterSequence(std::vector<fastjet::PseudoJet>{},fastjet::JetDefinition{});")

#from TTH.GenLevel.eventsgen import Events
#from TTH.MEAnalysis.MEMUtils import set_integration_vars, add_obj
#from TTH.MEAnalysis.MEMConfig import MEMConfig

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *
#from PhysicsTools.HeppyCore.utils.deltar import matchObjectCollection

CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")
CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")

#wrappers for functions we can't call from python
#make a function which increments an iterator, we can't easily do in python
#ROOT.gInterpreter.ProcessLine("namespace Util { HepMC::GenEvent::particle_const_iterator next_particle(HepMC::GenEvent::particle_const_iterator it) {it++; return it;}; } ")
#ROOT.gInterpreter.ProcessLine("namespace Util { HepMC::GenVertex::particle_iterator next_particle(HepMC::GenVertex::particle_iterator it) {it++; return it;}; } ")
#make a function which dereferences an iterator 
#ROOT.gInterpreter.ProcessLine("namespace Util { HepMC::GenParticle* get_particle(HepMC::GenEvent::particle_const_iterator it) {return *it;}; } ")
#ROOT.gInterpreter.ProcessLine("namespace Util { HepMC::GenParticle* get_particle(HepMC::GenVertex::particle_iterator it) {return *it;}; } ")

#Needed to correctly unpickle, otherwise
#   File "/opt/cms/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed4/lib/ROOT.py", line 303, in _importhook
#     return _orig_ihook( name, *args, **kwds )
# ImportError: No module named TFClasses
#import TTH.MEAnalysis.TFClasses as TFClasses
#sys.modules["TFClasses"] = TFClasses

class Conf(dict):
    def __getattr__(self, x):
        return self[x]

conf = Conf()
conf["Jet"] = {
    "pt": 30,
    "eta": 2.4,
#    "pt_clustering": 10,
#    "def":  "ROOT.fastjet.JetDefinition(ROOT.fastjet.antikt_algorithm, 0.5)"
}

conf["el"] = {
    "pt": 30,
    "eta": 2.1
}

conf["mu"] = {
    "pt": 26,
    "eta": 2.1
}

conf["fatjet"] = {
    "mass" : (110, 210),
    "tau32" : 0.7
}


conf["met"] = {
    "pt": 20
}

# test analyzer
class TestAnalyzer(Analyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TestAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def process(self, event):

        return True


# Event analyzer (brings input in same fromat as for nanoTree analysis)
import DelphesTreeClasses
class EventAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):

        event.Jet = DelphesTreeClasses.Jet.make_array(event.input)
        event.Electron = DelphesTreeClasses.Electron.make_array(event.input)
        event.Muon = DelphesTreeClasses.Muon.make_array(event.input) 
        event.met = DelphesTreeClasses.met(event.input) 
        event.ScalarHT = DelphesTreeClasses.ScalarHT(event.input) 
        event.GenParticle = DelphesTreeClasses.GenParticle.make_array(event.input) 
        event.FatJet = DelphesTreeClasses.FatJet.make_array(event.input)


# Lepton analyzer
class LeptonAnalyzer(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def process(self, event):

        event.mu = event.Muon
        event.el = event.Electron
        event.good_leptons = []

        # Apply pt, eta cuts
        # isolation still missing
        for flv in ["mu", "el"]:
                
                lepcuts = conf[flv]
                leps = filter(lambda x, lepcuts=lepcuts: (
                        x.pt > lepcuts["pt"] and abs(x.eta) < lepcuts["eta"]
                    ), getattr(event, flv)
                )
                event.good_leptons += leps

        event.good_leptons = sorted(event.good_leptons, key=lambda x: x.pt, reverse=True)
        return True

from collections import OrderedDict
from TTH.MEAnalysis.vhbb_utils import SystematicObject
from TTH.MEAnalysis.Analyzer import FilterAnalyzer

# Jet analyzer
class JetAnalyzer(FilterAnalyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)

    def calculate_nBtags(self, jets):
        count = 0
        for i in range(len(jets)):
            count += int(jets[i].btag)
        return count   

    def calculate_mbb_closest(self, bjet_candidates):

        if len(bjet_candidates)<2:
            return 0

        #find closest pair in deltaR
        pairs = set([])
        ordered = {}
        for j1 in bjet_candidates:
            for j2 in bjet_candidates:
                if j1 == j2:
                    continue
                if (j1, j2) in pairs or (j2, j1) in pairs:
                    continue
                pairs.update([(j1, j2)])
                #lv1 = lvec(j1)
                lv1 = j1
                #lv2 = lvec(j2)
                lv2 = j2
                dr = lv1.DeltaR(lv2)
                ordered[dr] = (lv1, lv2)
        dr0 = sorted(ordered.keys())[0]
        mbb_closest = (ordered[dr0][0] + ordered[dr0][1]).M()
        return mbb_closest

    def process(self, event):
       
        evdict = OrderedDict()

        #We create a wrapper around the base event with nominal quantities
        evdict["nominal"] = SystematicObject(event, {"systematic": "nominal"})
        event.systResults = evdict

        # Apply pt, eta cuts
        # isolation still missing
        event.jet = event.Jet
        jetcuts = conf["Jet"]
        jets = filter(lambda x, jetcuts=jetcuts: (
                        x.pt > jetcuts["pt"] and abs(x.eta) < jetcuts["eta"]
                    ), event.jet
                )

        event.systResults["nominal"].good_jets = sorted(jets, key=lambda x: x.pt, reverse=True)
       
        # add high-level variables
        jets = event.systResults["nominal"].good_jets
        event.nBtags = self.calculate_nBtags(jets)

        # !!! check definition of ht30 !!! not sure if ht30 == HT in Delphes file
        event.ht30 = event.ScalarHT.HT 

        bjet_candidates = []
        for j in jets:
            if int(j.btag)==1:
                lv = ROOT.TLorentzVector()
                lv.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)
                bjet_candidates.append(lv)
        event.mbb_closest = self.calculate_mbb_closest(bjet_candidates)

        event.good_jets_nominal = event.systResults["nominal"].good_jets

        return True

# tagging top candidates
class TopTaggerAnalyzer(FilterAnalyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TopTaggerAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(TopTaggerAnalyzer, self).beginLoop(setup)

    def process(self, event):
       
        event.fatjets = event.FatJet

        fatjetcuts = conf["fatjet"]
        fatjets = filter(lambda x, fatjetcuts=fatjetcuts: (
                        fatjetcuts["mass"][0] < x.mass and x.mass < fatjetcuts["mass"][1] and x.Nsub[3]/x.Nsub[2] < fatjetcuts["tau32"]
                    ), event.fatjets
                  )

        event.systResults["nominal"].boosted_tops = sorted(fatjets, key=lambda x: x.pt, reverse=True)

        # remove here AK4 jets which are within the AK8 jets

        event.systResults["nominal"].resolved_jets = event.systResults["nominal"].good_jets

        event.fat_jets = event.systResults["nominal"].boosted_tops
        if len(event.fat_jets) == 1 or len(event.fat_jets) == 2:
            return True
        else:
            return False
 
# import JointLikelihoodAnalyzer from CMSSW workflow
from TTH.MEAnalysis.JointLikelihoodAnalyzer import JointLikelihoodAnalyzer 

# import NNAnalyzer from CMSSW workflow
from TTH.MEAnalysis.NNAnalyzer import NNAnalyzer
    

if __name__ == "__main__":

    import PhysicsTools.HeppyCore.framework.config as cfg

    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf

    event_ana = cfg.Analyzer(
        EventAnalyzer,
        'DelphesTree',
    )
    
    test_ana = cfg.Analyzer(
        TestAnalyzer,
        'eventnumber'
    )

    lepton_ana = cfg.Analyzer(
        LeptonAnalyzer,
        'lepton'
    )

    jet_ana = cfg.Analyzer(
        JetAnalyzer,
        'jet'
    )

    toptag_ana = cfg.Analyzer(
        TopTaggerAnalyzer,
        'top_tag'
    )
    
    jlr_ana = cfg.Analyzer(
        JointLikelihoodAnalyzer,
        'jlr',
        _conf = python_conf,
        do_jlr = True
    )

    NN_ana = cfg.Analyzer(
        NNAnalyzer,
        'NN_input',
        _conf = python_conf,
        framework = "Delphes",
        training = True,
        boosted = False
    )

    #Override the default fillCoreVariables and declareCoreVariables in heppy,
    #as otherwise they would mess with some variables like puWeight etc
    def fillCoreVariables(self, tr, event, isMC):
        pass

    def declareCoreVariables(self, tr, isMC):
        pass

    AutoFillTreeProducer.declareCoreVariables = declareCoreVariables
    AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

    jetType = NTupleObjectType("jetType", variables = [
        NTupleVariable("pt", lambda x : x.pt),
        NTupleVariable("eta", lambda x : x.eta),
        NTupleVariable("phi", lambda x : x.phi),
        NTupleVariable("mass", lambda x : x.mass),
        NTupleVariable("btag", lambda x : x.btag)
    ])

    fatjetType = NTupleObjectType("fatjetType", variables = [
        NTupleVariable("pt", lambda x : x.pt),
        NTupleVariable("eta", lambda x : x.eta),
        NTupleVariable("phi", lambda x : x.phi),
        NTupleVariable("mass", lambda x : x.mass),
    ])


    leptonType = NTupleObjectType("leptonType", variables = [
        NTupleVariable("pt", lambda x : x.pt),
        NTupleVariable("eta", lambda x : x.eta),
        NTupleVariable("phi", lambda x : x.phi),
        NTupleVariable("mass", lambda x : x.mass),
    ])

    metType = NTupleObjectType("metType", variables = [
        NTupleVariable("eta", lambda x : x.eta),
        NTupleVariable("phi", lambda x : x.phi),
        NTupleVariable("pt", lambda x : x.pt),
    ])

    treeProducer = cfg.Analyzer(
        class_object = AutoFillTreeProducer,
        defaultFloatType = "F",
        verbose = False,
        vectorTree = True,
        globalVariables = [
            NTupleVariable(
               "prob_ttHbb", lambda ev: ev.prob_ttHbb,
               type=float,
               help="squared matrix element for hypo ttHbb", mcOnly=True
            ),
            NTupleVariable(
               "prob_ttbb", lambda ev: ev.prob_ttbb,
               type=float,
               help="squared matrix element for hypo ttbb", mcOnly=True
            ),
            NTupleVariable(
               "JLR", lambda ev: ev.jointlikelihood,
               type=float,
               help="joint likelihood ratio", mcOnly=True
            ),
            NTupleVariable(
               "HT", lambda ev: ev.ht30,
               type=float,
               help=" ", mcOnly=False
            ),
            NTupleVariable(
               "MET_eta", lambda ev: ev.met.eta,
               type=float,
               help=" ", mcOnly=False
            ),
            NTupleVariable(
               "MET_phi", lambda ev: ev.met.phi,
               type=float,
               help=" ", mcOnly=False
            ),
            NTupleVariable(
               "MET_pt", lambda ev: ev.met.pt,
               type=float,
               help=" ", mcOnly=False
            ),

        ],
        collections = {
            "good_jets_nominal" : NTupleCollection("jets", jetType, 16, help="Selected resolved jets, pt ordered"),
            "good_leptons" : NTupleCollection("leps", leptonType, 2, help="Selected leptons, pt ordered"),
            #"fat_jets" : NTupleCollection("fatjets", fatjetType, 2, help="fat jet for top candidates (pt ordered)")
        }
    )

    sequence = cfg.Sequence([
        event_ana,
        lepton_ana,
        jet_ana,
        #toptag_ana,
        jlr_ana,
        NN_ana,
        treeProducer
    ])

    from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
    output_service = cfg.Service(
        TFileService,
        'outputfile',
        name="outputfile",
        fname='tree.root',
        option='recreate'
    )

    from TTH.MEAnalysis.samples_base import getSitePrefix
    fns = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    print "debug grid-control"
    print os.getcwd()
    #fns = os.environ["FILE_NAMES"].split()
    if len(fns) != 1:
        raise Exception("need only one file")
    dataset = os.environ["DATASETPATH"]
    firstEvent = int(os.environ["SKIP_EVENTS"])
    nEvents = int(os.environ["MAX_EVENTS"])

    print fns
    print dataset
    print firstEvent
    print nEvents

    comp_cls = cfg.MCComponent

    comp = comp_cls(
        dataset,
        files = fns,
        tree_name = "Delphes", #DS requires change to ../../PhysicsTools/HeppyCore/python/framework/config.py
    )
   

    #from PhysicsTools.HeppyCore.framework.eventsDelphes import Events
    from TTH.MEAnalysis.eventsDelphes import Events
    config = cfg.Config(
        #Run across these inputs
        components = [comp],
        sequence = sequence,
        services = [output_service],
        events_class = Events
    )


    from PhysicsTools.HeppyCore.framework.looper import Looper
    looper = Looper(
        'Loop',
        config,
        nPrint = 0,
        firstEvent = firstEvent,
        nEvents = nEvents
    )
    looper.loop()
    looper.write()

