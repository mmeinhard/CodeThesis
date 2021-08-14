from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.mem["calcME"] = True
Conf.general["systematics"] = ["nominal"]
Conf.mem["selection"] = lambda event: (
    (event.is_sl or event.is_dl) and 
    (event.numJets>=4 and event.nBDeepCSVM >= 3)
    and event.cat != "NOCAT"
)
