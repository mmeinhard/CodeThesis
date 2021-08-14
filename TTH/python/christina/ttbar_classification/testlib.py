import matplotlib
matplotlib.use("Agg")
import numpy as np
import ROOT
from root_numpy import fill_hist
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.metrics import roc_curve, auc
from sklearn.externals import joblib
import sys
import os
import glob
import pandas as pd
import rootpy.plotting.root2matplotlib as rplt
import matplotlib as mpl
from rootpy.plotting import Hist
from scipy.interpolate import interp1d

# logit transformation
def logit(x):

    res = np.log(x / (1-x))
    return res



# calculate naive discriminator
def CSVM(btags, d, proc):

    # cut on events from special process 
    if proc == "2b":
        d_cut = d[d["ttCls"] == 0]
    elif proc == "4b":
        d_cut = d[d["ttCls"] == 1] 
    nevt = d_cut.shape[0]
    #print "number of " + proc + " " + str(nevt)

    # use nBCSVM as discriminant
    if btags == 4:
        d_cut = d_cut[d_cut["nBCSVM"] >= btags]
    elif btags == 3:
        d_cut = d_cut[d_cut["nBCSVM"] == btags]
    nevt_nBCSVM = d_cut.shape[0]

    eff = nevt_nBCSVM/float(nevt)

    #print eff
    return eff


# plot histograms 
def histograms(test):

    test = pd.read_csv(test) 

    numJets = 6
    var = ["jets_btagCSV_" + str(x) for x in range(numJets)]
    test_4b = test[test["ttCls"] == 1]
    test_2b = test[test["ttCls"] == 0]
    data_4b = np.array(test_4b[var])
    data_4b = np.sort(data_4b)
    data_2b = np.array(test_2b[var])
    data_2b = np.sort(data_2b)


    # plot histograms
    for i in var:
        fig = plt.figure()

        label = var[-(var.index(i)+1)]
        print label

        plt.hist(data_4b[:,var.index(i)], 50, range = (0.0,1.0), normed = 1, histtype = "step", alpha = 0.75, label = "4b")
        plt.hist(data_2b[:,var.index(i)], 50, range = (0.0,1.0), normed = 1, histtype = "step", alpha = 0.75, label = "2b")
        plt.xlabel(label)
        plt.legend(loc = "lower left")
        plt.ylabel("number of entries")
        #plt.grid(True)

        fig.savefig("histograms/" + label + ".pdf")


# function to merge gc output
def load_gc_output(fpath):

    # load grid-control output
    os.chdir(fpath)

    count = 0
    for npfile in glob.glob("*_dataframe.csv"):
        filepath = os.path.join(fpath, npfile)
        print filepath
        if count == 0:
            d = pd.read_csv(filepath)
        else:
            d = d.append(pd.read_csv(filepath), ignore_index = True)
        count += 1

    return d
    


# make ttH test sample
def test_sample(fpath_4b, fpath_2b):

    d_4b = load_gc_output(fpath_4b)

    # set ttCls to one in whole sample
    d_4b["ttCls"] = 1
    os.chdir(sys.path[0])
    d_4b.to_csv("output/dataframe_4b.csv")

    d_2b = load_gc_output(fpath_2b)
    # make sure to only consider tt+light events
    d_2b = d_2b[d_2b["ttCls"] == 0]

    # merge two dataframes to test sample
    d_4b = d_4b.append(d_2b, ignore_index=True)
    d = d_4b.sample(frac=1, random_state=0).reset_index(drop=True)
    os.chdir(sys.path[0])
    d.to_csv("output/dataframe_test.csv")


# function to plot input histograms in ROC curve
def plot_input(process, h, plot):

    ax = {}

    fig = plt.figure()
    for p in process:

        h[p].linewidth = 1
        if p == "4b":
            h[p].linecolor = "b"
        if p == "2b":
            h[p].linecolor = "r"

        h[p].Rebin(10)

        ax[p], = rplt.step(h[p])

    names = [i for i in process]
    ob = [ax[i] for i in process]
    plt.legend(ob, names, prop={'size': 18})
    os.chdir(sys.path[0])
    fig.savefig("output/input_" + plot + ".pdf")



# calculate fpr, tpr for roc curve
def roc(y_true, y_score, unc = False , weight = None, plot = None):

    # fill histo to calculate tpr, fpr
    h = {}
    c_histo = {}

    nbin = 10000 
    hmin = np.amin(y_score)
    hmax = np.amax(y_score)

    if hmin == -9999 or hmin == -10:
        hmin = 0

    #output = ROOT.TFile.Open("output/BLR.root", "RECREATE")

    process = ["4b", "2b"]
    for p in process:
        h[p] = Hist(nbin, hmin, hmax, name = p, title = p)
        if p == "4b":
            y_filtered = y_score[y_true == 1]
            if unc == True:
                weights = weight[y_true == 1] 
        elif p == "2b":
            y_filtered = y_score[y_true == 0]
            if unc == True:
                weights = weight[y_true == 0]
        if unc == True:
            fill_hist(h[p], y_filtered, weights=weights)
        else:
            fill_hist(h[p], y_filtered)
        N = h[p].Integral()
        if N == 0:
            raise ValueError("Integral of histogram equals zero, normalization not possible")
        else:
            h[p].Scale(1.0/N)

        #h[p].Write()

        c_histo[p] = h[p].GetCumulative()
    
    nbin = h[process[0]].GetNbinsX()
    tpr = []
    fpr = []

    for j in range(0, nbin + 2):
        #tpr.append(1 - c_histo[process[0]].GetBinContent(j))
        #fpr.append(1 - c_histo[process[1]].GetBinContent(j))
        tpr.append(float(h[process[0]].Integral(j, nbin+2)))
        fpr.append(float(h[process[1]].Integral(j, nbin+2)))

    if plot != None:

        plot_input(process, h, plot)

    #output.Close()    
    return tpr, fpr

# plot comparison of input files based on .root files containing histograms
def comparison_inputs(file1, file2, name1, name2, output):

    f = root_open(file1)
    h1 = f.Get(name1)

    f = root_open(file2)
    h2 = f.Get(name2)

    fig = plt.figure()
    h1.linewidth = 1
    h2.linewidth = 1
    h1.linecolor = "b"
    h2.linecolor = "r"

    nbin1 = h1.GetNbinsX()
    nbin2 = h2.GetNbinsX()
    #print nbin1
    #print nbin2
    h1.Rebin(10)
    h2.Rebin(10)

    ax1, = rplt.step(h1)
    ax2, = rplt.step(h2)

    names = ["joosep", "christina"]
    ob = [ax1, ax2]
    plt.legend(ob, names, prop={"size":18})
    os.chdir(sys.path[0])
    fig.savefig(output + ".pdf")


# plot roc curves
def plot_roc(true, test, unc, weight, style, label):

    if unc == True:
        tpr_up, fpr_up = roc(true, test, unc = unc,  weight = weight )
        f_up = interp1d(tpr_up, fpr_up)
        tpr_down, fpr_down = roc(true, test, unc = unc, weight = weight)
        f_down = interp1d(tpr_down, fpr_down)
        tpr, fpr = roc(true, test, unc = unc, weight = weight)
        f = interp1d(tpr, fpr)

        xnew = np.linspace(min(tpr), max(tpr), num = 1000, endpoint = True)

        #plt.plot(tpr, fpr, style, label=label)
        #plt.plot(tpr_up, fpr_up, style, alpha = 0.5 )
        #plt.plot(tpr_down, fpr_down, style, alpha = 0.5)
        plt.semilogy(tpr, fpr, style, label=label, zorder = 500)
        plt.semilogy(tpr_up, fpr_up, style, alpha = 0.5 )
        plt.semilogy(tpr_down, fpr_down, style, alpha = 0.5)
        plt.fill_between(xnew, f_up(xnew), f_down(xnew), style, alpha = 0.5)
    else:
        tpr, fpr = roc(true, test)
        #plt.plot(tpr, fpr, style, label=label)
        plt.semilogy(tpr, fpr, style, label=label)

    return tpr, fpr

# measure improvment in comparison to naive estimate
def improvement(eff_sig, eff_bkg, tpr, fpr, c = "k--"):

    f = interp1d(tpr, fpr, kind="linear")
    xnew = np.linspace(min(tpr), max(tpr), num = 1000, endpoint = True)

    #plt.plot(xnew, f(xnew), c)
    print "Naive estimate:", eff_bkg
    print "Alternative:", f(eff_sig)
    print "Improvement:", eff_bkg/f(eff_sig)


# plot roc curves for test and training sample in same figure
def plot_test_training(classifier, btagger, data_test, data_train, unc = False):

    data = {"test" : data_test, "train" : data_train}

    fig = plt.figure()

    clf = joblib.load(classifier)
    numJets = 6
    var = [btagger, "pt", "eta"]
    arrays = {}

    for i in ["test", "train"]:

        d = pd.read_csv(data[i])
        l = []

        for n in var:
            names = ["jets_" + n + "_" + str(x) for x in range(numJets)]
            arr = np.array(d[names])
            if n == btagger:
                index = np.argsort(arr, axis = -1)
                static = np.indices(arr.shape)
            arr = arr[static[0], index]
            #arr = np.sort(arr)
            l.append(arr)

        arrays[i] = l
        if i == "test":
            y_test = np.array(d["ttCls"])
            X_test = np.hstack(tuple(arrays[i]))
        elif i == "train":
            y_train = np.array(d["ttCls"])
            X_train = np.hstack(tuple(arrays[i]))

    # plot test sample
    y_score = clf.decision_function(X_test)
    #y_score = clf.predict_proba(X_test)[:,0]
    tpr, fpr = plot_roc(y_test, y_score, unc, False, "r-", "test")


    # plot train sample
    y_score = clf.decision_function(X_train)
    #y_score = clf.predict_proba(X_test)[:,0]
    tpr, fpr = plot_roc(y_train, y_score, unc, False, "b-", "train")

    # some further style settings
    plt.xlim([0.0, .5])
    #plt.ylim([0.0, 1.05])
    plt.ylabel('tt+jets (light) efficiency', fontsize=16)
    plt.xlabel('ttH efficiency', fontsize=16)
    plt.title(r"SL, $N_j = 6$", fontsize=16)
    plt.legend(loc="upper left")
    os.chdir(sys.path[0])
    fig.savefig("output/roc_" + btagger + "_test_train.pdf")



# plot all roc curves and naiv estimate in same figure 
def plot_comp(btaggers, data, unc = False):

    fig = plt.figure()

    # load test sample
    test = pd.read_csv(data)

    # add naive estimates
    eff_sig_4 = CSVM(4, test, "4b")
    eff_bkg_4 = CSVM(4, test, "2b")
    plt.scatter([eff_sig_4], [eff_bkg_4], c="k", marker = "^", label = "4x BCSVM", zorder = 1000)

    eff_sig_3 = CSVM(3, test, "4b")
    eff_bkg_3 = CSVM(3, test, "2b")
    plt.scatter([eff_sig_3], [eff_bkg_3], c="k", marker = "o", label = "3x BCSVM", zorder = 1000)

    # BDT btagCSV output
    for b in btaggers:
        clf = joblib.load("output/classifier_" + b + ".pkl")
        numJets = 6
        l = []
        var = [b, "pt", "eta"]
        for n in var:
            names = ["jets_" + n + "_" + str(x) for x in range(numJets)]
            arr = np.array(test[names])
            if n == b:
                index = np.argsort(arr, axis = -1)
                static = np.indices(arr.shape)
            arr = arr[static[0], index]
            #arr = np.sort(arr)
            l.append(arr)

        X_test = np.hstack(tuple(l))
        #print X_train.shape
        y_test = np.array(test["ttCls"])

        y_score = clf.decision_function(X_test)
        #y_score = clf.predict_proba(X_test)[:,0]
        if b == "btagCSV":
            tpr, fpr = plot_roc(y_test, y_score, unc, False, "r-", "BDT (CSV)")
        elif b == "btagDeepCSV":
            tpr, fpr = plot_roc(y_test, y_score, unc, False, "m-", "BDT (DeepCSV)")
        improvement(eff_sig_4, eff_bkg_4, tpr, fpr)

    # BLR 
    blr = test["btag_LR_4b_2b_btagCSV"]
    #blr = logit(blr)
    ttCls = np.array(test["ttCls"])
    tpr, fpr = plot_roc(ttCls, blr, unc, False, "g-", "BLR")
    improvement(eff_sig_4, eff_bkg_4, tpr, fpr)

    # 3rd jet btagCSV
    jetbtag = X_test[:,3]
    ttCls = np.array(test["ttCls"])
    tpr, fpr = plot_roc(ttCls, jetbtag, unc, False, "b-", "3rd jet btagCSV")

    # some further style settings
    plt.xlim([0.0, .5])
    #plt.ylim([0.0, 1.05])
    plt.ylabel('tt+jets (light) efficiency', fontsize=16)
    #plt.xlabel('ttH efficiency', fontsize=16)
    plt.xlabel('tt+bb efficiency', fontsize=16)
    plt.title(r"SL, $N_j = 6$", fontsize=16)
    plt.legend(loc="upper left")
    os.chdir(sys.path[0])
    fig.savefig("output/roc_comp.pdf")

if __name__ == "__main__":

    #test_sample("/mnt/t3nfs01/data01/shome/creissel/tth/gc/bdt/GC61b0ed3d6c5e/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8", "/mnt/t3nfs01/data01/shome/creissel/tth/gc/bdt/GC61b0ed3d6c5e/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8")
    #histograms("output/dataframe_ttH.csv")
    #plot_comp(["output/classifier_btagCSV.pkl", "output/classifier_btagDeepCSV.pkl"], "output/dataframe_test.csv", unc = False)
    #plot_test_training("output/classifier_btagDeepCSV.pkl", "btagDeepCSV", "output/test.csv", "output/train.csv", unc = False)
    #plot_test_training("output/classifier_btagCSV.pkl", "btagCSV", "output/test.csv", "output/train.csv", unc = False)
    plot_comp(["btagCSV", "btagDeepCSV"], "output/test.csv", unc = False)

