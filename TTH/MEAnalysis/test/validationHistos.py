import ROOT, sys
ROOT.gROOT.SetBatch(True)

fn = sys.argv[1]
tf = ROOT.TFile(fn)
tt = tf.Get("tree")

for cutname, cut in [
    ("is_sl", "is_sl"),
    ("is_dl", "is_dl"),
    ("is_fh", "is_fh")
]:
    for funcname, func in [
        ("jets_pt", "jets_pt"),
        ("leps_pt", "leps_pt"),
    ]:
        print cutname, funcname
        fn = "{0}__{1}.pdf".format(cutname, funcname)
        c = ROOT.TCanvas()
        tt.Draw(func, cut)
        c.SaveAs(fn)
