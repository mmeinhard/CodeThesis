import os
import ROOT
import rootpy
from TTH.Plotting.joosep import plotlib_prefit as plotlib
import sys

channel_fit = {}

channel_fit["resolved"] = [
    "sl_jge6_tge4",
    "sl_jge6_t3",
    "sl_j5_tge4",
    "sl_j5_t3",
    "sl_j4_tge4",
    "sl_j4_t3",
    "dl_jge4_tge4",
    "dl_jge4_t3"
]


channel_fit["boosted"] = [
    "sl_jge6_tge4_noboost",
    "sl_jge6_t3_noboost",
    "sl_j5_tge4_noboost",
    "sl_j5_t3_noboost",
    "sl_j4_tge4_noboost",
    "sl_j4_t3_noboost",
    "dl_jge4_tge4_noboost",
    "dl_jge4_t3_noboost"
    "sl_jge6_tge4_sj",
    "sl_j5_tge4_sj",
    "sl_j4_tge4_sj",
    "dl_jge4_tge4_sj"
]

names = {}

names["resolved"] = {
    "ch1":"sl_jge6_tge4",
    "ch2":"sl_jge6_t3",
    "ch3":"sl_j5_tge4",
    "ch4":"sl_j5_t3",
    "ch5":"sl_j4_tge4",
    "ch6":"sl_j4_t3",
    "ch7":"dl_jge4_tge4",
    "ch8":"dl_jge4_t3"
}

names["resolved_6j4t"] = {
    "sl_jge6_tge4__met_pt":"sl_jge6_tge4",
    "sl_jge6_t3__met_pt":"sl_jge6_t3",
    "sl_j5_tge4__met_pt":"sl_j5_tge4",
    "sl_j5_t3__met_pt":"sl_j5_t3",
    "sl_j4_tge4__met_pt":"sl_j4_tge4",
    "sl_j4_t3__met_pt":"sl_j4_t3",
    "ch1":"sl_jge6_tge4",
    "ch2":"sl_jge6_t3",
    "ch3":"sl_j5_tge4",
    "ch4":"sl_j5_t3",
    "ch5":"sl_j4_tge4",
    "ch6":"sl_j4_t3",
    "sl_j5_tge4_sj_only__mem_SL_1w2h2t_sj_p":"sl_jge6_tge4",
}

names["onlyboosted"] = {
    "ch1_ch1":"sl_jge6_tge4_sj",
    "ch1_ch2":"sl_j5_tge4_sj",
    "ch1_ch3":"sl_j4_tge4_sj",
    "ch2":"dl_jge4_tge4_sj",
}

names["boosted"] = {
    "ch1":"sl_jge6_tge4_noboost",
    "ch2":"sl_jge6_t3_noboost",
    "ch3":"sl_j5_tge4_noboost",
    "ch4":"sl_j5_t3_noboost",
    "ch5":"sl_j4_tge4_noboost",
    "ch6":"sl_j4_t3_noboost",
    "ch7":"dl_jge4_tge4_noboost",
    "ch8":"dl_jge4_t3_noboost",
    "ch9":"sl_jge6_tge4_sj",
    "ch10":"sl_j5_tge4_sj",
    "ch11":"sl_j4_tge4_sj",
    "ch12":"dl_jge4_tge4_sj"
}

names["boosted"] = {
    "ch1":"sl_jge6_tge4",
    "ch2":"sl_jge6_t3",
    "ch3":"sl_j5_tge4",
    "ch4":"sl_j5_t3",
    "ch5":"sl_j4_tge4",
    "ch6":"sl_j4_t3",
    "ch7":"dl_jge4_tge4",
    "ch8":"dl_jge4_t3",
    "ch9":"boosted"
    #"ch9":"sl_jge6_tge4_sj_only",
    #"ch10":"sl_j5_tge4_sj_only",
    #"ch11":"sl_j4_tge4_sj_only",
    #"ch12":"dl_jge4_tge4_sj_only"
}



#templates_fit = {}

templates_fit = {
    #"sl_jge6_tge4" : rootpy.plotting.Hist(20,0,200),
    #"sl_jge6_tge4" : rootpy.plotting.Hist(6,0,1),
    "sl_jge6_t3" : rootpy.plotting.Hist(6,1,6),
    #"sl_j5_tge4" : rootpy.plotting.Hist(6,0,1),
    "sl_j5_t3" : rootpy.plotting.Hist(6,0,5),
    #"sl_j4_tge4" : rootpy.plotting.Hist(6,0,1),
    "sl_j4_t3" : rootpy.plotting.Hist(6,-1,4),
    "sl_jge6_tge4" : rootpy.plotting.Hist(6,2,8),
    "sl_j5_tge4" : rootpy.plotting.Hist(6,2,8),
    "sl_j4_tge4" : rootpy.plotting.Hist(6,2,8),
    #"sl_jge6_t3" : rootpy.plotting.Hist(20,0,200),
    #"sl_j5_tge4" : rootpy.plotting.Hist(20,0,200),
    #"sl_j5_t3" : rootpy.plotting.Hist(20,0,200),
    #"sl_j4_tge4" : rootpy.plotting.Hist(20,0,200),
    #"sl_j4_t3" : rootpy.plotting.Hist(20,0,200),
    #"dl_jge4_tge4" : rootpy.plotting.Hist(6,0,1),
   #"boosted" : rootpy.plotting.Hist(6,0.5,1.5),
   "boosted" : rootpy.plotting.Hist(6,-10,-2),
    #"boosted": rootpy.plotting.Hist(6,-10,-2),
    "dl_jge4_tge4" : rootpy.plotting.Hist(6,2,8),
    "dl_jge4_t3" : rootpy.plotting.Hist(6,-1,6),
    "sl_jge6_tge4_noboost" : rootpy.plotting.Hist(6,0,1),
    "sl_jge6_t3_noboost" : rootpy.plotting.Hist(6,1,6),
    "sl_j5_tge4_noboost" : rootpy.plotting.Hist(6,0,1),
    "sl_j5_t3_noboost" : rootpy.plotting.Hist(6,0,5),
    "sl_j4_tge4_noboost" : rootpy.plotting.Hist(6,0,1),
    "sl_j4_t3_noboost" : rootpy.plotting.Hist(6,-1,4),
    "dl_jge4_tge4_noboost" : rootpy.plotting.Hist(6,0,1),
    "dl_jge4_t3_noboost" : rootpy.plotting.Hist(6,-1,6),
    "sl_jge6_tge4_sj" : rootpy.plotting.Hist(6,0,1),
    "sl_j5_tge4_sj" : rootpy.plotting.Hist(6,0,1),
    "sl_j4_tge4_sj" : rootpy.plotting.Hist(6,0,1),
    "dl_jge4_tge4_sj" : rootpy.plotting.Hist(6,0,1),
    "sl_jge6_tge4_sj_only" : rootpy.plotting.Hist(6,0,1),
    "sl_j5_tge4_sj_only" : rootpy.plotting.Hist(6,0,1),
    "sl_j4_tge4_sj_only" : rootpy.plotting.Hist(6,0,1),
    "dl_jge4_tge4_sj_only" : rootpy.plotting.Hist(6,0,1),
    "sl_jge6_tge4__jetsByPt_0_lightjet_pt" : rootpy.plotting.Hist(30,0,200),
    "sl_jge6_tge4__jetsByPt_1_bjet_pt" : rootpy.plotting.Hist(30,0,300),
    "dl_jge4_tge4__jetsByPt_0_lightjet_pt" : rootpy.plotting.Hist(30,0,200),
    "dl_jge4_tge4__jetsByPt_1_bjet_pt" : rootpy.plotting.Hist(30,0,300),
    "dl_jge2_tge1__jetpt" : rootpy.plotting.Hist(30,0,500),
    "dl_jge2_tge1__numjets" : rootpy.plotting.Hist(10,2,12),
    "dl_jge2_tge1__btags" : rootpy.plotting.Hist(4,1,5),
    "dl_jge2_tge1__leppt" : rootpy.plotting.Hist(20,0,400),
    "sl_jge4_tge2__jetpt" : rootpy.plotting.Hist(20,0,500),
    "sl_jge4_tge2__numjets" : rootpy.plotting.Hist(10,4,14),
    "sl_jge4_tge2__btags" : rootpy.plotting.Hist(4,2,6),
    "sl_jge4_tge2__leppt" : rootpy.plotting.Hist(20,0,400)
}


channel_control = [
    #"dl_jge2_tge1__jetpt",
    #"dl_jge2_tge1__leppt",
    #"dl_jge2_tge1__numjets",
    #"dl_jge2_tge1__btags"

    #"sl_jge4_tge2__jetpt",
    #"sl_jge4_tge2__leppt",
    #"sl_jge4_tge2__numjets",
    #"sl_jge4_tge2__btags",

    #"dl_jge4_tge4__lightjet",
    #"dl_jge4_tge4__bjet",

    "sl_jge6_tge4__lightjet",
    "sl_jge6_tge4__bjet"
] 

channels = {
    "sl_jge6_tge4" : "shapes_sl_jge6_tge4__mem_SL_2w2h2t_p.txt",
    "sl_jge6_t3": "shapes_sl_jge6_t3__btag_LR_4b_2b_btagCSV_logit.txt" ,
    "sl_j5_tge4": "shapes_sl_j5_tge4__mem_SL_1w2h2t_p.txt",
    "sl_j5_t3": "shapes_sl_j5_t3__btag_LR_4b_2b_btagCSV_logit.txt",
    "sl_j4_tge4": "shapes_sl_j4_tge4__mem_SL_0w2h2t_p.txt",
    "sl_j4_t3": "shapes_sl_j4_t3__btag_LR_4b_2b_btagCSV_logit.txt",
    "dl_jge4_tge4": "shapes_dl_jge4_tge4__mem_DL_0w2h2t_p.txt",
    "dl_jge4_t3": "shapes_dl_jge4_t3__btag_LR_4b_2b_btagCSV_logit.txt",

    "dl_jge2_tge1__jetpt": "shapes_dl_jge2_tge1__jetsByPt_0_pt.txt", 
    "dl_jge2_tge1__leppt": "shapes_dl_jge2_tge1__leps_0_pt.txt",
    "dl_jge2_tge1__numjets": "shapes_dl_jge2_tge1__numJets.txt",
    "dl_jge2_tge1__btags": "shapes_dl_jge2_tge1__nBCSVM.txt",

    "sl_jge4_tge2__jetpt": "shapes_sl_jge4_tge2__jetsByPt_0_pt.txt",
    "sl_jge4_tge2__leppt": "shapes_sl_jge4_tge2__leps_0_pt.txt",
    "sl_jge4_tge2__numjets": "shapes_sl_jge4_tge2__numJets.txt",
    "sl_jge4_tge2__btags": "shapes_sl_jge4_tge2__nBCSVM.txt",

    "dl_jge4_tge4__lightjet": "shapes_dl_jge4_tge4__jetsByPt_0_lightjet_pt.txt",
    "dl_jge4_tge4__bjet": "shapes_dl_jge4_tge4__jetsByPt_1_bjet_pt.txt",

    "sl_jge6_tge4__lightjet": "shapes_sl_jge6_tge4__jetsByPt_0_lightjet_pt.txt",
    "sl_jge6_tge4__bjet": "shapes_sl_jge6_tge4__jetsByPt_1_bjet_pt.txt"
}

varnames = {
    #"sl_jge6_tge4" : r"MET [GeV]",
    #"sl_jge6_tge4" : r"MEM discriminant",
    "sl_jge6_tge4" : r"b tagging likelihood ratio",
    "sl_jge6_t3": r"b tagging likelihood ratio" ,
    #"sl_j5_tge4": r"MEM discriminant",
    "sl_j5_tge4": r"b tagging likelihood ratio",
    "sl_j5_t3": r"b tagging likelihood ratio",
    #"sl_j4_tge4": r"MEM discriminant",
    "sl_j4_tge4": r"b tagging likelihood ratio",
    "sl_j4_t3": r"b tagging likelihood ratio",
    #"dl_jge4_tge4": r"MEM discriminant",
    "dl_jge4_tge4": r"b tagging likelihood ratio",
    "dl_jge4_t3": r"b tagging likelihood ratio",

    #"boosted": r"average $\eta$ between jets",
    "boosted": r"b tagging likelihood ratio",
    "sl_jge6_tge4_noboost" : r"MEM discriminant",
    "sl_jge6_t3_noboost": r"b tagging likelihood ratio" ,
    "sl_j5_tge4_noboost": r"MEM discriminant",
    "sl_j5_t3_noboost": r"b tagging likelihood ratio",
    "sl_j4_tge4_noboost": r"MEM discriminant",
    "sl_j4_t3_noboost": r"b tagging likelihood ratio",
    "dl_jge4_tge4_noboost": r"MEM discriminant",
    "dl_jge4_t3_noboost": r"b tagging likelihood ratio",


    "sl_jge6_tge4_sj" : r"MEM discriminant",
    "sl_j5_tge4_sj": r"MEM discriminant",
    "sl_j4_tge4_sj": r"MEM discriminant",
    "dl_jge4_tge4_sj": r"MEM discriminant",

    #"sl_jge6_tge4_sj_only" : r"MEM discriminant",
    #"sl_j5_tge4_sj_only": r"MEM discriminant",
    #"sl_j4_tge4_sj_only": r"MEM discriminant",
    #"dl_jge4_tge4_sj_only": r"MEM discriminant",

    "sl_jge6_tge4_sj_only" : r"b tagging likelihood ratio",
    "sl_j5_tge4_sj_only": r"b tagging likelihood ratio",
    "sl_j4_tge4_sj_only": r"b tagging likelihood ratio",
    "dl_jge4_tge4_sj_only": r"b tagging likelihood ratio",




    "dl_jge2_tge1__jetpt": r"leading jet $p_T$ [GeV]", 
    "dl_jge2_tge1__leppt": r"leading lepton $p_T$ [GeV]",
    "dl_jge2_tge1__numjets": r"jet multiplicity",
    "dl_jge2_tge1__btags": r"b-tag multiplicity",

    "sl_jge4_tge2__jetpt": r"leading jet $p_T$ [GeV]",
    "sl_jge4_tge2__leppt": r"leading lepton $p_T$ [GeV]",
    "sl_jge4_tge2__numjets": r"jet multiplicity",
    "sl_jge4_tge2__btags": r"b-tag multiplicity",

    "dl_jge4_tge4__jetsByPt_0_lightjet_pt": r"leading light jet $p_T$ [GeV]",
    "dl_jge4_tge4__jetsByPt_1_bjet_pt": r"subleading b-jet $p_T$ [GeV]",

    "sl_jge6_tge4__jetsByPt_0_lightjet_pt": r"leading light jet $p_T$ [GeV]",
    "sl_jge6_tge4__jetsByPt_1_bjet_pt": r"subleading b-jet $p_T$ [GeV]"
}

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
    ("diboson", "diboson"),
    ("singlet", "single top"),
    ("ttv", "tt+V"),
    ("wjets", "w+jets"),
    ("zjets", "dy")
]


def postprocess_hist(h, template):
    #if h.GetNbinsX() != template.GetNbinsX():
    #    raise Exception("Expected {0} bins but got {1}".format(h.GetNbinsX(), template.GetNbinsX()))
    h2 = template.Clone(h.GetName())
    for ibin in range(h.GetNbinsX()+2):
        h2.SetBinContent(ibin, h.GetBinContent(ibin))
        h2.SetBinError(ibin, h.GetBinError(ibin))
    return h2



# Make datacard
def make_datacard(channel_fit, channel_control, channels, datacard):
    
    make_datacard = "combineCards.py"

    #for i in channel_fit:
    #    make_datacard += " " + i + "=" + channels[i]
        
    for i in channel_control:  
        make_datacard += " " + i + "=" + channels[i]

    make_datacard += " > " + datacard

    print make_datacard
    os.system(make_datacard)


# run combine and save shapes
def run_combine(datacard, channel_control):

    # Make workspace
    make_workspace = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO verbose --PO 'map=.*/ttH_hbb:r_ttH[1,-5,5]' --PO 'map=.*/ttH_nonhbb:r_ttH[1,-5,5]' --PO 'map=.*/ttbarPlusBBbar:r_ttbb[1,-5,5]' " + datacard + " -o model_dl_control.root" + " --channel-masks"
    print make_workspace 
    os.system(make_workspace)

    # run combine
    make_run = "combine -M FitDiagnostics model_dl_control.root -v 3 --robustFit 0 --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 -n channel_mask_dlcontrol --saveShapes --saveWithUncertainties --setParameters "
    for i in channel_control:
        make_run += "mask_{0}=1,".format(i)

    make_run = make_run + "|& tee mask.log"
    print make_run
    os.system(make_run) 


# draw prefit and postfit shapes
def prefit_postfit(input, cat, templates=templates_fit):

    tf = rootpy.io.File(input)

    if "SLDL" in input:
        typ = "resolved"
    elif "BoostedAnalysis" in input:
        typ = "boosted"
    elif "BoostedAnalysisV2" in input:
        typ = "boostedv2"
    if "SLDL_sj" in input:
        typ = "onlyboosted"
    elif "test_normal" in input:
        typ = "resolved_6j4t"
 
    print typ, cat

    ch = names[typ][cat]


    template = templates[ch]
    
    print "...", ch
    
    xlabel = varnames[ch]
    
    
    
    #if xlabel==r"MEM discriminant":
    #    template = rootpy.plotting.Hist(6,0,1)
    #if xlabel==r"b tagging likelihood ratio":
    #    template = rootpy.plotting.Hist(6,1,6)
    #if xlabel==r"leading jet $p_T$ [GeV]":
    #    template = rootpy.plotting.Hist(30,0,500)
    #if xlabel==r"leading lepton $p_T$ [GeV]":
    #    template = rootpy.plotting.Hist(20,0,400)
    #if xlabel==r"jet multiplicity":
    #    template = rootpy.plotting.Hist(10,4,14)
    #if xlabel==r"b-tag multiplicity":
    #    template = rootpy.plotting.Hist(4,2,6)
    #if xlabel==r"leading light jet $p_T$ [GeV]":
    #    template = rootpy.plotting.Hist()
    #if xlabel==r"subleading b-jet $p_T$ [GeV]"
    #
    histos = [k.GetName() for k in tf.Get("shapes_prefit/{}".format(cat)).GetListOfKeys()]
    print histos
    #histos = [k.GetName() for k in tf.Get(ch + "_prefit").GetListOfKeys()]
    
    procs = []
    for proc in procs_names:
        if proc[0] in histos:
            procs += [proc]
        elif "ttH_nonhbb" in proc[0] and "ttH_hcc" in histos:
            procs += [proc]
        elif "ttv" in proc[0] and "ttbarW" in histos:
            procs += [proc]

    
    
    print "PROCS: ", procs
    
    
    # draw prefit histograms
    ret = plotlib.draw_data_mc(tf, "",
        procs,
        [],
        #["ttH_hbb", "ttH_nonhbb"],
        #["ttbarPlusBBbar"],
        dataname = "data",
        #rebin = 1,
        colors = plotlib.colors,
        #pattern = ch + "_prefit" + "/{sample}",
        pattern ="shapes_prefit/" + cat + "/{sample}",
        legend_loc = "best",
        title_extended = ch + " prefit",
        legend_fontsize=12,
        xlabel = xlabel,
        ylabel = "events / bin",
        xunit = "",
        postprocess_hist = lambda x, template=template: postprocess_hist(x, template),
        do_tex = False,
        #do_log = True,
    )
    
    #ymax = 10000.0*sum([h.GetMaximum() for h in ret["nominal"].values()])
    ymax = 2.0*sum([h.GetMaximum() for h in ret["nominal"].values()])
    ret["axes"][0].set_ylim(0,ymax)
    ret["axes"][1].set_ylim(0.5,1.5)

    ret["axes"][1].set_xlim(ret["axes"][0].get_xlim())
    #plotlib.svfg( "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/HiggsAnalysis/CombinedLimit/data/tth/results/prefit" + "/{0}_prefit.pdf".format(ch))
    #plotlib.svfg( "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/HiggsAnalysis/CombinedLimit/data/tth/results/prefit" + "/{0}_prefit.png".format(ch))
    plotlib.svfg( "./{0}_prefit.pdf".format(ch))
    plotlib.svfg( "./{0}_prefit.png".format(ch))
    
    
    # draw postfit histograms
    ret = plotlib.draw_data_mc(tf, "",
        procs,
        [],
        dataname = "data",
        #rebin = 3,
        colors = plotlib.colors,
        #pattern = ch + "_postfit" + "/{sample}",
        pattern ="shapes_fit_s/" + cat + "/{sample}",
        legend_loc = "best",
        title_extended = ch + " postfit",
        legend_fontsize=12,
        xlabel = xlabel,
        ylabel = "events / bin",
        xunit = "",
        postprocess_hist = lambda x, template = template: postprocess_hist(x, template),
        do_tex = False,
        #do_log = True,
    )
    
    print "..........", ret["ws"], ymax, ret["axes"][0].get_xlim()
    ret["axes"][0].set_ylim(0,ymax)
    ret["axes"][1].set_ylim(0.5,1.5)
    ret["axes"][1].set_xlim(ret["axes"][0].get_xlim())
    #plotlib.svfg( "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/HiggsAnalysis/CombinedLimit/data/tth/results/postfit" + "/{0}_postfit.pdf".format(ch))
    #plotlib.svfg( "/work/mameinha/testcrab/CMSSW_10_2_15_patch2/src/HiggsAnalysis/CombinedLimit/data/tth/results/postfit" + "/{0}_postfit.png".format(ch))
    plotlib.svfg( "./{0}_postfit.pdf".format(ch))
    plotlib.svfg( "./{0}_postfit.png".format(ch))
    return ret

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Choose analysis')
    parser.add_argument(
        '--analysis',
        action="store",
        help="Analysis to process",
        required=True
    )
    
    args = parser.parse_args()
    if args.analysis == "test_normal":
        chs = ["ch1","ch2","ch3","ch4","ch5","ch6"]
        #chs = ["sl_jge6_tge4__met_pt","sl_jge6_t3__met_pt","sl_j5_tge4__met_pt","sl_j5_t3__met_pt","sl_j4_tge4__met_pt","sl_j4_t3__met_pt"]
    elif args.analysis == "SLDL_sj_combined_bla":
        chs = ["ch1_ch1","ch1_ch2","ch1_ch3","ch2"]
    elif args.analysis == "SLDL_combined_unblind":
        chs = ["ch1","ch2","ch3","ch4","ch5","ch6","ch7","ch8"]
    elif args.analysis == "SLDL_combined_unblind":
        chs = ["ch1","ch2","ch3","ch4","ch5","ch6","ch7","ch8"]
    elif args.analysis == "BoostedAnalysis_mu1":
	chs = ["ch1","ch2","ch3","ch4","ch5","ch6","ch7","ch8","ch9"]
    elif args.analysis == "BoostedAnalysis_unblind":
        chs = ["ch1","ch2","ch3","ch4","ch5","ch6","ch7","ch8","ch9"]

    print args.analysis, chs

    #path = os.path.dirname(os.path.realpath(__file__)) 
    #print path

    #make_datacard(channel_fit, channel_control, channels, "card_ttbbshapes_sl.txt")
    #run_combine("/mnt/t3nfs01/data01/shome/creissel/ttbb/final/card_dl_control.txt", channel_control)

    #for i in channel_control:
    #    prefit_postfit("shapes_sl_control.root", i, varnames[i])
    #for i in channel_fit:
    #    prefit_postfit("2D_shapes.root", i, varnames[i])

    for c in chs:
        prefit_postfit("fitDiagnostics_{}.root".format(args.analysis), c)

