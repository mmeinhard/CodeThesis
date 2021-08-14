from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf
import copy

Conf.mem["calcME"] = True
Conf.mem["methodsToRun"] = [
    "SL_2w2h2t",
    "SL_2w2h2t_points_500",
    "SL_2w2h2t_points_1000",
    "SL_2w2h2t_points_2000",
    "SL_2w2h2t_points_3000",
    "SL_2w2h2t_points_4000",
]
Conf.mem_configs["SL_2w2h2t"].do_calculate = lambda ev, mcfg: (
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

Conf.mem_configs["SL_2w2h2t_points_500"] = copy.deepcopy(Conf.mem_configs["SL_2w2h2t"])
Conf.mem_configs["SL_2w2h2t_points_500"].ncalls = 500

Conf.mem_configs["SL_2w2h2t_points_1000"] = copy.deepcopy(Conf.mem_configs["SL_2w2h2t"])
Conf.mem_configs["SL_2w2h2t_points_1000"].ncalls = 1000

Conf.mem_configs["SL_2w2h2t_points_2000"] = copy.deepcopy(Conf.mem_configs["SL_2w2h2t"])
Conf.mem_configs["SL_2w2h2t_points_2000"].ncalls = 2000

Conf.mem_configs["SL_2w2h2t_points_3000"] = copy.deepcopy(Conf.mem_configs["SL_2w2h2t"])
Conf.mem_configs["SL_2w2h2t_points_3000"].ncalls = 3000

Conf.mem_configs["SL_2w2h2t_points_4000"] = copy.deepcopy(Conf.mem_configs["SL_2w2h2t"])
Conf.mem_configs["SL_2w2h2t_points_4000"].ncalls = 4000
