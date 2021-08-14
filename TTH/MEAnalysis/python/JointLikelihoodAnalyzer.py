import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM

import numpy as np

from TTH.MEAnalysis.MEMUtils import set_integration_vars, add_obj
from TTH.MEAnalysis.MEMConfig import MEMConfig

import logging

LOG_MODULE_NAME = logging.getLogger(__name__)

from TTH.MEAnalysis.Analyzer import FilterAnalyzer

# function to calculate the joint likelihood ratio using the MEM::Integrand::scattering function
class JointLikelihoodAnalyzer(FilterAnalyzer):
    """
    Perfomrs the calculation of the joint likelihood ratio using the MEM::Integrand::scattering function
    in order to follow the approach presented in https://arxiv.org/pdf/1805.00013.pdf

    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(FilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        self.mem_configs = self.conf.mem_configs

        cfg = MEMConfig(self.conf)
        self.integrator = MEM.Integrand(
            0,#verbosity (debug code) 1=output,2=input,4=init,8=init_more,16=event,32=integration
            cfg.cfg
        )
        
        self.do_jlr = self.cfg_ana.do_jlr

        #self.mem_configs = self.conf.mem_configs
        #self.memkeysToRun = self.conf.mem["methodsToRun"]

        #cfg = MEMConfig(self.conf)
        #cfg.configure_transfer_function(self.conf)
        #cfg.cfg.num_jet_variations = len(self.conf.mem["jet_corrections"])
        #self.integrator = MEM.Integrand(
        #    0,#verbosity (debug code) 1=output,2=input,4=init,8=init_more,16=event,32=integration
        #    cfg.cfg
        #)

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)

    def process(self, event):
        
        #set defaults for metree.py
        event.prob_ttHbb = -9999
        event.prob_ttbb = -9999
        event.jointlikelihood = -9999
            
        event.jlr_top = ROOT.TLorentzVector()
        event.jlr_atop = ROOT.TLorentzVector()
        event.jlr_bottom = ROOT.TLorentzVector()
        event.jlr_abottom = ROOT.TLorentzVector()
        event.jlr_addRad = ROOT.TLorentzVector()

        if self.cfg_comp.isMC and self.do_jlr:

            # get inputs for scattering amplitudes
            #double MEM::Integrand::scattering(const LV &top, const LV &atop, const LV &b1,
            #                      const LV &b2, const LV &additional_jet,
            #                      double &x1, double &x2)



            idx = [(event.GenParticle[p].genPartIdxMother, event.GenParticle[p].pdgId) for p in range(len(event.GenParticle))]


            # get correct tops, bottoms and Higgs boson entries
            top_idx = [(i, tupl) for i, tupl in enumerate(idx) if tupl[1] == 6][0][0]
            atop_idx = [(i, tupl) for i, tupl in enumerate(idx) if tupl[1] == -6][0][0]

            bottoms = [(i, tupl) for i, tupl in enumerate(idx) if tupl[1] == 5]
            abottoms = [(i, tupl) for i, tupl in enumerate(idx) if tupl[1] == -5]
            Higgs = [(i, tupl) for i, tupl in enumerate(idx) if tupl[1] == 25]
            if len(Higgs) == 0:
                bottom_idx = bottoms[0][0]
                abottom_idx = abottoms[0][0]
            else:
                j = Higgs[0][0]
                while j < len(event.GenParticle):
                    decay = [(i,tupl) for i,tupl in enumerate(idx) if tupl[0] == j]
                    if len(decay) == 1:
                        j = decay[0][0]
                    else:
                        break
                for d in decay:
                    if d[1][1] == 5:
                        bottom_idx = d[0]
                    if d[1][1] == -5:
                        abottom_idx = d[0]

            # get top/antitop and bottom/anti-bottom LV 
            top = ROOT.TLorentzVector()
            atop = ROOT.TLorentzVector()
            bottom = ROOT.TLorentzVector()
            abottom = ROOT.TLorentzVector()
            add_rad = ROOT.TLorentzVector()

            top.SetPtEtaPhiM(event.GenParticle[top_idx].pt, event.GenParticle[top_idx].eta, event.GenParticle[top_idx].phi, event.GenParticle[top_idx].mass)
            atop.SetPtEtaPhiM(event.GenParticle[atop_idx].pt, event.GenParticle[atop_idx].eta, event.GenParticle[atop_idx].phi, event.GenParticle[atop_idx].mass)
            bottom.SetPtEtaPhiM(event.GenParticle[bottom_idx].pt, event.GenParticle[bottom_idx].eta, event.GenParticle[bottom_idx].phi, event.GenParticle[bottom_idx].mass)    
            abottom.SetPtEtaPhiM(event.GenParticle[abottom_idx].pt, event.GenParticle[abottom_idx].eta, event.GenParticle[abottom_idx].phi, event.GenParticle[abottom_idx].mass)   

            # check if enough information to compute joint likelihood, o.w. set all values to -9999
            if bottom == ROOT.TLorentzVector() or abottom == ROOT.TLorentzVector() or top == ROOT.TLorentzVector() or atop == ROOT.TLorentzVector():
    
                event.prob_ttHbb = -9999
                event.prob_ttbb = -9999
                event.jointlikelihood = -9999

            else:

                # call MEM scattering to get the probability for hypo = TTH and hypo = TTBB
                prob = {}
                # TTH
                self.integrator.set_hypo(MEM.Hypothesis.TTH)
                prob["ttHbb"] = self.integrator.scattering(top, atop, bottom, abottom, add_rad, ROOT.Double(0), ROOT.Double(0))
                # TTBB
                self.integrator.set_hypo(MEM.Hypothesis.TTBB)
                prob["ttbb"] = self.integrator.scattering(top, atop, bottom, abottom, add_rad, ROOT.Double(0), ROOT.Double(0))

                event.prob_ttHbb = prob["ttHbb"]    
                event.prob_ttbb = prob["ttbb"]

                r = prob["ttbb"]/prob["ttHbb"]
                event.jointlikelihood = r

            # save information of the LVs
            event.jlr_top = top
            event.jlr_atop = atop
            event.jlr_bottom = bottom
            event.jlr_abottom = abottom
            event.jlr_addRad = add_rad

        return True        
