import ROOT
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pylab
import argparse
import numpy as np

params = {'legend.fontsize': 'x-large', 'axes.labelsize': 'x-large', 'axes.titlesize':'x-large', 'xtick.labelsize':'x-large', 'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

def plot(input, pars):

    # Load file
    file = ROOT.TFile(input)
    fit = file.Get("fit_mdf")

    # Read in correlations
    out = {"pars": pars}
    out["corrs"] = []
    
    for i in pars:
        for j in pars:
            out["corrs"] += [(i, j, fit.correlation(i, j))]
            if i == "r_ttH" and j == "r_ttbb":
                print fit.correlation(i,j)

    #print out["corrs"]

    # Build correlation matrix
    mat = np.zeros((len(out["pars"]), len(out["pars"])))
    
    for i, ip in enumerate(out["pars"]):
        for j, jp in enumerate(out["pars"]):
            mat[i, j] = out["corrs"][i + len(out["pars"])*j][2]

    # Plot correlation matrix
    plt.figure(figsize=(15,15))
    m = plt.imshow(mat, cmap = "seismic", vmin =-1, vmax =1)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            plt.text(i, j, "{0: .1f}".format(mat[i,j]), color = "orange", fontsize = 13, ha = "center", va = "center")
    out["pars"][0] = r"$\mu_{ttH}$"
    out["pars"][1] = r"$\mu_{tt+bjets}$"
    plt.xticks(range(len(out["pars"])), out["pars"], rotation = 90, fontsize = 18)
    plt.yticks(range(len(out["pars"])), out["pars"], fontsize = 18)
    plt.gcf().subplots_adjust(left=0.3)
    plt.gcf().subplots_adjust(bottom=0.3)
    cbar = plt.colorbar(m)
    cbar.set_label("post-fit correlation", size=18)
    plt.savefig("correlation.pdf", bbox_inches='tight')


if __name__ == "__main__":

    
    parser = argparse.ArgumentParser(description = 'Plot correlation matrix')
    
    parser.add_argument('--input', '-i', help = '.root file containing correlation matrix', required = True)

    
    args = parser.parse_args()

    #pars = [
    #    "r_ttH","r_ttbb",
    #    "bgnorm_ttbarPlus2B","bgnorm_ttbarPlusB","bgnorm_ttbarPlusCCbar",
    #    #"CMS_scaleFlavorQCD","CMS_scalePileUpDataMC","CMS_res",
    #    "CMS_ttH_CSVcferr1","CMS_ttH_CSVcferr2","CMS_ttH_CSVhf","CMS_ttH_CSVhfstats1","CMS_ttH_CSVhfstats2","CMS_ttH_CSVjes","CMS_ttH_CSVlf","CMS_ttH_CSVlfstats1","CMS_ttH_CSVlfstats2"
    #    ]

    #pars = ["r_ttH", "r_ttbb", "bgnorm_ttbarPlusCCbar", "bgnorm_ttbarPlus2B", "bgnorm_ttbarPlusB", "CMS_ttjetsisr", "CMS_ttjetsfsr", "CMS_ttjetstune", "CMS_ttjetshdamp", "CMS_ttH_CSVcferr1","CMS_ttH_CSVcferr2","CMS_ttH_CSVhf","CMS_ttH_CSVhfstats1","CMS_ttH_CSVhfstats2","CMS_ttH_CSVjes","CMS_ttH_CSVlf","CMS_ttH_CSVlfstats1","CMS_ttH_CSVlfstats2", "CMS_scaleFlavourQCD_j", "lumi", "CMS_pu", "pdf_gg", "pdf_qqbar", "pdf_qg", "pdf_Higgs_ttH", "QCDscale_t", "QCDscale_ttH", "QCD_ttbar", "CMS_ttH_scaleME"] 
    pars = ["r","CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_res_j","CMS_scaleFlavorQCD_j","CMS_scalePileUpDataMC_j","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar"]
    #
    
    plot(args.input, pars)
