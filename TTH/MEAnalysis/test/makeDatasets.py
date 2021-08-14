#!/usr/bin/env python
#Prepares grid-control dataset files based on a scan of the /pnfs file system tree
import sys
import glob
import ROOT
import os

import argparse
parser = argparse.ArgumentParser(description='Gets the list of files from /pnfs and creates a .txt file for grid-control')
parser.add_argument(
    '--treename',
    action="store",
    help="Name of TTree to check in file",
    required=False,
    default="Events"
)
parser.add_argument(
    '--prefix',
    action="store",
    help="XRootD prefix to open files",
    required=False,
    default="root://t3dcachedb.psi.ch"
)
parser.add_argument(
    '--path',
    action="store",
    help="Path to scan for files, must be accessible using POSIX tools (ls)",
    required=True,
)
parser.add_argument(
    '--sample',
    action="store",
    help="Sample name to use in []-brackets in output file. Take last directory if not specified.",
    required=False,
    default=None,
)
parser.add_argument(
    '--outpath',
    action="store",
    help="Path where to store output .txt file",
    required=True,
)
args = parser.parse_args(sys.argv[1:])
if not args.sample:
    args.sample = os.path.basename(os.path.normpath(args.path))

fns = glob.glob(args.path + "/*.root")
print "Got {0} files for sample {1}".format(len(fns), args.sample)
outfile = open("{0}/{1}.txt".format(args.outpath, args.sample), "w")
outfile.write("[{0}]\n".format(args.sample))
for fn in fns:
    print args.prefix + fn
    tf = ROOT.TFile.Open(args.prefix + fn)
    tree = tf.Get(args.treename)
    if not tree:
        raise Exception("Could not get tree {0}".format(args.treename))
    nev = tree.GetEntries()
    s = "{0}/{1} = {2}\n".format(args.prefix, fn, int(nev))
    outfile.write(s)

outfile.close()
