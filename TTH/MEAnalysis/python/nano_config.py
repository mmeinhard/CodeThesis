#Creates the era-dependent configuration for the NanoAOD postprocessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector

class NanoConfig:
    def __init__(self, setEra, jec=False, btag=False, pu=False, isData=False, run=None):
        ###################################################################################################
        if setEra == "80X":
            self.eraMC = "Run2_2016,run2_miniAOD_80XLegacy"
            self.eraData = "Run2_2016,run2_miniAOD_80XLegacy"
            self.conditionsMC = "auto:run2_mc"
            self.conditionsData = "auto:run2_data_relval"
            self.eraBtagSF = "2016"
            self.algoBtag = "csvv2"
            print "Using CMSSW 80X"
        elif setEra == "92X":
            self.eraMC = "Run2_2017,run2_nanoAOD_92X"
            self.eraData = "Run2_2017,run2_nanoAOD_92X"
            self.conditionsMC = "auto:phase1_2017_realistic"
            self.conditionsData = "auto:run2_data_relval"
            self.eraBtagSF = "2017"
            self.algoBtag = "csvv2"
            print "Using CMSSW 92X"
        #For RunIIFall17MiniAOD we need v1
        elif setEra == "94Xv1": 
            self.eraMC = "Run2_2017,run2_nanoAOD_94XMiniAODv1"
            self.eraData = "Run2_2017,run2_nanoAOD_94XMiniAODv1"
            self.conditionsMC = "94X_mc2017_realistic_v13"
            self.conditionsData = "94X_dataRun2_ReReco_EOY17_v6"
            self.eraBtagSF = "2017"
            self.algoBtag = "deepcsv"
            print "Using CMSSW 94X with v1 era"
        elif setEra == "94Xv2":
            self.eraMC = "Run2_2017,run2_nanoAOD_94XMiniAODv2"
            self.eraData = "Run2_2017,run2_nanoAOD_94XMiniAODv2"
            self.conditionsMC = "102X_mc2017_realistic_v7"
            self.conditionsData = "102X_dataRun2_v12"
            self.jecMC = "Fall17_17Nov2017_V32_MC"
            self.jecData = "Fall17_17Nov2017_V32_DATA"
            # self.jecMC = "Fall17_17Nov2017_V32_M<C"
            # self.jecData = "Fall17_17Nov2017_V32_DATA"
            self.eraBtagSF = "2017"
            self.algoBtag = "deepcsv"
            self.redoJEC = True
            self.redoJECData = True
            self.puWeight = 'puAutoWeight_2017'
            print "Using CMSSW 102X with v2 era"
        elif setEra == "102Xv1":
            self.eraMC = "Run2_2018,run2_nanoAOD_102Xv1"
            self.eraData = "Run2_2018,run2_nanoAOD_102Xv1"
            self.conditionsMC = "102X_upgrade2018_realistic_v19"
            self.conditionsData = "102X_dataRun2_Sep2018Rereco_v1"
            self.jecMC = "Autumn18_V19_MC"
            self.jecData = "Autumn18_V19_DATA"
            # self.jecMC = "Fall17_17Nov2017_V32_M<C"
            # self.jecData = "Fall17_17Nov2017_V32_DATA"
            self.eraBtagSF = "2018"
            self.algoBtag = "deepcsv"
            self.redoJEC = True
            self.redoJECData = True
            self.increaseHEMUnc = True
            self.puWeight = 'puAutoWeight_2018'
            print "Using CMSSW 102X with v2 era"


        
        imports = []
        if jec  and not isData:
            #imports += [
            #    ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties', 'jetmetUncertainties2017All')
            #]
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertaintiesSubjets', 'jetmetUncertainties2017HTTSubjetAll')
            ]
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertaintiesSubjets', 'jetmetUncertainties2017AK8PuppiSubjetAll')
            ]


        if btag:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer','btagSFProducer')
            ]
        if pu:
            imports += [
                ('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer','puAutoWeight_2017')
            ]

        self.json = None #Intended use: Skimming
        self.cuts = None #Intended use: Skimming
        self.branchsel = None #Intended use: Skimming
        
        from importlib import import_module
        import sys

        #Imports the various nanoAOD postprocessor modules
        self.modules = []
        for mod, names in imports: 
            import_module(mod)
            obj = sys.modules[mod]
            selnames = names.split(",")
            for name in dir(obj):
                if name[0] == "_": continue
                if name in selnames:
                    print "Loading %s from %s " % (name, mod)
                    if name == "btagSFProducer":
                        self.modules.append(getattr(obj,name)(self.eraBtagSF, self.algoBtag, "Jet"))
                        self.modules.append(getattr(obj,name)(self.eraBtagSF, self.algoBtag, "SubJet"))
                        self.modules.append(getattr(obj,name)(self.eraBtagSF, self.algoBtag, "HTTV2Subjets"))
                    else:
                        self.modules.append(getattr(obj,name)())


        if jec:
            self.modules.append(
                createJMECorrector(
                    isMC = (not isData),
                    dataYear = self.eraBtagSF,
                    runPeriod = run,
                    jesUncert = "All",
                    redojec = self.redoJEC,
                    metBranchName = "METFixEE2017"
                    #increaseHEMUnc = self.increaseHEMUnc,
                )()
            )

        print "======================================================================"
        print "====================== CONFIG SETTINGS ==============================="
        for attribute in self.__dict__:
            if attribute != "modules":
                print "   ",attribute,"=",getattr(self, attribute)
        print "----------------------------------------------------------------------"
        print "    Will use modules:"
        for mod in self.modules:
            print "       ", mod
        print "======================================================================"
