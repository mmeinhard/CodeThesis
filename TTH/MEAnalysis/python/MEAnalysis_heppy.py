import os
import sys
import logging
from copy import deepcopy
import imp
#pickle and transfer function classes to load transfer functions
import cPickle as pickle

import TTH.MEAnalysis.TFClasses as TFClasses
import TTH.MEAnalysis.config as cfg
#import PhysicsTools.HeppyCore.framework.config as cfg
import ROOT

sys.modules["TFClasses"] = TFClasses
ROOT.gROOT.SetBatch(True)

LOG_MODULE_NAME = logging.getLogger(__name__)

class BufferedTree:
    """Class with buffered TTree access, so that using tree.branch does not load the entry twice

    Attributes:
        branches (dict string->branch): TTree branches
        buf (dict string->data): The buffer, according to branch name
        iEv (int): Current event
        maxEv (int): maximum number of events in the TTree
        tree (TTree): Underlying TTree
    """
    def __init__(self, tree):
        self.tree = tree
        self.tree.SetCacheSize(10*1024*1024)

        #stores the branches of the current tree
        self.branches = {}
        for br in self.tree.GetListOfBranches():
            self.branches[br.GetName()] = br

        self.tree.AddBranchToCache("*")

        #stores the branch values for the current event
        self.buf = {}
        self.iEv = 0
        self.maxEv = int(self.tree.GetEntries())

    def __getattr__(self, attr, defval=None):
        #print "BufferedTree getAttr", attr, defval
        if self.__dict__["branches"].has_key(attr):
            if self.__dict__["buf"].has_key(attr):
                return self.__dict__["buf"][attr]
            else:
                val = getattr(self.__dict__["tree"], attr)
                self.__dict__["buf"][attr] = val
                return val
        elif attr == "__deepcopy__":
            return getattr(self, attr)
        else:
            if not (defval is None):
                return defval
            raise Exception("Could not find branch with key: {0}".format(attr))
            #raise AttributeError

    def __str__(self):
        return self.tree.GetName()

    def GetEntries(self):
        return self.tree.GetEntries()

    def GetEntry(self, idx):
        self.buf = {}
        self.iEv = idx
        return self.tree.GetEntry(idx)

    def __deepcopy__(self, memo):
        return BufferedTree(deepcopy(self.tree, memo))
    
    def __iter__(self):
        return self
    
class BufferedChain( object ):
    """Wrapper to TChain, with a python iterable interface.

    Example of use:  #TODO make that a doctest / nose?
       from chain import Chain
       the_chain = Chain('../test/test_*.root', 'test_tree')
       event3 = the_chain[2]
       print event3.var1

       for event in the_chain:
           print event.var1
    """

    def __init__(self, files, tree_name=None):
        """
        Create a chain.

        Parameters:
          input     = either a list of files or a wildcard (e.g. 'subdir/*.root').
                      In the latter case all files matching the pattern will be used
                      to build the chain.
          tree_name = key of the tree in each file.
                      if None and if each file contains only one TTree,
                      this TTree is used.
        """
        self.files = files
        self.tree_name = tree_name
        self.base_chain = ROOT.TChain(tree_name)

        #Add all input files, which need to be opened, to the chain
        for fi in self.files:
            LOG_MODULE_NAME.info("Adding tree {0}".format(fi))
            ret = self.base_chain.AddFile(fi, 0)
            if ret == 0:
                raise IOError("Could not open file {0} with tree_name {1}".format(fi,self.tree_name))
        self.chain = BufferedTree(self.base_chain)

        self.iTree = 0

    def __getattr__(self, attr, defval=None):
        """
        All functions of the wrapped TChain are made available
        """
        return self.chain.__getattr__(attr, defval)

    def __len__(self):
        return int(self.chain.GetEntries())

    
    def __getitem__(self, index):
        """
        Returns the event at position index.
        """
        bytes = self.chain.GetEntry(index)

        #Check if the chain has moved to the next tree
        curTree = self.base_chain.GetTreeNumber()
        if curTree != self.iTree:
            LOG_MODULE_NAME.info("Switching tree to {0}".format(self.files[curTree]))
            self.iTree = curTree

            #Remake underlying tree along with the buffers
            self.chain = BufferedTree(self.base_chain)

        if bytes < 0:
            raise Exception("Could not read entry {0}".format(self.iEv))


        return self

def main(analysis_cfg, sample_name=None, schema=None, firstEvent=0, numEvents=None, files=[], output_name=None, dataset=None, sampleName=None, loglevel="INFO"):
    #configure logging
    log_format = ('%(levelname)-8s %(module)-20s %(message)s')
    logging.basicConfig(stream=sys.stdout, level=getattr(logging, loglevel), format=log_format)
    
    mem_python_config = analysis_cfg.mem_python_config.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
    #Create python configuration object based on path

    if len(mem_python_config) > 0:
        LOG_MODULE_NAME.info("Loading ME python config from {0}".format(mem_python_config))
        meconf = imp.load_source("meconf", mem_python_config)
        from meconf import Conf as python_conf
    else:
        LOG_MODULE_NAME.info("Loading ME python config from TTH.MEAnalysis.MEAnalysis_cfg_heppy")
        from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str

    #Load transfer functions from pickle file
    pi_file = open(python_conf.general["transferFunctionsPickle"] , 'rb')
    python_conf.tf_matrix = pickle.load(pi_file)
    #Pre-compute the TF formulae
    # eval_gen:specifies how the transfer functions are interpreted
    #     If True, TF [0] - reco, x - gen
    #     If False, TF [0] - gen, x - reco
    #FIXME!!!: remove this flag in future versions!
    eval_gen=False
    python_conf.tf_formula = {}
    for fl in ["b", "l"]:
        python_conf.tf_formula[fl] = {}
        for bin in [0, 1]:
                python_conf.tf_formula[fl][bin] = python_conf.tf_matrix[fl][bin].Make_Formula(eval_gen)

    pi_file.close()

    #Load the subjet transfer functions from pickle file
    #For Top subjets
    pi_file = open(python_conf.general["transferFunctions_htt_Pickle"] , 'rb')
    python_conf.tf_htt_matrix = pickle.load(pi_file)
    pi_file.close()

    #For Higgs subjets
    pi_file = open(python_conf.general["transferFunctions_higgs_Pickle"] , 'rb')
    python_conf.tf_higgs_matrix = pickle.load(pi_file)
    pi_file.close()

    bdtTop = open(python_conf.general["BDT_Top"], "rb")
    python_conf.topBDT = pickle.load(bdtTop)
    bdtTop.close()

    if sample_name:
        an_sample = analysis_cfg.get_sample(sample_name)
        sample_name = an_sample.name
        step1_tree_name = an_sample.step1_tree_name
        schema = an_sample.schema
        if len(files) == 0:
            files = an_sample.file_names_step1[:an_sample.debug_max_files]
        if not output_name:
            output_name = "Loop_" + sample_name
    elif schema:
        sample_name = dataset if dataset else "sample"
        if sampleName is not None:
            sample_name = sampleName
        #step1_tree_name = "nanoAOD/Events"
        step1_tree_name = "Events"
        pass
    else:
        raise Exception("Must specify either sample name or schema")

    #Event contents are defined here
    #This is work in progress
    if schema == "mc":
        from TTH.MEAnalysis.nanoTree import EventAnalyzer
    else:
        from TTH.MEAnalysis.nanoTree_data import EventAnalyzer


    #This analyzer reads branches from event.input (the TTree/TChain) to event.XYZ (XYZ is e.g. jets, leptons etc)
    evs = cfg.Analyzer(
        EventAnalyzer,
        'events',
    )

    if python_conf.general["boosted"] == True:
        if schema == "mc":
            from TTH.MEAnalysis.nanoTreeBoosted import EventAnalyzerBoosted
        else:
            from TTH.MEAnalysis.nanoTreeBoosted_data import EventAnalyzerBoosted
        boost = cfg.Analyzer(
            EventAnalyzerBoosted,
            'events',
        )


    #Here we define all the main analyzers
    import TTH.MEAnalysis.MECoreAnalyzers as MECoreAnalyzers

    #throws away events that are not containing at least 4 jets
    prefilter = cfg.Analyzer(
        MECoreAnalyzers.PrefilterAnalyzer,
        'prefilter',
        _conf = python_conf
    )

    #Checks that the event can be read
    counter = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter',
        _conf = python_conf,
        counter_name = "",
    )

    #Filters events by the run,lumi,event triplet
    evtid_filter = cfg.Analyzer(
        MECoreAnalyzers.EventIDFilterAnalyzer,
        'eventid',
        _conf = python_conf
    )

    
    #Set passMETFilters flag according to list in config
    metfilter_ana = cfg.Analyzer(
        MECoreAnalyzers.METFilterAnalyzer,
        'metfilter',
        _conf = python_conf,
        _analysis_conf = analysis_cfg,
    )
    
    #Set the json flag according to the provided data json
    lumilist_ana = cfg.Analyzer(
        MECoreAnalyzers.LumiListAnalyzer,
        'lumilist',
        _conf = python_conf,
        _analysis_conf = analysis_cfg,
    )

    #As an option, we can recompute pileup weight
    puweight_ana = cfg.Analyzer(
        MECoreAnalyzers.PUWeightAnalyzer,
        'puweight',
        _conf = python_conf,
        _analysis_conf = analysis_cfg,
    )

    #fills the passPV flag 
    pvana = cfg.Analyzer(
        MECoreAnalyzers.PrimaryVertexAnalyzer,
        'pvana',
        _conf = python_conf
    )

    trigger = cfg.Analyzer(
        MECoreAnalyzers.TriggerAnalyzer,
        'trigger',
        _conf = python_conf
    )

    counter_trg = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter_trg',
        _conf = python_conf,
        counter_name = "_trg",
    )

    #This class performs lepton selection and SL/DL disambiguation
    leps = cfg.Analyzer(
        MECoreAnalyzers.LeptonAnalyzer,
        'leptons',
        _conf = python_conf
    )
    counter_lep = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter_lep',
        _conf = python_conf,
        counter_name = "_lep",
    )

    #This class performs jet selection and b-tag counting
    jets = cfg.Analyzer(
        MECoreAnalyzers.JetAnalyzer,
        'jets',
        _conf = python_conf
    )
    
    btagweight = cfg.Analyzer(
        MECoreAnalyzers.BtagWeightAnalyzer,
        'btagweight',
        _conf = python_conf,
        boosted = False
    )

    btagweightsubjet = cfg.Analyzer(
        MECoreAnalyzers.BtagWeightAnalyzer,
        'btagweightsubjet',
        _conf = python_conf,
        boosted = True
    )

    counter_jet = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter_jet',
        _conf = python_conf,
        counter_name = "_jet",
    )

    triggerSF = cfg.Analyzer(
        MECoreAnalyzers.TriggerWeightAnalyzer,
        "triggerWeight",
        _conf = python_conf,
        _analysis_conf = analysis_cfg,
    )
    
    #calculates the number of matched simulated B, C quarks for tt+XY matching
    genrad = cfg.Analyzer(
        MECoreAnalyzers.GenRadiationModeAnalyzer,
        'genrad',
        _conf = python_conf
    )

    #calculates the b-tag likelihood ratio
    btaglr = cfg.Analyzer(
        MECoreAnalyzers.BTagLRAnalyzer,
        'btaglr',
        _conf = python_conf,
        btagAlgo = "btagDeepCSV"
    )
    counter_blr = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter_blr',
        _conf = python_conf,
        counter_name = "_blr",
    )

    ##calculates the b-tag likelihood ratio
    #btaglr_bdt = cfg.Analyzer(
    #    MECoreAnalyzers.BTagLRAnalyzer,
    #    'btaglr_bdt',
    #    _conf = python_conf,
    #    btagAlgo = "btagBDT"
    #)

    #calculates the b-tag likelihood ratio
    qglr = cfg.Analyzer(
        MECoreAnalyzers.QGLRAnalyzer,
        'qglr',
        _conf = python_conf
    )

    #assigns the ME category based on leptons, jets and the bLR
    mecat = cfg.Analyzer(
        MECoreAnalyzers.MECategoryAnalyzer,
        'mecat',
        _conf = python_conf
    )

    #performs W-tag calculation on pairs of untagged jets
    wtag = cfg.Analyzer(
        MECoreAnalyzers.WTagAnalyzer,
        'wtag',
        _conf = python_conf
    )

    subjet_analyzer = cfg.Analyzer(
        MECoreAnalyzers.SubjetAnalyzer,
        'subjet',
        _conf = python_conf
    )

    #multiclass_analyzer = cfg.Analyzer(
    #    MECoreAnalyzers.MulticlassAnalyzer,
    #    'multiclass',
    #    _conf = conf
    #)

    #Calls the C++ MEM integrator with good_jets, good_leptons and
    #the ME category
    mem_analyzer = cfg.Analyzer(
        MECoreAnalyzers.MEAnalyzer,
        'mem',
        _conf = python_conf
    )

    #compute joint likelihood ratio
    jointlikelihood_ana = cfg.Analyzer(
        MECoreAnalyzers.JointLikelihoodAnalyzer,
        'joint_likelihood',
        _conf = python_conf,
        _analysis_conf = analysis_cfg,
        #only run JLR computation on the ttH sample
        do_jlr = sample_name in ["ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8"]
    )

    # computes input for NN (training or prediction)
    NN_ana = cfg.Analyzer(
        MECoreAnalyzers.NNAnalyzer,
        'NN_input',
        _conf = python_conf,
        _analysis_conf = analysis_cfg,
        framework = "nanoAOD",
        training = True,
        boosted = False
    )

    gentth_pre = cfg.Analyzer(
        MECoreAnalyzers.GenTTHAnalyzerPre,
        'gentth_pre',
        _conf = python_conf
    )

    gentth = cfg.Analyzer(
        MECoreAnalyzers.GenTTHAnalyzer,
        'gentth',
        _conf = python_conf
    )

    mva = cfg.Analyzer(
        MECoreAnalyzers.MVAVarAnalyzer,
        'mva',
        _conf = python_conf
    )

    treevar = cfg.Analyzer(
        MECoreAnalyzers.TreeVarAnalyzer,
        'treevar',
        _conf = python_conf
    )
    memory_ana = cfg.Analyzer(
        MECoreAnalyzers.MemoryAnalyzer,
        'memory',
        _conf = python_conf
    )
    counter_final = cfg.Analyzer(
        MECoreAnalyzers.CounterAnalyzer,
        'counter_final',
        _conf = python_conf,
        counter_name = "_final",
    )
    import TTH.MEAnalysis.metree

    #Make the final output tree producer
    from TTH.MEAnalysis.metree import getTreeProducer
    treeProducer = getTreeProducer(python_conf)

    # definition of a sequence of analyzers,
    # the analyzers will process each event in this order

    if python_conf.general["boosted"] == False:
        sequence = cfg.Sequence([
            counter,
            # memory_ana,
            evtid_filter,
            #prefilter,
            evs,
            #After this, the event object has been created
            lumilist_ana,
            metfilter_ana,
            #puweight_ana, #possible to recompute the PU weight on the fly by uncommenting
            gentth_pre,
            pvana,
            trigger,
            counter_trg,
            leps,
            counter_lep,
            jets,
            #btagweight,
            counter_jet,
            #triggerSF,
            btaglr,
            counter_blr,
            #btaglr_bdt,
            #qglr,
            wtag,
            mecat,
            #subjet_analyzer,
            genrad,
            gentth,
            #multiclass_analyzer,
            mem_analyzer,
            mva,
            treevar,

            #Write the output tree
            treeProducer,
            counter_final,
        ])
    else:
        sequence = cfg.Sequence([
            counter,
            # memory_ana,
            evtid_filter,
            #prefilter,
            evs,
            boost,
            #After this, the event has been created
            lumilist_ana,
            metfilter_ana,
            #puweight_ana,
            gentth_pre,
            pvana,
            trigger,
            counter_trg,
            leps,
            counter_lep,
            jets,
            #btagweight,
            counter_jet,
            #triggerSF,
            btaglr,
            counter_blr,
            #btaglr_bdt,
            #qglr,
            wtag,
            mecat,
            subjet_analyzer,
            #btagweightsubjet,
            genrad,
            gentth,
            #multiclass_analyzer,
            mem_analyzer,
            mva,
            treevar,

            #Write the output tree
            treeProducer,
            counter_final,
        ])

    #Book the output file
    from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
    output_service = cfg.Service(
        TFileService,
        'outputfile',
        name="outputfile",
        fname='tree.root',
        option='recreate'
    )

    comp_cls = cfg.MCComponent
    if schema == "data":
        comp_cls = cfg.DataComponent

    comp = comp_cls(
        sample_name,
        files = files,
        tree_name = step1_tree_name, #DS requires change to ../../PhysicsTools/HeppyCore/python/framework/config.py
    )

    #from PhysicsTools.HeppyCore.framework.chain import Chain
    heppy_config = cfg.Config(
        #Run across these inputs
        components = [comp],

        #Using this sequence
        sequence = sequence,

        #save output to these services
        services = [output_service],

        #This defines how events are loaded
        #BufferedChain should be faster, but is kind of hacky
        events_class = BufferedChain
        #events_class = Chain
    )

    #Configure the number of events to run
    from PhysicsTools.HeppyCore.framework.looper import Looper

    kwargs = {}
    if python_conf.general.get("eventWhitelist", None) is None and not (numEvents is None):
        kwargs["nEvents"] = numEvents
    kwargs["firstEvent"] = firstEvent
    looper = Looper(
        'Loop_'+an_sample.name if len(output_name) == 0 else output_name,
        heppy_config,
        nPrint = 0,
        **kwargs
    )

    LOG_MODULE_NAME.info("Running looper")
    #execute the code
    looper.loop()
    LOG_MODULE_NAME.info("Looper done")
    
    tf = looper.setup.services["outputfile"].file
    #tf.cd()
    #ts = ROOT.TNamed("config", conf_to_str(python_conf))
    #ts.Write("", ROOT.TObject.kOverwrite)

    #write the output
    LOG_MODULE_NAME.info("writing the looper output to {0}".format(looper.name))
    looper.write()
    
    return looper.name, files

if __name__ == "__main__":   
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    if len(sys.argv) == 1:
        print "Call signature:"
        print "  {0} analysis.cfg".format(sys.argv[0])
        print "Please provide a path to an analysis configuration, e.g. in data/default.cfg"
        print "Exiting..."
        sys.exit(0)
    an = analysisFromConfig(sys.argv[1])

    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        choices=[samp.name for samp in an.samples],
        required=True
    )
    parser.add_argument(
        '--numEvents',
        action="store",
        help="Number of events to process",
        default=10000,
    )
    parser.add_argument(
        '--files',
        action="store",
        help="list of files to process",
        default=None,
        required=False
    )
    parser.add_argument(
        '--loglevel',
        action="store",
        help="log level",
        choices=["ERROR", "INFO", "DEBUG"],
        default="INFO",
        required=False
    )
    args = parser.parse_args(sys.argv[2:])

    

    if args.files:
        files = args.files.split(",")
    else:
        files = []
    print an
    looper_dir, files = main(an, sample_name=args.sample, numEvents=args.numEvents, files=files, loglevel = args.loglevel)

#    import TTH.MEAnalysis.counts as counts
#    counts.main(files, "{0}/tree.root".format(looper_dir))
