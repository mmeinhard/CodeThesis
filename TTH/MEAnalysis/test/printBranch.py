import ROOT, sys
import fnmatch
from TTH.MEAnalysis.samples_base import getSitePrefix

tf = ROOT.TFile.Open(getSitePrefix(sys.argv[1]))
if not tf:
    raise Exception("Could not open file")
tt = tf.Get(sys.argv[2])
branch_glob = sys.argv[3]

branches = fnmatch.filter([br.GetName() for br in tt.GetListOfBranches()], branch_glob)
print " ".join(branches)
for ev in tt:
    vs = []
    for br in branches:
        vs += [getattr(ev, br)]
    s = " ".join([str(v) for v in vs])
    print s

