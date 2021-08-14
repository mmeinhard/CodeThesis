import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
import os
import glob
import sys
from scipy.interpolate import interp1d

# function to make ttH test sample
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

# function to sort the jets according to the btagging discriminant
def make_BDT_input(data, features, btagger):

    l = []
    numJets = 6

    for n in features:
        names = ["jets_" + n + "_" + str(x) for x in range(numJets)]
        arr = np.array(data[names])
        if n == btagger:
            index = np.argsort(arr, axis = -1)
            static = np.indices(arr.shape)
        arr = arr[static[0], index]
        l.append(arr)

    X = np.hstack(tuple(l))
    y = np.array(data["ttCls"])
    return X, y

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

# function to plot discriminant distribution
def input_distributions(csvfile, var, btagger = None):

    sample = pd.read_csv(csvfile)
    
    sample_4b = sample[sample["ttCls"] == 1]
    sample_2b = sample[sample["ttCls"] == 0]

    fig = plt.figure()

    if var == "BDT":
        
        if btagger == None:
            raise ValueError('BDT output requires the btagging algorithm.')
        else:
            clf = joblib.load("output/classifier_" + btagger + ".pkl")
            numJets = 6
            features = [btagger, "pt", "eta"]
            
            print clf.classes_

            X_4b, y_4b = make_BDT_input(sample_4b, features, btagger)
            #y_4b_score = clf.decision_function(X_4b)
            y_4b_score = clf.predict_log_proba(X_4b)[:,1]
            print y_4b_score
            X_2b, y_2b = make_BDT_input(sample_2b, features, btagger)
            #y_2b_score = clf.decision_function(X_2b)
            y_2b_score = clf.predict_log_proba(X_2b)[:,1]
            print y_2b_score

            plot_4b = y_4b_score
            plot_2b = y_2b_score

    elif var == "jetsBybtag_3":

        if btagger == None:
            raise ValueError('Variable requires btagging algorithm.')
        else:
            numJets = 6
            names = ["jets_" + btagger + "_" + str(x) for x in range(numJets)]
            arr = np.array(sample_4b[names])
            np.sort(arr)
            plot_4b = arr[:,3]

            arr = np.array(sample_2b[names])
            np.sort(arr)
            plot_2b = arr[:,3]
                
    else:

        plot_4b = sample_4b[var]
        plot_2b = sample_2b[var]        


    plt.hist(plot_4b, 50, range = (np.amin(plot_4b), np.amax(plot_4b)), normed = 1, histtype = "step", alpha = 0.75, label = "4b") 
    plt.hist(plot_2b, 50, range = (np.amin(plot_2b), np.amax(plot_2b)), normed = 1, histtype = "step", alpha = 0.75, label = "2b")
    plt.xlabel(var)
    plt.legend(loc="upper left")
    plt.ylabel("number of entries")
    
    fig.savefig("output/distribution_" + var + ".pdf")

# function to calculate improvement
def improvement(eff_sig, eff_bkg, tpr, fpr, c = "k--"):

    f = interp1d(tpr, fpr, kind="linear")
    xnew = np.linspace(min(tpr), max(tpr), num = 1000, endpoint = True)

    #plt.plot(xnew, f(xnew), c)
    print "Naive estimate:", eff_bkg
    print "Alternative:", f(eff_sig)
    print "Improvement:", eff_bkg/f(eff_sig)


# plot roc curve
def roc_comp(csvfile, var, btagger):

    sample = pd.read_csv(csvfile)
    numJets = 6

    fig = plt.figure()

    # add naive estimates
    eff_sig_4 = CSVM(4, sample, "4b")
    eff_bkg_4 = CSVM(4, sample, "2b")
    plt.scatter([eff_sig_4], [eff_bkg_4], c="k", marker = "^", label = "4x BCSVM", zorder = 1000)

    eff_sig_3 = CSVM(3, sample, "4b")
    eff_bkg_3 = CSVM(3, sample, "2b")
    plt.scatter([eff_sig_3], [eff_bkg_3], c="k", marker = "o", label = "3x BCSVM", zorder = 1000)

    from sklearn import metrics

    for v in var:
        
        if v == "BDT":

            clf = joblib.load("output/classifier_" + btagger + ".pkl")
            features = [btagger, "pt", "eta"]

            X, y = make_BDT_input(sample, features, btagger)
            y_score = clf.predict_log_proba(X)[:,1]

            fpr, tpr, thresholds = metrics.roc_curve(y, y_score, pos_label = 1)
            improvement(eff_sig_4, eff_bkg_4, tpr, fpr)
            plt.semilogy(tpr, fpr, "r-", label = "BDT")

        elif v == "jetsBybtag_3":

            names = ["jets_" + btagger + "_" + str(x) for x in range(numJets)]
            arr = np.array(sample[names])
            arr = np.sort(arr)
            jetsbybtag_3 = arr[:,3]

            fpr, tpr, thresholds = metrics.roc_curve(sample["ttCls"], jetsbybtag_3, pos_label = 1)
            improvement(eff_sig_4, eff_bkg_4, tpr, fpr)
            plt.semilogy(tpr, fpr, "b-", label = "3rd jet btag")

        else:
    
            fpr, tpr, thresholds = metrics.roc_curve(sample["ttCls"], sample[v], pos_label = 1)
            improvement(eff_sig_4, eff_bkg_4, tpr, fpr)
            plt.semilogy(tpr, fpr, "g-", label = "BLR")

    plt.legend(loc="upper left")
    plt.xlim([0.0,0.5])
    plt.xlabel("tt+bb efficiency")
    #plt.xlabel("ttH efficiency")
    plt.ylabel("tt+jets (light) efficiency")
    plt.title("SL, N_j = 6, btagCSV")
    fig.savefig("output/roc_comp.pdf")

if __name__ == "__main__":

    #input_distributions("output/test.csv", "btag_LR_4b_2b_btagCSV", "btagCSV")
    #input_distributions("output/test.csv", "BDT", "btagCSV")
    #input_distributions("output/test.csv", "jetsBybtag_3", "btagCSV")

    #test_sample("/mnt/t3nfs01/data01/shome/creissel/tth/2017/gc/bdt/GCd0aee52f0099/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8", "/mnt/t3nfs01/data01/shome/creissel/tth/2017/gc/bdt/GCd0aee52f0099/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8")

    roc_comp("output/full.csv", ["btag_LR_4b_2b_btagCSV", "BDT", "jetsBybtag_3"], "btagCSV")

