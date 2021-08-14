import ROOT, sys, json

import matplotlib
matplotlib.use('PS') #needed on T3
from matplotlib import rc

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=False)
matplotlib.rcParams['text.latex.preamble']=[
    r"\usepackage{mathastext}"
]

import matplotlib.pyplot as plt
from TTH.Plotting.joosep import plotlib
import numpy as np

def get_corrs(fn):
    tf = ROOT.TFile.Open(fn)
    fit = tf.Get("fit_s")
    
    pars = [
        "r",
        "bgnorm_ttbarPlusBBbar", "bgnorm_ttbarPlusCCbar", "bgnorm_ttbarPlus2B", "bgnorm_ttbarPlusB",
        "CMS_ttjetsisr", "CMS_ttjetsfsr", "CMS_ttjetstune", "CMS_ttjetshdamp",
        "CMS_ttH_CSVhf", "CMS_ttH_CSVcferr1", "CMS_ttH_CSVcferr2", "CMS_ttH_CSVjes",
        "CMS_scaleFlavorQCD_j",
        "lumi", "CMS_pu",
        "pdf_gg", "pdf_qqbar", "pdf_qg", "pdf_Higgs_ttH",
        "QCDscale_t", "QCDscale_ttH", "QCDscale_ttbar",
        "CMS_ttH_scaleME"
    ]
    
    out = {"pars": pars}
    out["corrs"] = []
    for p1 in pars:
        for p2 in pars:
            out["corrs"] += [(p1, p2, fit.correlation(p1, p2))]
    
    of = open("corrs.json", "w")
    json.dump(out, of, indent=2)
    of.close()
    return out

def draw_corrs(corrs, path):
    mat = np.zeros((len(corrs["pars"]), len(corrs["pars"])))
    for ip1, p1 in enumerate(corrs["pars"]):
        for ip2, p2 in enumerate(corrs["pars"]):
            mat[ip1, ip2] = corrs["corrs"][ip1+len(corrs["pars"])*ip2][2]

    plt.figure(figsize=(12,12))
    m = plt.imshow(mat, cmap="seismic", vmin=-1, vmax=1)
    for ip1 in range(mat.shape[0]):
        for ip2 in range(mat.shape[1]):
            plt.text(ip1, ip2, "{0:.1f}".format(mat[ip1, ip2]), color="orange", fontsize=6, ha="center", va="center")
    corrs["pars"][0] = r"$\mu$"
    plt.xticks(range(len(corrs["pars"])), corrs["pars"], rotation=90, fontsize=16)
    plt.yticks(range(len(corrs["pars"])), corrs["pars"], fontsize=16)
    plt.colorbar(m, label="post-fit correlation")
    plotlib.svfg(path + "/nuis_corr.pdf")

if __name__ == "__main__":
    path = sys.argv[1]
    corrs = get_corrs(path + "/limits/mlfitshapes_group_group_sldl.root")
    draw_corrs(corrs, path)
