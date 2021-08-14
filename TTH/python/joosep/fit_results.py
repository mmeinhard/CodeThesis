from matplotlib import rc
rc('text', usetex=False)

import tabulate, json, math
from TTH.Plotting.joosep.plotlib import brazilplot 
from TTH.Plotting.joosep import plotlib
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator
import numpy as np
import sys

def plot_bestfit_comb(fit_data):
    bestfit = {
        "sl": [fit_data["group_sl_bestfit"][0],
            [fit_data["group_sl_bestfit_statonly"][3],
             fit_data["group_sl_bestfit_statonly"][2]
            ],
            [fit_data["group_sl_bestfit"][3], fit_data["group_sl_bestfit"][2]],
            [math.sqrt(fit_data["group_sl_bestfit"][3]**2 - fit_data["group_sl_bestfit_statonly"][3]**2),
             math.sqrt(fit_data["group_sl_bestfit"][2]**2 - fit_data["group_sl_bestfit_statonly"][2]**2)
            ]],
        "dl": [fit_data["group_dl_bestfit"][0],
            [fit_data["group_dl_bestfit_statonly"][3],
             fit_data["group_dl_bestfit_statonly"][2]
            ],
            [fit_data["group_dl_bestfit"][3], fit_data["group_dl_bestfit"][2]],
            [math.sqrt(fit_data["group_dl_bestfit"][3]**2 - fit_data["group_dl_bestfit_statonly"][3]**2),
             math.sqrt(fit_data["group_dl_bestfit"][2]**2 - fit_data["group_dl_bestfit_statonly"][2]**2)
            ]],
        "comb": [
            fit_data["group_sldl_bestfit"][0],
            [fit_data["group_sldl_bestfit_statonly"][3],
             fit_data["group_sldl_bestfit_statonly"][2]
            ],
            [fit_data["group_sldl_bestfit"][3], fit_data["group_sldl_bestfit"][2]],
            [math.sqrt(fit_data["group_sldl_bestfit"][3]**2 - fit_data["group_sldl_bestfit_statonly"][3]**2),
             math.sqrt(fit_data["group_sldl_bestfit"][2]**2 - fit_data["group_sldl_bestfit_statonly"][2]**2)
            ]
        ],
    }
    
    order = ["sl", "dl", "comb"]
    titles = ["SL", "DL", "comb."]
    ys = [3,2,1]
    plt.figure(figsize=(6,4))
    axes = plt.axes()
    
    plt.errorbar(
        [bestfit[o][0] for o in order],
        ys, xerr=np.array([bestfit[o][2] for o in order]).T,
        marker=None, lw=0, elinewidth=2, color="blue", capsize=5, capthick=2
    )
    
    plt.errorbar(
        [bestfit[o][0] for o in order],
        ys, xerr=np.array([bestfit[o][1] for o in order]).T,
        marker=None, lw=0, elinewidth=2, color="red", capsize=5, capthick=2
    )
    
    plt.errorbar(
        [bestfit[o][0] for o in order],
        ys,
        marker="s", lw=0, color="black", markersize=4
    )
    
    shift = 1
    plt.text(shift + 2.2, 3.4, "$\mu$", fontsize=14, va="center")
    plt.text(shift + 3.8, 3.4, "tot.", fontsize=14, va="center", color="blue")
    plt.text(shift + 5.6, 3.4, "stat.", fontsize=14, va="center", color="red")
    plt.text(shift + 7.5, 3.4, "syst.", fontsize=14, va="center")
    
    for iy, y in enumerate(ys):
        mu, stat, tot, syst = bestfit[order[iy]]
        plt.text(shift + 2, y, "{0:.2f}".format(mu), color="black", ha="left", va="center", fontsize=12)
        plt.text(shift + 3.8, y+0.1, "+{0:.2f}".format(tot[0]), color="blue", ha="left", va="center", fontsize=12)
        plt.text(shift + 3.8, y-0.1, "-{0:.2f}".format(tot[1]), color="blue", ha="left", va="center", fontsize=12)
    
        plt.text(shift + 5.6, y+0.1, "+{0:.2f}".format(stat[0]), color="red", ha="left", va="center", fontsize=12)
        plt.text(shift + 5.6, y-0.1, "-{0:.2f}".format(stat[1]), color="red", ha="left", va="center", fontsize=12)
    
        plt.text(shift + 7.5, y+0.1, "+{0:.2f}".format(syst[0]), color="black", ha="left", va="center", fontsize=12)
        plt.text(shift + 7.5, y-0.1, "-{0:.2f}".format(syst[1]), color="black", ha="left", va="center", fontsize=12)
    
    plt.title(
        r"$\mathbf{CMS}$ private work",
        fontsize=16, x=0.05, ha="left", y=0.95, va="top", fontname="Helvetica"
    )
    plt.text(0.99, 1.00,
        "$35.9\ \mathrm{fb}^{-1}\ \mathrm{(13\ TeV)}$",
        fontsize=16, ha="right", va="bottom", transform=axes.transAxes, fontname="Helvetica"
    )
    
    minorLocator = AutoMinorLocator()
    axes.xaxis.set_minor_locator(minorLocator)
    
    axes.tick_params(axis = 'both', which = 'major', labelsize=16)
    axes.tick_params(axis = 'both', which = 'minor')
        
    plt.ylim(0.5,4.0)
    plt.xlim(-3,11)
    plt.xlabel("Best fit $\mu$", fontsize=20)
    plt.axvline(1.0, ymin=0.05, ymax=0.8, color="black", ls="--", lw=0.5)
    plt.yticks(ys, titles, fontsize=20)
    plotlib.svfg(path + "/bestfit.pdf")

if __name__ == "__main__":

    path = sys.argv[1]
    lims_data = json.load(open(path + "/limits.json"))

    #suf = "_asimov"
    suf = ""
    plt.figure(figsize=(5,4))
    tab = brazilplot(
        {
            "dl": lims_data["group_dl" + suf] + [lims_data["group_dl_asimov_sig1"][-1]],
            "sl": lims_data["group_sl" + suf] + [lims_data["group_sl_asimov_sig1"][-1]],
            "sldl": lims_data["group_sldl" + suf] + [lims_data["group_sldl_asimov_sig1"][-1]],
        },
        [
            ("sldl", "comb."),
            ("dl", r"DL"),
            ("sl", r"SL"),
        ],
        legend_loc=(0.5, 0.65),
        doObserved=True
    )
    #plt.ylim(-1,3)
    plt.xlim(0,5)
    plt.ylim(-0.5, 4.5)
    plotlib.svfg(path + "/limits_comb.pdf")

    plt.figure(figsize=(10, 10))
    tab = brazilplot(
        {
            #"sl_4tag": lims_data["group_sl_4tag_lims"],
            "sl_j4_t3": lims_data["sl_j4_t3__btag_LR_4b_2b_btagCSV_logit" + suf] + [lims_data["sl_j4_t3__btag_LR_4b_2b_btagCSV_logit_asimov_sig1"][-1]],
            "sl_j4_tge4": lims_data["sl_j4_tge4__mem_SL_0w2h2t_p" + suf] + [lims_data["sl_j4_tge4__mem_SL_0w2h2t_p_asimov_sig1"][-1]],
            "sl_j5_tge4": lims_data["sl_j5_tge4__mem_SL_1w2h2t_p" + suf] + [lims_data["sl_j5_tge4__mem_SL_1w2h2t_p_asimov_sig1"][-1]],
            "sl_j5_t3": lims_data["sl_j5_t3__btag_LR_4b_2b_btagCSV_logit" + suf] + [lims_data["sl_j5_t3__btag_LR_4b_2b_btagCSV_logit_asimov_sig1"][-1]],
            "sl_jge6_tge4": lims_data["sl_jge6_tge4__mem_SL_2w2h2t_p" + suf] + [lims_data["sl_jge6_tge4__mem_SL_2w2h2t_p_asimov_sig1"][-1]],
            "sl_jge6_t3": lims_data["sl_jge6_t3__btag_LR_4b_2b_btagCSV_logit" + suf] + [lims_data["sl_jge6_t3__btag_LR_4b_2b_btagCSV_logit_asimov_sig1"][-1]],
            #"dl_4tag": lims_data["group_dl_4tag_lims"],
            "dl": lims_data["group_dl" + suf] + [lims_data["group_dl_asimov_sig1"][-1]],
            "sl": lims_data["group_sl" + suf] + [lims_data["group_sl_asimov_sig1"][-1]],
            "dl_jge4_t3": lims_data["dl_jge4_t3__btag_LR_4b_2b_btagCSV_logit" + suf] + [lims_data["dl_jge4_t3__btag_LR_4b_2b_btagCSV_logit_asimov_sig1"][-1]],
            "dl_jge4_tge4": lims_data["dl_jge4_tge4__mem_DL_0w2h2t_p" + suf] + [lims_data["dl_jge4_tge4__mem_DL_0w2h2t_p_asimov_sig1"][-1]],
            #"sldl_4tag": lims_data["group_sldl_4tag_lims"],
            "sldl": lims_data["group_sldl" + suf] + [lims_data["group_sldl_asimov_sig1"][-1]],
        },
        [
            ("sldl", "comb."),
            ("sl", "SL"),
            ("sl_jge6_tge4", r"SL $\geq$6j $\geq$4t"),
            ("sl_jge6_t3", r"SL $\geq$6j $3$t"),
            ("sl_j5_tge4", r"SL 5j $\geq$ 4t"),
            ("sl_j5_t3", r"SL 5j3t"),
            ("sl_j4_tge4", r"SL 4j4t"),
            ("sl_j4_t3", r"SL 4j3t"),
            ("dl", r"DL"),
            ("dl_jge4_tge4", r"DL $\geq$4j $\geq$4t"),
            ("dl_jge4_t3", r"DL $\geq$4j 3t"),
        ],
        legend_loc=1,
        doObserved=True
    )
    plt.axhline(0.5, ls="--", lw=0.5)
    plt.axhline(7.5, ls="--", lw=0.5)
    
    #plt.ylim(-1,4)
    plt.xlim(0,40)
    plotlib.svfg(path + "/limits.pdf")
    
    of = open(path + "/lims.tex", "w")
    of.write(tabulate.tabulate(tab[::-1], headers=["category", "low", "median", "high", "observed", "injected"], tablefmt="latex_raw", floatfmt=".2f"))
    of.close()
    
    of = open(path + "/lims_comb.tex", "w")
    of.write(tabulate.tabulate(tab[::-1], headers=["category", "low", "median", "high", "observed", "injected"], tablefmt="latex_raw", floatfmt=".2f"))
    of.close()

    plot_bestfit_comb(lims_data)
