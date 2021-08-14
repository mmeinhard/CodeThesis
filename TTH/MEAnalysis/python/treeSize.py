import ROOT, sys

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tree")

tot = 0
tot_c = 0
nev = float(tt.GetEntries())
for br in tt.GetListOfBranches():
    tot += br.GetTotBytes()/nev
    tot_c += br.GetZipBytes()/nev
    print "{0} {1} {2:.4f} {3:.4f}".format(
        br.GetName(),
        br.GetListOfLeaves()[0].GetTypeName(),
        br.GetTotBytes()/nev,
        br.GetZipBytes()/nev
    )

print "total", tot/nev, tot_c/nev
