import ROOT, sys
from glob import glob

if len(sys.argv) == 2 and not sys.argv[1].endswith(".root"):
    files = glob(sys.argv[1]+"/*.root")
    sys.argv = [sys.argv[0]] + files


for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    countw = 0
    countgen = 0
    tree = f.Get("Runs")
    for ient in range(tree.GetEntries()):
        tree.GetEntry(ient)
        countw += tree.genEventSumw
        countgen += tree.genEventCount
    print fn, countw, countgen

    #normmuFUp = tree.LHEScaleSumw[4]/tree.LHEScaleSumw[5]
    #normmuFDown = tree.LHEScaleSumw[4]/tree.LHEScaleSumw[3]
    #normmuRUp = tree.LHEScaleSumw[4]/tree.LHEScaleSumw[7]
    #normmuRDown = tree.LHEScaleSumw[4]/tree.LHEScaleSumw[1]

    #print "Normalisation for muF, muR uncertainty:"
    #print "muF_up", normmuFUp, "muFdown", normmuFDown
    #print "muR_up", normmuRUp, "muRdown", normmuRDown
