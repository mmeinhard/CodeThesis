import ROOT, sys

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tree")

of = ROOT.TFile("out.root", "RECREATE")

cut = "is_sl==1 && numJets==4 && nBCSVM==3 && ttCls<=0"

tt.Draw(
    "log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV)) >> hunw(10,-6,6)",
    "(1.0) * ({0})".format(cut)
)

tt.Draw(
    "log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV)) >> hnom(10,-6,6)",
    "(btagWeightCSV) * ({0})".format(cut)
)

tt.Draw(
    "log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV)) >> hu(10,-6,6)",
    "(btagWeightCSV_up_cferr1) * ({0})".format(cut)
)

tt.Draw(
    "log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV)) >> hd(10,-6,6)",
    "( btagWeightCSV_down_cferr1) * ({0})".format(cut)
)

of.Write()
of.Close()
