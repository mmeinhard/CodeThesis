import TTH.Plotting.Helpers.CompareDistributionsHelpers as compare_utils
from TTH.Plotting.Helpers.CompareDistributionsHelpers import combinedPlot, plot
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.sparse import save_hdict
import os, sys

import TTH.MEAnalysis.MEAnalysis_cfg_heppy as cfg

import ROOT
ROOT.TH1.SetDefaultSumw2(True)

btag_weights_suff = [
    b+"_"+a for a in ["cferr1", "cferr2", "hf", "hfstats1", "hfstats2", "jes", "lf", "lfstats1", "lfstats2"] for b in ["up", "down"]
]

btag_weights_csv = ["btagWeightCSV_" + suff for suff in btag_weights_suff]
btag_weights_cmva = ["btagWeightCMVAV2_" + suff for suff in btag_weights_suff]

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--cfg', action="store", help="path to analysis configuration", required=True)
    args = parser.parse_args()

    analysis = analysisFromConfig(args.cfg)

    DATASETPATH = os.environ["DATASETPATH"]
    prefix, sample_name = get_prefix_sample(DATASETPATH)
    FILE_NAMES = os.environ["FILE_NAMES"].split()
    
    sample = analysis.get_sample(sample_name)

    combinedPlot(
        "numJets",
        [
            plot("sl", "numJets", "is_sl", "sample"),
            plot("dl", "numJets", "is_dl", "sample"),
        ],
        10,
        0,
        10,
    )

    combinedPlot(
        "nBCSVM",
        [
            plot("sl", "nBCSVM", "is_sl", "sample"),
            plot("dl", "nBCSVM", "is_dl", "sample"),
            plot("sl_j4", "nBCSVM", "is_sl && numJets==4", "sample"),
            plot("sl_j5", "nBCSVM", "is_sl && numJets==5", "sample"),
            plot("sl_jge6", "nBCSVM", "is_sl && numJets>=6", "sample"),
            plot("sl_jge6_tge4", "nBCSVM", "is_sl && numJets>=6 && nBCSVM>=4", "sample"),
        ],
        10,
        0,
        10,
    )

    combinedPlot(
        "nBCMVAM",
        [
            plot("sl", "nBCMVAM", "is_sl", "sample"),
            plot("dl", "nBCMVAM", "is_dl", "sample"),
            plot("sl_j4", "nBCMVAM", "is_sl && numJets==4", "sample"),
            plot("sl_j5", "nBCMVAM", "is_sl && numJets==5", "sample"),
            plot("sl_jge6", "nBCMVAM", "is_sl && numJets>=6", "sample"),
            plot("sl_jge6_tge4", "nBCMVAM", "is_sl && numJets>=6 && nBCSVM>=4", "sample"),
        ],
        10,
        0,
        10,
    )

    combinedPlot(
        "jets_pt_0",
        [
            plot("sl", "jets_pt[0]", "is_sl", "sample"),
        ],
        100,
        0,
        400,
    )

    combinedPlot(
        "jets_eta_0",
        [
            plot("sl", "jets_eta[0]", "is_sl", "sample"),
        ],
        100,
        -5,
        5,
    )

    combinedPlot(
        "leps_pt_0",
        [
            plot("sl", "leps_pt[0]", "is_sl", "sample"),
            plot("dl", "leps_pt[0]", "is_dl", "sample"),
        ],
        100,
        0,
        300,
    )

    combinedPlot(
        "leps_pdgId_0",
        [
            plot("sl", "leps_pdgId[0]", "is_sl", "sample"),
            plot("dl", "leps_pdgId[0]", "is_dl", "sample"),
        ],
        30,
        -15,
        15,
    )
    
    combinedPlot(
        "leps_pdgId_1",
        [
            plot("dl", "leps_pdgId[1]", "is_dl", "sample"),
        ],
        30,
        -15,
        15,
    )

    combinedPlot(
        "leps_pt_1",
        [
            plot("dl", "leps_pt[1]", "is_dl", "sample"),
        ],
        100,
        0,
        300,
    )

    combinedPlot(
        "jets_btagCSV",
        [
            plot("sl_all", "jets_btagCSV", "btagWeightCSV * (is_sl)", "sample"),
            plot("sl_b", "jets_btagCSV", "btagWeightCSV * (is_sl && abs(jets_hadronFlavour) == 5)", "sample"),
            plot("sl_c", "jets_btagCSV", "btagWeightCSV * (is_sl && abs(jets_hadronFlavour) == 4)", "sample"),
            plot("sl_l", "jets_btagCSV", "btagWeightCSV * (is_sl && abs(jets_hadronFlavour) != 5 && abs(jets_hadronFlavour) != 4)", "sample"),
        ],
        100,
        0,
        1,
    )

    combinedPlot(
        "jets_btagCMVA",
        [
            plot("sl_all", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl)", "sample"),
            plot("sl_b", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl && abs(jets_hadronFlavour) == 5)", "sample"),
            plot("sl_c", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl && abs(jets_hadronFlavour) == 4)", "sample"),
            plot("sl_l", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl && abs(jets_hadronFlavour) != 5 && abs(jets_hadronFlavour) != 4)", "sample"),
        ],
        100,
        -1,
        1,
    )

    combinedPlot(
        "btag_LR_4b_2b_btagCSV",
        [
            plot("sl_jge4", "btag_LR_4b_2b_btagCSV", "is_sl && numJets>=4", "sample"),
            plot("dl_jge4", "btag_LR_4b_2b_btagCSV", "is_dl && numJets>=4", "sample"),
        ],
        100,
        0,
        1,
    )

    combinedPlot(
        "btag_LR_4b_2b_btagCMVA",
        [
            plot("sl_jge4", "btag_LR_4b_2b_btagCMVA", "is_sl && numJets>=4", "sample"),
            plot("dl_jge4", "btag_LR_4b_2b_btagCMVA", "is_dl && numJets>=4", "sample"),
        ],
        100,
        0,
        1,
    )
    
    combinedPlot(
        "btag_LR_4b_2b_btagCMVA",
        [
            plot("sl_jge4", "btag_LR_4b_2b_btagCMVA", "is_sl && numJets>=4", "sample"),
            plot("dl_jge4", "btag_LR_4b_2b_btagCMVA", "is_dl && numJets>=4", "sample"),
        ],
        100,
        0,
        1,
    )

    files = {
        "sample": (map(getSitePrefix, FILE_NAMES), "tree")
    }
    print "mapping over files", files

    ret = compare_utils.createHistograms(
        files
    )

    ret2 = {}
    for (k,v) in ret.items():
        ret2[sample_name + "/" + k] = v

    save_hdict(
        "out.root",
        ret2
    )

