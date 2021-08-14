from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.mem["calcME"] = True
Conf.mem["methodsToRun"] = [
    "SL_2w2h2t",
]
Conf.general["systematics"] = [
    "nominal",
    "TotalUp",
    "TotalDown"
]
Conf.mem["enabled_systematics"] = [
    "nominal",
    "TotalUp",
    "TotalDown",
]
