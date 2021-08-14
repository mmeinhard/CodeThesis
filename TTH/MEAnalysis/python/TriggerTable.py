'''
Trigger defintions:

Set different trigger configurations containing one or more HLT paths. If more than on is given 
for a configuration the or of all is used.

Possibility to define dataset sprecific configurations. Define configuration with name [ttH_configname]
that is used as default. For dataset specific variatitions add element to dict with [ttH_configname]:[datasetname].
The [datasetname] sould be true for the comparison of [datasetname] in cfg_comp.name (the name set in e.g. in 
default.cfg). For this dataset the default configuration will be replaced.
'''

triggerTable = {
    "ttH_SL_el" : [
        #"HLT_Ele35_WPTight_Gsf",
        "HLT_Ele32_WPTight_Gsf_L1DoubleEG", 
        #("and" , "Flag_ele32DoubleL1ToSingleL1"),
        "HLT_Ele28_eta2p1_WPTight_Gsf_HT150",
    ],
    "ttH_SL_mu" : [
        #"HLT_IsoMu24_eta2p1",
        "HLT_IsoMu27",
    ],
    "ttH_DL_mumu" : [
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
    ],
    "ttH_DL_elmu" : [
        "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_DL_elel" : [
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_FH_RunCF" : [
        "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5",
        "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0",
        "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
    ],
    "ttH_FH_RunCF:JetHT" : [
        "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5",#Prescaled in RunC < 301000
        "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
        ("and not","HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0")
    ],
    "ttH_FH_RunCF:BTagCSV" : [
        "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0"#Prescaled in RunC < 301000
    ],
    "FH_control" : [
        "HLT_HT300PT30_QuadJet_75_60_45_40",#RunB only
        "HLT_PFHT300PT30_QuadPFJet_75_60_45_40",#RunC ->
        "HLT_PFHT380_SixPFJet32",#RunC ->
        "HLT_PFHT430_SixPFJet40",#RunC ->
    ],
    "FH_other" : [
        "HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2",
    ],
    "FH_JetHT" : [
        "HLT_PFHT1050",
        "HLT_PFHT780",
        "HLT_PFHT680",
        "HLT_PFHT510",
        "HLT_PFHT590",
        "HLT_PFHT430",
        "HLT_PFJet500",
    ],
    "VBF" : [
        "HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1",
        "HLT_QuadPFJet103_88_75_15_DoubleBTagCSV_p013_p08_VBF1",
        "HLT_QuadPFJet105_90_76_15_DoubleBTagCSV_p013_p08_VBF1",
        "HLT_QuadPFJet111_90_80_15_DoubleBTagCSV_p013_p08_VBF1",
        "HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2",
        "HLT_QuadPFJet103_88_75_15_BTagCSV_p013_VBF2",
        "HLT_QuadPFJet105_88_76_15_BTagCSV_p013_VBF2",
        "HLT_QuadPFJet111_90_80_15_BTagCSV_p013_VBF2",
    ],
    #Triggers changed names between RunB and RunC
    #TODO: Include functionality differently named triggers are written to the same output branch?
    "ttH_FH_RunB" : [
        "HLT_PFHT430_SixJet40_BTagCSV_p080",
        "HLT_PFHT380_SixJet32_DoubleBTagCSV_p075",
        "HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07"
    ],
    "ttH_FH_RunB:JetHT" : [
        "HLT_PFHT430_SixJet40_BTagCSV_p080",
        "HLT_PFHT380_SixJet32_DoubleBTagCSV_p075",
        ("and not","HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07")
    ],
    "ttH_FH_RunB:BTagCSV" : [
        "HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07"
    ],
}



'''
ttH paths from https://github.com/jpata/cmssw/blob/vhbbHeppy80X_july31/VHbbAnalysis/Heppy/python/TriggerTable.py#L218-L247
'''

triggerTable2016 = {

    "ttH_SL_el" : [
        "HLT_Ele27_WPTight_Gsf",
    ],
    "ttH_SL_mu" : [
        "HLT_IsoMu24",
        "HLT_IsoTkMu24",
    ],
    "ttH_DL_mumu" : [
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",
    ],
    "ttH_DL_elmu" : [
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
#Disabled as not there in nanoAOD for data
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_DL_elel" : [
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
    ],
    "ttH_FH" : [
        "HLT_PFHT450_SixJet40_BTagCSV_p056",
        "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056",
    ],
    "ttH_FH_prescaled" : [
        "HLT_PFHT450_SixJet40",
        "HLT_PFHT400_SixJet30",
    ],

}
