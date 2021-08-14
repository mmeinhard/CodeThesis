#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname
import ROOT
ROOT.gSystem.Load("libTTHMEAnalysis")
from array import array


Cvectordouble = getattr(ROOT, "std::vector<double>")

########################################
# Define Input Files and
# output directory
########################################

def vec_from_list(vec_type, src):
    """
    Creates a std::vector<T> from a python list.
    vec_type (ROOT type): vector datatype, ex: std::vector<double>
    src (iterable): python list
    """
    v = vec_type()
    for item in src:
        v.push_back(item)
    return v


########################################
# Run code
########################################

def process(file_names, output_file): 

    files = ' '.join(file_names)
    os.system('hadd -f tree.root ' + files)
    
    f = ROOT.TFile.Open("tree.root", "READ")
    ttree = f.Get("tree")

    outfile = ROOT.TFile("out.root","recreate")
    #outtree = ROOT.TTree("tree", "Skimmed nano tree")
    print "hereh"

    outtree = ttree.CloneTree(-1)
    f.Close()

    print "hereh"
    
    bufs = {}
    #bufs["PDFweight_central"] = array( 'f', [ 0 ] )
    bufs["PDFweight_up"] = array( 'f', [ 0 ] )
    bufs["PDFweight_down"] = array( 'f', [ 0 ] )
    
    
    #outtree.Branch("PDFweight_central", bufs["PDFweight_central"], "PDFweight_central/F")
    outtree.Branch("PDFweight_up", bufs["PDFweight_up"], "PDFweight_up/F")
    outtree.Branch("PDFweight_down", bufs["PDFweight_down"], "PDFweight_down/F")
    
    counter = 0

    
    #Here matched means Delta R < 0.8 to generated particle or jet or whatever...
    
    for event in outtree :
        counter += 1
        print event.evt
        try:
            array2 = [x for x in event.LHEPDFWeights_wgt]
            array2.pop(0)
            CppVector = vec_from_list(Cvectordouble, array2)
        
            cls_pdf = ROOT.PDFObject(CppVector)
        
            print cls_pdf.errplus, cls_pdf.errminus
        
            #bufs["jetAK8_tau21ddt"][0] = tau21ddt
            #bufs["PDFweight_central"][0] = cls_pdf.central
            bufs["PDFweight_up"][0] = cls_pdf.errplus
            bufs["PDFweight_down"][0] = cls_pdf.errminus
    
        except: 

            bufs["PDFweight_up"][0] = 1
            bufs["PDFweight_down"][0] = 1

        outtree.Fill()
    
    
    
        if counter > 10:
            break

    print counter
    
    outfile.cd()
    outtree.Write()
    outfile.Close()

    
    f.Close()
    #ff.Close()


##### Main
if __name__ == "__main__":

    ##### Settings

    import os
    if os.environ.get("FILE_NAMES") is not None:
        file_names = os.environ["FILE_NAMES"].split()
    else:
        trimmed_file = "/work/mameinha/TTH/CMSSW_9_4_9/CMSSW_9_4_9/src/TTH/Plotting/python/joosep/out_trimmer.root"
        signal_file_1 = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jul08/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Jul08/190708_165826/0000/tree_172.root"
        signal_file_2 = 'root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/creissel/tth/Mar27/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Mar27/190327_085009/0000/tree_100.root'
        background_file = 'root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Aug02/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/Aug02/190802_081104/0000/tree_34.root '
        f1 = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v1/GC5dc7ce893526/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/job_324_out.root"
        f2 = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v1/GC5dc7ce893526/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/job_2_out.root"
        f3 = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/trimmer/TTH_Boosted_v1/GC5dc7ce893526/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/job_322_out.root"
        file_names = [f2]

    output_file = 'out.root'

    process(file_names, output_file)
