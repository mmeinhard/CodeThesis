import ROOT
import nanoTreeClasses
import nanoTreeGenClasses
from TTH.MEAnalysis.vhbb_utils import match_deltaR, remove_duplicates
from PhysicsTools.HeppyCore.statistics.tree import Tree
from TTH.MEAnalysis.samples_base import getSitePrefix
import os

tree = ROOT.TChain("Events")
filenames_pref = map(getSitePrefix, os.environ["FILE_NAMES"].split())
for fi in filenames_pref:
    tree.Add(fi)

outfile = ROOT.TFile("out.root", "RECREATE")
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

for i in range(tree.GetEntries()):
    if i%1000 == 0:
        print i

    tree.GetEntry(i)

    #print "---"
    #print "event", i, tree.run, tree.luminosityBlock, tree.event

    Jet = nanoTreeClasses.Jet.make_array(tree, MC = True)
    Electron = nanoTreeClasses.Electron.make_array(tree, MC = True)
    Muon = nanoTreeClasses.Muon.make_array(tree, MC = True)
    GenJet = nanoTreeGenClasses.GenJet.make_array(tree)
    GenParticle = nanoTreeGenClasses.GenParticle.make_array(tree)
    GenLepFromTop = nanoTreeGenClasses.GenLepFromTop.make_array(GenParticle)
    GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(GenParticle)
    GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(GenParticle)
    GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(GenParticle)

    all_quarks = GenBQuarkFromTop + GenWZQuark + GenBQuarkFromH
    cleaned_quarks = remove_duplicates(all_quarks)

    #Take particles from the hard process
    #http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
    cleaned_quarks = filter(lambda x: x.status == 23, cleaned_quarks)
    
    #for obj in sorted(cleaned_quarks, key=lambda x: x.pt, reverse=True):
    #    print obj.pt, obj.eta, obj.phi, obj.pdgId

    matches = match_deltaR(cleaned_quarks, Jet, 0.3)
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
        quark.match_btagCSV = 0

    for quark_idx in matches_by_quark.keys():
        quark = cleaned_quarks[quark_idx]
        quark.num_matches = len(matches_by_quark[quark_idx])
        if quark.num_matches > 0:
            jet_idx, dr = matches_by_quark[quark_idx][0]
            best_match = Jet[jet_idx]
            quark.match_pt = best_match.pt
            quark.match_eta = best_match.eta
            quark.match_phi = best_match.phi
            quark.match_mass = best_match.mass
            quark.match_btagCSV = best_match.btagCSV
            quark.match_dr = dr

    for quark in cleaned_quarks:
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
        outtree.fill("Jet_btagCSV", quark.match_btagCSV)
        outtree.tree.Fill()

outfile.Write()
outfile.Close()
