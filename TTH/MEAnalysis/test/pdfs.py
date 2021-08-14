import ROOT, sys, os
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample

file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
out = ROOT.TFile("out.root", "RECREATE")

for ifi, fi in enumerate(file_names):
    
    tf = ROOT.TFile.Open(fi)
    tt = tf.Get("tree")
    
    out.cd()

    bins = ""
    if ifi == 0:
        bins = "(6,0,1)"

    nom = tt.Draw(
        "mem_SL_2w2h2t_p>>+h_nom" + bins,
        "(btagWeightCSV * puWeight) * (is_sl && numJets>=6 && nBCSVM>=4)"
    )
    print nom
    
    tt.Draw(
        "mem_SL_2w2h2t_p>>+h_puUp" + bins,
        "(btagWeightCSV * puWeightUp) * (is_sl && numJets>=6 && nBCSVM>=4)"
    )
    
    tt.Draw(
        "mem_SL_2w2h2t_p>>+h_puDown" + bins,
        "(btagWeightCSV * puWeightDown) * (is_sl && numJets>=6 && nBCSVM>=4)"
    )
    
    tt.Draw(
        "mem_SL_2w2h2t_p>>+h_hfUp" + bins,
        "(btagWeightCSV_up_hf * puWeight) * (is_sl && numJets>=6 && nBCSVM>=4)"
    )
    
    tt.Draw(
        "mem_SL_2w2h2t_p>>+h_hfDown" + bins,
        "(btagWeightCSV_down_hf * puWeight) * (is_sl && numJets>=6 && nBCSVM>=4)"
    )

    for iwgt in range(0,102):
        tt.Draw(
            "mem_SL_2w2h2t_p>>+h_pdfw{0}".format(iwgt) + bins,
            "(LHE_weights_pdf_wgt[{0}] * btagWeightCSV * puWeight) * (is_sl && numJets>=6 && nBCSVM>=4)".format(iwgt)
        )

out.Write()
out.Close()
