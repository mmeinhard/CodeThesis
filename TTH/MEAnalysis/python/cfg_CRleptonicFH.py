from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.leptons["selection"] = lambda event: event.is_sl #DS                                                                                                                                      
Conf.general["systematics"] = ["nominal"]
Conf.mem["calcME"] = False #DS                                                                                                                                                                 
Conf.mem["methodsToRun"] = [
    #"DL_0w2h2t",                                                                                                                                                                              
    #"SL_0w2h2t",                                                                                                                                                                              
    #"SL_1w2h2t",                                                                                                                                                                              
    #"SL_2w2h1t_l",                                                                                                                                                                            
    #"SL_2w2h1t_h",                                                                                                                                                                            
    "SL_2w2h2t",
    #"SL_2w2h2t_1j",                                                                                                                                                                           
    #"SL_2w2h2t_sj",                                                                                                                                                                           
]
Conf.mem["enabled_systematics"] = ["nominal"]
Conf.mem["selection"] = lambda event: event.is_fh #(                                                                                                                                           
#        ((event.is_sl or event.is_dl) and event.nominal_event.numJets>=4 and event.nominal_event.nBCSVM >= 4)                                                                                 
#)        
