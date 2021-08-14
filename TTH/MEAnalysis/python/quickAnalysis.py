import ROOT, uuid, glob, os, copy
from TTH.Plotting.Datacards.sparse import save_hdict
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
import sys

def process_chain(chain, func, bins, cut, max_entries=ROOT.TTree.kMaxEntries):
    _hname = str(uuid.uuid4())

    ndims = len(bins)/3
    if ndims == 1:
        h = ROOT.TH1D(_hname, "", *bins)
    elif ndims == 2:
        h = ROOT.TH2D(_hname, "", *bins)

    print cut
    h.Sumw2()
    h.SetDirectory(ROOT.gROOT)
    n = chain.Draw("{0} >> {1}".format(func, _hname), cut, "goff", max_entries, 0)
    return h

def is_data(s):
    return s in [
        "SingleMuon", "SingleElectron", "DoubleMuon", "DoubleEG", "MuonEG"
    ]

def is_ttbar(s):
    return s in [
        "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
        "TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8",
        "TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8",
        "TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8",
        "TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
    ]

def get_hists(dataset, chain, variable, bins, cut, mc_weight, name=""):
    hists = {}
   
    if is_data(dataset):
        print "adding json cut"
        hists[dataset + name] = process_chain(
            chain,
            variable,
            bins,
            #"(json==1 && ({0}))".format(cut)
            "({0})".format(cut)
        )
    elif is_ttbar(dataset): 
        hists[dataset + "_light" + name] = process_chain(
            chain,
            variable,
            bins,
            "({0}) * ({1} && ttCls==0)".format(mc_weight, cut)
        )

        hists[dataset + "_heavy" + name] = process_chain(
            chain,
            variable,
            bins,
            "({0}) * ({1} && ttCls > 0)".format(mc_weight, cut)
        )
    else:
        hists[dataset + name] = process_chain(
            chain,
            variable,
            bins,
            "({0}) * ({1})".format(mc_weight, cut)
        )

    return hists

if __name__ == "__main__":
    
    file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    prefix, dataset = get_prefix_sample(os.environ["DATASETPATH"])

    chain = ROOT.TChain("tree")
    hc = None 
    for fi in file_names:
        chain.Add(fi)

    weight = "1"
    if not is_data(dataset):
        weight = "(genWeight)"

    hists = get_hists(
        dataset, chain,
        "numJets",
        (6, 4, 10),
        "((HLT_ttH_SL_mu==1 && abs(leps_pdgId[0]==13))) && is_sl==1 && numJets>=4 && nBCSVM>=2",
        weight,
        "__numJets"
    )
    hists.update(get_hists(
        dataset, chain,
        "jets_pt",
        (300, 0, 300),
        "((HLT_ttH_SL_mu==1 && abs(leps_pdgId[0]==13))) && is_sl==1 && numJets>=4 && nBCSVM>=2",
        weight,
        "__jets_pt"
    ))
    hists.update(get_hists(
        dataset, chain,
        "jets_pt",
        (300, -2.5, 2.5),
        "((HLT_ttH_SL_mu==1 && abs(leps_pdgId[0]==13))) && is_sl==1 && numJets>=4 && nBCSVM>=2",
        weight,
        "__jets_eta"
    ))
    save_hdict(sys.argv[1], copy.deepcopy(hists))
