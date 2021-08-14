import ROOT
import uuid
ROOT.gROOT.SetBatch(True)

def draw_hist(files, func, bins, cut):
    #import ROOT, rootpy
    #ROOT.gROOT.SetBatch(True)
    tch = ROOT.TChain("tree")
    for fi in files:
        tch.AddFile(fi)
    ROOT.gROOT.cd()
    hist_name = str(uuid.uuid4())
    h = ROOT.TH1D(hist_name, hist_name, *bins)
    tch.Draw("{0} >> {1}".format(func, hist_name), cut)
    return h

def get_count(files):
    print files
    #import ROOT
    count = 0
    for fi in files:
        tf = ROOT.TFile.Open(fi)
        h = tf.Get("Count")
        if not h:
            h = tf.Get("vhbb/Count")
        count += h.GetBinContent(1)
    return count

def draw_hist_wrap(x):
    return draw_hist(*x)
