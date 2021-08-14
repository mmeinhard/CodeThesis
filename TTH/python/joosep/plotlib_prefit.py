import os
import time

#if os.environ.has_key("CMSSW_BASE"):
#    from cleanPath import fixPythonPath
#    import sys
#    sys.path = fixPythonPath(sys.path)

import ROOT
ROOT.gROOT.SetBatch(True)

import uuid

import matplotlib
matplotlib.use('Agg')
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt

print "VERSION", matplotlib.__version__, matplotlib.__path__

import numpy as np

import rootpy
import rootpy.io
from rootpy.plotting.root2matplotlib import errorbar, hist, fill_between
from collections import OrderedDict

import math

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

from matplotlib.ticker import AutoMinorLocator

#Configure fonts for CMS style
matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
matplotlib.rc("axes", labelsize=24)
matplotlib.rc("axes", titlesize=16)
#needs to be enabled to use latex in plot titles
#plt.rc('text', usetex=True)

#All the colors of the various processes
#extracted using the apple color picker tool
colors = {
    "ttbarOther": (251, 102, 102),
    "ttbarPlusCCbar": (204, 2, -0),
    "ttbarPlusB": (153, 51, 51),
    "ttbarPlusBBbar": (102, 0, 0),
    "ttbarPlus2B": (80, 0, 0),
    "ttH": (44, 62, 167),
    "ttH_hbb": (44, 62, 167),
    "ttH_nonhbb": (90, 115, 203),
    "diboson": (42, 100, 198),
    "wjets": (102, 201, 77),
    "zjets": (102, 201, 77),
    "singlet": (235, 73, 247),
    "ttv": (204, 204, 251),
    "qcd": (102, 201, 77),
    "qcd_ht300to500"   : (102, 201, 76),
    "qcd_ht500to700"   : (102, 201, 79),
    "qcd_ht700to1000"  : (102, 201, 80),
    "qcd_ht1000to1500" : (102, 201, 81),
    "qcd_ht1500to2000" : (102, 201, 82),
    "qcd_ht2000toinf"  : (102, 201, 83),
    "dy": (251, 73, 255),
    "other": (251, 73, 255),
}

#create floats of colors from 0..1
for cn, c in colors.items():
    colors[cn] = (c[0]/255.0, c[1]/255.0, c[2]/255.0)

#list of all variable names, suitable for latex
varnames = {
    "jetsByPt_0_pt": r"leading jet $p_T$ [GeV]",
    "jetsByPt_1_pt": r"subleading jet $p_T$ [GeV]",
    "jetsByPt_2_pt": r"third jet $p_T$ [GeV]",
    "jetsByPt_3_pt": r"fourth jet $p_T$ [GeV]",
    
    "jetsByPt_0_btagCSV": r"leading jet CSV",
    "jetsByPt_1_btagCSV": r"subleading jet CSV",
    "jetsByPt_2_btagCSV": r"third jet CSV",
    "jetsByPt_3_btagCSV": r"fourth jet CSV",
    
    "jetsByPt_0_eta": r"leading jet $\eta$",
    "jetsByPt_1_eta": r"subleading jet $\eta$",
    "jetsByPt_2_eta": r"third jet $\eta$",
    "jetsByPt_3_eta": r"fourth jet $\eta$",
    
    "leps_0_pt": r"leading lepton $p_T$ [GeV]",
    "leps_1_pt": r"subleading lepton $p_T$ [GeV]",
    "leps_0_eta": r"leading lepton $\eta$",
    "leps_1_eta": r"subleading lepton $\eta$",

    "numJets": r"jet multiplicity, $N_{\mathrm{jets}}$",
    "nBCSVM": r"b tag multiplicity, $N_{\mathrm{CSVM}}$",
    "nBDeepCSVM": r"b tag multiplicity, $N_{\mathrm{DeepCSVM}}$",

    "btag_LR_4b_2b_btagCSV_logit" : r"b tagging likelihood ratio, $\mathcal{BLR}$",
    "mem_SL_0w2h2t_p": r"MEM discriminant, $P_{\mathrm{s/b}}$",
    "mem_SL_1w2h2t_p": r"MEM discriminant, $P_{\mathrm{s/b}}$",
    "mem_SL_2w2h2t_p": r"MEM discriminant, $P_{\mathrm{s/b}}$",
    "mem_DL_0w2h2t_p": r"MEM discriminant, $P_{\mathrm{s/b}}$",
    "Wmass": "W boson candidate mass, $m_{qq}$",
    "met_pt": "MET [GeV]",
    "ht": "scalar sum of jet momenta, $H_T$ [GeV]",
    "mll": "dilepton invariant mass, $m_{\ell\ell}$ [GeV]",
    "nPVs": "number of primary vertices, $N_{PV}$",

    "nhiggsCandidate":r"Higgs candidate multiplicity $N_{\mathrm{Higgs c.}}$",
    "higgsCandidate_msoftdrop":r"Higgs candidate SD mass $m_{SD, \mathrm{Higgs c.}}$",
    "higgsCandidate_pt":r"Higgs candidate $p_T$ [GeV]",
    "higgsCandidate_eta":r"Higgs candidate $\eta$",
    "higgsCandidate_tau21":r"Higgs candidate $\tau_{21}$",
    "higgsCandidate_bbtag":r"Higgs candidate $bbtag$",
    "higgsCandidate_btagL":r"Higgs candidate $btag_{L}$",
    "higgsCandidate_btagSL":r"Higgs candidate $btag_{SL}$",
    "higgsCandidate_ptsjL":r"Higgs candidate $p_{T,L}$ [GeV]",
    "higgsCandidate_ptsjSL":r"Higgs candidate $p_{T,SL}$ [GeV]",
    "ntopCandidate":r"Top candidate multiplicity $N_{\mathrm{top c.}}$",
    "topCandidate_mass":r"Top candidate mass $m_{\mathrm{Higgs c.}}$",
    "topCandidate_pt":r"Top candidate $p_T$ [GeV]",
    "topCandidate_eta":r"Top candidate $\eta$",
    "topCandidate_tau32SD":r"Top candidate $\tau_{32_SD}$",
    "topCandidate_fRec":r"Top candidate $f_{\mathrm{Rec}}$",
    "topCandidate_delRopt":r"Top candidate $R_{\mathrm{opt}}$",
    "topCandidate_btagL":r"Top candidate $btag_{L}$",
    "topCandidate_btagSL":r"Top candidate $btag_{SL}$",
    "topCandidate_ptsjL":r"Top candidate $btag_{SSL}$",
    "topCandidate_ptsjSL":r"Top candidate $p_{T,L}$ [GeV]",
}

#the units for variables
varunits = {
    "jetsByPt_0_pt": "GeV",
    "jetsByPt_1_pt": "GeV",
    "topCandidate_pt": "GeV",
    "topCandidate_mass": "GeV",
    "higgsCandidate_pt": "GeV",
    "higgsCandidate_mass": "GeV",
    "higgsCandidate_mass_pruned": "GeV",
    "higgsCandidate_mass_softdrop": "GeV",
}

def process_sample_hist(fnames, hname, func, bins, cut, **kwargs):
    """
    Takes a list of files and projects a 1D histogram with the specified cut.
    fnames (list of strings): list of filenames to be opened
    hname (string): name of the output histogram, must be unique
    func (string): the function (ROOT string) to be evaluated
    bins (3-tuple): the (nbins, low, high) of the histograms
    cut (string): the weight and cut string (ROOT format) to be evaluated.
    
    returns: TH1D in the gROOT directory
    """

    for ifn in range(len(fnames)):
        fn = fnames[ifn]
        if type(fn) is str:
            fnames[ifn] = (fnames[ifn], 1.0)
    
    hs = []
    for fn, xsw in fnames:
        tt = ROOT.TChain("tree")
        tt.Add(fn)
        ROOT.gROOT.cd()
        _hname = str(uuid.uuid4())
        ndims = len(bins)/3
        if ndims == 1:
            h = ROOT.TH1D(_hname, "", *bins)
        elif ndims == 2:
            h = ROOT.TH2D(_hname, "", *bins)
        h.Sumw2()
        h.SetDirectory(ROOT.gROOT)
        n = tt.Draw("{0} >> {1}".format(func, _hname), cut)
        h.Scale(xsw)
        h = rootpy.asrootpy(h)
        hs += [h]
    htot = sum(hs)
    htot.SetName(hname)
    return htot

def mc_stack(
    hlist,
    histtotal,
    hs_syst,
    systematics,
    colors="auto"
    ):
    """Draws a list of histograms as a stack, optionally with a systematic band
    
    Args:
        hlist (list of Hist): The nominal histograms to plot 
        hs_syst (dict): nested dict of systematic -> sample -> histogram
        systematics (list of strings): List of the systematics to retrieve from hs_syst
        colors (str or list): "auto" for automatic colors, otherwise a list of colors
    
    Returns:
        dict: Description
    """
    #choose the colors
    if colors=="auto":
        #create a color iterator
        coloriter = iter(plt.cm.jet(np.linspace(0,1,len(hlist))))
        for h in hlist:
            h.color = next(coloriter)
    #colors given for each item
    elif isinstance(colors, list) and len(colors) == len(hlist):
        for h, c in zip(hlist, colors):
            h.color = c

    #make sure histograms are filled
    for h in hlist:
        h.fillstyle = "solid"
    
    #create stack using root2matplotlib
    #FIXME: Temporary workaround for failed fill, only works when hatch is specified
    stack = hist(hlist, stacked=True, hatch=".", lw=2)
    
    #Create total MC histogram
    htot = sum(hlist)
    htot.color="black"
    xs = np.array([i for i in htot.x()])
    ws = np.array([i for i in htot.xwidth()])
    ys = np.array([i for i in htot.y()])
    err1p = [] 
    #for i in range(0,htot.GetNbinsX()):
    histtot = sum(histtotal)
    for i in range(1,htot.GetNbinsX()+1):
    	print ".......", histtot.GetBinError(i)
        err1p.append(histtot.GetBinError(i))
    err1 = np.array(err1p)
    err2 = err1
    #err1 = np.array([i for i in htot.yerrl()])
    #err2 = np.array([i for i in htot.yerrh()])
    #print err1, err2

    #Plot MC statistical error
    stat_error_bar = plt.bar(xs, err1+err2, width=ws, bottom=ys-err1, hatch="//////", facecolor="none", zorder=100)

    #Symmetrize statistical error
    errs_stat_sym = (err2 + err1)/2.0

    #create an array of symmetrized systematic errors
    errs_syst = np.zeros((htot.GetNbinsX(), len(systematics)+1))
    
    for isyst, (syst_up, syst_down) in enumerate(systematics):
        h_up = np.array([y for y in sum(hs_syst[syst_up].values()).y()])
        h_down = np.array([y for y in sum(hs_syst[syst_down].values()).y()])
        # Dirty quick fix
        isnan = False
        for i in h_up:
            if math.isnan(i):
                isnan = True
        if isnan:
            for i in range(len(h_up)):
                h_up[i] = 0
                h_down[i] = 0 
        
        sym = np.abs(h_up - h_down)/2.0
        errs_syst[:, isyst] = sym[:]



    errs_syst[:, -1] = errs_stat_sym[:]

    #add the systematic and statistical errors in quadrature
    errs_syst_tot = np.sqrt(np.sum(np.power(errs_syst, 2), 1))
    
    #plot the systematic error bar
    syst_error_bar = plt.bar(
        xs,
        2.0*errs_syst_tot,
        width=ws,
        bottom=ys - errs_syst_tot,
        hatch="\\\\\\\\",
        facecolor="none",
        zorder=100
    )

    return {
        "hists": stack,
        "tot": htot,
        "stat_error_bar": stat_error_bar,
        "syst_error_bar": syst_error_bar,
        "stat_error": errs_stat_sym,
        "syst_error": errs_syst_tot,
    }

def dice(h, nsigma=1.0):
    hret = h.clone()
    for i in range(1, h.nbins()+1):
        m, e = h.get_bin_content(i), h.get_bin_error(i)
        if e<=0:
            e = 1.0
        n = np.random.normal(m, nsigma*e)
        hret.set_bin_content(i, n)
    return hret

def make_uoflow(h):
    """
    Given a TH1 with bins [1...nbins], fill the underflow entries (bin 0) into the first bin and
    the overflow entries (nbins+1) into the last bin (nbins).
    """
    nb = h.GetNbinsX()
    #h.SetBinEntries(1, h.GetBinEntries(0) + h.GetBinEntries(1))
    #h.SetBinEntries(nb+1, h.GetBinEntries(nb) + h.GetBinEntries(nb + 1))
    h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
    h.SetBinContent(nb+1, h.GetBinContent(nb) + h.GetBinContent(nb + 1))
    h.SetBinError(1, math.sqrt(h.GetBinError(0)**2 + h.GetBinError(1)**2))
    h.SetBinError(nb+1, math.sqrt(h.GetBinError(nb)**2 + h.GetBinError(nb + 1)**2))

def zero_error(h):
    for i in range(1, h.GetNbinsX()+1):
        h.SetBinError(i, 0)

def fill_overflow(hist):
    """
    Puts the contents of the overflow bin in the last visible bin
    """
    nb = hist.GetNbinsX()
    o = hist.GetBinContent(nb + 1)
    oe = hist.GetBinError(nb + 1)
    hist.SetBinContent(nb, hist.GetBinContent(nb) + o)
    hist.SetBinError(nb, math.sqrt(hist.GetBinError(nb)**2 + oe**2))
    
    #fixme recalculate error
    hist.SetBinContent(nb+1, 0)
    hist.SetBinError(nb+1, 0)


def getHistograms(tf, samples, hname, pattern="{sample}/{hname}", rename_func=lambda x: x, postprocess_hist=lambda x: x):
    """Summary
    
    Args:
        tf (rootpy.io.File): Input ROOT file
        samples (list of tuples): (sample, sample_name) of the input samples
        hname (string): name of the histogram
        pattern (str, optional): pattern to find histograms in file
        rename_func (TYPE, optional): Description
    
    Returns:
        TYPE: Description
    """
    hs = OrderedDict()
    for sample, sample_name in samples:
        pat = pattern.format(sample=sample, hname=hname)
        #print pat
	print sample
        h = None
        try:
            if sample == "ttH_nonhbb":
                h = tf.get(pat.replace("ttH_nonhbb","ttH_hcc")).Clone()
                h2 = tf.get(pat.replace("ttH_nonhbb","ttH_hzz")).Clone()
                h3 = tf.get(pat.replace("ttH_nonhbb","ttH_hww")).Clone()
                h4 = tf.get(pat.replace("ttH_nonhbb","ttH_htt")).Clone()
                try:
		    h5 = tf.get(pat.replace("ttH_nonhbb","ttH_hgg")).Clone()
                except:
		    h5 = tf.get(pat.replace("ttH_nonhbb","ttH_hcc")).Clone()
		    h5.Reset()
		h6 = tf.get(pat.replace("ttH_nonhbb","ttH_hgluglu")).Clone()
                #h7 = tf.get(pat.replace("ttH_nonhbb","ttH_hzg")).Clone()
                h.Add(h2)
                h.Add(h3)
                h.Add(h4)
                h.Add(h5)
                h.Add(h6)
                #h.Add(h7)
            elif sample == "ttv":
                h = tf.get(pat.replace("ttv","ttbarZ")).Clone()
                h2 = tf.get(pat.replace("ttv","ttbarW")).Clone()
                h.Add(h2)
            elif sample == "dy":
                h = tf.get(pat.replace("dy","wjets")).Clone()
                h2 = tf.get(pat.replace("dy","zjets")).Clone()
                h.Add(h2)
            else:
                h = tf.get(pat).Clone()
        #histo didn't exist, create empty dummy
        except rootpy.io.file.DoesNotExist as e:
            print "ERROR: could not load hist {0}: {1}".format(pat, e)
            for key in tf.GetListOfKeys():
                if hname in key.GetName():
		    print "create dummy"
                    h = rootpy.asrootpy(tf.get(key.GetName()).Clone())
            if not h:
                raise Exception("Could not find histogram with name {0} or replacement".format(pat))

            #set all bins, including underflow and overflow, to 0
            for ibin in range(0, h.GetNbinsX() + 2):
                h.SetBinContent(ibin, 0.0)
                h.SetBinError(ibin, 0.0)
            h.SetEntries(0.0)
        h = postprocess_hist(h)
        #create or add to output
        if not hs.has_key(rename_func(sample)):
            hs[rename_func(sample)] = rootpy.asrootpy(h)
        else:
            hs[rename_func(sample)] += rootpy.asrootpy(h)
    return hs


def graph_to_hist(d):
    h = rootpy.plotting.Hist(d.GetN(), 0, d.GetN())
    for i in range(1, d.GetN()+1):
        x = ROOT.Double()
        y = ROOT.Double()
        d.GetPoint(i-1, x, y)
        h.SetBinContent(i, y)
        h.SetBinError(i, d.GetErrorY(i))
    return h

def draw_data_mc(tf, hname, processes, signal_processes, **kwargs):
    """
    Given a root file in the combine datacard format, draws a data/mc histogram,
    ratio and systematic band.
    tf (TFile): input root file
    hname (string): name of histogram, example "sl_jge6_tge4/jetsByPt_0_pt"
    processes (list of (str, str) tuples): processes to use for the plot. First
        argument of tuple is the name in the file, second the name on the plot.
        The order here defines the order of plotting (bottom to top). Assume that
        signal is the first process.
    signal_processes (list of str): process names to consider as signal
    """

    # name (string) of the data process.
    # Example: "data" (real data), "data_obs" (fake data)
    #must exist in the input file
    dataname = kwargs.get("dataname", None)
    
    xlabel = kwargs.get("xlabel", escape_string(hname))
    xunit = kwargs.get("xunit", "XUNIT")
    ylabel = kwargs.get("ylabel", "auto")
    rebin = kwargs.get("rebin", 1)

    rename_func = kwargs.get("rename_func", lambda x: x)
    postprocess_hist = kwargs.get("postprocess_hist", lambda x: x)

    #legend properties
    do_legend = kwargs.get("do_legend", True)
    do_log = kwargs.get("do_log", False)
    legend_loc = kwargs.get("legend_loc", (1.1,0.1))
    legend_fontsize = kwargs.get("legend_fontsize", 6)

    #Dictionary of sample (string) -> color (tuple of floats) to use as colors
    #or "auto" to generate a sequence of colors
    colors = kwargs.get("colors", "auto")

    #True if you want to put the contents of the overflow bin into the last
    #visible bin of the histogram, False otherwise
    show_overflow = kwargs.get("show_overflow", False)

    #Use latex
    do_tex = kwargs.get("do_tex", False)

    #function f: TH1D -> TH1D to apply on data to blind it.
    blindFunc = kwargs.get("blindFunc", None)
    
    pattern = kwargs.get("pattern", "{sample}__{hname}")

    #array of up-down pairs for systematic names to use for the systematic band,
    #e.g.[("_CMS_scale_jUp", "_CMS_scale_jDown")]
    systematics = kwargs.get("systematics", [])

    title_extended = kwargs.get("title_extended", "")

    histograms_nominal = getHistograms(tf, processes, hname, pattern=pattern, rename_func=rename_func, postprocess_hist=postprocess_hist)
    histototal = getHistograms(tf, [ ('total', 'total')], hname, pattern=pattern, rename_func=rename_func, postprocess_hist=postprocess_hist)


    if len(histograms_nominal) == 0:
        raise KeyError(
            "getHistograms: processes={0} hname={1} pattern={2}".format(processes, hname, pattern) +
            "did not find any histograms for MC"
        )

    histograms_systematic = OrderedDict()
    #get the systematically variated histograms
    for systUp, systDown in systematics:
        histograms_systematic[systUp] = getHistograms(tf, processes, hname+systUp, pattern=pattern, rename_func=rename_func)
        histograms_systematic[systDown] = getHistograms(tf, processes, hname+systDown, pattern=pattern, rename_func=rename_func)
        if len(histograms_systematic[systUp])==0 or len(histograms_systematic[systDown])==0:
            print "Could not read histograms for {0}".format(hname+systUp)

    processes_d = dict(processes)

    counts = {}
    ####### GET BACK EVENT YIELDS HERE
    #Compute the counts of all histograms, rebin and fix the overflow bins
    for histo_dict in [histograms_nominal] + histograms_systematic.values():
        for (proc, h) in histo_dict.items():
            h.title = processes_d[proc] + " ({0:.1f})".format(h.Integral())
            counts[proc] = h.Integral()
            h.rebin(rebin)
            if show_overflow:
                fill_overflow(h)
            
    fig = plt.figure(figsize=(6,6))

    #Create top panel
    a1 = plt.axes([0.0, 0.22, 1.0, 0.8])
    
    if do_tex:
        fig.suptitle(r"$\mathrm{CMS}$ Work In Progress",
           y=0.98, x=0.02,
           horizontalalignment="left", verticalalignment="top", fontsize=16
        )
    else:
        fig.suptitle(r"$\mathbf{CMS}$ Work In Progress",
           y=1.02, x=0.02,
           horizontalalignment="left", verticalalignment="bottom", fontsize=16
        )
        fig.text(0.98, 1.02, title_extended, ha="right", va="bottom", fontsize=16) 

    stacked_hists = mc_stack(
        histograms_nominal.values(),
        histototal.values(),
        histograms_systematic,
        systematics,
        colors = [colors[p] for p, _ in processes]
    )

    #Create the normalized signal shape
    histogram_signal = sum([histograms_nominal[sig] for sig in signal_processes])
    histogram_total_mc = sum(histograms_nominal.values())

    xs = np.array([i for i in histogram_total_mc.x()])
    ws = np.array([i for i in histogram_total_mc.xwidth()])
    ys = np.array([i for i in histogram_total_mc.y()])

    print "-------", signal_processes

    if not histogram_signal:
        histogram_signal = histogram_total_mc.Clone()
        histogram_signal.Scale(0.0)
        
    if histogram_signal.Integral()>0:
        histogram_signal.Scale(50.0)
    histogram_signal.title = processes[0][1] + " x50"
    histogram_signal.linewidth=2
    histogram_signal.fillstyle = None
    #draw the signal shape
    hist([histogram_signal])
    
    histogram_total_mc.title = "pseudodata"
    histogram_total_mc.color = "black"

    histogram_total_bkg = sum([
        histograms_nominal[k] for k in histograms_nominal.keys()
        if k not in signal_processes]
    )
    
    #Get the data histogram
    data = None
    if not dataname is None:
        try:
            data = tf.get(pattern.format(sample=dataname, hname=hname))
        #try to read fake data
        except rootpy.io.file.DoesNotExist as e:
            print e
            data = tf.get(pattern.format(sample="data_obs", hname=hname))
        
        if "Graph" in data.__class__.__name__:
            data = graph_to_hist(data)

        data = postprocess_hist(data)
        if rebin > 1:
            data.rebin(rebin)
        if blindFunc:
            data = blindFunc(data)
        if show_overflow:
            fill_overflow(data)
        #data.title = "data ({0:.2f})".format(data.Integral())
        data.title = "data"
        data.marker = "o"
        data.markersize = 2
        data.linecolor = "black"

        if isinstance(data, rootpy.plotting.Hist):
            #set data error to 0 in case no data (FIXME) 
            for ibin in range(data.GetNbinsX()):
                if data.GetBinContent(ibin) == 0:
                    data.SetBinError(ibin, 1)
        errorbar(data)

    if do_legend:
        #create nice filled legend patches for all the processes
        patches = []
        if data:
            dataline = mlines.Line2D([], [], color='black', marker='o', label=data.title)
            patches += [dataline]

        #old matplotlib/rootpy
        if isinstance(stacked_hists["hists"][0], matplotlib.lines.Line2D):
            for line1, h in zip(stacked_hists["hists"], histograms_nominal.values()):
                patch = mpatches.Patch(color=line1.get_color(), label=h.title)
                patches += [patch]
        else: #new matplotlib/rootpy
            for (line1, line2), h in zip(stacked_hists["hists"], histograms_nominal.values()):
                patch = mpatches.Patch(color=line1.get_color(), label=h.title)
                patches += [patch]
        patches += [mlines.Line2D([], [], color=histogram_signal.color[0], label=histogram_signal.title, linewidth=2)]
        patches += [mpatches.Patch(facecolor="none", edgecolor="black", label="stat", hatch="//////")]
        patches += [mpatches.Patch(facecolor="none", edgecolor="gray", label="stat+syst", hatch=r"\\\\")]
        plt.legend(handles=patches, loc=legend_loc, numpoints=1, prop={'size':legend_fontsize}, ncol=2, frameon=False)
        
    #create an automatic bin width label on the y axis
    if ylabel == "auto":
        ylabel = "events / {0:.2f} {1}".format(histogram_signal.get_bin_width(1), xunit)
    plt.ylabel(ylabel)

    if data:
        #hide x ticks on main panel
        ticks = a1.get_xticks()
        a1.get_xaxis().set_visible(False)
    
    a1.set_ylim(bottom=0, top=2*a1.get_ylim()[1])
    a1.grid(zorder=100000)

    if do_log:
        a1.set_yscale("log")
        a1.set_ylim(bottom=1, top=100*a1.get_ylim()[1])

    a2 = a1
    
    ys_data = None

    #do ratio panel
    if data:
        a2 = plt.axes([0.0,0.0, 1.0, 0.18], sharex=a1)
        minorLocator = AutoMinorLocator()
        a2.yaxis.set_minor_locator(minorLocator)

        plt.xlabel(xlabel)
        a2.grid()
        
        ys_data = np.array([i for i in data.y()])
        
        data_ratio = data.clone()
        data_ratio.linecolor = "black"
        data_ratio.marker = "o"
        data_ratio.markersize = 2
        data_ratio.Divide(histogram_total_mc)

        #In case MC was empty, set data/mc ratio to 0
        for ibin in range(data_ratio.GetNbinsX()+1):
            bc = histogram_total_mc.GetBinContent(ibin)
            if bc > 0:
                data_ratio.SetBinError(ibin, data.GetBinError(ibin)/bc)
            if bc==0:
                data_ratio.SetBinContent(ibin, 0)
        
        #blind the data also on the ratio
        if blindFunc:
            data_ratio = blindFunc(data_ratio)
        errorbar(data_ratio)
        
        #Draw the stat
        ratio = stacked_hists["stat_error"]/ys
        ratio[np.isnan(ratio)] = 1.0
        ratio[np.isinf(ratio)] = 1.0
  
        plt.bar(
            xs,
            2.0*ratio,
            width=ws,
            bottom=1.0 - ratio,
            hatch="//////",
            facecolor="none",
            zorder=100,
            alpha=1.0
        )
        
        # #Draw the syst+stat
        ratio = stacked_hists["syst_error"]/ys
        ratio[np.isnan(ratio)] = 1.0
        ratio[np.isinf(ratio)] = 1.0

        print "-----***", ratio, ws

        plt.bar(
            xs,
            2.0*ratio,
            width=ws,
            bottom=1.0 - ratio,
            hatch="\\\\\\\\",
            facecolor="none",
            zorder=100,
            alpha=1.0
        )
        axes = plt.gca()
        #axes.set_xlim([0.5,1.5])


        pvalue = data.Chi2Test(histogram_total_mc, "UW")
        print data.Integral(), histogram_total_mc.Integral(), pvalue
        #plt.title("data={0:.1f} MC={1:.1f} r={2:.2f} p={3:.4E}".format(
        #    data.Integral(),
        #    stacked_hists["tot"].Integral(),
        #    data.Integral()/stacked_hists["tot"].Integral(),
        #    pvalue
        #    ), x=0.01, y=1.00, fontsize=10, horizontalalignment="left"
        #)
        plt.ylabel(r"$\frac{\mathrm{data}}{\mathrm{pred.}}$", fontsize=16)
        plt.axhline(1.0, color="black")
        #a2.set_ylim(0.5, 1.5)
        #hide last tick on ratio y axes
        #a2.set_yticks(a2.get_yticks()[:-1])
        a2.set_xticks(ticks)

    print "*******", xs

    return {
        "axes": (a1, a2),
        "xs": xs,
        "ys": ys,
        "ws": ws,
        "ys_data": ys_data,
        "nominal": histograms_nominal,
        "stacked": stacked_hists,
        "systematic": histograms_systematic,
        "counts" : counts,
    }

def escape_string(s):
    return s.replace("_", " ")

def draw_mem_data_mc(*args, **kwargs):
    a1, a2, hs = draw_data_mc(*args, **kwargs)
    plt.sca(a1)
    h = hs["tth_13TeV_phys14"].Clone()
    h.fillstyle = "hollow"
    h.linewidth = 2
    h.title = h.title + " x10"
    h.Scale(10)
    hist(h)
    plt.legend(loc=(1.01,0.0))
    a1.set_ylim(bottom=0)
    return a1, a2, hs

def calc_roc(h1, h2, rebin=1):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Rebin(rebin)
    h2.Rebin(rebin)

    if h1.Integral()>0:
        h1.Scale(1.0 / h1.Integral())
    if h2.Integral()>0:
        h2.Scale(1.0 / h2.Integral())
    roc = np.zeros((h1.GetNbinsX()+2, 2))
    err = np.zeros((h1.GetNbinsX()+2, 2))
    e1 = ROOT.Double(0)
    e2 = ROOT.Double(0)
    for i in range(0, h1.GetNbinsX()+2):
        I1 = h1.Integral(0, h1.GetNbinsX())
        I2 = h2.Integral(0, h2.GetNbinsX())
        if I1>0 and I2>0:
            roc[i, 0] = float(h1.IntegralAndError(i, h1.GetNbinsX()+2, e1)) / I1
            roc[i, 1] = float(h2.IntegralAndError(i, h2.GetNbinsX()+2, e2)) / I2
            err[i, 0] = e1
            err[i, 1] = e2
    return roc, err

def draw_shape(f, samples, hn, **kwargs):
    rebin = kwargs.get("rebin", 1)

    hs = []
    for s in samples:
        h = f.get(s[0] + hn).Clone()
        h.Scale(1.0 / h.Integral())
        h.rebin(rebin)
        h.title = s[1]
        hs += [h]

    coloriter = iter(plt.cm.jet(np.linspace(0,1,len(hs))))

    for h in hs:
        h.color = next(coloriter)
        errorbar(h)
    plt.legend()
    for h in hs:
        hist(h, lw=1, ls="-")

def svfg(fn, **kwargs):
    path = os.path.dirname(fn)
    if not os.path.exists(path):
        os.makedirs(path)
        time.sleep(2) #for NFS
    plt.savefig(fn, pad_inches=0.5, bbox_inches='tight', **kwargs)
    #plt.clf()


def get_yields(inf, cat, suffix, samples):
    hs = []
    for x in samples:
        try:
            h = inf.get("{0}{2}/{1}/jet0_pt".format(x, cat, suffix))
            hs += [h]
        except rootpy.io.DoesNotExist as e:
            pass
    if len(hs)==0:
        hs = [rootpy.plotting.Hist(10, 0, 1)]
    hs = sum(hs)
    
    e1 = ROOT.Double(0)
    i1 = hs.IntegralAndError(0, hs.GetNbinsX()+1, e1)
    return i1, e1

def get_sb(inf, cat, suffix):
    """
    Returns the S/sqrt(B) [sob] and error in a category.
    inf - input file (rootpy.io.File)
    cat - category string (e.g. "sl_mu_jge6_tge4")
    suffix - optional suffix string to append to samples (e.g. "_cfg_noME_jetPt20")

    returns (sob, error_sob)
    """

    signal = "ttH_hbb"
    backgrounds = ["ttbarOther", "ttbarPlusCCbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusBBbar"]
    
    i1, e1 = get_yields(inf, cat, suffix, [signal])
    i2, e2 = get_yields(inf, cat, suffix, backgrounds)

    sob = i1/np.sqrt(i2) if i2>0 else 0.0
    if i1>0 and i2>0:
        err_sob = sob * np.sqrt((e1/i1)**2 + (e2/i2)**2)
    else:
        err_sob = 0
    return i1/np.sqrt(i2), err_sob

def get_sb_cats(inf, categories, suffix=""):
    ys = []
    es = []
    xs = []
    for cat in categories:
        y, e = get_sb(inf, cat, suffix)
        xs += [cat]
        ys += [y]
        es += [e]
    xs_num = np.array(range(len(xs)))+0.5
    return xs, xs_num, ys, es

def get_cut_at_eff(h, eff):
    h = h.Clone()
    h.Scale(1.0 / h.Integral())
    hc = h.GetCumulative()
    bins = np.array([hc.GetBinContent(i) for i in range(1, hc.GetNbinsX()+1)])
    idx = np.searchsorted(bins, eff)
    return idx

def brazilplot(limits, categories, axes=None, doObserved=False, legend_loc=1):
    """Draws the a set of limits on a brazil plot

    Args:
        limits (dict of string->(lim, error): the actual limit data, as from CombineHelper:get_limits
        categories (list of string): the categories (dict keys) to draw
        category_names (list of string): The beautified names of the categories, in the same order as categories
        axes (None, optional): the pyplot axes to use

    Returns:
        TYPE: nothing
    """
    if not axes:
        axes = plt.axes()

    central_limits = []
    observed_limits = []
    injected_limits = []
    errs = np.zeros((len(categories), 4))

    #fill in the data
    i = 0
    for catname, cattitle in categories:

        #central value
        central_limits += [limits[catname][2]]
        observed_limits += [limits[catname][5]]
        injected_limits += [limits[catname][6]]

        #error band
        errs[i,0] = limits[catname][1]
        errs[i,1] = limits[catname][3]
        errs[i,2] = limits[catname][0]
        errs[i,3] = limits[catname][4]

        i += 1

    #y coordinates
    ys = np.array(range(len(categories)))

    table_data = []
    #draw points
    i = 0
    for y, l, o, inj, e1, e2, e3, e4 in zip(ys, central_limits, observed_limits, injected_limits, errs[:, 0], errs[:, 1], errs[:, 2], errs[:, 3]):

        leg_args = {}
        if i == 0:
            leg_args["label"] = "median"
        #black line
        axes.add_line(plt.Line2D([l, l], [y-0.45, y+0.45], lw=2, color="black", ls="--", **leg_args))

        leg_args = {}
        if i == 0:
            leg_args["label"] = "$\mu=1$ injected"
        #black line
        axes.add_line(plt.Line2D([inj, inj], [y-0.45, y+0.45], lw=2, color="red", ls="--", **leg_args))

        
        leg_args = {}
        #axes.add_line(plt.Line2D([o, o], [y-0.4, y+0.4], lw=2, color="black", ls="-"))
        if i == 0:
            leg_args["label"] = "observed"
        if doObserved:
            axes.errorbar([o], [y], [0.4], marker="s", color="black", **leg_args)
        
        #value
        #plt.text(l+0.5, y, "{0:.2f}".format(l), horizontalalignment="left", verticalalignment="center")

        leg_args1 = {}
        leg_args2 = {}
        if i == 0:
            leg_args1["label"] = "95% expected"
            leg_args2["label"] = "68% expected"
        #error bars
        axes.barh(y, (e4-e3), height=0.8, left=e3, color=np.array([254, 247, 2])/255.0, lw=0, align="center", **leg_args1)
        axes.barh(y, (e2-e1), height=0.8, left=e1, color=np.array([51, 247, 2])/255.0 , lw=0, align="center", **leg_args2)
        table_data += [(categories[i][1], e3, l, e4, o, inj)]
        i += 1
    #set ranges

    plt.xlim(0, 1.2*max(central_limits))
    plt.ylim(ys[0]-0.5, ys[-1]*1.2)

    #set category names
    plt.yticks(ys, [k[1] for k in categories], verticalalignment="center", fontsize=22, ha="right")
    plt.xlabel("95% CL on $\mu$")
    yax = axes.get_yaxis()
    
    
    minorLocator = AutoMinorLocator()
    axes.xaxis.set_minor_locator(minorLocator)

    axes.tick_params(axis = 'both', which = 'major', labelsize=16)
    axes.tick_params(axis = 'both', which = 'minor')

    plt.legend(loc=legend_loc, fontsize=12, numpoints = 1, frameon=False, ncol=2)
    plt.title(
        r"$\mathbf{CMS}$ Work In Progress",
        fontsize=16, x=0.05, ha="left", y=0.95, va="top", fontname="Helvetica"
    )
    plt.text(0.99, 1.00,
        "$35.9\ \mathrm{fb}^{-1}\ \mathrm{(13\ TeV)}$",
        fontsize=16, ha="right", va="bottom", transform=axes.transAxes, fontname="Helvetica"
    )

    # find the maximum width of the label on the major ticks
    #pad = 150
    #yax.set_tick_params(pad=pad)
    return table_data
    #plt.grid()

def make_df_hist(bins, x, w=1.0):
    h = rootpy.plotting.Hist(*bins)
    a = np.array(x).astype("float64")
    if isinstance(w, float):
        b = np.repeat(w, len(a)).astype("float64")
    else:
        b = np.array(w).astype("float64")
    h.FillN(len(a), a, b)
    return h

if __name__ == "__main__":
    tf = rootpy.io.File("test.root")

    r = draw_data_mc(tf, "mu__jet_pt",
        [
            ("ttjets_heavy", "tt+hf"),
            ("ttjets_light", "tt+lf")
        ], [],
        systematics = [
            ("__jecUp", "__jecDown"),
            ("__jerUp", "__jerDown"),
        ],
        dataname="data",
        legend_loc="best",
        legend_fontsize=16,
        colors={"ttjets_heavy": "darkred", "ttjets_light": "red"},
        rebin=2
    );
    svfg("./test_data_mc.pdf")

    tf.close()
