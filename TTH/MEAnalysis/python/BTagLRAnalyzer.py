import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM
import itertools
import math
import logging

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

import numpy as np
Cvectoruint = getattr(ROOT, "std::vector<unsigned int>")

LOG_MODULE_NAME = logging.getLogger(__name__)

def logit(x):
    return math.log(x/(1.0 - x)) if x > 0 else -10

class BTagLRAnalyzer(FilterAnalyzer):
    """
    Performs b-tag likelihood ratio calculations
    FIXME: doc
    """

    def getPdfs(self, cplots, algo):
        """
        Returns a dictionary with the b-tagging PDF-s
        cplots (TFile): input ROOT file with the PDF-s
        algo (string): name of the b-tagger for which to retrieve the distributiosn
        """
        csv_pdfs = {}

        for x in ["b", "c", "l"]:
            name = "{1}_{0}_pt_eta".format(x, algo) 
            LOG_MODULE_NAME.debug("getting pdf {0} from file {1}".format(name, cplots))
            obj = cplots.Get(name)
            if not obj:
                raise Exception("Could not get PDF {0}".format(name))
            csv_pdfs[(x, "pt_eta")] = obj
        return csv_pdfs

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BTagLRAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.default_bTagAlgo = self.conf.jets["btagAlgo"]
        
        self.cplots = ROOT.TFile(self.conf.general["controlPlotsFile"])
        self.csv_pdfs = {}
        for algo in ["btagCSV", "btagDeepCSV"]:
            self.csv_pdfs[algo] = self.getPdfs(self.cplots, algo)

        self.conf.BTagLRAnalyzer = self
        self.jlh = MEM.JetLikelihood()

    def get_pdf_prob(self, csv_pdfs, flavour, pt, eta, taggerval):

        h = csv_pdfs[(flavour, "pt_eta")]
        nb = h.FindBin(pt, abs(eta), taggerval)
        ret = h.GetBinContent(nb)
        return ret

    def beginLoop(self, setup):
        super(BTagLRAnalyzer, self).beginLoop(setup)

    def evaluate_jet_prob(self, pdfs, pt, eta, taggerval):
        return (
            self.get_pdf_prob(pdfs, "b", pt, eta, taggerval),
            self.get_pdf_prob(pdfs, "c", pt, eta, taggerval),
            self.get_pdf_prob(pdfs, "l", pt, eta, taggerval)
        )

    def btag_likelihood2(self, probs, nB):
        self.jlh.next_event()
        for ijet in range(len(probs)):
            jp = ROOT.MEM.JetProbability()
            jp.setProbability(MEM.JetInterpretation.b, probs[ijet][0])
            jp.setProbability(MEM.JetInterpretation.c, probs[ijet][1])
            jp.setProbability(MEM.JetInterpretation.l, probs[ijet][2])
            self.jlh.push_back_object(jp)

        bperm = Cvectoruint()
        P = self.jlh.calcProbability(MEM.JetInterpretation.b, MEM.JetInterpretation.l, nB, bperm)
        best_perm = [bperm.at(i) for i in range(bperm.size())]
        return P, best_perm
        #end permutation loop

    def process(self, event):
        if event.catChange: #DS
            if "systematics" in self.conf.general["verbosity"]:
                autolog("BLRAna: processing catChange")
            res = self._process(event.catChange)
            event.catChange = res #DS

        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_jet:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_btag = False
        return self.conf.general["passall"] or np.any([v.passes_btag for v in event.systResults.values()])

    def getJetProbs(self, pdfs, event, taggers):
        jets_for_btag_lr = {}
        jet_probs        = {}

        for tagger in taggers:
            #Use only the first N jets by b-tagger value for likelihood ratio calculation 
            jets_for_btag_lr[tagger] =  sorted(
                #event.good_jets, key=lambda x: x.pt, reverse=True #CHECK: Changed by DS
                event.good_jets, key=lambda x, tagger=tagger: getattr(x, tagger), reverse=True
            )[0:self.conf.jets["NJetsForBTagLR"]]
            jet_probs[tagger] =  [ 
                self.evaluate_jet_prob(pdfs[tagger], j.pt, j.eta, getattr(j, tagger))
                for j in jets_for_btag_lr[tagger]
            ]
        return jets_for_btag_lr, jet_probs

    def lratio(self, l1, l2):
        if l1+l2>0:
            return l1/(l1+l2)
        else:
            return 0.0

    def _process(self, event):

        #btag algos for which to calculate btag LR
        btagalgos = ["btagCSV","btagDeepCSV"]
        jets_for_btag_lr, jet_probs = self.getJetProbs(self.csv_pdfs, event, btagalgos )

        btag_likelihood_results = {}
        btag_likelihood_ratio_results = {}
        btag_likelihood_ratio_results_4b_3b = {}
        btag_likelihood_ratio_results_3b_2b = {}
        btag_likelihood_ratio_results_geq2b_leq1b = {}
        for btagalgo in btagalgos:
            btag_lr_4b, best_4b_perm = self.btag_likelihood2(jet_probs[btagalgo], 4)
            btag_lr_3b, best_3b_perm = self.btag_likelihood2(jet_probs[btagalgo], 3)
            btag_lr_2b, best_2b_perm = self.btag_likelihood2(jet_probs[btagalgo], 2)
            btag_lr_1b, best_1b_perm = self.btag_likelihood2(jet_probs[btagalgo], 1)
            btag_lr_0b, best_0b_perm = self.btag_likelihood2(jet_probs[btagalgo], 0)
            btag_likelihood_results[btagalgo] = (btag_lr_4b, btag_lr_2b, best_4b_perm, best_2b_perm,
                                                 btag_lr_3b, best_3b_perm, btag_lr_1b, best_1b_perm,
                                                 btag_lr_0b, best_0b_perm)
            btag_likelihood_ratio_results[btagalgo] = self.lratio(btag_lr_4b, btag_lr_2b)
            btag_likelihood_ratio_results_4b_3b[btagalgo] = self.lratio(btag_lr_4b, btag_lr_3b)
            btag_likelihood_ratio_results_3b_2b[btagalgo] = self.lratio(btag_lr_3b, btag_lr_2b)
            btag_likelihood_ratio_results_geq2b_leq1b[btagalgo] = self.lratio(max(btag_lr_4b,btag_lr_3b,btag_lr_2b), max(btag_lr_1b,btag_lr_0b))
            setattr(event, "jet_perm_btag_lr_" + btagalgo,
                [event.good_jets.index(j) for j in jets_for_btag_lr[btagalgo]]
            )
            setattr(event,
                "btag_LR_4b_2b_" + btagalgo, btag_likelihood_ratio_results[btagalgo]
            )
            setattr(event,
                "btag_LR_4b_3b_" + btagalgo, btag_likelihood_ratio_results_4b_3b[btagalgo]
            )
            setattr(event,
                "btag_LR_3b_2b_" + btagalgo, btag_likelihood_ratio_results_3b_2b[btagalgo]
            )
            setattr(event,
                "btag_LR_geq2b_leq1b_" + btagalgo, btag_likelihood_ratio_results_geq2b_leq1b[btagalgo]
            )
        #default btagger used
        event.btag_lr_4b = btag_likelihood_results[self.default_bTagAlgo][0]
        event.btag_lr_3b = btag_likelihood_results[self.default_bTagAlgo][4]
        event.btag_lr_2b = btag_likelihood_results[self.default_bTagAlgo][1]
        event.btag_lr_1b = btag_likelihood_results[self.default_bTagAlgo][6]
        event.btag_lr_0b = btag_likelihood_results[self.default_bTagAlgo][8]
        event.btag_LR_4b_2b = btag_likelihood_ratio_results[self.default_bTagAlgo]
        event.btag_LR_4b_3b = btag_likelihood_ratio_results_4b_3b[self.default_bTagAlgo]
        event.btag_LR_3b_2b = btag_likelihood_ratio_results_3b_2b[self.default_bTagAlgo]
        best_4b_perm = btag_likelihood_results[self.default_bTagAlgo][2]
        best_3b_perm = btag_likelihood_results[self.default_bTagAlgo][5]

        # use default btag method always
        event.buntagged_jets_maxLikelihood_4b = [jets_for_btag_lr[self.default_bTagAlgo][i] for i in best_4b_perm[4:]]
        event.btagged_jets_maxLikelihood_4b = [jets_for_btag_lr[self.default_bTagAlgo][i] for i in best_4b_perm[0:4]] 
        event.buntagged_jets_maxLikelihood_3b = [jets_for_btag_lr[self.default_bTagAlgo][i] for i in best_3b_perm[3:]]
        event.btagged_jets_maxLikelihood_3b = [jets_for_btag_lr[self.default_bTagAlgo][i] for i in best_3b_perm[0:3]]

        for i in range(len(event.good_jets)):
            event.good_jets[i].btagFlag = 0.0

        event.fh_region = -99 #DS QCD estimation region
        #Jets are untagged according to the b-tagging likelihood ratio permutation
        if self.conf.jets["untaggedSelection"] == "btagLR":
            if "debug" in self.conf.general["verbosity"]:
                autolog("using btagLR for btag/untag jet selection")
            if event.is_fh:
                if (event.btag_LR_4b_2b > self.conf.mem["FH_bLR_4b_SR"]):
                    event.selected_btagged_jets = event.btagged_jets_maxLikelihood_4b
                    event.buntagged_jets = event.buntagged_jets_maxLikelihood_4b
                    event.fh_region = 0
                    #if event.systematic == "nominal":
                    #    print "BTagLRAna: considered 4b SR event" #DS temp
                elif (event.btag_LR_3b_2b > self.conf.mem["FH_bLR_3b_SR"]):
                    event.selected_btagged_jets = event.btagged_jets_maxLikelihood_3b
                    event.buntagged_jets = event.buntagged_jets_maxLikelihood_3b
                    event.fh_region = 1
                    #if event.systematic == "nominal":
                    #    print "BTagLRAna: considered 3b SR event" #DS temp
#DS FIXME - allow TTbar MC to have CRs...                        or "TT" in self.cfg_comp.name
                elif ( not self.cfg_comp.isMC or "TT" in self.cfg_comp.name or "QCD" in self.cfg_comp.name ) and (event.btag_LR_4b_2b > self.conf.mem["FH_bLR_4b_CR_lo"] and event.btag_LR_4b_2b < self.conf.mem["FH_bLR_4b_CR_hi"]):
                    event.selected_btagged_jets = event.btagged_jets_maxLikelihood_4b
                    event.buntagged_jets = event.buntagged_jets_maxLikelihood_4b
                    event.fh_region = 2
                    #if event.systematic == "nominal":
                    #    print "BTagLRAna: considered 4b CR event" #DS temp
                elif (not self.cfg_comp.isMC or "TT" in self.cfg_comp.name or "QCD" in self.cfg_comp.name ) and (event.btag_LR_3b_2b > self.conf.mem["FH_bLR_3b_CR_lo"] and event.btag_LR_3b_2b < self.conf.mem["FH_bLR_3b_CR_hi"]):
                    event.selected_btagged_jets = event.btagged_jets_maxLikelihood_3b
                    event.buntagged_jets = event.buntagged_jets_maxLikelihood_3b
                    event.fh_region = 3
                    #if event.systematic == "nominal":
                    #    print "BTagLRAna: considered 3b CR event" #DS temp
                else: #event considered 2b event (2bs in random order)
                    event.selected_btagged_jets = event.btagged_jets_maxLikelihood_3b[:2]
                    event.buntagged_jets = event.buntagged_jets_maxLikelihood_3b + event.btagged_jets_maxLikelihood_3b[2:]
                    event.fh_region = 4
                    #if event.systematic == "nominal":
                    #    print "BTagLRAna: considered 2b event" #DS temp
            else:
                event.buntagged_jets = event.buntagged_jets_maxLikelihood_4b
                event.selected_btagged_jets = event.btagged_jets_maxLikelihood_4b
        else:
            #set untagged jets according to not b-tagged
            event.buntagged_jets = event.buntagged_jets_bdisc
            event.selected_btagged_jets = event.btagged_jets_bdisc
            if self.conf.jets["untaggedSelection"] != "btagLR" and event.is_fh and (not "ttH" in self.cfg_comp.name): #DS
                if len(event.btagged_jets_bdisc)>=4:
                    event.buntagged_jets = event.buntagged_jets_bdisc
                    event.selected_btagged_jets = event.btagged_jets_bdisc
                    #if event.systematic == "nominal":
                        #print "BTagLRAna: considered 4b SR event" #DS temp
                elif len(event.btagged_jets_bdisc)==3:
                    event.buntagged_jets = event.buntagged_jets_bdisc
                    event.selected_btagged_jets = event.btagged_jets_bdisc
                    #if event.systematic == "nominal":
                        #print "BTagLRAna: considered 3b SR event" #DS temp
                elif len(event.btagged_jets_bdisc)==2 and len(event.loosebtag_jets_bdisc)>=4:
                    event.buntagged_jets = event.loosebuntag_jets_bdisc
                    event.selected_btagged_jets = event.loosebtag_jets_bdisc
                    #if event.systematic == "nominal":
                        #print "BTagLRAna: considered 4b CR event" #DS temp
                elif len(event.btagged_jets_bdisc)==2 and len(event.loosebtag_jets_bdisc)==3:
                    event.buntagged_jets = event.loosebuntag_jets_bdisc
                    event.selected_btagged_jets = event.loosebtag_jets_bdisc                
                    #if event.systematic == "nominal":
                        #print "BTagLRAna: considered 3b CR event" #DS temp
                else:
                    event.buntagged_jets = event.buntagged_jets_bdisc
                    event.selected_btagged_jets = event.btagged_jets_bdisc
                    #if event.systematic == "nominal":
                        #print "BTagLRAna: considered 2b event" #DS temp
            else:
                event.buntagged_jets = event.buntagged_jets_bdisc
                event.selected_btagged_jets = event.btagged_jets_bdisc


        if "debug" in self.conf.general["verbosity"]:
            autolog("N(untagged)={0} N(tagged)={1}".format(
                len(event.buntagged_jets),
                len(event.selected_btagged_jets)
            ))

        btagged = sorted(event.selected_btagged_jets, key=lambda x, self=self: getattr(x, self.default_bTagAlgo) , reverse=True)
        looseb = sorted(event.loosebtag_jets_bdisc, key=lambda x, self=self: getattr(x, self.default_bTagAlgo) , reverse=True)
        #Take first 4 most b-tagged jets, these are used for the top and higgs candidates
        event.selected_btagged_jets_high = btagged[0:4]

        #any leftover b-tagged jets could be used for the W reconstruction
        event.selected_btagged_jets_low = btagged[4:]

        #Set these jets to be used as b-quarks in the MEM
        #We don't want to use more than 4 b-quarks in the hypothesis
        for jet in event.selected_btagged_jets_high:
            #idx = event.good_jets.index(jet)
            #event.good_jets[idx].btagFlag = 1.0
            jet.btagFlag = 1.0

        event.passes_btag = len(event.selected_btagged_jets)>=0
        if "debug" in self.conf.general["verbosity"]:
            autolog("BTag selection pass={0}, len(btagged_jets)={1} using the method={2}".format(
                event.passes_btag,
                len(event.selected_btagged_jets),
                self.conf.jets["untaggedSelection"]
            ))

        #do category-specific blr cuts
        cat = ""
        if event.is_sl:
            cat += "sl_"

            if len(event.good_jets) == 4:
                cat += "j4_"
            elif len(event.good_jets) == 5:
                cat += "j5_"
            elif len(event.good_jets) >= 6:
                cat += "jge6_"

            if event.nBDeepCSVM == 2:
                cat += "t2"
            elif event.nBDeepCSVM == 3:
                cat += "t3"
            elif event.nBDeepCSVM >= 4:
                cat += "tge4"
            else:
                cat = "unknown"
        elif event.is_dl:
            cat += "dl_"
            if len(event.good_jets)==3 and event.nBDeepCSVM==2:
                cat += "j3_t2"
            elif len(event.good_jets)==3 and event.nBDeepCSVM==3:
                cat += "j3_t3"
            elif len(event.good_jets)>=4 and event.nBDeepCSVM==3:
                cat += "jge4_t3"
            elif len(event.good_jets)>=4 and event.nBDeepCSVM==2:
                cat += "jge4_t2"
            elif len(event.good_jets)>=4 and event.nBDeepCSVM>=4:
                cat += "jge4_tge4"
            else:
                cat = "unknown"
        elif event.is_fh:  #DS
            cat += "fh_"
            if len(event.good_jets) == 7:
                cat += "j7_"
            elif len(event.good_jets) == 8:
                cat += "j8_"
            elif len(event.good_jets) >= 9:
                cat += "jge9_"

            if event.nBCSVM == 3:
                cat += "t3"
            elif event.nBCSVM == 4:
                cat += "t4"
            elif event.nBCSVM >= 5:
                cat += "tge5"
            else:
                cat = "unknown"
        else:
            cat = "unknown"

        event.category_string = cat
        blr_cut = self.conf.mem["blr_cuts"].get(cat, -20)
        if cat != "unknown":
            event.pass_category_blr = logit(event.btag_LR_4b_2b) > blr_cut 
        else:
            event.pass_category_blr = False
        if "debug" in self.conf.general["verbosity"]:
            autolog("SL/DL category: {0}, pass blr cut {1}: {2}".format(
                event.category_string, blr_cut, event.pass_category_blr)
            )
        return event
