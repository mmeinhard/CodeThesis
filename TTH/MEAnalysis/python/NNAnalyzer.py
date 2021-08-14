from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import *
import numpy as np
from rootpy.tree import Tree
from rootpy.io import root_open

# analyzer to prepare the data for training or prediction
class NNAnalyzer(FilterAnalyzer):

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)

        # options to be passed later
        # setup: "Delphes" for Delphes input, "nanoAOD" for CMSSW input 
        self.setup = self.cfg_ana.framework
        # defines if training or validation
        self.training = self.cfg_ana.training
        self.boosted = self.cfg_ana.boosted

        # define the objects and variables for training/ predictions
        if self.setup == "nanoAOD":
            self.var = {"leptons":(2,["pt","eta", "phi", "mass", "charge"]), "jets":(10, ["pt", "eta", "phi", "mass", "btagDeepCSV", "matchFlag"]), "met":(0, ["pt", "phi", "sumEt"]), "high_level_var":(0,["nBDeepCSVM", "mbb_closest", "ht30", "nMatch_wq", "nMatch_tb", "nMatch_hb"]), "nu":(2, ["pt", "eta", "phi"])}
        if self.setup == "Delphes":
            self.var = {"leptons":(2,["pt","eta", "phi", "mass", "charge"]), "jets":(10, ["pt", "eta", "phi", "mass", "btag"]), "met":(0, ["eta", "phi", "pt"]), "high_level_var":(0,["nBtags", "mbb_closest", "ht30"])}

        if self.boosted == True:
            self.var["fatjets"] = (2, ["pt", "eta", "phi", "mass"])

        # open output file
        if self.training == True:
            self.output = open("training.csv", "w")

            # make header for file
            # reco
            l = ["leptons", "jets", "met", "high_level_var"]
            if self.boosted == True:
                l.append("fatjets")
            for o in l:
                if o == "leptons" or o == "jets" or o == "nu" or o == "fatjets":
                    self.output.write("num_" + o + " ")
                for var in self.var[o][1]:
                    if self.var[o][0] > 0:
                        for i in range(self.var[o][0]):
                            self.output.write(o + "_" + var + "_" + str(i) + " ")
                    else:
                         if o == "high_level_var":
                             self.output.write(var + " ")
                         else:
                             self.output.write(o + "_" + var + " ")

            # add generator level information for CMSSW file
            if self.setup == "nanoAOD":
                l = ["leptons", "jets", "nu"]
                for o in l:
                    self.output.write("gen_num_" + o + " ")
                    for var in self.var[o][1]:
                        if var != "btagDeepCSV":
                            if self.var[o][0] > 0:
                                for i in range(self.var[o][0]):
                                    self.output.write("gen_" + o + "_" + var + "_" + str(i) + " ")

            """
            # add columns for inv_mass of combinations
            import scipy.special
            n_comb = scipy.special.binom(self.var["jets"][0], 2)
            for i in range(int(n_comb)):
                self.output.write("comb_mass_" + str(i) + " ")
            """

            # parton
            for o in ["top", "atop", "bottom", "abottom"]:
                for var in ["pt", "eta", "phi", "mass"]:
                    self.output.write(o + "_" + var + " ")

            self.output.write("prob_ttH ")
            self.output.write("prob_ttbb ")
            self.output.write("JLR\n")

    def process(self, event):

        features = []

        # Leptons
        features.append(len(getattr(event.systResults["nominal"], "good_leptons")))
        for var in self.var["leptons"][1]:
            for i in range(self.var["leptons"][0]):
                if i in range(len(getattr(event.systResults["nominal"], "good_leptons"))):
                    io = event.systResults["nominal"].good_leptons[i]
                    features.append(getattr(io,var, 0.0))
                else:
                    features.append(0.)

        # Jets
        # check if training because otherwise also systematics have to be evaluated
        features.append(len(event.systResults["nominal"].good_jets))
        if self.training == True:
            for var in self.var["jets"][1]:
                for i in range(self.var["jets"][0]):
                    if i in range(len(event.systResults["nominal"].good_jets)):
                        io = event.systResults["nominal"].good_jets[i]
                        features.append(getattr(io,var, 0.0))
                    else:
                        features.append(0.)

        # MET
        for var in self.var["met"][1]:
            io = getattr(event.systResults["nominal"], "met")
            features.append(getattr(io,var))
        

        # high level variables
        for var in self.var["high_level_var"][1]:
            io = getattr(event.systResults["nominal"], var, 0.0)
            features.append(float(io))

        # add boosted jet variables
        if self.boosted == True:
            features.append(len(event.systResults["nominal"].boosted_tops))
            for var in self.var["fatjets"][1]:
                for i in range(self.var["fatjets"][0]):
                    if i in range(len(event.systResults["nominal"].boosted_tops)):
                        io = event.systResults["nominal"].boosted_tops[i]
                        features.append(getattr(io,var, 0.0))
                    else:
                        features.append(0.)



        # for CMSSW file: add Gen level information
        if self.setup == "nanoAOD":

            # Leptons
            features.append(len(event.GenLep))
            for var in self.var["leptons"][1]:
                for i in range(self.var["leptons"][0]):
                    if i in range(len(event.GenLep)):
                        io = event.GenLep[i]
                        features.append(getattr(io,var))
                    else:
                        features.append(0.)

            # Jets
            features.append(len(event.GenJet))
            if self.training == True:
                for var in self.var["jets"][1]:
                    if var != "btagDeepCSV":
                        for i in range(self.var["jets"][0]):
                            if i in range(len(event.GenJet)):
                                io = event.GenJet[i]
                                features.append(getattr(io,var, 0.0))
                            else:
                                features.append(0.)

            # Nu
            features.append(len(event.GenNu))
            for var in self.var["nu"][1]:
                for i in range(self.var["nu"][0]):
                    if i in range(len(event.GenNu)):
                        io = event.GenNu[i]
                        features.append(getattr(io,var))
                    else:
                        features.append(0.)

        """
        # add combinations
        import itertools
        comb = [x for x in itertools.combinations(range(self.var["jets"][0]), 2)]
        for c in comb:
            idx1 = c[0]
            idx2 = c[1]
            lv1 = ROOT.TLorentzVector() 
            lv2 = ROOT.TLorentzVector() 
            if idx1 in range(len(event.systResults["nominal"].good_jets)):
                jet1 = event.systResults["nominal"].good_jets[idx1]
                lv1.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
            if idx2 in range(len(event.systResults["nominal"].good_jets)):
                jet2 = event.systResults["nominal"].good_jets[idx2]
                lv2.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass)
            v = lv1+lv2
            features.append(v.M())
        """

        # add parton level information
        for p in ["top", "atop", "bottom", "abottom"]:
            LZ = getattr(event, "jlr_" + p, ROOT.TLorentzVector())
            features.append(LZ.Pt())
            features.append(LZ.Eta())
            features.append(LZ.Phi())
            features.append(LZ.M())

        # target: joint likelihood ratio
        if self.training == True:
            features.append(np.log10(getattr(event, "prob_ttHbb", 1.0)))
            features.append(np.log10(getattr(event, "prob_ttbb", 1.0)))
            features.append(np.log10(getattr(event, "jointlikelihood", 1.0)))

        if self.training == True:
            for f in features:
                self.output.write("%f " %f)
            self.output.write("\n")

        return True
