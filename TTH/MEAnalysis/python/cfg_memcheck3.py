from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.mem["calcME"] = True
Conf.mem["methodsToRun"] = [
    "SL_2w2h2t",
    "SL_2w2h2t_sudakov",
    "SL_2w2h2t_recoil",
    "SL_2w2h2t_notag",
    "SL_2w2h2t_nosym",
]
Conf.mem_configs["SL_2w2h2t"].do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
Conf.mem_configs["SL_2w2h2t_sudakov"].do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)

Conf.mem_configs["SL_2w2h2t_recoil"].do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)

Conf.general["systematics"] = [
    "nominal",
]
Conf.mem["enabled_systematics"] = [
    "nominal",
]
