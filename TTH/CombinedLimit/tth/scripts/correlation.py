import ROOT
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pylab
import argparse
import numpy as np

params = {'legend.fontsize': 'x-large', 'axes.labelsize': 'x-large', 'axes.titlesize':'x-large', 'xtick.labelsize':'x-large', 'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

def plot(input, pars, outputname):

    # Load file
    file = ROOT.TFile(input)
    fit = file.Get("fit_s")

    # Read in correlations
    out = {"pars": pars}
    out["corrs"] = []
    
    for i in pars:
        for j in pars:
            out["corrs"] += [(i, j, fit.correlation(i, j))]
            #print i, j, fit.correlation(i, j)
            #if i == "r_ttH" and j == "r_ttbb":
            #    print fit.correlation(i,j)

    #print out["corrs"]

    # Build correlation matrix
    mat = np.zeros((len(out["pars"]), len(out["pars"])))
    #print len(out["pars"])
    
    for i, ip in enumerate(out["pars"]):
        for j, jp in enumerate(out["pars"]):
            mat[i, j] = out["corrs"][i + len(out["pars"])*j][2]

    # Plot correlation matrix
    fig = plt.figure(figsize=(30,30))
    m = plt.imshow(mat, cmap = "seismic", vmin =-1, vmax =1,interpolation='none')
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            plt.text(i, j, "{0: .2f}".format(mat[i,j]), color = "orange", fontsize = 25, ha = "center", va = "center")
    out["pars"][0] = r"$\mu_{ttH}$"

    out["pars2"] = []
    out["pars3"] = []
    for i in out["pars"]:
        out["pars2"].append(i.replace("CMS_",""))
    #   #i = b

    for i in out["pars2"]:
        out["pars3"].append(i.replace("_j",""))

    plt.xticks(range(len(out["pars3"])), out["pars3"], rotation = 90, fontsize = 30)
    plt.yticks(range(len(out["pars3"])), out["pars3"], fontsize = 30)
    plt.text(-0.5, -1,
        r"$\mathbf{CMS}$ Work In Progress",
        fontsize=38, ha="left", va="top", fontname="Helvetica"
    )
    plt.text(14.5, -1,
        "$41.5\ \mathrm{fb}^{-1}\ \mathrm{(13\ TeV)}$",
        fontsize=28, ha="right", va="top", fontname="Helvetica"
    )
    plt.gcf().subplots_adjust(left=0.3)
    plt.gcf().subplots_adjust(bottom=0.3)
    cbaxes = fig.add_axes([0.92, 0.3, 0.03, 0.6]) 
    cbar = plt.colorbar(m, cax = cbaxes)   
    cbar.set_label("post-fit correlation", size=18)
    plt.savefig("correlation_{}.png".format(outputname), bbox_inches='tight')
    plt.savefig("correlation_{}.pdf".format(outputname), bbox_inches='tight')


if __name__ == "__main__":

    
    parser = argparse.ArgumentParser(description = 'Plot correlation matrix')
    
    parser.add_argument('--input', '-i', help = '.root file containing correlation matrix', required = True)
    parser.add_argument('--outputname', '-o', help = 'name of output plot', required = True)
    
    args = parser.parse_args()

    #pars = [
    #    "r_ttH","r_ttbb",
    #    "bgnorm_ttbarPlus2B","bgnorm_ttbarPlusB","bgnorm_ttbarPlusCCbar",
    #    #"CMS_scaleFlavorQCD","CMS_scalePileUpDataMC","CMS_res",
    #    "CMS_ttH_CSVcferr1","CMS_ttH_CSVcferr2","CMS_ttH_CSVhf","CMS_ttH_CSVhfstats1","CMS_ttH_CSVhfstats2","CMS_ttH_CSVjes","CMS_ttH_CSVlf","CMS_ttH_CSVlfstats1","CMS_ttH_CSVlfstats2"
    #    ]

    #pars = ["r_ttH", "r_ttbb", "bgnorm_ttbarPlusCCbar", "bgnorm_ttbarPlus2B", "bgnorm_ttbarPlusB", "CMS_ttjetsisr", "CMS_ttjetsfsr", "CMS_ttjetstune", "CMS_ttjetshdamp", "CMS_ttH_CSVcferr1","CMS_ttH_CSVcferr2","CMS_ttH_CSVhf","CMS_ttH_CSVhfstats1","CMS_ttH_CSVhfstats2","CMS_ttH_CSVjes","CMS_ttH_CSVlf","CMS_ttH_CSVlfstats1","CMS_ttH_CSVlfstats2", "CMS_scaleFlavourQCD_j", "lumi", "CMS_pu", "pdf_gg", "pdf_qqbar", "pdf_qg", "pdf_Higgs_ttH", "QCDscale_t", "QCDscale_ttH", "QCD_ttbar", "CMS_ttH_scaleME"] 
    #pars = ["CMS_btag_cferr1_2017","CMS_btag_cferr2_2017","CMS_btag_hf_2017","CMS_btag_hfstats1_2017","CMS_btag_hfstats2_2017","CMS_btag_lf_2017","CMS_btag_lfstats1_2017","CMS_btag_lfstats2_2017","CMS_effTrigger_dl","CMS_effTrigger_e","CMS_effTrigger_m","CMS_eff_e","CMS_eff_m","CMS_res_j_2017","CMS_scaleAbsoluteMPFBias_j_2017","CMS_scaleAbsoluteScale_j_2017","CMS_scaleAbsoluteStat_j","CMS_scaleFlavorQCD_j_2017","CMS_scaleFragmentation_j_2017","CMS_scalePileUpDataMC_j_2017","CMS_scalePileUpPtBB_j_2017","CMS_scalePileUpPtEC1_j_2017","CMS_scalePileUpPtRef_j_2017","CMS_scaleRelativeBal_j_2017","CMS_scaleRelativeFSR_j_2017","CMS_scaleRelativeJEREC1_j","CMS_scaleRelativePtBB_j_2017","CMS_scaleRelativePtEC1_j","CMS_scaleRelativeStatEC_j","CMS_scaleRelativeStatFSR_j","CMS_scaleSinglePionECAL_j_2017","CMS_scaleSinglePionHCAL_j_2017","CMS_scaleTimePtEta_j","CMS_ttHbb_L1PreFiring","CMS_ttHbb_PU","CMS_ttHbb_scaleMuF","CMS_ttHbb_scaleMuR","CMS_ttHbb_bgnorm_ttbarPlus2B","CMS_ttHbb_bgnorm_ttbarPlusB","CMS_ttHbb_bgnorm_ttbarPlusBBbar","CMS_ttHbb_bgnorm_ttbarPlusCCbar","QCDscale_ttH","QCDscale_ttbar","lumi_13TeV","pdf_Higgs_ttH","pdf_gg"]
    #pars = ["CMS_btag_cferr1_2017","CMS_btag_cferr2_2017","CMS_btag_hf_2017","CMS_btag_hfstats1_2017","CMS_btag_hfstats2_2017","CMS_btag_lf_2017","CMS_btag_lfstats1_2017","CMS_btag_lfstats2_2017","CMS_ttHbb_L1PreFiring","CMS_ttHbb_PU","CMS_ttHbb_scaleMuF","CMS_ttHbb_scaleMuR","CMS_ttHbb_bgnorm_ttbarPlus2B","CMS_ttHbb_bgnorm_ttbarPlusB","CMS_ttHbb_bgnorm_ttbarPlusBBbar","CMS_ttHbb_bgnorm_ttbarPlusCCbar","QCDscale_ttH","QCDscale_ttbar","lumi_13TeV","pdf_Higgs_ttH","pdf_gg"]
    #pars = ["CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_effTrigger_dl","CMS_effTrigger_e","CMS_effTrigger_m","CMS_eff_e","CMS_eff_m","CMS_res_j","CMS_scaleAbsoluteMPFBias_j","CMS_scaleAbsoluteScale_j","CMS_scaleAbsoluteStat_j","CMS_scaleFlavorQCD_j","CMS_scaleFragmentation_j","CMS_scalePileUpDataMC_j","CMS_scalePileUpPtBB_j","CMS_scalePileUpPtEC1_j","CMS_scalePileUpPtRef_j","CMS_scaleRelativeBal_j","CMS_scaleRelativeFSR_j","CMS_scaleRelativeJEREC1_j","CMS_scaleRelativePtBB_j","CMS_scaleRelativePtEC1_j","CMS_scaleRelativeStatEC_j","CMS_scaleRelativeStatFSR_j","CMS_scaleSinglePionECAL_j","CMS_scaleSinglePionHCAL_j","CMS_scaleTimePtEta_j","CMS_ttHbb_FSR_ttbarOther","CMS_ttHbb_FSR_ttbarPlus2B","CMS_ttHbb_FSR_ttbarPlusB","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarOther","CMS_ttHbb_ISR_ttbarPlus2B","CMS_ttHbb_ISR_ttbarPlusB","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar","CMS_ttHbb_L1PreFiring","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_scaleMuF","CMS_ttHbb_scaleMuR","QCDscale_V","QCDscale_VV","QCDscale_t","QCDscale_ttH","QCDscale_ttbar","lumi_13TeV","pdf_Higgs_ttH","pdf_gg","pdf_qg","pdf_qqbar","CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar","CMS_ttHbb_HDAMP_ttbarOther","CMS_ttHbb_HDAMP_ttbarPlus2B","CMS_ttHbb_HDAMP_ttbarPlusB","CMS_ttHbb_HDAMP_ttbarPlusBBbar","CMS_ttHbb_HDAMP_ttbarPlusCCbar","CMS_ttHbb_UE_ttbarOther","CMS_ttHbb_UE_ttbarPlus2B","CMS_ttHbb_UE_ttbarPlusB","CMS_ttHbb_UE_ttbarPlusBBbar","CMS_ttHbb_UE_ttbarPlusCCbar"]
    

    #Normal
    pars = ["r","CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_effTrigger_dl","CMS_effTrigger_e","CMS_effTrigger_m","CMS_eff_e","CMS_eff_m","CMS_res_j","CMS_scaleAbsoluteMPFBias_j","CMS_scaleAbsoluteScale_j","CMS_scaleAbsoluteStat_j","CMS_scaleFlavorQCD_j","CMS_scaleFragmentation_j","CMS_scalePileUpDataMC_j","CMS_scalePileUpPtBB_j","CMS_scalePileUpPtEC1_j","CMS_scalePileUpPtRef_j","CMS_scaleRelativeBal_j","CMS_scaleRelativeFSR_j","CMS_scaleRelativeJEREC1_j","CMS_scaleRelativePtBB_j","CMS_scaleRelativePtEC1_j","CMS_scaleRelativeStatEC_j","CMS_scaleRelativeStatFSR_j","CMS_scaleSinglePionECAL_j","CMS_scaleSinglePionHCAL_j","CMS_scaleTimePtEta_j","CMS_ttHbb_FSR_ttbarOther","CMS_ttHbb_FSR_ttbarPlus2B","CMS_ttHbb_FSR_ttbarPlusB","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarOther","CMS_ttHbb_ISR_ttbarPlus2B","CMS_ttHbb_ISR_ttbarPlusB","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar","CMS_ttHbb_L1PreFiring","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_scaleMuF","CMS_ttHbb_scaleMuR","QCDscale_V","QCDscale_VV","QCDscale_t","QCDscale_ttH","QCDscale_ttbar","lumi_13TeV","pdf_Higgs_ttH","pdf_gg","pdf_qg","pdf_qqbar","CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar","CMS_ttHbb_HDAMP_ttbarOther","CMS_ttHbb_HDAMP_ttbarPlus2B","CMS_ttHbb_HDAMP_ttbarPlusB","CMS_ttHbb_HDAMP_ttbarPlusBBbar","CMS_ttHbb_HDAMP_ttbarPlusCCbar","CMS_ttHbb_UE_ttbarOther","CMS_ttHbb_UE_ttbarPlus2B","CMS_ttHbb_UE_ttbarPlusB","CMS_ttHbb_UE_ttbarPlusBBbar","CMS_ttHbb_UE_ttbarPlusCCbar"]
    pars = ["r","CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf",
    "CMS_btag_lf","CMS_res_j","CMS_scaleFlavorQCD_j","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_scaleMuF",
    "CMS_ttHbb_scaleMuR","CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar","CMS_effTop","CMS_effHiggs"]
    

    #50 normalization uncertainty
    #pars = ["r","CMS_ttHbb_bgnorm_ttbarOther","CMS_ttHbb_bgnorm_ttbarPlus2B","CMS_ttHbb_bgnorm_ttbarPlusB","CMS_ttHbb_bgnorm_ttbarPlusBBbar","CMS_ttHbb_bgnorm_ttbarPlusCCbar", "CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_effTrigger_dl","CMS_effTrigger_e","CMS_effTrigger_m","CMS_eff_e","CMS_eff_m","CMS_res_j","CMS_scaleAbsoluteMPFBias_j","CMS_scaleAbsoluteScale_j","CMS_scaleAbsoluteStat_j","CMS_scaleFlavorQCD_j","CMS_scaleFragmentation_j","CMS_scalePileUpDataMC_j","CMS_scalePileUpPtBB_j","CMS_scalePileUpPtEC1_j","CMS_scalePileUpPtRef_j","CMS_scaleRelativeBal_j","CMS_scaleRelativeFSR_j","CMS_scaleRelativeJEREC1_j","CMS_scaleRelativePtBB_j","CMS_scaleRelativePtEC1_j","CMS_scaleRelativeStatEC_j","CMS_scaleRelativeStatFSR_j","CMS_scaleSinglePionECAL_j","CMS_scaleSinglePionHCAL_j","CMS_scaleTimePtEta_j","CMS_ttHbb_FSR_ttbarOther","CMS_ttHbb_FSR_ttbarPlus2B","CMS_ttHbb_FSR_ttbarPlusB","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarOther","CMS_ttHbb_ISR_ttbarPlus2B","CMS_ttHbb_ISR_ttbarPlusB","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar","CMS_ttHbb_L1PreFiring","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_scaleMuF","CMS_ttHbb_scaleMuR","QCDscale_V","QCDscale_VV","QCDscale_t","QCDscale_ttH","QCDscale_ttbar","lumi_13TeV","pdf_Higgs_ttH","pdf_gg","pdf_qg","pdf_qqbar","CMS_ttHbb_HDAMP_ttbarOther","CMS_ttHbb_HDAMP_ttbarPlus2B","CMS_ttHbb_HDAMP_ttbarPlusB","CMS_ttHbb_HDAMP_ttbarPlusBBbar","CMS_ttHbb_HDAMP_ttbarPlusCCbar","CMS_ttHbb_UE_ttbarOther","CMS_ttHbb_UE_ttbarPlus2B","CMS_ttHbb_UE_ttbarPlusB","CMS_ttHbb_UE_ttbarPlusBBbar","CMS_ttHbb_UE_ttbarPlusCCbar"]
    #pars = ["r","CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_res_j","CMS_scaleFlavorQCD_j","CMS_scalePileUpDataMC_j","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar"]
    #With boosted
    #pars = ["r","CMS_btag_cferr1","CMS_btag_cferr2","CMS_btag_hf","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_lf","CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_res_j","CMS_scaleFlavorQCD_j","CMS_scalePileUpDataMC_j","CMS_ttHbb_FSR_ttbarPlusBBbar","CMS_ttHbb_FSR_ttbarPlusCCbar","CMS_ttHbb_ISR_ttbarPlusBBbar","CMS_ttHbb_ISR_ttbarPlusCCbar","CMS_ttHbb_PDF","CMS_ttHbb_PU","CMS_ttHbb_bgnorm_ttbarPlusBB","CMS_ttHbb_bgnorm_ttbarPlusCCbar","CMS_effTop","CMS_effHiggs"]   
    plot(args.input, pars, args.outputname)
    print len(pars)
    
