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

    arr = tree2array(chain, branches=["is_sl", "is_dl"])
    d = pd.DataFrame(arr)

# save pandas dataframe
    #print d
    d.to_csv("dataframe.csv", index = False)


if __name__ == "__main__":

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    else:
        file_names = np.loadtxt("/mnt/t3nfs01/data01/shome/creissel/tth/sw/CMSSW/src/TTH/MEAnalysis/gc/datasets/nano_05Feb2018/step2/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.txt", usecols = [0], dtype = str, skiprows = 1)
        file_names = file_names[:10]
        # print file_names

    read_data(file_names)

