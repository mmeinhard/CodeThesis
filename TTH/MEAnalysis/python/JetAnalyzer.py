from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import *
from copy import deepcopy
import numpy as np
import copy
from collections import OrderedDict
import logging

LOG_MODULE_NAME = logging.getLogger(__name__)

#FIXME: understand the effect of cropping the transfer functions
def attach_jet_transfer_function(jet, conf):
    """
    Attaches transfer functions to the supplied jet based on the jet eta bin.
    """
    jet_eta_bin = 0
    if abs(jet.eta)>1.0:
        jet_eta_bin = 1
    jet.tf_b = conf.tf_formula['b'][jet_eta_bin]
    jet.tf_l = conf.tf_formula['l'][jet_eta_bin]
    jet.tf_b.SetNpx(10000)
    jet.tf_b.SetRange(0, 500)

    jet.tf_l.SetNpx(10000)
    jet.tf_l.SetRange(0, 500)


class JetAnalyzer(FilterAnalyzer):
    """
    Performs jet selection and b-tag counting.
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)

    def variateJets(self, jets, systematic, sigma):
        """Recalculate pt and mass of Jet depending on jet systematic

        Args:
            jets (list): input jet collection
            systematic (str): Part of mem["factorized_sources"] in config
            sigma (float): Either 1.0 for Up variation of -1.0 for Down

        Returns:
            newjets : A list of jet pt and mass for systematic change
        """
        newjets = [SystematicObject(jet, {"pt": jet.pt, "mass": jet.mass}) for jet in jets]
        count = 0
        if "systematics" in self.conf.general["verbosity"]:
            autolog("Processing: {0}, sigma {1}".format(systematic, sigma))
        for i in range(len(jets)):
            if sigma > 0:
                sdir = "Up"
                _sigma = sigma
            elif sigma < 0:
                sdir = "Down"
                _sigma = abs(sigma)
            else:
                raise Exception("sigma must be != 0")
            corr_pt = getattr(newjets[i], "pt_corr_{0}{1}".format(systematic, sdir))
            nominal_pt = newjets[i].pt

            
            

            newjets[i].pt = corr_pt
            newjets[i].mass *= corr_pt/nominal_pt
            if "systematics" in self.conf.general["verbosity"]:
                autolog("Correction jet with pt = {0:06.2f}, eta = {1:05.2f}, oldcorr = {2:.4f}, newcorr {3:.4f}, cf = {4:.8f}".format(jets[i].pt, jets[i].eta, old_corr, new_corr, cf))

        return newjets

    
    def compareJets(self, jetsvar, jetsnom): #DS
        newjets = []
        for jvar in jetsvar:
            match = False
            for jnom in jetsnom:
                if (abs(jvar.eta - jnom.eta)<0.01 and abs(jvar.phi - jnom.phi)<0.01):
                    match = True
                    newjets.append(jnom)
                    break
            if not match:
                print "compareJets: no match found jvar_pt={0}".format(jvar.pt)
                newjets.append(jvar)
        #Preliminary fix: attach transfer function to jets which do not pass nominal selection (needed for catChange)
        for jet in newjets:
            if not hasattr(jet,"tf_b"):
                attach_jet_transfer_function(jet, self.conf)

        return newjets #DS



    
    def calculate_mbb_closest(self, bjet_candidates):

        if len(bjet_candidates)<2:
            return 0

        #find closest pair in deltaR
        pairs = set([])
        ordered = {}
        for j1 in bjet_candidates:
            for j2 in bjet_candidates:
                if j1 == j2:
                    continue
                if (j1, j2) in pairs or (j2, j1) in pairs:
                    continue
                pairs.update([(j1, j2)])
                lv1 = lvec(j1)
                lv2 = lvec(j2)
                dr = lv1.DeltaR(lv2)
                ordered[dr] = (lv1, lv2)
        dr0 = sorted(ordered.keys())[0]
        mbb_closest = (ordered[dr0][0] + ordered[dr0][1]).M()
        return mbb_closest

    def process(self, event):
        event.MET = MET(metobj=event.met, systs=self.conf.mem["factorized_sources"])
        event.MET_gen = MET(pt=event.MET.genPt, phi=event.MET.genPhi)
        event.MET_tt = MET(px=0, py=0)
        evdict = OrderedDict()
        
        #We create a wrapper around the base event with nominal quantities
        if "nominal" in self.conf.general["systematics"]:
            evdict["nominal"] = SystematicObject(event, {"systematic": "nominal"})

        #add events with variated jets
        if self.cfg_comp.isMC:
            jets_variated = {}
            for fjc in self.conf.mem["factorized_sources"]:
                for sdir, sigma in [("Up", 1.0), ("Down", -1.0)]:
                    jet_var = self.variateJets(event.Jet, fjc, sigma)
                    jets_variated[fjc+sdir] = jet_var
            for name, jets in jets_variated.items():
                #skip processing of systematics that are not enabled
                if not name in self.conf.general["systematics"]:
                    continue

                ev = SystematicObject(event, {"Jet": jets, "systematic": name})
                evdict[name] = ev
                
        for syst, event_syst in evdict.items():
            event_syst.systematic = syst 
            res = self._process(event_syst, evdict)

            #For variated events, add pointer to nominal event
            #if syst != "nominal":#DS possibly source of exploding Memory usage
            #    res.nominal_event = evdict["nominal"]
            evdict[syst] = res
        event.systResults = evdict 
        btag_wp = self.conf.jets["btagWP"]
        
        event.systResults["nominal"].changes_jet_category = False
        event.systResults["nominal"].nominal_event = event.systResults["nominal"]
        nj_nominal = event.systResults["nominal"].numJets
        nt_nominal = getattr(event.systResults["nominal"],"nB"+btag_wp)
        pass_nominal = event.systResults["nominal"].passes_jet #DS
        event.catChange = 0


        #Loop over all systematic variations to find change in category, number of jets or tags
        for syst in evdict.keys():
            if not evdict[syst].passes_jet:
                continue #DS
            nj = evdict[syst].numJets
            nt = getattr(evdict[syst],"nB"+btag_wp)
            evdict[syst].changes_jet_category = False
            #Do for all syst. variation that do
            # - not pass nominal selection OR
            # - have different number of good jets than nominal OR
            # - have different number of btags than nominal
            if not pass_nominal or nj != nj_nominal or nt != nt_nominal: #DS
                evdict[syst].changes_jet_category = True
                # Only consider the first change in Category
                if not event.catChange: #DS
                    LOG_MODULE_NAME.info(syst+" invokes catChange from (j,b): {0},{1} to {2},{3}".format(nj_nominal,nt_nominal,nj,nt))
                    if not pass_nominal:
                        LOG_MODULE_NAME.debug("   --> nominal did not pass")
                    event.catChange = deepcopy( evdict[syst] ) #requires change in BufferedTree class
                    event.catChange.systematic = "CatChange"
                    event.catChange.syst = syst
                    event.catChange.changes_jet_category = False
                    if syst.rfind("Up") == (len(syst)-2):
                        name = syst.rsplit("Up",1)[0]
                        #print name ##DS temp
                        jets_var = self.variateJets(event.catChange.good_jets, name, -1.0)
                        event.catChange.good_jets = self.compareJets(jets_var, event.systResults["nominal"].Jet)
                    elif syst.rfind("Down") == (len(syst)-4):
                        name = syst.rsplit("Down",1)[0]
                        #print name ##DS temp
                        jets_var = self.variateJets(event.catChange.good_jets, name, 1.0)
                        event.catChange.good_jets = self.compareJets(jets_var, event.systResults["nominal"].Jet)
            evdict[syst].catChange_event = event.catChange


        ret = self.conf.general["passall"] or np.any([v.passes_jet for v in event.systResults.values()])
        return ret

    def _process(self, event, evdict):
        
        #FIXME: why discarded jets no longer in vhbb?
        #injets = event.Jet+event.DiscardedJet
        event.injets = event.Jet
        #pt-descending input jets
        if LOG_MODULE_NAME.parent.level <= 10:
            for ij, j in enumerate(event.injets):
                LOG_MODULE_NAME.debug("InJetReco {0},pt = {1:06.2f}, eta = {2:05.2f},  deepcsv = {3:1.2f}, jetID = {4}, PUID = {5} ".format(ij, j.pt, j.eta, j.btagDeepCSV, j.jetId, j.puId))

        #choose pt cut key based on lepton channel
        pt_cut  = "pt"
        eta_cut = "eta"
        jetSel = "baseSelection"
        if event.is_sl:
            pt_cut  = "pt_sl"
            eta_cut = "eta_sl"
        elif event.is_dl:
            pt_cut  = "pt_dl"
            eta_cut = "eta_dl"
            jetSel = "tightSelection"
        
        #define lepton-channel specific selection function
        jetsel = lambda x, self=self, pt_cut=pt_cut, eta_cut=eta_cut: (
            x.pt > self.conf.jets[pt_cut]
            and abs(x.eta) < self.conf.jets[eta_cut]
            and self.conf.jets[jetSel](x)
        )
        
        jetsel_loose_pt = lambda x, self=self, pt_cut=pt_cut, eta_cut=eta_cut: (
            x.pt > 20
            and abs(x.eta) < self.conf.jets[eta_cut]
            and self.conf.jets[jetSel](x)
        )

        #Identify loose jets by (pt, eta)
        loose_jets = sorted(filter(
            jetsel_loose_pt, event.injets
            ), key=lambda x: x.pt, reverse=True
        )

        #Take care of overlaps between jets and veto leptons
        jets_to_remove = []
        for lep in event.veto_leptons:
            #overlaps removed by delta R
            for jet in loose_jets:
                lv1 = lvec(jet)
                lv2 = lvec(lep)
                dr = lv1.DeltaR(lv2)
                if dr < 0.4:
                    jets_to_remove += [jet]

        #Now actually remove the overlapping jets
        for jet in jets_to_remove:
            LOG_MODULE_NAME.debug("removing jet pt = {0:06.2f}, eta =  {1:05.2f}".format(jet.pt, jet.eta))
            if jet in loose_jets:
                loose_jets.remove(jet)
        
        #in DL apply two-stage pt cuts
        #Since this relies on jet counting, needs to be done **after** any other jet filtering
        if event.is_dl:
            good_jets_dl = []
            for jet in loose_jets:
                if len(good_jets_dl) < 2:
                    ptcut = self.conf.jets["pt_sl"]
                else:
                    ptcut = self.conf.jets["pt_dl"]
                if jet.pt > ptcut:
                    good_jets_dl += [jet]
            loose_jets = good_jets_dl

        #Now apply true pt cuts to identify analysis jets
        event.good_jets = filter(jetsel, loose_jets)
        event.loose_jets = filter(lambda x, event=event: x not in event.good_jets, loose_jets) 

        if LOG_MODULE_NAME.parent.level <= 10:
            LOG_MODULE_NAME.debug("Loose jets: "+str(len(event.loose_jets)))
            for ix,x in enumerate(event.loose_jets):
                LOG_MODULE_NAME.debug("Jet: {0} - pt = {1:06.2f}, eta= {2:05.2f}, btag= {3:01.4f}".format(ix, x.pt, x.eta, x.btagDeepCSV))
            LOG_MODULE_NAME.debug("Good jets:"+str(len(event.good_jets)))
            for ix,x in enumerate(event.good_jets):
                LOG_MODULE_NAME.debug("Jet: {0} - pt = {1:06.2f}, eta= {2:05.2f}, btag= {3:01.4f}".format(ix, x.pt, x.eta, x.btagDeepCSV))

            
        if "debug" in self.conf.general["verbosity"]:
            autolog("All jets: ", len(event.injets))
            for ix, x in enumerate(event.injets):
                if event.systematic != "nominal":
                    autolog("Jet: {0}: -pt = {1:06.2f}, eta= {2:05.2f}, {3} = {4:.4f}".format(ix, x.pt, x.eta, event.systematic, getattr(x, "corr_"+event.systematic)))
                else:
                    autolog("Jet: {0}: -pt = {1:06.2f}, eta= {2:05.2f}".format(ix, x.pt, x.eta))
            autolog("Loose jets: ", len(event.loose_jets))
            for ix,x in enumerate(event.loose_jets):
                autolog("Jet: {0} - pt = {1:06.2f}, eta= {2:05.2f}".format(ix, x.pt, x.eta))
            autolog("Good jets: ", len(event.good_jets))
            for ix,x in enumerate(event.good_jets):
                autolog("Jet: {0} - pt = {1:06.2f}, eta= {2:05.2f}".format(ix, x.pt, x.eta))


        #Adding jet transfer functions
        for jet in event.loose_jets + event.good_jets:
            attach_jet_transfer_function(jet, self.conf)

        event.numJets = len(event.good_jets)

        event.btagged_jets_bdisc_flav = {}
        event.btagged_jets_bdisc = {}
        event.buntagged_jets_bdisc = {}

        event.btagged_jets_bdisc_flav["btagDeepFlav"] = filter(
                lambda x, algo="btagDeepFlav", wp="DeepFlavM": getattr(x, algo) > wp,
                event.good_jets
            )
        setattr(event, "nBDeepFlavM", len(event.btagged_jets_bdisc_flav["btagDeepFlav"]))

        for (btag_wp_name, btag_wp) in self.conf.jets["btagWPs"].items():
            algo, wp = btag_wp
            event.btagged_jets_bdisc[btag_wp_name] = filter(
                lambda x, algo=algo, wp=wp: getattr(x, algo) > wp,
                event.good_jets
            )
            event.buntagged_jets_bdisc[btag_wp_name] = filter(
                lambda x, algo=algo, wp=wp: getattr(x, algo) <= wp,
                event.good_jets
            )
            if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                autolog("btagged jets", btag_wp_name, btag_wp, len(event.btagged_jets_bdisc[btag_wp_name]))
            setattr(event, "nB"+btag_wp_name, len(event.btagged_jets_bdisc[btag_wp_name]))

        #Find jets that pass/fail the specified default b-tagging algo/working point
        event.loosebuntag_jets_bdisc = event.buntagged_jets_bdisc[self.conf.jets["looseBWP"]] #DS
        event.loosebtag_jets_bdisc = event.btagged_jets_bdisc[self.conf.jets["looseBWP"]] #DS

        event.buntagged_jets_bdisc = event.buntagged_jets_bdisc[self.conf.jets["btagWP"]]
        event.btagged_jets_bdisc = event.btagged_jets_bdisc[self.conf.jets["btagWP"]]

        #calculate mass of closest mbb pair
        event.mbb_closest = self.calculate_mbb_closest(event.btagged_jets_bdisc)
        
        #Find how many of these tagged jets are actually true b jets
        if self.cfg_comp.isMC:
            event.n_tagwp_tagged_true_bjets = 0
            for j in event.btagged_jets_bdisc:
                if abs(j.partonFlavour) == 5:
                    event.n_tagwp_tagged_true_bjets += 1

        btag_wp = self.conf.jets["btagWP"]

        #Require at least 4 good resolved jets to continue analysis
        passes = True
        if event.systematic == "nominal":
            event_proxy = event
        else:
            event_proxy = evdict["nominal"]
        if event.is_sl and not (len(event_proxy.good_jets) >= 4 and getattr(event_proxy,"nB"+btag_wp)>=2):
            if "debug" in self.conf.general["verbosity"]:
                autolog("fails because SL NJ<3")
            passes = False
        elif event.is_dl:
            if not (len(event_proxy.good_jets) >= 2 and getattr(event_proxy,"nB"+btag_wp)>=1):
                if "debug" in self.conf.general["verbosity"]:
                    autolog("fails because DL NJ<2")
                passes = False
        elif event.is_fh:
            if len(event.good_jets) < self.conf.jets["minjets_fh"]: #DS
                passes = False
                if "debug" in self.conf.general["verbosity"]:
                    autolog("fails because FH NJ<{0}".format(self.conf.jets["minjets_fh"]))
            if len(event.good_jets) >= self.conf.jets["minjets_fh"]:
                if event.good_jets[ self.conf.jets["nhard_fh"]-1 ].pt<self.conf.jets["pt_fh"]:
                    if "debug" in self.conf.general["verbosity"]:
                        autolog("fails because FH Jet {0} pt = {1} (> {2} requ.)".format(self.conf.jets["nhard_fh"]-1,
                                                                                        event.good_jets[ self.conf.jets["nhard_fh"]-1 ].pt,
                                                                                        self.conf.jets["pt_fh"] )
                        )
                    passes = False

        #Calculate jet corrections to MET
        corrMet_px = event.MET.px
        corrMet_py = event.MET.py
        sum_dEx = 0
        sum_dEy = 0
        if self.cfg_comp.isMC:
            for jet in event.good_jets:
                Prec = lvec(jet)
                Pgen = lvec(jet)
                Pgen.SetPtEtaPhiM(jet.mcPt, jet.mcEta, jet.mcPhi, jet.mcM)
                Erec = Prec.E()
                Egen = Pgen.E()
                dEx = (Erec-Egen) * Prec.Px()/Prec.P()
                dEy = (Erec-Egen) * Prec.Py()/Prec.P()
                sum_dEx += dEx
                sum_dEy += dEy
        corrMet_px += sum_dEx
        corrMet_py += sum_dEy
        event.MET_jetcorr = MET(px=corrMet_px, py=corrMet_py)
        event.passes_jet = passes
        
        #Do gen-jet analysis
        if self.cfg_comp.isMC:
            genjets = event.GenJet
            for jet in event.good_jets:
                pt1 = jet.mcPt
                eta1 = jet.mcEta
                phi1 = jet.mcPhi
                mass1 = jet.mcM
                lv1 = ROOT.TLorentzVector()
                lv1.SetPtEtaPhiM(pt1, eta1, phi1, mass1)
                for gj in genjets:
                    lv2 = lvec(gj)
                    if lv1.DeltaR(lv2) < 0.01:
                        jet.genjet = gj
                        genjets.remove(gj)
                        break

        # calculat ht, qgl weight and highest csv variables
        event.ht = sum(map(lambda x: x.pt, event.good_jets))
        ht30 = 0
        ht40 = 0
        count = 0
        csv1 = -30
        csv2 = -30
        qgWeight = 1
        for jet in event.good_jets:
            if self.cfg_comp.isMC:
                qgSF = -99.0
                if jet.qgl<0:
                    qgSF = 1.0
                elif jet.partonFlavour==21:
                    qgSF = ( -55.7067*pow(jet.qgl,7) + 113.218*pow(jet.qgl,6)
                             -21.1421*pow(jet.qgl,5) -99.927*pow(jet.qgl,4) 
                             + 92.8668*pow(jet.qgl,3) -34.3663*pow(jet.qgl,2) 
                             + 6.27*jet.qgl + 0.612992 )
                else:
                    qgSF = ( -0.666978*pow(jet.qgl,3) + 0.929524*pow(jet.qgl,2)
                             -0.255505*jet.qgl + 0.981581 )
                idx = event.good_jets.index(jet)
                setattr(event.good_jets[idx],"qg_sf",qgSF)
                qgWeight *= qgSF
            if abs(jet.eta)<2.4:
                count += 1
                if jet.pt>30:
                    ht30 += jet.pt
                    #if jet.btagCSV>csv1:
                    #    csv2 = csv1
                    #    csv1 = jet.btagCSV
                    #elif jet.btagCSV>csv2:
                    #    csv2 = jet.btagCSV
                if jet.pt>40:
                    ht40 += jet.pt
                
        event.ht30 = ht30
        event.ht40 = ht40
        event.csv1 = csv1
        event.csv2 = csv2
        event.qgWeight = qgWeight


        """#TODO Implement Trigger SF
        #calculate trigger scale factor
        if self.cfg_comp.isMC:
            if len(event.good_jets)>5:
                trigSF = get_trigger_factor(event.ht, event.good_jets[5].pt, event.nBCSVM)
            else:
                trigSF = get_trigger_factor(event.ht, 0.0, event.nBCSVM)
            #print "nb={0} 6jpt={1} ht={2} SF={3} err={4}".format(event.nBCSVM, event.good_jets[5].pt, event.ht, trigSF[0], trigSF[1] ) ##DS temp
        else:
            trigSF = (1.0,0.0)
        event.triggerWeight = trigSF[0]
        event.triggerWeightErr = trigSF[1]
        event.triggerWeightUp = trigSF[0]+trigSF[1]
        event.triggerWeightDown = trigSF[0]-trigSF[1]
        """
        
        return event
