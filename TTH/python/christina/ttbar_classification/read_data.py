import numpy as np
import ROOT
import pandas as pd
from root_numpy import tree2array
import os
from TTH.MEAnalysis.samples_base import getSitePrefix

### slow part: read and prepare data for training
def read_data(file_names):

# Adding all files to TChain
    
    chain = ROOT.TChain("tree")     
    for file_name in file_names:         
        print "Adding file {0}".format(file_name)         
        chain.AddFile(file_name)         
    print "Chain contains {0} events".format(chain.GetEntries())

    numJets = 6
    arr = tree2array(chain, branches=["jets_btagCSV", "jets_btagDeepCSV", "is_sl", "is_dl", "btag_LR_4b_2b_btagCSV", "ttCls", "nBCSVM", "jets_pt", "jets_eta"], selection="numJets=={0}".format(numJets))
    d = pd.DataFrame(arr)

# apply cuts: semi-leptonic events 
    d = d[(d['is_sl'] == 1)]
    #d = d[(d['is_sl'] == 1) | (d['is_dl'] == 1)]
    #d = d[(d['ttCls'] == 0) | (d['ttCls'] >= 51)]

# split jet values

    for n in ["btagCSV", "btagDeepCSV", "pt", "eta"]:

        j = pd.DataFrame(d["jets_" + n].values.tolist())
        names = []
        for i in range(j.shape[1]):
            names.append("jets_" + n + "_" + str(i))
        j.columns = names

        d = d.reset_index(drop=True)
        d = pd.concat([d,j], axis = 1)
        d = d.drop(["jets_" + n], axis = 1)

# save pandas dataframe
    print d
    d.to_csv("dataframe.csv", index = False)

"""
# split per jet variables btagCSV
    j = pd.DataFrame(d["jets_btagCSV"].values.tolist())
    names = []
    for i in range(j.shape[1]):
        names.append("jets_btagCSV_" + str(i))
    #print names
    j.columns = names

# get arrays as BDT input
    var = ["jets_btagCSV_" + str(x) for x in range(numJets)]
    data = np.array(j[var])
    target = np.array(d["ttCls"])
    blr = np.array(d["btag_LR_4b_2b_btagCSV"])
    btagWeight_up = np.array(d["btagWeightCSV_up_lf"])
    btagWeight_down = np.array(d["btagWeightCSV_down_lf"])

# save arrays to text file
    np.save("data.npy", data)
    np.save("target.npy", target)
    np.save("blr.npy", blr)
    np.save("btagWeightCSV_up.npy", btagWeight_up)
    np.save("btagWeightCSV_down.npy", btagWeight_down)
"""

if __name__ == "__main__":

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    else:
        file_names = np.loadtxt("/mnt/t3nfs01/data01/shome/creissel/tth/sw/CMSSW/src/TTH/MEAnalysis/gc/datasets/nano_05Feb2018/step2/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.txt", usecols = [0], dtype = str, skiprows = 1)
        file_names = file_names[:10]
        # print file_names

    read_data(file_names)

