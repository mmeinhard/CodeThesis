import ROOT
import nanoTreeClasses
import nanoTreeGenClasses
from TTH.MEAnalysis.vhbb_utils import  lvec, remove_duplicates
from PhysicsTools.HeppyCore.statistics.tree import Tree
from TTH.MEAnalysis.samples_base import getSitePrefix
import os
from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *

#Match two lists, remove objects which are matched to two objects
def match_deltaR(coll1, coll2, deltaR=0.3):
    pairs = []
    used = []
    for idx1, obj1 in enumerate(coll1):
        lv1 = lvec(obj1)
        for idx2, obj2 in enumerate(coll2):
            lv2 = lvec(obj2)
            dr = lv1.DeltaR(lv2)
            if dr < deltaR:
                pairs += [(idx1, idx2, dr)]
                used.append(idx2)
    for p in reversed(pairs):
        if used.count(p[1]) >= 2:
            pairs.pop(pairs.index(p))


    return pairs

tree = ROOT.TChain("nanoAOD/Events")
filenames_pref = map(getSitePrefix, os.environ["FILE_NAMES"].split())
for fi in filenames_pref:
    tree.Add(fi)
#tree.Add("root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/chreisse/tth/Apr16/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Apr16/180416_072809/0000/tree_109.root")

outfile = ROOT.TFile("out_top.root", "RECREATE")
outfile.cd()

outtree = Tree('Quarks', 'Quarks matched to jets')
outtree.var("Jet_pt")
outtree.var("Jet_eta")
outtree.var("Jet_phi")
outtree.var("Jet_mass")
outtree.var("Jet_btagCSV")
outtree.var("Quark_pt")
outtree.var("Quark_eta")
outtree.var("Quark_phi")
outtree.var("Quark_mass")
outtree.var("Quark_pdgId")
outtree.var("Quark_num_matches")
outtree.var("Quark_match_dr")
outtree.var("evt")

print tree.GetEntries()

for i in range(tree.GetEntries()):

    if i%1000 == 0:
        print i


    #if i>10000:
    #    break

    tree.GetEntry(i)

    #print "---"
    #print "event", i, tree.run, tree.luminosityBlock, tree.event

    GenParticle = nanoTreeGenClasses.GenParticle.make_array(tree)
    GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(GenParticle)
    GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(GenParticle)
    GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(GenParticle)

    HTTV2Subjet = nanoTreeClasses.HTTV2Subjet.make_array(tree, MC = True)

 

    all_quarks = GenBQuarkFromTop + GenWZQuark
    cleaned_quarks = remove_duplicates(all_quarks)

    #Take particles from the hard process
    #http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
    cleaned_quarks = filter(lambda x: x.status == 23, cleaned_quarks)
    
    #for obj in sorted(cleaned_quarks, key=lambda x: x.pt, reverse=True):
    #    print obj.pt, obj.eta, obj.phi, obj.pdgId

    matches = match_deltaR(cleaned_quarks, HTTV2Subjet, 0.3)
    sorted_matches = sorted(matches, key=lambda x: (x[0], x[2]))
    matches_by_quark = {}
    for quark_idx, jet_idx, dr in sorted_matches:
        if not matches_by_quark.has_key(quark_idx):
            matches_by_quark[quark_idx] = []
        matches_by_quark[quark_idx] += [(jet_idx, dr)]
  
    for quark in cleaned_quarks:
        quark.num_matches = 0
        quark.match_pt = 0
        quark.match_eta = 0
        quark.match_phi = 0
        quark.match_mass = 0
        quark.match_pdgId = 0
        quark.match_dr = 0
        quark.match_btagDeepCSV = 0

    for quark_idx in matches_by_quark.keys():
        quark = cleaned_quarks[quark_idx]
        quark.num_matches = len(matches_by_quark[quark_idx])
        if quark.num_matches > 0:
            jet_idx, dr = matches_by_quark[quark_idx][0]
            best_match = HTTV2Subjet[jet_idx]
            quark.match_pt = best_match.pt
            quark.match_eta = best_match.eta
            quark.match_phi = best_match.phi
            quark.match_mass = best_match.mass
            quark.match_btagDeepCSV = best_match.btag
            quark.match_dr = dr

    for quark in cleaned_quarks:
        if (quark.num_matches >0):
            outtree.fill("evt", tree.event)
            outtree.fill("Quark_pt", quark.pt)
            outtree.fill("Quark_eta", quark.eta)
            outtree.fill("Quark_phi", quark.phi)
            outtree.fill("Quark_mass", quark.mass)
            outtree.fill("Quark_pdgId", quark.pdgId)
            outtree.fill("Quark_num_matches", quark.num_matches)
            outtree.fill("Quark_match_dr", quark.match_dr)
            outtree.fill("Jet_pt", quark.match_pt)
            outtree.fill("Jet_eta", quark.match_eta)
            outtree.fill("Jet_phi", quark.match_phi)
            outtree.fill("Jet_mass", quark.match_mass)
            outtree.fill("Jet_btagCSV", quark.match_btagDeepCSV)
            outtree.tree.Fill()

outfile.Write()
outfile.Close()
