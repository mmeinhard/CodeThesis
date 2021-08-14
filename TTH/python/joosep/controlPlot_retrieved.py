print "starting"
import logging
import multiprocessing

import math
import json

print "ROOT"
import ROOT
import logging

print "mpl"
import matplotlib
from matplotlib import rc
matplotlib.use('Agg')
if __name__== "__main__":
    matplotlib.use('PS')
import matplotlib.pyplot as plt

print "sys"
import sys, os, copy
import os.path
from collections import OrderedDict
import plotlib

print "plotlib"
from plotlib import escape_string, zero_error

print "rootpy"
import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt
import sklearn
import sklearn.metrics

print "done importing"
DO_PARALLEL = False

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    #("ttH_hcc", "tt+H(cc)"),
    #("ttH_hzz", "tt+H(ZZ)"),
    #("ttH_hww", "tt+H(WW)"),
    #("ttH_htt", "tt+H(tt)"),
    #("ttH_hgg", "tt+H(gg)"),
    #("ttH_hgluglu", "tt+H(gluglu)"),
    #("ttH_hzg", "tt+H(Zg)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
#    ("diboson", "diboson"),
#    ("stop", "single top"),
#    ("ttv", "tt+V"),
#    ("wjets", "w+jets"),
#    ("dy", "dy")
]

procs = [x[0] for x in procs_names]

syst_pairs = []
syst_pairs.extend([
    ("__CMS_btag_cferr1_2017Up", "__CMS_btag_cferr1_2017Down"),
    ("__CMS_btag_cferr2_2017Up", "__CMS_btag_cferr2_2017Down"),
    ("__CMS_btag_hf_2017Up", "__CMS_btag_hf_2017Down"),
    ("__CMS_btag_hfstats1_2017Up", "__CMS_btag_hfstats1_2017Down"),
    ("__CMS_btag_hfstats2_2017Up", "__CMS_btag_hfstats2_2017Down"),
    ("__CMS_btag_lf_2017Up", "__CMS_btag_lf_2017Down"),
    ("__CMS_btag_lfstats1_2017Up", "__CMS_btag_lfstats1_2017Down"),
    ("__CMS_btag_lfstats2_2017Up", "__CMS_btag_lfstats2_2017Down"),
    ("__CMS_scale_j_2017Up", "__CMS_scale_j_2017Down"),
    ("__CMS_effTrigger_dlUp", "__CMS_effTrigger_dlDown"),
    ("__CMS_effTrigger_eUp", "__CMS_effTrigger_eDown"),
    ("__CMS_effTrigger_mUp", "__CMS_effTrigger_mDown"),
    ("__CMS_eff_eUp", "__CMS_eff_eDown"),
    ("__CMS_eff_mUp", "__CMS_eff_mDown"),
    ("__CMS_ttHbb_FSR_2017Up", "__CMS_ttHbb_FSR_2017Down"),
    #("__CMS_ttHbb_FSR_ttbarOther_2017Up", "__CMS_ttHbb_FSR_ttbarOther_2017Down"),
    #("__CMS_ttHbb_FSR_ttbarPlus2B_2017Up", "__CMS_ttHbb_FSR_ttbarPlus2B_2017Down"),
    #("__CMS_ttHbb_FSR_ttbarPlusBBbar_2017Up", "__CMS_ttHbb_FSR_ttbarPlusBBbar_2017Down"),
    #("__CMS_ttHbb_FSR_ttbarPlusB_2017Up", "__CMS_ttHbb_FSR_ttbarPlusB_2017Down"),
    #("__CMS_ttHbb_FSR_ttbarPlusCCbar_2017Up", "__CMS_ttHbb_FSR_ttbarPlusCCbar_2017Down"),
    ("__CMS_ttHbb_ISR_2017Up", "__CMS_ttHbb_ISR_2017Down"),
    #("__CMS_ttHbb_ISR_ttbarOther_2017Up", "__CMS_ttHbb_ISR_ttbarOther_2017Down"),
    #("__CMS_ttHbb_ISR_ttbarPlus2B_2017Up", "__CMS_ttHbb_ISR_ttbarPlus2B_2017Down"),
    #("__CMS_ttHbb_ISR_ttbarPlusBBbar_2017Up", "__CMS_ttHbb_ISR_ttbarPlusBBbar_2017Down"),
    #("__CMS_ttHbb_ISR_ttbarPlusB_2017Up", "__CMS_ttHbb_ISR_ttbarPlusB_2017Down"),
    #("__CMS_ttHbb_ISR_ttbarPlusCCbar_2017Up", "__CMS_ttHbb_ISR_ttbarPlusCCbar_2017Down"),
    ("__CMS_ttHbb_scaleMuFUp", "__CMS_ttHbb_scaleMuFDown"),
    ("__CMS_ttHbb_scaleMuRUp", "__CMS_ttHbb_scaleMuRDown"),
    ("__CMS_res_j_2017Up", "__CMS_res_j_2017Down"),
    ("__CMS_scaleAbsoluteMPFBias_j_2017Up", "__CMS_scaleAbsoluteMPFBias_j_2017Down"),
    ("__CMS_scaleAbsoluteScale_j_2017Up", "__CMS_scaleAbsoluteScale_j_2017Down"),
    ("__CMS_scaleAbsoluteStat_jUp", "__CMS_scaleAbsoluteStat_jDown"),
    ("__CMS_scaleFlavorQCD_j_2017Up", "__CMS_scaleFlavorQCD_j_2017Down"),
    ("__CMS_scaleFragmentation_j_2017Up", "__CMS_scaleFragmentation_j_2017Down"),
    ("__CMS_scalePileUpDataMC_j_2017Up", "__CMS_scalePileUpDataMC_j_2017Down"),
    ("__CMS_scalePileUpPtBB_j_2017Up", "__CMS_scalePileUpPtBB_j_2017Down"),
    ("__CMS_scalePileUpPtEC1_j_2017Up", "__CMS_scalePileUpPtEC1_j_2017Down"),
    ("__CMS_scalePileUpPtRef_j_2017Up", "__CMS_scalePileUpPtRef_j_2017Down"),
    ("__CMS_scaleRelativeBal_j_2017Up", "__CMS_scaleRelativeBal_j_2017Down"),
    ("__CMS_scaleRelativeFSR_j_2017Up", "__CMS_scaleRelativeFSR_j_2017Down"),
    ("__CMS_scaleRelativeJEREC1_jUp", "__CMS_scaleRelativeJEREC1_jDown"),
    ("__CMS_scaleRelativePtBB_j_2017Up", "__CMS_scaleRelativePtBB_j_2017Down"),
    ("__CMS_scaleRelativePtEC1_jUp", "__CMS_scaleRelativePtEC1_jDown"),
    ("__CMS_scaleRelativeStatEC_jUp", "__CMS_scaleRelativeStatEC_jDown"),
    ("__CMS_scaleRelativeStatFSR_jUp", "__CMS_scaleRelativeStatFSR_jDown"),
    ("__CMS_scaleSinglePionECAL_j_2017Up", "__CMS_scaleSinglePionECAL_j_2017Down"),
    ("__CMS_scaleSinglePionHCAL_j_2017Up", "__CMS_scaleSinglePionHCAL_j_2017Down"),
    ("__CMS_scaleTimePtEta_jUp", "__CMS_scaleTimePtEta_jDown"),
    ("__CMS_ttHbb_PDF_2017Up", "__CMS_ttHbb_PDF_2017Down"),
    ("__CMS_ttHbb_PUUp","__CMS_ttHbb_PUDown"),
])


#optional function f: TH1D -> TH1D to blind data
def blind(h):
    hc = h.Clone()
    for i in range(h.GetNbinsX()+1):
        hc.SetBinContent(i, 0)
        hc.SetBinError(i, 0)
    return hc

def plot_syst_updown(nominal, up, down):
    plt.figure(figsize=(6,6))
    a1 = plt.axes([0.0, 0.52, 1.0, 0.5])
    nominal.color = "black"
    up.color = "red"
    down.color = "blue"
    
    In = float(nominal.Integral())
    Iu = float(up.Integral())
    Id = float(down.Integral())
    
    rplt.step(nominal, label="nominal ({0:.2f}, {1})".format(In, nominal.GetEntries()), linewidth=2, color="black")
    rplt.step(up, label="up ({0:.2f}, {1:.2f}%, {2})".format(Iu, 100.0*(Iu-In)/In, up.GetEntries()) if In>0 else 0.0, linewidth=2)
    rplt.step(down, label="down ({0:.2f}, {1:.2f}%, {2})".format(Id, 100.0*(Id-In)/In if In>0 else 0.0, down.GetEntries()), linewidth=2)
    ticks = a1.get_xticks()
    a1.get_xaxis().set_visible(False)
    a1.grid()
    plt.legend(loc="best", fontsize=12)

    a2 = plt.axes([0.0, 0.0, 1.0, 0.48], sharex=a1)
    up = up.Clone()
    up.Divide(nominal)
    zero_error(up)

    down = down.Clone()
    down.Divide(nominal)
    zero_error(down)

    up.color = "red"
    down.color = "blue"
    rplt.step(up, color="red", linewidth=2)
    rplt.step(down, color="blue", linewidth=2)
    plt.axhline(1.0, color="black", linewidth=2)
    a2.set_ylim(0.5, 1.5)
    a2.grid()

def blind_mem(h):
    print "blinding MEM"
    h = h.Clone()
    for ibin in range(0, h.GetNbinsX()+1):
        if ibin > h.GetNbinsX()/2:
            h.SetBinContent(ibin, 0)
            h.SetBinError(ibin, 0)
    return h

def no_blind(h):
    return h

blind_funcs = {
    "blind_mem": blind_mem,
    "no_blind": no_blind,
}

def plot_worker(kwargs):
    #temporarily disable true latex for fast testing
    do_tex = kwargs.get("do_tex", False)

    if do_tex:
        rc('text', usetex=True)
    else:
        rc('text', usetex=False)
    matplotlib.use('PS') #needed on T3

    inf = rootpy.io.File(kwargs.pop("infile"))
    outname = kwargs.pop("outname")
    histname = kwargs.pop("histname")
    procs = kwargs.pop("procs")
    signal_procs = kwargs.pop("signal_procs")
    do_syst = kwargs.pop("do_syst")
   
    if kwargs.has_key("blindFunc"):
        blind = kwargs.pop("blindFunc")
        if blind_funcs.has_key(blind):
            kwargs["blindFunc"] = blind_funcs[blind]

    fig = plt.figure(figsize=(6,6))

    ret = plotlib.draw_data_mc(
        inf,
        histname,
        procs,
        signal_procs,
        **kwargs
    )
    

    logging.info("saving {0}".format(outname))
    plotlib.svfg(outname + ".pdf")
    plotlib.svfg(outname + ".png")
    plt.clf()

    if do_syst:
        #systematic shapes
        for samp, sampname in procs:
            #print samp, sampname, ret["stacked"]
            #print type(ret["stacked"]), type(ret["nominal"]), type(ret["nominal"][samp])
            hnom = ret["nominal"][samp]
            for systUp, systDown in kwargs["systematics"]:
                syst_name = systUp[2:-2]
                #print type(ret["systematic"][systUp][samp])
                hup = ret["systematic"][systUp][samp]
                hdown = ret["systematic"][systDown][samp]
                plot_syst_updown(hnom, hup, hdown)
                plt.suptitle(escape_string(systUp.replace("Up", "")) + " " + sampname, y=1.1)
                plt.xlabel(kwargs["xlabel"]) 
                outname_syst = os.path.join(outname, syst_name, samp)
                logging.info("saving systematic {0}".format(outname_syst))
                plotlib.svfg(outname_syst + ".pdf")
                plt.clf()

        for samp, sampname in procs:
            if 'hnom2' in locals():
                hnom2 = hnom2 + ret["nominal"][samp]
            else:
                hnom2 = ret["nominal"][samp]
        for systUp, systDown in kwargs["systematics"]:
            for samp, sampname in procs:
                syst_name2 = systUp[2:-2]
                if 'hup2' in locals():
                    hup2 = hup2 + ret["systematic"][systUp][samp]
                    hdown2 = hdown2 + ret["systematic"][systDown][samp]
                else:
                    hup2 = ret["systematic"][systUp][samp]
                    hdown2 = ret["systematic"][systDown][samp]

            plot_syst_updown(hnom2, hup2, hdown2)
            plt.suptitle(escape_string(systUp.replace("Up", "")) , y=1.1)
            plt.xlabel(kwargs["xlabel"]) 
            outname_syst = os.path.join(outname, syst_name2)
            logging.info("saving systematic {0}".format(outname_syst))
            plotlib.svfg(outname_syst + ".pdf")
            plt.clf()

            del hup2 
            del hdown2 
#


    ##ROC plots
    #plt.figure(figsize=(6,6))
    #plt.plot([0,1],[0,1], color="black")
    #hsig = sum([ret["nominal"][s] for s in signal_procs])
    ##draw rocs
    #for samp, sampname in procs:
    #    if samp in signal_procs:
    #        continue
    #    hbkg = ret["nominal"][samp]
    #    r, e = plotlib.calc_roc(hsig, hbkg)
    #    plt.plot(r[:, 0], r[:, 1], marker=".", label=sampname + " AUC={0:.2f}".format(sklearn.metrics.auc(r[:, 0], r[:, 1])))
    #plt.legend(loc="best", fontsize=8)
    #plt.xlim(0,1)
    #plt.ylim(0,1)
    #outname_roc = outname + "_roc"
    #plotlib.svfg(outname_roc + ".pdf")
    #plt.clf()

    #pie plot
    #plt.figure(figsize=(3,3))
    #yields = [ret["nominal"][samp].Integral() for samp, sampname in procs]
    #plt.pie(
    #    yields,
    #    colors=[kwargs.get("colors")[p] for p, _ in procs],
    #    labels=[s[1] + "\n{0:.1f}".format(y) for s, y in zip(procs, yields)]
    #)
    #yield_s = 0.0
    #yield_b = 0.0
    #for y, (samp, sampname) in zip(yields, procs):
    #    if samp in signal_procs:
    #        yield_s += y
    #    else:
    #        yield_b += y

    #if yield_b == 0:
    #    plt.title(escape_string(kwargs.get("category", "unknown_category")))
    #else:
    #    plt.title(escape_string(kwargs.get("category", "unknown category")) + "\n" + r"$S/\sqrt{B} = " + "{0:.2f}$".format(yield_s / math.sqrt(yield_b)))
    #plotlib.svfg(outname + "_pie.pdf")
    #plt.clf()


    inf.Close()
    #return ret["nominal"]

def get_base_plot(basepath, outpath, analysis, category, variable):
    #s = "{0}/{1}/{2}".format(basepath, analysis, category)
    s = "{0}".format(basepath, analysis, category)
    ret = {
        "infile": s + ".root",
        "histname": "__".join([category, variable]),
        "outname": "/".join(["out", outpath, analysis, category, variable]),
        "category": category,
        "procs": procs_names,
        "signal_procs": ["ttH_hbb", "ttH_nonhbb"],
        "dataname": "data",#"data", #data_obs for fake data
        "rebin": 1,
        "xlabel": plotlib.varnames[variable] if variable in plotlib.varnames.keys() else "PLZ add me to Varnames", 
        "xunit": plotlib.varunits[variable] if variable in plotlib.varunits.keys() else "" ,
        "legend_fontsize": 12,
        "legend_loc": "best",
        "colors": plotlib.colors,
        "do_legend": True,
        "show_overflow": True,
        "title_extended": r" 2017 pp 41.3 $\mathrm{fb}^{-1}$ (13 TeV)",
        "systematics": syst_pairs,
        "do_syst": False,
        "blindFunc": "blind_mem" if "mem" in variable else "no_blind",
    }
    if variable in ["numJets", "nBDeepCSVM"]:
        ret["do_log"] = True
    return ret

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)

    # Plot for all SL categories
    simple_vars = [
        "numJets",
        "nBDeepCSVM",
        #"btag_LR_4b_2b_btagCSV_logit",
        #"nPVs",
#        "jetsByPt_0_btagCSV",
#        "jetsByPt_1_btagCSV",
#        "jetsByPt_2_btagCSV",
#        "jetsByPt_3_btagCSV",
        "jetsByPt_0_pt",
#        "jetsByPt_1_pt",
#        "jetsByPt_2_pt",
#        "jetsByPt_3_pt",
#        "jetsByPt_0_eta",
#        "jetsByPt_1_eta",
#        "jetsByPt_2_eta",
#        "jetsByPt_3_eta",
        "leps_0_pt"
    ]


    boosted_varsTH = [
        "topCandidate_mass",
        "topCandidate_pt",
        "topCandidate_fRec",
        "higgsCandidate_msoftdrop",
        "higgsCandidate_pt",
        "higgsCandidate_bbtag",
        "jetsByPt_0_pt", 
        "leps_0_pt",
        "met_pt"
    ]

    boosted_varsT = [
        #"ntopCandidate",
        "topCandidate_mass",
        "topCandidate_pt",
        #"topCandidate_eta",
        #"topCandidate_tau32SD",
        "topCandidate_fRec",
        #"topCandidate_delRopt",
        #"topCandidate_btagL",
        #"topCandidate_btagSL",
        #"topCandidate_ptsjL",
        #"topCandidate_ptsjSL",
        "jetsByPt_0_pt", 
        "leps_0_pt",
        "met_pt"
    ]

    boosted_varsH = [
        #"nhiggsCandidate",
        "higgsCandidate_msoftdrop",
        "higgsCandidate_pt",
        #"higgsCandidate_eta",
        #"higgsCandidate_tau21",
        "higgsCandidate_bbtag",
        #"higgsCandidate_btagL",
        #"higgsCandidate_btagSL",
        #"higgsCandidate_ptsjL",
        #"higgsCandidate_ptsjSL",
        "jetsByPt_0_pt", 
        "leps_0_pt",
        "met_pt"
    ]

    cats = [
        #("sl_jge4_tge2", simple_vars),
        #("dl_jge4_tge2", simple_vars),
        #("dl_jge4_t3", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("dl_jge4_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt"]),
        #("sl_jge6_t3", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("sl_jge6_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt"]),
        #("sl_j5_t3", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("sl_j5_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt","mem_SL_1w2h2t_p"]),
        #("sl_j4_t3", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("sl_j4_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt"]),
        #("dl_jge4_t3_noboost", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("dl_jge4_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt"]),
        #("sl_jge6_t3_noboost", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("sl_jge6_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt"]),
        #("sl_j5_t3_noboost", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("sl_j5_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt","mem_SL_1w2h2t_p"]),
        #("sl_j4_t3_noboost", ["jetsByPt_0_pt", "leps_0_pt","met_pt","btag_LR_4b_2b_btagCSV_logit"]),
        #("sl_j4_tge4", ["jetsByPt_0_pt", "leps_0_pt","met_pt"]),
        ("sl_jge6_tge4_sj", boosted_varsTH),
        #("sl_j5_tge4_sj", boosted_varsH),
        #("sl_j4_tge4_sj", boosted_varsH),
        #("dl_jge4_tge4_sj", boosted_varsH),
        #("sl_jge4_t3", simple_vars),
        #("sl_jge4_tge3", simple_vars),
        #("sl_jge4_tge4", simple_vars),
    ]

    args = []

    pairs = []
    for cat, variables in cats:
        for var in variables:
            pairs += [(cat, var)]
    
    args += [get_base_plot(
        sys.argv[1].replace(".root", ""),
        "test", "categories", cat, var) for (cat, var) in pairs
    ]

    for arg in args:
        arg["do_syst"] = False
        arg["do_tex"] = False
        if "numJets" in arg["histname"]:
            arg["do_log"] = True
        #plot_worker(arg)
    
    pool = multiprocessing.Pool(8)
    pool.map(plot_worker, args)
    pool.close()
