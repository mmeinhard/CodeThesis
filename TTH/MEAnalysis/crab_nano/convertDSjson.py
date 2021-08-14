import json

datasets = {}
datasets2 = {}


me_cfgs = {
    "default": "cfg_noME.py",
    "cMVA": "cfg_noME.py",
    "nome": "cfg_noME.py",
    "leptonic": "cfg_noME.py",
    "hadronic": "cfg_noME.py",
}


datasets.update({
    'ttHTobb': {
        "ds": '/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 10,
        "runtime": 10,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'ttHToNonbb': {
        "ds": '/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 20,
        "runtime": 10,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_inc': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'ttbb': {
        "ds": '/ttbb_4FS_OpenLoops_13TeV-sherpa/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_isr_up': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_isr_down1': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_isr_down2': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_fsr_up1': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_fsr_up2': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_fsr_down': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-fsrdown-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
   
    'TTbar_tune_up1': {
        "ds": '/TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_tune_up2': {
        "ds": '/TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_tune_down1': {
        "ds": '/TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_tune_down2': {
        "ds": '/TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_hdamp_up1': {
        "ds": '/TT_hdampUP_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_hdamp_up2': {
        "ds": '/TT_hdampUP_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_hdamp_down1': {
        "ds": '/TT_hdampDOWN_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_hdamp_down2': {
        "ds": '/TT_hdampDOWN_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_sl': {
        "ds": '/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 20,
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_dl': {
        "ds": '/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 20,
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script.sh'
    },
    
   'ww1': {
       "ds": '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ww2': {
       "ds": '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wz1': {
       "ds": '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wz2': {
       "ds": '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zz1': {
       "ds": '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zz2': {
       "ds": '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttw_wlnu1': {
       "ds": '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttw_wlnu2': {
       "ds": '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttw_wqq': {
       "ds": '/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttz_zllnunu1': {
       "ds": '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttz_zllnunu2': {
       "ds": '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttz_zqq': {
       "ds": '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   
   'wjets': {
       "ds": '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   
   # 'wjets_ht_100_200': {
   #     "ds": '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 
   # 'wjets_ht_200_400': {
   #     "ds": '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'wjets_ht_400_600': {
   #     "ds": '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'wjets_ht_600_800': {
   #     "ds": '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 
   # 'wjets_ht_800_1200': {
   #     "ds": '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'wjets_ht_1200_2500': {
   #     "ds": '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },


   # 'wjets_ht_2500_inf': {
   #     "ds": '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },

   'dy_10_50': {
       "ds": '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 80,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'dy_50_inf1': {
       "ds": '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 80,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'dy_50_inf2': {
       "ds": '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 80,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   
   'st_t': {
       "ds": '/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'stbar_t': {
       "ds": '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'st_tw': {
       "ds": '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'stbar_tw': {
       "ds": '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'st_s': {
       "ds": '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },


    'QCD300': {
        "ds": '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 250,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD300_ext1': {
        "ds": '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 250,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD500': {
        "ds": '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 250,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD500_ext1': {
        "ds": '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 250,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD700': {
        "ds": '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD700_ext1': {
        "ds": '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1000': {
        "ds": '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1000_ext1': {
        "ds": '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1500': {
        "ds": '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 60,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD2000': {
        "ds": '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 60,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
})


datasets2.update({
    'ttHTobb': {
        "ds": '/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 10,
        "runtime": 10,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'ttHToNonbb': {
        "ds": '/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 20,
        "runtime": 10,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_inc': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_isr_up': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_isr_down1': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_isr_down2': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_fsr_up1': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_fsr_up2': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_fsr_down': {
        "ds": '/TT_TuneCUETP8M2T4_13TeV-powheg-fsrdown-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 20,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },

    'TTbar_sl': {
        "ds": '/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 20,
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script.sh'
    },
    
    'TTbar_dl': {
        "ds": '/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 20,
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script.sh'
    },
    
   'ww1': {
       "ds": '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ww2': {
       "ds": '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #7.0m events
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wz1': {
       "ds": '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 100, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wz2': {
       "ds": '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 100, #3.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zz1': {
       "ds": '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zz2': {
       "ds": '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttw_wlnu1': {
       "ds": '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttw_wlnu2': {
       "ds": '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttw_wqq': {
       "ds": '/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 10, #0.8m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttz_zllnunu1': {
       "ds": '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttz_zllnunu2': {
       "ds": '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20,
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'ttz_zqq': {
       "ds": '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 8, #0.75m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets100_1': {
       "ds": '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 100, #30m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets100_2': {
       "ds": '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 100, #40m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets200_1': {
       "ds": '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 100, #15m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets200_2': {
       "ds": '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 100, #20m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets400_1': {
       "ds": '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #2m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets400_2': {
       "ds": '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #6m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets600': {
       "ds": '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #15m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets800': {
       "ds": '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #6m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets1200': {
       "ds": '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #7m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'wjets2500': {
       "ds": '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #2m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m5_100': {
       "ds": '/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #9m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m5_200': {
       "ds": '/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #2m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m5_400': {
       "ds": '/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #2m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m5_600': {
       "ds": '/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #2m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_100': {
       "ds": '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #8m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_200': {
       "ds": '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #9m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_400': {
       "ds": '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #9m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_600': {
       "ds": '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 40, #8m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_800': {
       "ds": '/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #3m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_1200': {
       "ds": '/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #0.6m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'zjets_m50_2500': {
       "ds": '/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 20, #0.4m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },


   # 'wjets_ht_100_200': {
   #     "ds": '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 
   # 'wjets_ht_200_400': {
   #     "ds": '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'wjets_ht_400_600': {
   #     "ds": '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'wjets_ht_600_800': {
   #     "ds": '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 
   # 'wjets_ht_800_1200': {
   #     "ds": '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'wjets_ht_1200_2500': {
   #     "ds": '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },


   # 'wjets_ht_2500_inf': {
   #     "ds": '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },

   # 'dy_10_50': {
   #     "ds": '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 20,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 'dy_50_inf': {
   #     "ds": '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
   #     "maxlumis": -1,
   #     "perjob": 40,
   #     "runtime": 10,
   #     "mem_cfg": me_cfgs["leptonic"],
   #     "script": 'heppy_crab_script.sh'
   # },
   # 
   'st_t': {
       "ds": '/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #6.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'stbar_t': {
       "ds": '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #4.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'st_tw': {
       "ds": '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'stbar_tw': {
       "ds": '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'st_s': {
       "ds": '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #1.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["leptonic"],
       "script": 'heppy_crab_script.sh'
   },
   'st_s_inc': {
       "ds": '/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
       "maxlumis": -1,
       "perjob": 50, #3.0m events total
       "runtime": 10,
       "mem_cfg": me_cfgs["hadronic"],
       "script": 'heppy_crab_script.sh'
   },

    'QCD300': {
        "ds": '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD300_ext1': {
        "ds": '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD500': {
        "ds": '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD500_ext1': {
        "ds": '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD700': {
        "ds": '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD700_ext1': {
        "ds": '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 150,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1000': {
        "ds": '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 60,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1000_ext1': {
        "ds": '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 60,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1500': {
        "ds": '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD2000': {
        "ds": '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 60,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },

    'QCDHT300bEnriched': {
        "ds": '/QCD_bEnriched_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT500bEnriched': {
        "ds": '/QCD_bEnriched_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT700bEnriched': {
        "ds": '/QCD_bEnriched_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT1000bEnriched': {
        "ds": '/QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 60,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT1500bEnriched': {
        "ds": '/QCD_bEnriched_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT2000bEnriched': {
        "ds": '/QCD_bEnriched_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },

    'QCDHT300BGenFilter': {
        "ds": '/QCD_HT300to500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT500BGenFilter': {
        "ds": '/QCD_HT500to700_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT700BGenFilter': {
        "ds": '/QCD_HT700to1000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT1000BGenFilter': {
        "ds": '/QCD_HT1000to1500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 80,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT1500BGenFilter': {
        "ds": '/QCD_HT1500to2000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCDHT2000BGenFilter': {
        "ds": '/QCD_HT2000toInf_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 50,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'WJetsToQQ600': {
        "ds": '/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 20, #1.0m events total
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'WJetsToQQ180': {
        "ds": '/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', #GS has TuneCUETP8M1 although not in name
        "maxlumis": -1,
        "perjob": 150, #22.4m events total
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'ZJetsToQQ600': {
        "ds": '/ZJetsToQQ_HT600toInf_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100, #1.0m events total
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'WWTo4Q': {
        "ds": '/WWTo4Q_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 20, #2.0m events total
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'ZZTo4Q': {
        "ds": '/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        "maxlumis": 25000, #~5m events
        "perjob": 20, #30.4m events total
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
})




uniqueDSs = set(datasets.keys()+datasets2.keys())

print uniqueDSs

QCDdict = {}
ttbardict = {}
ttHdict = {}
otherbkgdict = {}


for key in uniqueDSs:
    if datasets2.has_key(key):
        ds = datasets2[key] 
    else:
        ds = datasets[key]

    if "QCD" in key:
        QCDdict[key] = ds
    elif "TTbar" in key or ( "tt" in key and not "ttH" in key):
        ttbardict[key] = ds
    elif "ttH" in key or "tth" in key:
        ttHdict[key] = ds
    else:
        otherbkgdict[key] = ds
        
for name, dict_ in [("QCD",QCDdict), ("ttbar",ttbardict), ("ttH",ttHdict), ("otherbkg",otherbkgdict)]:
    with open(name+".json", "w") as outfile:
        json.dump(dict_, outfile, sort_keys=True,
                   indent=4, separators=(',', ': '))
            
