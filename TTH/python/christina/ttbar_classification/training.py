import matplotlib
matplotlib.use("Agg")
import numpy as np
import ROOT
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split 
import os
import glob
from sklearn.externals import joblib
import sys
import pandas as pd

### fast part: training
def training(fpath, btaggers):

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

    os.chdir(sys.path[0])
    d.to_csv("output/dataframe.csv")

# label data correctly
    # define all tt+b jets processes as signal
    d.loc[d["ttCls"] > 50, "ttCls"] = 1
    # remove tt+cc processes
    d = d[(d['ttCls'] == 0) | (d['ttCls'] == 1)]

# divide dataframe in train and test sample
    d = d.sample(frac=1, random_state=0).reset_index(drop=True)
    #print d
    nevt = d.shape[0]
    train = d[:int(nevt*0.9)]
    test = d[int(nevt*0.9):]

    train.to_csv("output/train.csv")
    test.to_csv("output/test.csv")

# get arrays as BDT input
    numJets = 6

    for b in btaggers:

        l = []
        var = [b, "pt", "eta"]
        for n in var:
            names = ["jets_" + n + "_" + str(x) for x in range(numJets)]
            arr = np.array(train[names])
            if n == b:
                index = np.argsort(arr, axis = -1)
                static = np.indices(arr.shape)
            arr = arr[static[0], index]        
            #arr = np.sort(arr)
            l.append(arr)

        X_train = np.hstack(tuple(l))
        #print X_train.shape
        y_train = np.array(train["ttCls"])

# construct estimator for classification
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0) 
        clf.fit(X_train, y_train)
    
        n_classes = clf.n_classes_
        print "number of classes:", n_classes
        print "mean score:", clf.score(X_train, y_train)
        print "feature importance:", clf.feature_importances_

# save model
        joblib.dump(clf, "output/classifier_" + b + ".pkl")

    """
    from sklearn import svm
    clf = svm.SVC()
    clf.fit(data_train, target_train)
    print clf.score(data_test, target_test)
    """
if __name__ == "__main__":

    training("/mnt/t3nfs01/data01/shome/creissel/tth/gc/bdt/GC92ddf318943f/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8", ["btagCSV", "btagDeepCSV"])
