from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.general["passall"] = False
Conf.leptons["selection"] = lambda event: event.is_fh 
Conf.general["systematics"] = ["nominal"]
Conf.jets["untaggedSelection"] = "btagCSV"
Conf.mem["calcME"] = True
Conf.mem["selection"] = lambda event: (
    event.is_fh  and event.ht>450
    and event.cat in ["cat7","cat8","cat9","cat10","cat11","cat12"]
)
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
