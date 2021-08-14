from matplotlib import rc
rc('text', usetex=False)
from TTH.Plotting.joosep import plotlib
import rootpy
import rootpy.io
import sys, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
    ("diboson", "diboson"),
    ("stop", "single top"),
    ("ttv", "tt+V"),
    ("wjets", "w+jets"),
    ("dy", "dy")
]

channel_titles = dict([
    ("sl_j4_t3", "SL 4j3t"),
    ("sl_j4_tge4", "SL 4j4t"),
    ("sl_j5_t3", "SL 5j3t"),
    ("sl_j5_tge4", "SL 5j $\geq$4t"),
    ("sl_jge6_t3", "SL $\geq$6j 3t"),
    ("sl_jge6_tge4", "SL $\geq$6j $\geq$4t"),
    ("dl_jge4_t3", "DL $\geq$4j 3t"),
    ("dl_jge4_tge4", "DL $\geq$4j $\geq$4t")
])

channel_map = dict([
    ("ch1", "sl_j4_t3"),
    ("ch2", "sl_j4_tge4"),
    ("ch3", "sl_j5_t3"),
    ("ch4", "sl_j5_tge4"),
    ("ch5", "sl_jge6_t3"),
    ("ch6", "sl_jge6_tge4"),
    ("ch7", "dl_jge4_tge4"),
    ("ch8", "dl_jge4_t3"),
])

def postprocess_hist(h, template):
    #Combine messes up histogram bins, so just assume template is correct
    #if h.GetNbinsX() != template.GetNbinsX():
    #    raise Exception("Expected {0} bins but got {1} for {2}".format(h.GetNbinsX(), template.GetNbinsX(), h.GetName()))
    h2 = template.Clone(h.GetName())
    for ibin in range(template.GetNbinsX()+2):
        h2.SetBinContent(ibin, h.GetBinContent(ibin))
        h2.SetBinError(ibin, h.GetBinError(ibin))
    return h2

def draw_channel_prefit_postfit(ch, chname, template, xlabel, path):

    available_hists = [k.GetName() for k in tf.Get("shapes_prefit").Get(ch).GetListOfKeys()]

    procs = []
    for proc in procs_names:
        if proc[0] in available_hists:
            procs += [proc]
    print tf.Get("shapes_prefit/{0}/ttH_hbb".format(ch)).GetNbinsX()
    ret = plotlib.draw_data_mc(tf, "",
        procs,
        ["ttH_hbb", "ttH_nonhbb"],
        dataname = "data",
        rebin = 1,
        colors = plotlib.colors,
        pattern="shapes_prefit/" + ch + "/{sample}",
        legend_loc="best",
        title_extended = channel_titles[chname] + r" $35.9\ \mathrm{fb}^{-1}$ (13 TeV)",
        legend_fontsize=12,
        xlabel = xlabel,
        ylabel = "events / bin",
        xunit = "",
        postprocess_hist = lambda x, template=template: postprocess_hist(x, template),
        do_tex = False
    )
    ymax = 3.0*sum([h.GetMaximum() for h in ret["nominal"].values()])
    h = ret["nominal"].values()[0]
    xticks = [h.GetBinLowEdge(i) for i in range(1, h.GetNbinsX()+1)]
    ret["axes"][0].text(0.05, 0.95, "prefit", ha="left", va="top", transform=ret["axes"][0].transAxes, fontsize=16)
    ret["axes"][0].set_ylim(0, ymax)
    ret["axes"][1].set_ylim(0.5, 1.5)
    #ret["axes"][0].set_xticks(xticks)
    #ret["axes"][1].set_xticks(xticks)
    minorLocator = AutoMinorLocator()
    ret["axes"][1].xaxis.set_minor_locator(minorLocator)
    plotlib.svfg(path + "/{0}_prefit.pdf".format(chname))

    ret = plotlib.draw_data_mc(tf, "",
        procs,
        ["ttH_hbb", "ttH_nonhbb"],
        dataname = "data",
        rebin = 1,
        colors = plotlib.colors,
        pattern="shapes_fit_s/" + ch + "/{sample}",
        legend_loc="best",
        title_extended = channel_titles[chname] + r" $35.9\ \mathrm{fb}^{-1}$ (13 TeV)",
        legend_fontsize=12,
        xlabel = xlabel,
        ylabel = "events / bin",
        xunit = "",
        postprocess_hist = lambda x, template=template: postprocess_hist(x, template),
        do_tex = False

    )
    ymax = 3.0*sum([h.GetMaximum() for h in ret["nominal"].values()])
    ret["axes"][0].set_ylim(0, ymax)
    ret["axes"][1].set_ylim(0.5, 1.5)
    ret["axes"][0].text(0.05, 0.95, "postfit", ha="left", va="top", transform=ret["axes"][0].transAxes, fontsize=16)
    #ret["axes"][0].set_xticks(xticks)
    #ret["axes"][1].set_xticks(xticks)
    minorLocator = AutoMinorLocator()
    ret["axes"][1].xaxis.set_minor_locator(minorLocator)
    plotlib.svfg(path + "/{0}_postfit.pdf".format(chname))
    return ret

def barchart(vals, colors, axes=None):
    if not axes:
        axes = plt.geaxes()
    ret = axes.bar(range(len(vals)), vals, color=colors, width=1.0)
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    ax.set_xticks([])
    #ax.spines['bottom'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    return ret

if __name__ == "__main__":
    path = sys.argv[1]
    tf = rootpy.io.File(path + "/limits/mlfitshapes_group_group_sldl.root")

    for ch, chname, template, xlabel in [
        ("ch1", "sl_j4_t3", rootpy.plotting.Hist(6,-1,4), r"b tagging likelihood ratio, $\mathcal{BLR}$"),
        ("ch2", "sl_j4_tge4", rootpy.plotting.Hist(6,0,1), r"MEM discriminant, $P_{\mathrm{s/b}}$"),
        ("ch3", "sl_j5_t3", rootpy.plotting.Hist(6,0,5), r"b tagging likelihood ratio, $\mathcal{BLR}$"),
        ("ch4", "sl_j5_tge4", rootpy.plotting.Hist(6,0,1), r"MEM discriminant, $P_{\mathrm{s/b}}$"),
        ("ch5", "sl_jge6_t3", rootpy.plotting.Hist(6,1,6), r"b tagging likelihood ratio, $\mathcal{BLR}$"),
        ("ch6", "sl_jge6_tge4", rootpy.plotting.Hist(6,0,1), r"MEM discriminant, $P_{\mathrm{s/b}}$"),
        ("ch8", "dl_jge4_t3", rootpy.plotting.Hist(6,-1,6), r"b tagging likelihood ratio, $\mathcal{BLR}$"),
        ("ch7", "dl_jge4_tge4", rootpy.plotting.Hist(6,0,1), r"MEM discriminant, $P_{\mathrm{s/b}}$"),
        ]:
        print ch, chname 
        ret = draw_channel_prefit_postfit(ch, chname, template, xlabel, path)

    #draw bar plots with yields
    plt.figure(figsize=(5,5))
    ich = 1
    nch = len(tf.Get("shapes_prefit").GetListOfKeys())
    process_histograms = {
        p: rootpy.plotting.Hist(nch, 0, nch) for p in [x[0] for x in procs_names]
    }
    channel_yields = {}
    for ch in tf.Get("shapes_prefit").GetListOfKeys():
        ax = plt.subplot(3,3,ich)
        chname = ch.GetName()
        kl = [k.GetName() for k in ch.ReadObj().GetListOfKeys()]
        yields = []
        yields_proc = {}
        colors = []
        #print kl
        for proc in procs_names:
            if proc[0] in kl:
                yields += [ch.ReadObj().Get(proc[0]).Integral()]
                colors += [plotlib.colors[proc[0]]]
                yields_proc[proc[0]] = ch.ReadObj().Get(proc[0]).Integral()
            else:
                yields_proc[proc[0]] = 0
        for proc, y in yields_proc.items():
            process_histograms[proc].SetBinContent(ich, y/sum(yields_proc.values()))
        s = ch.ReadObj().Get("total_signal").Integral()
        b = ch.ReadObj().Get("total_background").Integral()
        sob = s/math.sqrt(b)
        leg = barchart([yields_proc[p[0]] for p in procs_names], [plotlib.colors[p[0]] for p in procs_names], axes=ax)
        ich += 1
        plt.title(channel_titles[channel_map[chname]], y=0.98)
        ax.set_ylim(0, max(yields)*1.5)
        plt.text(0.5, 0.8, r"$S/\sqrt{{B}}={0:.2f}$".format(sob), transform=ax.transAxes, ha="center", fontsize=8)
        channel_yields[chname] = np.array(yields)
        
        minorLocator1 = AutoMinorLocator()
        ax.yaxis.set_minor_locator(minorLocator1)
        
    plt.legend(leg, [p[1] for p in procs_names], loc=(1.2, 0.05), frameon=False, ncol=2, fontsize=10)
    plt.tight_layout()
    plotlib.svfg(path + "/pies.pdf")
