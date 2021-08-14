#!/usr/bin/python
"""
This file contains a few tools to handle sparse histograms.
All tests should be written in test/testDatacards.py
"""
import ROOT

from collections import OrderedDict
import logging, copy

LOG_MODULE_NAME = logging.getLogger(__name__)

def mkdirs(fi, path):
    path = path.encode("ascii", "ignore")
    pathspl = path.split("/")
    sfi = fi
    for p in pathspl:
        d = sfi.Get(str(p))
        if d == None:
            d = sfi.mkdir(p)
            d.Write()
        print p, d
        sfi = d
    return sfi


def save_hdict(ofn="", hdict={}, outfile=None):
    """
    Saves a dictionary of ROOT objects in an output file. The objects will be
    renamed according to the keys in the dictionary.
    
    Args:
        ofn (str, optional): path to the output file which will be recreated
        hdict (dict, optional): dict of "/absolute/path/objname" -> TObject pairs that will
        be saved to the output.
        outfile (None, optional): TFile
    
    Raises:
        Exception: Description
        KeyError: Description
    """
    if not outfile:
        outfile = ROOT.TFile(ofn, "recreate")
    if not outfile or outfile.IsZombie():
        raise Exception(
            "Could not open output file {0}".format(ofn)
        )
    dirs = {}

    for key, obj in sorted(hdict.items(), key=lambda x: x[0]):
        kpath = "/".join(key.split("/")[:-1])
        kname = key.split("/")[-1]
        if len(kname) == 0:
            raise KeyError("Object had no name")
        if kpath:
            d = outfile.Get(kpath)
            if not d:
                d = mkdirs(outfile, kpath)
                dirs[kpath] = d
            assert(obj != None)
            assert(d != None)
            obj.SetName(kname)
            d.Add(obj)
        else:
            obj.SetName(kname)
            outfile.Add(obj)
    outfile.Write()
    outfile.Close()

def add_hdict(d1, d2):
    """
    Add two sets of dictionaries containing histograms.
    """
    out = OrderedDict()
    ks1 = set(d1.keys())
    ks2 = set(d2.keys())
    #print len(ks1), len(ks2)
    for k in ks1.intersection(ks2):
        out[k] = d1[k]
        out[k].Add(d2[k])
        out[k].SetName(d1[k].GetName())
    for k in ks1.difference(ks2):
        out[k] = d1[k]
    for k in ks2.difference(ks1):
        out[k] = d2[k]
    return out
