import ROOT
ROOT.gROOT.SetBatch(True)

import sys
import uuid
import multiprocessing
import time
from collections import OrderedDict
import json
import glob

from TTH.Plotting.Datacards.sparse import save_hdict
from TTH.MEAnalysis.samples_base import get_files

def add_hist(self, other):
    new = self.Clone()
    new.Add(other)
    return new

ROOT.TH1D.__add__ = add_hist

def add_hdict(d1, d2):
    """
    Add two sets of dictionaries containing histograms.
    """
    out = HistogramDict()
    ks1 = set(d1.keys())
    ks2 = set(d2.keys())
    for k in ks1.intersection(ks2):
        out[k] = d1[k] + d2[k]
    for k in ks1.difference(ks2):
        out[k] = d1[k]
    for k in ks2.difference(ks1):
        out[k] = d2[k]
    return out

class HistogramDict(OrderedDict):
    def __add__(self, other):
        return add_hdict(self, other)

class Result:
    def __init__(self, diagnostics=[], payload=HistogramDict()):
        self.diagnostics = diagnostics
        self.payload = payload

    def __add__(self, other):
        return Result(
            diagnostics = self.diagnostics + other.diagnostics,
            payload = self.payload + other.payload
        )

class HistCommand:
    def __init__(self, name, func, weight, bins):
        self.name = name
        self.func = func
        self.bins = bins
        self.weight = weight

class CategoryCommand:
    def __init__(self, name, cut, hist_commands):
        self.name = name
        self.cut = cut
        self.hist_commands = hist_commands

def set_cut(tree, cut):
    ROOT.gROOT.cd()
    tree.SetEntryList(0) #clear tree state
    elist = ROOT.TEntryList("elist-{0}".format(str(uuid.uuid4())), "")
    tree.Draw(">>+{0}".format(elist.GetName()), cut, "entrylist")
    tree.SetEntryList(elist)
    print cut, tree.GetEntries(), elist.GetN()

def draw_hist(tree, func, weight, bins):
    t0 = time.time()
    
    ROOT.gROOT.cd()
    h = ROOT.TH1D("_".join([func, str(uuid.uuid4())]), func, *bins)
    h.Sumw2()
    tree.Draw("{0} >> {1}".format(func, h.GetName()), weight, "goff")
    print func, tree.GetEntries(), h.GetEntries()
    dt = time.time() - t0
    return h

def process_file(filename, cat_commands):
    tf = ROOT.TFile.Open(filename)
    tree = tf.Get("tree")
  
    outdict = HistogramDict()

    for cat_command in cat_commands:
        set_cut(tree, cat_command.cut)
        
        for hist_command in cat_command.hist_commands:
            outdict[cat_command.name + "/" + hist_command.name] = draw_hist(tree, hist_command.func, hist_command.weight, hist_command.bins)

    tf.Close()
    return Result(payload=outdict)

def func(args):
    fn, cat_commands = args
    return process_file(fn, cat_commands)

def xrdfs_cat(server, path):
    process = Popen(['xrdfs', server, 'cat', path], stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()

def get_files_path(path):
    prefix = "root://t3dcachedb.psi.ch/"
    files = [prefix + f for f in glob.glob(path + "/*.root")]

    input_nanoaod_files = []
    for fi in files:
        input_file = fi.replace("out.root", "inputs.txt")

    return files

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(description='Runs a simple histogram reduction')
    parser.add_argument(
        '--parallelize',
        action="store",
        help="Whether and how to parallelize the processing",
        choices=["no", "multiprocessing"],
        default="no",
        required=False
    )
    parser.add_argument(
        '--files_path',
        action="store",
        help="Path with files to process",
        required=True
    )
    parser.add_argument(
        '--prefix',
        action="store",
        help="Prefix in output file",
        required=False,
        default=""
    )
    parser.add_argument(
        '--outfile',
        action="store",
        help="Output file",
        required=True,
    )
    args = parser.parse_args(sys.argv[1:])

    file_names = get_files_path(args.files_path)

    histograms = [
        HistCommand("jets_pt0", "jets_pt[0]", "(genWeight)", (100, 0, 300)),
        HistCommand("jets_pt1", "jets_pt[1]", "(genWeight)", (100, 0, 300)),
        HistCommand("jets_pt2", "jets_pt[2]", "(genWeight)", (100, 0, 300)),
        HistCommand("jets_pt3", "jets_pt[3]", "(genWeight)", (100, 0, 300)),
        HistCommand("jets_pt4", "jets_pt[4]", "(genWeight)", (100, 0, 300)),
        HistCommand("jets_pt5", "jets_pt[5]", "(genWeight)", (100, 0, 300)),
    ]
    
    cat_command0 = CategoryCommand("sl_jge6_tge4", "is_sl && numJets>=6 && nBCSVM>=4", histograms)
    cat_command1 = CategoryCommand("sl_jge6", "is_sl && numJets>=6", histograms)
    cat_command2 = CategoryCommand("sl_j5", "is_sl && numJets==5", histograms)
    cat_command3 = CategoryCommand("sl_j4", "is_sl && numJets==4", histograms)

    params = [(fn, [cat_command0, cat_command1, cat_command2, cat_command3]) for fn in file_names]

    if args.parallelize == "no":
        ds = map(func, params)
    elif args.parallelize == "multiprocessing":
        pool = multiprocessing.Pool(10)
        ds = pool.map(func, params)
        pool.close()

    outdict = reduce(lambda x,y:x+y, ds, Result())
   
    outdict_payload = HistogramDict([(args.prefix + key, value) for (key, value) in outdict.payload.items()])

    for (k, v) in outdict_payload.items():
        print k, v, v.GetEntries(), v.Integral(), v.GetMean()
    save_hdict(args.outfile, outdict_payload)
