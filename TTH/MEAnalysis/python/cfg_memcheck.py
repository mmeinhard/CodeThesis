from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.mem["calcME"] = True
Conf.mem["methodsToRun"] = [
#    "DL_0w2h2t",
#    "SL_0w2h2t",
#    "SL_1w2h2t",
    "SL_2w2h2t",
#    "SL_2w2h2t_1j",
]
Conf.mem["enabled_systematics"] = ["nominal"]
Conf.mem["selection"] = lambda event: (
        ((event.is_sl or event.is_dl) and event.nominal_event.numJets>=6 and event.nominal_event.nBCSVM >= 4)
)
Conf.mem_configs["SL_1w2h2t"].do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 1 and
    ev.numJets >= 5
)
Conf.mem_configs["SL_0w2h2t"].do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 0 and
    ev.numJets >= 4
)
Conf.general["systematics"] = ["nominal"]
Conf.mem["enabled_systematics"] = [
    "nominal",
#    "TotalUp",
#    "TotalDown",
]
