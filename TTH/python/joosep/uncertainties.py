from matplotlib import rc
rc('text', usetex=False)

import tabulate, json, math
from TTH.Plotting.joosep.plotlib import brazilplot 
from TTH.Plotting.joosep import plotlib
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator
import numpy as np

import ROOT

def uncs_in_category(tf, cat, var):
    #kl = [k.GetName() for k in tf.GetListOfKeys()]
    #kl = [k.split("__")[3] for k in kl if k.startswith('ttH_hbb__{0}__{1}'.format(cat, var)) and "CMS_scale" in k]
    #kl = [k.replace("jUp", "j").replace("jDown", "j") for k in kl]
    uncs = sorted(list(set([
        "CMS_scaleFlavorQCD_j",
        "CMS_res_j",
        "CMS_ttH_CSVhf", "CMS_ttH_CSVcferr1", "CMS_ttH_CSVcferr2", "CMS_ttH_CSVlf", "CMS_ttH_CSVjes",
        "CMS_pu",
        "CMS_ttjetsisr", "CMS_ttjetsfsr", "CMS_ttjetshdamp", "CMS_ttjetstune",
        "CMS_ttH_scaleME"
    ])))
    procs = ["ttH_hbb", "ttH_nonhbb", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar", "ttbarOther", "ttv"]

    vecs = np.zeros((6, len(uncs), len(procs)))
    for iunc, unc in enumerate(uncs):
        #print unc
        for iproc, proc in enumerate(procs):
            #print unc, proc
            h0 = tf.Get("{0}__{1}__{2}".format(proc, cat, var))
            h1 = tf.Get("{0}__{1}__{2}__{3}Up".format(proc, cat, var, unc))
            h2 = tf.Get("{0}__{1}__{2}__{3}Down".format(proc, cat, var, unc))
            if not h1:
                continue
            eup = ROOT.Double()
            edown = ROOT.Double()
            yup = h1.IntegralAndError(0, h1.GetNbinsX()+1, eup)/h0.Integral()
            ydown = h2.IntegralAndError(0, h1.GetNbinsX()+1, edown)/h0.Integral()
            eup /= h0.Integral()
            edown /= h0.Integral()
            vecs[0, iunc, iproc] = yup
            vecs[1, iunc, iproc] = eup
            vecs[2, iunc, iproc] = ydown
            vecs[3, iunc, iproc] = edown
            if h0.GetEntries()>0 and h1.GetEntries() > 0:
                vecs[4, iunc, iproc] = h1.Chi2Test(h0, "WW")
            if h0.GetEntries()>0 and h2.GetEntries() > 0:
                vecs[5, iunc, iproc] = h2.Chi2Test(h0, "WW")

            #print "  " + proc + " & {0:.4f} +- {1:.4f} & {2:.4f} +- {3:.4f}".format(yup, eup, ydown, edown)
            
    xs = np.arange(0,10*len(uncs), 10)
    plt.figure(figsize=(10,5))

    a1 = plt.axes([0.0,0.55,1.0,0.45])
    lines = []
    for iproc in range(len(procs)):
        l1 = plt.errorbar(xs+iproc, vecs[0, :, iproc], yerr=vecs[1, :, iproc], lw=0, elinewidth=1, marker="^", color=plotlib.colors[procs[iproc]])
        l2 = plt.errorbar(xs+iproc, vecs[2, :, iproc], yerr=vecs[3, :, iproc], lw=0, elinewidth=1, marker="v", color=plotlib.colors[procs[iproc]])
        lines += [l1]
        
    legend2 = plt.legend([l1, l2], ["up", "down"], frameon=True, loc=1)
    legend1 = plt.legend(lines, [plotlib.escape_string(p) for p in procs], loc=2, ncol=2, frameon=True)
    
    plt.gca().add_artist(legend1)
    plt.gca().add_artist(legend2)

    plt.xticks([])
    #plt.xticks(xs+3, [u.replace("_", " ") for u in uncs], rotation=90, fontsize=15);
    plt.axhline(1.0, color="black")
    for i in range(len(uncs)):
        plt.axvline(xs[i]-2, color="black", lw=0.5, ls="--")
    plt.ylabel("variation / nominal")
    plt.ylim(0.5, 1.5)
    plt.title("normalization effect of uncertainties in " + cat, fontsize=16)

    a2 = plt.axes([0.0, 0.0 ,1.0,0.45])

    lines = []
    for iproc in range(len(procs)):
        l1 = plt.errorbar(xs+iproc, vecs[4, :, iproc], lw=0, elinewidth=1, marker="^", color=plotlib.colors[procs[iproc]])
        l2 = plt.errorbar(xs+iproc, vecs[5, :, iproc], lw=0, elinewidth=1, marker="v", color=plotlib.colors[procs[iproc]])
        lines += [l1]
        
    plt.xticks(xs+3, [u for u in uncs], rotation=90, fontsize=15);
    plt.axhline(1.0, color="black")
    for i in range(len(uncs)):
        plt.axvline(xs[i]-2, color="black", lw=0.5, ls="--")
    plt.ylabel("p-value")
    plt.ylim(0.0, 1.1)
    plt.title("shape effect effect of uncertainties in " + cat, fontsize=16)
    plotlib.svfg("./out/uncs_{0}.pdf".format(cat))

if __name__ == "__main__":
    tf = ROOT.TFile("/mnt/t3nfs01/data01/shome/jpata/tth/gc/sparse/Oct25.root")
    uncs_in_category(tf, "sl_j4_t3", "btag_LR_4b_2b_btagCSV_logit")
    uncs_in_category(tf, "sl_j5_t3", "btag_LR_4b_2b_btagCSV_logit")
    uncs_in_category(tf, "sl_jge6_t3", "btag_LR_4b_2b_btagCSV_logit")
    uncs_in_category(tf, "sl_j4_tge4", "mem_SL_0w2h2t_p")
    uncs_in_category(tf, "sl_j5_tge4", "mem_SL_1w2h2t_p")
    uncs_in_category(tf, "sl_jge6_tge4", "mem_SL_2w2h2t_p")
