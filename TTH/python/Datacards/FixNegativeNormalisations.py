#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname
from array import array
import pandas
import rootpy
from rootpy.tree import Tree, TreeChain
from rootpy.io import root_open
import ROOT

import numpy as np

#from Helpers import *

def lvec(pt,eta,phi,mass):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(pt, eta, phi, mass)
    return lv

def round_decimals_up(number, decimals=10):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor


########################################
# Run code
########################################

# Function to create histograms
def process(file_names, output_file):

# file_names (list of strings): list of the file names to be opened
# skip_events (int): index of the first event (0-based) to be processed
# max_events (int): number of events to be processed
# variables (list of strings): names of variables from root file that are considered
# output_file (string): name/ path of output file

    # Output file
    #output = root_open(output_file, 'recreate')

    newhists = {}


    f = ROOT.TFile.Open(file_names[0])
    for key in f.GetListOfKeys():
        h = key.ReadObj()
        #if "avgdetabtag" in h.GetName():
        #    print h.GetName(), h.ClassName()
        if h.ClassName() == 'TH1D' or h.ClassName() == 'TH2F':
            #print h.GetName(),h.GetName().replace("_2017","")
            newhists[h.GetName()] = h.Clone()
            newhists[h.GetName()].SetDirectory(0)
    for key in f.GetListOfKeys():
        h = key.ReadObj()
        if h.ClassName() == 'TH1D' or h.ClassName() == 'TH2F':        
	    if newhists[h.GetName()].Integral() < 0:
                print newhists[h.GetName()].GetName(), "has weight below zero!!!", newhists[h.GetName()].Integral()
                if newhists[h.GetName()].GetName()[-2:] == "Up":
		    comp = newhists[h.GetName()].GetName()[:-2] + "Down"
		    comphist = newhists[comp]
		    nomdic = newhists[h.GetName()].GetName().split("__")
 		    nom = nomdic[0]+"__"+nomdic[1]+"__"+nomdic[2]
		    nomhist = newhists[nom]
		    for i in range(0,newhists[h.GetName()].GetNbinsX()+1):
			no = nomhist.GetBinContent(i)
        	        var = comphist.GetBinContent(i)
			if (no-var) > 0:
			    cor = no + (no-var)
			else:
              		    cor = no - (var-no)
			#print no, var, cor
                        newhists[h.GetName()].SetBinContent(i,cor)
	
		elif newhists[h.GetName()].GetName()[-4:] == "Down":
		    comp = newhists[h.GetName()].GetName()[:-4] + "Up"
                    comphist = newhists[comp]
                    nomdic = newhists[h.GetName()].GetName().split("__")
                    nom = nomdic[0]+"__"+nomdic[1]+"__"+nomdic[2]
                    nomhist = newhists[nom]
                    for i in range(0,newhists[h.GetName()].GetNbinsX()+1):
                        no = nomhist.GetBinContent(i)
                        var = comphist.GetBinContent(i)
                        if (no-var) > 0:
                            cor = no + (no-var)
                        else:
                            cor = no - (var-no)
                        #print no, var, cor
			newhists[h.GetName()].SetBinContent(i,cor)
		print "fixed integral to", newhists[h.GetName()].Integral()

    for key in f.GetListOfKeys():
        h = key.ReadObj()
        if h.ClassName() == 'TH1D' or h.ClassName() == 'TH2F':
            if newhists[h.GetName()].Integral() < 0:
		print newhists[h.GetName()].GetName(), "has weight below zero!!!", newhists[h.GetName()].Integral()
		print "last resort"
          	factor = -newhists[h.GetName()].Integral()
                nbins = newhists[h.GetName()].GetNbinsX()
                correction = round_decimals_up(factor / nbins)
                #print factor, nbins, correction
                for i in range(0,newhists[h.GetName()].GetNbinsX()+1):
                    newhists[h.GetName()].SetBinContent(i,newhists[h.GetName()].GetBinContent(i)+correction)
                print "fixed integral to", newhists[h.GetName()].Integral()



            #newhists[h.GetName().replace("_2017","")]
            #hnames.append(h.GetName())







    #output.cd()
    #outtree.Write()
    #output.Close()

    
    f.Close()
    #ff.Close()


    results = ROOT.TFile(output_file,"recreate")
    for key, value in newhists.iteritems():
        value.Write(key)
    results.Close()

if __name__ == "__main__":

    ##### Settings

    import os
    if os.environ.get("FILE_NAMES") is not None:
        file_names = os.environ["FILE_NAMES"].split()
    else:
        fi1 = "/work/mameinha/tth/gc/sparse/Feb5_FitFromZero.root"
        file_names = [fi1]

    output_file = 'out_fulleta_fixed.root'

    process(file_names, output_file)
                                        
