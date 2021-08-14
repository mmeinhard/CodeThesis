import ROOT
import rootpy
import numpy as np
import math
import sys
import os

import matplotlib
matplotlib.use('PS') #needed on T3

from matplotlib import pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

def compare_hists(files, labels, histo_name, out):
    
    hists = []
    tfiles = []

    for fi in files:
        tf = ROOT.TFile(fi)
        h = rootpy.asrootpy(tf.Get(histo_name))
        if not h:
            raise Exception("Could not get histo {0}".format(histo_name))
        tfiles += [tf]
        hists += [h]

    plt.figure(figsize=(5,5))

    a1 = plt.axes([0.0, 0.22, 1.0, 0.8])
    plt.title(histo_name)

    for hi, label in zip(hists, labels):
        color = next(a1._get_lines.prop_cycler)['color']
        hi.color = color
        rplt.step(hi, linewidth=2, label=label + " {0:.1f} ({1:.1f})".format(hi.Integral(), hi.GetEntries()))

    ticks = a1.get_xticks()
    a1.get_xaxis().set_visible(False)
    plt.legend()

    a2 = plt.axes([0.0,0.0, 1.0, 0.18], sharex=a1)

    for hi, label in zip(hists, labels):
        hir = rootpy.asrootpy(hi.Clone())
        hir.Divide(hists[0])
        rplt.step(hir, linewidth=2)

    plt.ylim(0.5, 1.5)
    plt.axhline(1.0, color="black", lw=1)

    plt.savefig(os.path.join(out, histo_name) + ".pdf", bbox_inches="tight")
    plt.savefig(os.path.join(out, histo_name) + ".png", bbox_inches="tight")
    return histo_name

import argparse
parser = argparse.ArgumentParser(description='Compares two sets of datacards')
parser.add_argument(
    '-p',
    '--process',
    action='append',
    help="Processes to compare",
    required=True
)

parser.add_argument(
    '-d',
    '--distribution',
    action='append',
    help="Distributions to compare",
    required=True
)

parser.add_argument(
    '-f',
    '--files',
    action='append',
    help="Files to compare",
    required=True
)

parser.add_argument(
    '--out',
    action='store',
    help="Output directory",
    required=True
)
args = parser.parse_args(sys.argv[1:])
os.makedirs(args.out)

html = open("{0}/index.html".format(args.out), "w")
html.write(" ".join(sys.argv) + "<br>\n")

file_names = []
file_tags = []
for fi in args.files:
    file_names += [fi]
    #file name without path or extension
    base = os.path.basename(fi)
    file_tags += [os.path.splitext(base)[0]]

html.write('<a name="top"></a>\n')
html.write('Distributions:<br><ul>\n')
for distr in args.distribution:
    html.write('  <li><a href="#{0}">{0}</a>\n'.format(distr))
    html.write('<ul>\n')
    for proc in args.process:
        html.write('  <li><a href="#{0}__{1}">{1}</a>\n'.format(distr, proc))
    html.write('</ul></li>\n')
html.write('</ul><hr>\n')

for distr in args.distribution:
    html.write('<a name="{0}"></a>\n'.format(distr))
    for proc in args.process:
        html.write('<a name="{0}__{1}"></a>\n'.format(distr, proc))
        histo = "{0}__{1}".format(proc, distr)

        plotfile = compare_hists(file_names, file_tags, histo, args.out)
        
        html.write('{0} <a href="#top">top</a><br>\n'.format(histo))
        html.write('<img src="{1}.png" alt=""><br>\n'.format(args.out, plotfile))
    html.write('<hr>\n'.format(distr))
html.close()
