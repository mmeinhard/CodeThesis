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

### plot reconstruction matrix
def matrix(fpath):

    # load grid-control output
    folders = [x[1] for x in os.walk(fpath)][0]
    print folders

    res = {}

    for f in folders:
        path = fpath + "/" + f
        print path
        os.chdir(path)
        count = 0
        for npfile in glob.glob("*_dataframe.csv"):
            filepath = os.path.join(path, npfile)
            print filepath
            if count == 0:
                d = pd.read_csv(filepath)
            else:
                d = d.append(pd.read_csv(filepath), ignore_index = True)
            count += 1
        
        # make leptonic gen vs. reco matrix    

        tot = d.shape[0]
        cat = ["sl", "dl", "fh"]
        reco = {}
        for c in cat:
            if c == "sl":
                d_reco = d[(d['is_sl'] == 1)]
            elif c == "dl":
                d_reco = d[(d['is_dl'] == 1)]
            elif c == "fh":
                d_reco = d[(d['is_dl'] == 0) & (d['is_sl'] == 0)]
            nevt = d_reco.shape[0]
            r = nevt/float(tot)
            reco[c] = r

        if f.find("TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8") != -1:
            res["sl"] = reco 
        if f.find("TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8") != -1:
            res["dl"] = reco
    
    #print res
    m = pd.DataFrame(res)
    print m

if __name__ == "__main__":

    matrix("/mnt/t3nfs01/data01/shome/creissel/tth/gc/bdt/GCb662f90b6af9")
