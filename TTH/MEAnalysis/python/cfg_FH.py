import os
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf
from ROOT import MEM

# integrator options
#for k in ["FH_4w2h2t", "FH_3w2h2t", "FH_4w2h1t", "FH_0w2h2t", "FH_0w2h1t", "FH_0w1h2t"]:
"""
for k, v in Conf.mem_configs.items():
    Conf.mem_configs[k].cfg.do_prefit = 0 #selects perms based on highest MEprob (Minimisation)
    Conf.mem_configs[k].cfg.do_perm_filtering = 0 #does runtime pruning of permutations
    Conf.mem_configs[k].cfg.abs = 0.0 #the absolute tolerance for cuba
    Conf.mem_configs[k].cfg.rel = 0.02 #the relative tolerance for cuba
    Conf.mem_configs[k].cfg.two_stage = 1 #two_stage integration, not implemented
    Conf.mem_configs[k].cfg.niters = 5 #max number of 2nd-stage iterations, not implemented
    #print "mem_configs[",k,"].cfg.rel = ",Conf.mem_configs[k].cfg.rel 
"""
#other options
Conf.general["passall"] = False
Conf.trigger["calcFHSF"] = False
Conf.leptons["selection"] = lambda event: event.is_fh 

Conf.mem["selection"] = lambda event: (event.is_fh and event.ht>450 
                                       and event.cat in ["cat7","cat8","cat9","cat10","cat11","cat12"]
                                       #and event.cat in ["cat8"]
                                       )

Conf.jets["untaggedSelection"] = "btagCSV" # or "btagLR" #DS need to set bLR in MEAnalysis_cfg_heppy!!!
Conf.jets["NJetsForBTagLR"] = 9
Conf.jets["btagAlgo"] = "btagCSV"
Conf.jets["btagWP"] = "CSVM"

Conf.mem["calcME"] = False
Conf.mem["weight"] = 0.02 #k in Psb = Ps/(Ps+k*Pb)    
Conf.mem["methodsToRun"] = [
            #"SL_0w2h2t",                 #[0]
            #"DL_0w2h2t",                 #[1]
            #"SL_1w2h2t",                 #[2]
            #"SL_2w2h1t_l",               #[3]
            #"SL_2w2h1t_h",               #[4]
            #"SL_2w2h2t",                 #[5]
            #"SL_2w2h2t_memLR",           #[6]
            #"SL_0w2h2t_memLR",           #[7]
            #"DL_0w2h2t_Rndge4t",         #[8]
            #"SL_2w2h2t_sj",              #[9]
            #"SL_0w2h2t_sj",              #[10]
            "FH_4w2h2t", #8j,4b & 9j,4b   #[11]
            "FH_3w2h2t", #7j,4b           #[12]
            "FH_4w2h1t", #all 3b cats     #[13]
            #"FH_4w1h2t", #7j,3b & 8j,3b & 9j,3b
            #"FH_3w2h1t", #7j,3b & 8j,3b (int. 1 jet)
            #"FH_0w2w2h2t", #all 4b cats
            #"FH_1w1w2h2t", #all 4b cats
            #"FH_0w0w2h2t", #all 4b cats  #[14]
            #"FH_0w0w2h1t", #all cats     #[15]
            #"FH_0w0w1h2t"  #all cats     #[16]   *********DO NOT RUN!!!********* 
        ]

Conf.general["verbosity"] = [
            #"eventboundary",
            #"input",
            #"matching",
            #"trigger",
            #"jets",
            #"gen", #print out gen-level info
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput", #info about particles used for MEM input
            #"commoninput", #print out inputs for CommonClassifier
            #"commonclassifier",
            #"systematics"
       ]

#Conf.general["systematics"] = ["nominal"]
#Conf.general["transferFunctionsPickle"] = os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_ttbar.pickle"
#Conf.general["transferFunctions_sj_Pickle"] = os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_sj_ttbar.pickle"
