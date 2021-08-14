from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.general["passall"] = True
Conf.leptons["force_isFH"] = True
Conf.leptons["selection"] = lambda event: event.is_sl
"""
Conf.mem["selection"] = lambda event: (event.is_fh and event.ht>450 
                                       and event.cat in ["cat7","cat8","cat9","cat10","cat11","cat12"]
                                       #and event.cat in ["cat8"]
                                       )
"""
#Conf.jets["untaggedSelection"] = "btagLR" #or "btagCSV" #DS needs to be set in MEAnalysis_cfg_heppy!!!
Conf.jets["NJetsForBTagLR"] = 9
Conf.jets["btagAlgo"] = "btagCSV"


Conf.mem["calcME"] = False
