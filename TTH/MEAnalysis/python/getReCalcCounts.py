import ROOT, sys
from glob import glob

if len(sys.argv) == 2 and not sys.argv[1].endswith(".root"):
    files = glob(sys.argv[1]+"/*.root")
results = []
for fn in files:
    f = ROOT.TFile(fn)
    hGen = f.Get("hGen")
    hGenWeighted = f.Get("hGenWeighted")

    nGen = hGen.GetBinContent(1)
    nGenWeighted = hGenWeighted.GetBinContent(1)

    results.append([fn.split("/")[-1].split(".")[0], nGen, nGenWeighted])

    
maxlenName = 0
maxlennGen = 0
maxlennGenW = 0
for res in results:
    clenName = len(str(res[0]))
    clennGen = len(str(res[1]))
    clennGenW = len(str(res[2]))
    if clenName > maxlenName:
        maxlenName = clenName
    if clennGen > maxlennGen:
        maxlennGen = clennGen
    if clennGenW > maxlennGenW:
        maxlennGenW = clennGenW


print "Name"+(maxlenName-len("Name"))*" "+" | "+"nGen"+(maxlennGen-len("nGen"))*" "+" | "+"nGenWei"+(maxlennGen-len("nGenWei"))*" "
for res in results:
    print res[0]+(maxlenName-len(res[0]))*" "+" | "+str(res[1])+(maxlennGen-len(str(res[1])))*" "+" | "+str(res[2])+(maxlennGen-len(str(res[2])))*" "
