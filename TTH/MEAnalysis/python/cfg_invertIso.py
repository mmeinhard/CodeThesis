from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.mem["calcME"] = False
Conf.leptons["selection"] = lambda event: event.is_sl and abs(event.good_leptons[0].pdgId) == 13
Conf.leptons["mu"]["SL"]["isoinverted"] = True
Conf.leptons["mu"]["veto"]["isoinverted"] = True