from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
import copy
import sys
import numpy as np
import math
import pickle
import pandas
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

import pdb


class Jet_container:
    def __init__(self, *args):

        # TLV
        if len(args) == 1:
            self.pt   = args[0].Pt()
            self.eta  = args[0].Eta()
            self.phi  = args[0].Phi()
            self.mass = args[0].M()
        # pt eta phi mass
        elif len(args) == 4:
            self.pt   = args[0]
            self.eta  = args[1]
            self.phi  = args[2]
            self.mass = args[3]



class SubjetAnalyzer(FilterAnalyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(SubjetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf


        self.R_cut = 0.3
        self.R_cut_fatjets = 1.0
        self.top_mass = 172.04
        self.btagAlgo = self.conf.jets["btagAlgo"]

        #TO DO: Is this needed? Also for Higgs
        self.GenTop_pt_cut = 150
        self.GenHiggs_pt_cut = 150


    def beginLoop(self, setup):
        super(SubjetAnalyzer, self).beginLoop(setup)


    def endLoop(self, setup):
        if "subjet" in self.conf.general["verbosity"]:
            print 'Running endLoop'


    def process(self, event):

        if event.catChange: #DS
            if "systematics" in self.conf.general["verbosity"]:
                autolog("SubjetAnalyzer: processing catChange")
            res = self._process(event.catChange,event.catChange.syst)
            event.catChange = res #DS

        #Process candidates with variated systematics
        for (syst, event_syst) in event.systResults.items():
            if getattr(event_syst, "passes_btag", False):
                res = self._process(event_syst,syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_subjet = False
        return self.conf.general["passall"] or np.any([v.passes_subjet for v in event.systResults.values()])

    def _process(self, event,syst):


        #Get correct systematic variation for all boosted objects
        self.BoostedJEC(event,syst)

        event.passes_subjet = True
        
        if "debug" in self.conf.general["verbosity"]:
            autolog("SubjetAnalyzer started")

        if "subjet" in self.conf.general["verbosity"]:
            print 'Printing from SubjetAnalyzer! iEv = {0}'.format(event.iEv)
            

        # Is set to True only after the event passed all criteria
        setattr(event, 'PassedSubjetAnalyzer', False)

        # Create two new lists for selected_btagged_jets and wquark_candidate_jets
        # Needs to be done here because the lists are needed in the mem config
        setattr(event, 'boosted_bjets', [])
        setattr(event, 'boosted_ljets', [])
        setattr(event, 'boosted_allljets', [])
        setattr(event, 'topCandidate', [])
        setattr(event, 'higgsCandidate', [])
        setattr(event, 'htt_subjets_b', [])
        setattr(event, 'htt_subjets_W', [])
        setattr(event, 'higgs_subjets', [])
        setattr(event, 'otherhtt_subjets', [])
        setattr(event, 'otherhiggs_subjets', [])
        setattr(event, 'boosted', 0)
        setattr(event, 'hastop', 0)
        setattr(event, 'hashiggs', 0)

        ###############################################
        #     Prepare objects for boosted analysis    #
        ###############################################

        # Match the top to a fatjet
        #  - Copies and tau_N, calculates n_subjettiness
        event.HTTV2 = self.Match_top_to_fatjet(event, event.HTTV2)

        # Calculate delR with the lepton for all tops that survived the cut
        # This also makes sure automatically that no top taggers are computed for DL events
        if event.is_sl: #LC
            for alltop in event.HTTV2:
                setattr( alltop, 'delR_lepton' ,
                          self.Get_DeltaR_two_objects(alltop, event.good_leptons[0]))
        else:
            for alltop in event.HTTV2:
                setattr( alltop, 'delR_lepton' , -1 )


        # Match the Higgs to a fatjet
        #  - Copies and tau_N, calculates n_subjettiness
        event.FatjetAK8 = self.Match_higgs_to_fatjet(event, event.FatjetAK8)


        ########################################
        #     Apply cuts to boosted objects    #
        ########################################

        # Keep track of number of andidates that passed the cut
        setattr(event, 'ntopCandidate', len(event.HTTV2))
        setattr(event, 'ntopCandidate_aftercuts', 0)
        setattr(event, 'nhiggsCandidate', len(event.FatjetAK8))
        setattr(event, 'nhiggsCandidate_aftercuts', 0)


        topcuts = self.conf.boost["top"]

        #Extract WP for highest top subjet btag
        #btag_wp = self.conf.jets["btagWPs"][topcuts["btagL"]][1]


        alltops = filter(
            lambda x, topcuts=topcuts: (
                x.ptreco > topcuts["pt"]
                and abs(x.eta) < topcuts["eta"]
                #and x.delR_lepton > topcuts["drl"]
                #and x.btagL > btag_wp
                #and x.tau32SD < topcuts["tau32SD"]
                #and x.massreco > topcuts["mass_inf"]
                #and x.massreco < topcuts["mass_sup"]
                #and x.fRec < topcuts["frec"]
                and x.subjetIDPassed > 0.5 
            ), event.HTTV2
        )

        #Cut on Top BDT:
        if len(alltops):
            for i in alltops:
                d = [(i.mass,i.fRec,i.delR_lepton)]
                df = pandas.DataFrame(d)               
                a =  self.conf.topBDT.predict_proba(d)
                setattr(i,"bdt",a[0][1])


        alltops = filter(
            lambda x, topcuts=topcuts: (
                x.bdt > topcuts["bdt"]             
            ), alltops
        )

        higgscuts = self.conf.boost["higgs"]

        allhiggs = filter(
            lambda x, higgscuts=higgscuts: (
                x.ptreco > higgscuts["pt"]
                and abs(x.eta) < higgscuts["eta"]  
                #and x.msoftdrop > higgscuts["msoft"]       
                #and x.massreco > higgscuts["msoft"]        
                #and x.tau21 < higgscuts["tau21SD"]
                and x.bbtag > higgscuts["bbtag"]
                #and x.btagSL > higgscuts["btagSL"]
            ), event.FatjetAK8
        )


        #################################
        #     Get the top candidates    #
        #################################

        # Keep track of how many httCandidates passed
        event.ntopCandidate_aftercuts = len(alltops)

        #Find the best hadronic gen top match for each top candidate
        if self.cfg_comp.isMC:
            gentops = getattr(event, "genTopHad", [])
            if len(gentops)>0:
                for topcandidate in alltops:
                    lv1 = lvec(topcandidate)
                    drs = []
                    for igentop, gentop in enumerate(gentops):
                        lv2 = lvec(gentop)
                        drs += [(lv1.DeltaR(lv2), gentop, igentop)]
                    drs = sorted(drs, key=lambda x: x[0])
                    best = drs[0]
                    topcandidate.genTopHad_dr = best[0]
                    topcandidate.genTopHad = best[1]
                    topcandidate.genTopHad_index = best[2]

        # If exactly 1 survived, simply continue with that candidate
        other_top_present = False

        # If more than 1 candidate survived the cutoff criteria, choose the
        # one whose delR with the lepton was biggest
        if len(alltops):
            other_top_present = True
            if event.is_sl: #SL 
                alltops = sorted(alltops, key=lambda x: -x.delR_lepton)
            else:
                alltops = sorted(alltops, key=lambda x: x.ptreco)


        if "subjet" in self.conf.general["verbosity"]:
            print "Number of top candidates ", len(alltops)

        #Get best top candidate
        top = None
        if len(alltops):
            top = alltops[0]


        # Get the subjets from the topCandidate
        #  - Also sets transfer functions as attributes
        #  - Returns subjets ordered by decreasing btag
        #  - First subjet has btagFlag==1.0, the other two btagFlag==0.0
        topsubjets = []
        for candidate in event.HTTV2Subjet:
            topsubjets.append(copy.deepcopy(candidate))

        if len(alltops) > 0:
            alltops_subjets = self.Get_Subjets_Top(alltops,topsubjets)
            top_subjets = alltops_subjets[0]
        else:
            alltops_subjets = []
            top_subjets = []



        ###################################
        #     Get the Higgs candidates    #
        ###################################

        event.nhiggsCandidate_aftercuts = len(allhiggs)


        higgs_present = False

        if len(allhiggs) > 0:
            higgs_present = True

        #Sort by bbtag for now
        allhiggs = sorted(allhiggs, key=lambda x: -x.bbtag)

        for higgs in allhiggs:
            if len(alltops) > 0:
                higgs.dr_top = self.Get_DeltaR_two_objects(higgs, alltops[0])
            else:
                higgs.dr_top = -1
                   
            if self.cfg_comp.isMC:
                #match higgs candidate to generated higgs
                genhiggs = [x for x in getattr(event, "GenHiggsBoson", []) if x.pt>self.GenHiggs_pt_cut]
                if len(genhiggs)>0:
                    lv1 = lvec(higgs)
                    lv2 = lvec(genhiggs[0])
                    higgs.dr_genHiggs = lv1.DeltaR(lv2)

                #match higgs candidate to generated tops
                gentops = [x for x in getattr(event, "GenTop", []) if x.pt>self.GenTop_pt_cut]
                if len(gentops)>0:
                    lv1 = lvec(higgs)
                    higgs.dr_genTop = min([lv1.DeltaR(lvec(x)) for x in gentops])
                else:
                    higgs.dr_genTop = -1

        #Need to filter Higgs list to remove top candidate
        if top is not None:
            allhiggs = filter(lambda x: (self.Get_DeltaR_two_objects(x,top) > 1.5), allhiggs)


        higgs = None
        if len(allhiggs):
            higgs = allhiggs[0]


        # Get the subjets from the higgsCandidate
        #  - Also sets transfer functions as attributes
        #  - Returns subjets ordered by decreasing btag
        #  - First subjet has btagFlag==1.0, the other two btagFlag==0.0
        higgssubjets = []
        for candidate in event.SubjetAK8:
            higgssubjets.append(copy.deepcopy(candidate))

        if len(allhiggs) > 0:
            allhiggs_subjets = self.Get_Subjets_Higgs(allhiggs,higgssubjets)
            higgs_subjets = allhiggs_subjets[0]
        else:
            allhiggs_subjets = []
            higgs_subjets = []



        ###################################
        #     Create new subjets lists    #
        ###################################

        # Create two new lists for btagged_jets and wquark_candidate_jets in the original events
        if event.is_sl: # There are at most 4 btagged jets
            reco_btagged_jets = copy.deepcopy( event.selected_btagged_jets_high )
            reco_ltagged_jets = copy.deepcopy( list( event.wquark_candidate_jets ) )
        else: #
            reco_ltagged_jets = event.buntagged_jets_bdisc
            reco_btagged_jets = event.btagged_jets_bdisc

        for jet in reco_btagged_jets:
            setattr( jet, 'btag', getattr(jet,self.btagAlgo) )
            setattr( jet, 'btagFlag', 1.0 )

        for jet in reco_ltagged_jets:
            setattr( jet, 'btag', getattr(jet,self.btagAlgo) )
            setattr( jet, 'btagFlag', 0.0 )

        #Only proceed if there is either a top or a Higgs candidate
        if len(alltops)+len(allhiggs) > 0:
  
            ########################################
            # Matching
            ########################################

            # Whenever a subjet has a 'match' (dR < dR_cut) to a resolved jet, 
            # the matched object should be excluded from the event

            # Match subjet to a bjet
            n_excluded_bjets = self.Match_two_lists(
                top_subjets+higgssubjets, 'subjet',
                reco_btagged_jets, 'bjet')

            # Match subjet to a ljet
            n_excluded_ljets = self.Match_two_lists(
                top_subjets+higgssubjets , 'subjet',
                reco_ltagged_jets, 'ljet')  

            if "subjet" in self.conf.general["verbosity"]:
                print "subjet nMatchB={0} nMatchL={1}".format(n_excluded_bjets, n_excluded_ljets)


            # In case of double matching to b and l quarks, choose the match with lowest delR
            # (This is not expected to happen often)
            for subjet in top_subjets+higgs_subjets:
                if hasattr(subjet, 'matched_bjet') and \
                    hasattr(subjet, 'matched_ljet') :
                    print '[SubjetAnalyzer] Double match detected'
                    if subjet.matched_bjet_delR < subjet.matched_ljet_delR:
                        del subjet.matched_ljet
                        del subjet.matched_ljet_delR
                        n_excluded_bjets -= 1
                    else:
                        del subjet.matched_bjet
                        del subjet.matched_bjet_delR
                        n_excluded_ljets -= 1


            ########################################
            # Modifying the bjets and ljets lists
            ########################################

            # These are the jets which will be fed into the MEM
            boosted_bjets = []
            boosted_ljets = []
            boosted_allljets = []

            # Check if we will have enough jets left to run the MEM (we need at least 4 btagged jets)
            # The original b-jet collection has at most 4 jets (check that less are also possible)
            # If we have:
            # Only top: 1 bjet will be gone, so we need at least 3 more
            # Only Higgs: 2 bjets will be gone, need 2 more
            # Higgs and top: 3 bjets will be used, need one more

            #Check the number of bjetse in the event
            nbjets = len(reco_btagged_jets)
            if top is not None:
                nbjets += 1
            if higgs is not None:
                nbjets += 2
            nbjets -= n_excluded_bjets


            

            if "subjet" in self.conf.general["verbosity"]:
                print "subjet replacing"
            # Add the subjets to the final output lists first
            if top is not None:
                for subjet in top_subjets:
                    if subjet.btagFlag == 1.0: boosted_bjets.append(subjet)
                    if subjet.btagFlag == 0.0: boosted_ljets.append(subjet)
            if higgs is not None:
                for subjet in higgs_subjets:
                    boosted_bjets.append(subjet)
            # Sort tl btagged jets by decreasing btag (to be sure, but should 
            # already be done in previous analyzer)
            # Only resolved b-jets
            reco_btagged_jets = sorted( reco_btagged_jets, key=lambda x: -x.btag )
            # Add up to 4 reco btagged jets to the output lists
            for bjet in reco_btagged_jets:
                # Check if the b-jet is not excluded
                if not hasattr( bjet, 'matched_subjet' ):
                    boosted_bjets.append(bjet)
                # Stop adding after 4 b-jets
                if len(boosted_bjets) == 4: break
            #boosted_allljets = boosted_ljets
            for ljet in reco_ltagged_jets:
                if not hasattr( ljet, 'matched_subjet' ):
                    boosted_allljets.append(ljet)
            if top is None:
                boosted_ljets = boosted_allljets

            if nbjets >= 4:
                event.PassedSubjetAnalyzer = True

            # If too many events are excluded, just run the default hypothesis
            else:
                if "subjet" in self.conf.general["verbosity"]:
                    print "[SubjetAnalyzer] subjet has too many overlaps, using reco"
                #boosted_bjets = reco_btagged_jets
                #boosted_ljets = reco_ltagged_jets
                event.PassedSubjetAnalyzer = False

        else:
            event.PassedSubjetAnalyzer = False
     


        ########################################
        # Write to event
        ########################################

        # Store output lists in event
        #Only if it either of the two candidates
        if len(alltops)+len(allhiggs) > 0:

            # Variables which we save to file for all systs
            event.topCandidate = alltops
            event.higgsCandidate = allhiggs

            # Subjets from best top (preliminary) for further use
            if len(top_subjets)==3:
                event.htt_subjets_b = [top_subjets[0]]
                event.htt_subjets_W = [top_subjets[1], top_subjets[2]]

            # Subjets from best Higgs (preliminary) for further use
            if len(higgs_subjets)==2:
                event.higgs_subjets = [higgs_subjets[0], higgs_subjets[1]]

            #Save also other candidate subjets
            if len(alltops) > 0:
                event.hastop = 1
                for ind,tsubjet in alltops_subjets.iteritems():
                    event.otherhtt_subjets = [tsubjet[0],tsubjet[1],tsubjet[2]]
            if len(allhiggs) > 0:
                event.hashiggs = 1
                for ind,hsubjet in allhiggs_subjets.iteritems():
                    event.otherhiggs_subjets = [hsubjet[0],hsubjet[1]]


            event.boosted_bjets = boosted_bjets
            event.boosted_ljets = boosted_ljets

            event.n_boosted_bjets = len(boosted_bjets)
            event.n_boosted_ljets = len(boosted_ljets)

            event.n_excluded_bjets = n_excluded_bjets
            event.n_excluded_ljets = n_excluded_ljets

            if event.PassedSubjetAnalyzer == True:
                event.boosted = 1
            else:
                event.boosted = 0

        else:
            event.boosted = 0


        if "subjet" in self.conf.general["verbosity"]:
            print '[SubjetAnalyzer] Exiting SubjetAnalyzer! event.PassedSubjetAnalyzer = {0}'.format(
                event.PassedSubjetAnalyzer
            )


        ########################################
        # Matching to Gen top
        ###########################################

        event.n_matched_TTgentop = -1
        event.matched_TTgentop_pt = -1
        event.n_matched_TTgenb = -1
        event.n_matched_TTgenW = -1

        if self.cfg_comp.isMC and len(alltops)>0:
            self.Do_GenTop_Matching(event,topsubjets)

        return event 

        ########################################
        # Quark Matching
        ########################################

        # This section is only useful for truth-level comparison, and can be turned
        # off if this is not needed.
        # Do_Quark_Matching( event ) sets number of matches with quarks as branches
        # in the event, but these branches do not have to be filled (they will be
        # automatically set to -1 in the final output root file).

        if self.cfg_comp.isMC:
            self.Do_Quark_Matching(event)

       
    ########################################
    # Functions
    ########################################

    def BoostedJEC(self, event, syst):
        for i in event.HTTV2Subjet + event.SubjetAK8:
            if syst == "nominal":
                pass
            else:
                corrfactor = getattr(i,"pt_corr_{}".format(syst))/i.pt
                i.mass = i.mass*corrfactor
                i.pt = getattr(i,"pt_corr_{}".format(syst))


    # ==============================================================================
    # Matches variables of fatjet to top
    def Match_top_to_fatjet(self, event, tops):

        # Loosely match the fatjets to the tops
        #n_matched_httcand_fatjet = self.Match_two_lists(
        #    tops, 'top',
        #    event.FatjetCA15, 'fatjet',
        #    R_cut = self.R_cut_fatjets)
        #
        n_matched_httcand_fatjet_softdrop = self.Match_two_lists(
            tops, 'top',
            event.FatjetCA15SoftDrop, 'fatjet_softdrop',
            R_cut = self.R_cut_fatjets)

        for top in tops:

            # First match to softdrop fatjet
            if hasattr(top, 'matched_fatjet_softdrop'):

                fatjet_softdrop = top.matched_fatjet_softdrop

                # Get n_subjettiness from the matched fatjet
                tau32SD = fatjet_softdrop.tau3 / fatjet_softdrop.tau2 if fatjet_softdrop.tau2 > 0.0 else 0.0 
                tau21SD = fatjet_softdrop.tau2 / fatjet_softdrop.tau1 if fatjet_softdrop.tau1 > 0.0 else 0.0 
   
                # Set n_subjettiness, tau_N and the bbtag
                top.tau32SD = tau32SD
                top.tau21SD = tau21SD
                top.tau1SD = fatjet_softdrop.tau1
                top.tau2SD = fatjet_softdrop.tau2
                top.tau3SD = fatjet_softdrop.tau3

                # Calculate delRopt
                top.delRopt = top.Ropt - top.RoptCalc

                #Get corrected mass from subjets
                s1 = lvec(event.HTTV2Subjet[top.subJetIdx1])
                s2 = lvec(event.HTTV2Subjet[top.subJetIdx2])
                s3 = lvec(event.HTTV2Subjet[top.subJetIdx3])
                vtop = s1+s2+s3
                top.massreco = vtop.M()
                top.ptreco = vtop.Pt()
                top.btagL = max(event.HTTV2Subjet[top.subJetIdx1].btag,
                    event.HTTV2Subjet[top.subJetIdx2].btag,
                    event.HTTV2Subjet[top.subJetIdx3].btag)
                
            else:
                print 'Warning: top candidate unmatchable to softdrop fatjet!'
                top.massreco = -999.
                top.ptreco = -999.

            # Match to fatjet
            #if hasattr(top, 'matched_fatjet'):

            #    fatjet = top.matched_fatjet

            #    # Get n_subjettiness from the matched fatjet
            #    tau32 = fatjet.tau3 / fatjet.tau2 if fatjet.tau2 > 0.0 else 0.0 
            #    tau21 = fatjet.tau2 / fatjet.tau1 if fatjet.tau1 > 0.0 else 0.0 
   
            #    # Set n_subjettiness, tau_N and the bbtag
            #    top.tau32 = tau32
            #    top.tau21 = tau21
            #    top.tau1 = fatjet.tau1
            #    top.tau2 = fatjet.tau2
            #    top.tau3 = fatjet.tau3
                
            #else:
            #    print 'Warning: top candidate unmatchable to fatjet!'     

        return tops

    # ==============================================================================
    # Matches variables of fatjet to higgs
    def Match_higgs_to_fatjet(self, event, higgses):

        # Loosely match the fatjets to the higgs
        for higgs in higgses:

            # Get n_subjettiness from the matched fatjet
            tau21 =  higgs.tau2 / higgs.tau1 if higgs.tau1 > 0.0 else 0.0 
 

            # Set n_subjettiness, tau_N and the bbtag and ungroomed kinematics
            higgs.tau21 = tau21
            higgs.tau1 = higgs.tau1
            higgs.tau2 = higgs.tau2
            higgs.tau3 = higgs.tau3            
            higgs.bbtag = higgs.bbtag
            if higgs.subJetIdx1 >=0 and higgs.subJetIdx2 >=0:
                higgs.btagL = max(event.SubjetAK8[higgs.subJetIdx1].btag,
                        event.SubjetAK8[higgs.subJetIdx2].btag)           
                higgs.btagSL = min(event.SubjetAK8[higgs.subJetIdx1].btag,
                        event.SubjetAK8[higgs.subJetIdx2].btag)
            else:
                higgs.btagL = -10
                higgs.btagSL = -10
            higgs.subJetIdx1 = higgs.subJetIdx1
            higgs.subJetIdx2 = higgs.subJetIdx2
            higgs.subjetIDPassed = 1

            if higgs.subJetIdx1 >=0 and higgs.subJetIdx2 >=0:
                s1 = lvec(event.SubjetAK8[higgs.subJetIdx1])
                s2 = lvec(event.SubjetAK8[higgs.subJetIdx2])
                vhiggs = s1+s2
                higgs.massreco = vhiggs.M()
                higgs.ptreco = vhiggs.Pt()

            else:
                higgs.massreco = -999.
                higgs.ptreco = -999.

        return higgses


    # ==============================================================================
    #Get Higgs subjets
    def Get_Subjets_Higgs(self, allhiggs, subjets):


        higgs_subjets = {}
        for higgs in allhiggs:

            if higgs is None:
                continue

            higgs_subjets[allhiggs.index(higgs)] = None
            subindex = [higgs.subJetIdx1,higgs.subJetIdx2]

            hs = []
            counter = 0
            for prefix in subindex:
                counter += 1
                if prefix == -1:
                    print "Careful, couldn't find Higgs subjets!"
                    x = Jet_container(-1000,-1000,-1000,-1000)
                    setattr(x, 'prefix', "sj{}".format(counter))
                    setattr(x,'btag',-10)
                    hs.append(x)
                else:
                    o = subjets[prefix]
                    x = Jet_container(
                        getattr(o,'pt'),
                        getattr(o,'eta'),
                        getattr(o,'phi'),
                        getattr(o,'mass'))
                    #Needed to get subjets in the correct format for the tree
                    setattr(x, 'prefix', "sj{}".format(subindex.index(prefix)+1))
                    setattr(x,'btag',getattr(o,'btag'))
                    if hasattr(o,'hadronFlavour'):
                        setattr(x,'hadronFlavour',getattr(o,'hadronFlavour'))
                    else:
                        setattr(x,'hadronFlavour',-100)
                    if hasattr(o,'corr') and hasattr(o,'corr_JER'):
                        setattr(x,'corr',getattr(o,'corr'))
                        setattr(x,'corr_JER',getattr(o,'corr_JER'))
                        for cor in self.conf.mem["factorized_sources"]:
                            for di in ["Up","Down"]:
                                setattr(x,'pt_corr_{}{}'.format(cor,di),getattr(o,'pt_corr_{}{}'.format(cor,di)))
                    else:
                        setattr(x,'corr',-100)
                        setattr(x,'corr_JER',-100)
                        for cor in self.conf.mem["factorized_sources"]:
                            for di in ["Up","Down"]:
                                setattr(x,'pt_corr_{}{}'.format(cor,di),-100)
                    #setattr(x, 'btagSF',getattr(o,'btagSF'))
                    #setattr(x, 'btagSF_up',getattr(o,'btagSF_up'))
                    #setattr(x, 'btagSF_down',getattr(o,'btagSF_down'))
                    #setattr(x, 'btagSF_shape',getattr(o,'btagSF_shape'))
                    #setattr(x, 'btagSF_shape_up_jes',getattr(o,'btagSF_shape_up_jes'))
                    #setattr(x, 'btagSF_shape_down_jes',getattr(o,'btagSF_shape_down_jes'))
                    #setattr(x, 'btagSF_shape_up_lf',getattr(o,'btagSF_shape_up_lf'))
                    #setattr(x, 'btagSF_shape_down_lf',getattr(o,'btagSF_shape_down_lf'))
                    #setattr(x, 'btagSF_shape_up_hf',getattr(o,'btagSF_shape_up_hf'))
                    #setattr(x, 'btagSF_shape_down_hf',getattr(o,'btagSF_shape_down_hf'))
                    #setattr(x, 'btagSF_shape_up_hfstats1',getattr(o,'btagSF_shape_up_hfstats1'))
                    #setattr(x, 'btagSF_shape_down_hfstats1',getattr(o,'btagSF_shape_down_hfstats1'))
                    #setattr(x, 'btagSF_shape_up_hfstats2',getattr(o,'btagSF_shape_up_hfstats2'))
                    #setattr(x, 'btagSF_shape_down_hfstats2',getattr(o,'btagSF_shape_down_hfstats2'))
                    #setattr(x, 'btagSF_shape_up_lfstats1',getattr(o,'btagSF_shape_up_lfstats1'))
                    #setattr(x, 'btagSF_shape_down_lfstats1',getattr(o,'btagSF_shape_down_lfstats1'))
                    #setattr(x, 'btagSF_shape_up_lfstats2',getattr(o,'btagSF_shape_up_lfstats2'))
                    #setattr(x, 'btagSF_shape_down_lfstats2',getattr(o,'btagSF_shape_down_lfstats2'))
                    #setattr(x, 'btagSF_shape_up_cferr1',getattr(o,'btagSF_shape_up_cferr1'))
                    #setattr(x, 'btagSF_shape_down_cferr1',getattr(o,'btagSF_shape_down_cferr1'))
                    #setattr(x, 'btagSF_shape_up_cferr2',getattr(o,'btagSF_shape_up_cferr2'))
                    #setattr(x, 'btagSF_shape_down_cferr2',getattr(o,'btagSF_shape_down_cferr2'))
                    hs.append(x)

            for sj in hs:
                setattr( sj, 'PDGID', 22 )


            # Adding subjet transfer functions
            for subjet in hs:
                jet_eta_bin = 0
                if abs(subjet.eta)>1.0:
                    jet_eta_bin = 1

                # If True, TF [0] - reco, x - gen
                # If False, TF [0] - gen, x - reco
                #Preliminary: Careful using mock htt TFs here!!
                eval_gen = False
                setattr( subjet, 'tf_b' ,
                    self.conf.tf_higgs_matrix['b'][jet_eta_bin].Make_Formula(eval_gen) )
                setattr( subjet, 'tf_l' ,
                    self.conf.tf_htt_matrix['l'][jet_eta_bin].Make_Formula(eval_gen) )
                setattr( subjet, 'tf_b_lost' ,
                    self.conf.tf_higgs_matrix['b'][jet_eta_bin].Make_CDF() )
                setattr( subjet, 'tf_l_lost' ,
                    self.conf.tf_htt_matrix['l'][jet_eta_bin].Make_CDF() )

                # Set jet pt threshold for CDF
                subjet.tf_b_lost.SetParameter(0, self.conf.jets["pt"])
                subjet.tf_l_lost.SetParameter(0, self.conf.jets["pt"])

                #PRELIMINARY - Add jet_corr 
                subjet.corr = subjet.corr
                subjet.corr_JER = subjet.corr_JER


            # Create a pointer in the top to its subjets
            setattr( higgs, 'subjets', hs )
            self.Attach_Subjets_To_Objects(higgs,hs)
   
            higgs_subjets[allhiggs.index(higgs)] = hs

        return higgs_subjets


    # ==============================================================================
    #Get Top subjets
    def Get_Subjets_Top( self, alltops, subjets ):

        top_subjets = {}
        for top in alltops:
            if top is None:
                continue
            top_subjets[alltops.index(top)] = None
            subindex = [top.subJetIdx1,top.subJetIdx2,top.subJetIdx3]

            ts = []
            for prefix in subindex:
                o = subjets[prefix]
                x = Jet_container(
                    getattr(o,'pt'),
                    getattr(o,'eta'),
                    getattr(o,'phi'),
                    getattr(o,'mass'))
                #Needed to get subjets in the correct format for the tree
                setattr(x, 'prefix', "sj{}".format(subindex.index(prefix)+1))
                setattr(x,'btag',getattr(o,'btag'))
                if hasattr(o,'hadronFlavour'):
                    setattr(x,'hadronFlavour',getattr(o,'hadronFlavour'))
                else:
                    setattr(x,'hadronFlavour',-100)
                if hasattr(o,'corr') and hasattr(o,'corr_JER'):
                    setattr(x,'corr',getattr(o,'corr'))
                    setattr(x,'corr_JER',getattr(o,'corr_JER'))
                    for cor in self.conf.mem["factorized_sources"]:
                        for di in ["Up","Down"]:
                            setattr(x,'pt_corr_{}{}'.format(cor,di),getattr(o,'pt_corr_{}{}'.format(cor,di)))
                else:
                    setattr(x,'corr',-100)
                    setattr(x,'corr_JER',-100)
                    for cor in self.conf.mem["factorized_sources"]:
                        for di in ["Up","Down"]:
                            setattr(x,'pt_corr_{}{}'.format(cor,di),-100)
                #setattr(x, 'btagSF',getattr(o,'btagSF'))
                #setattr(x, 'btagSF_up',getattr(o,'btagSF_up'))
                #setattr(x, 'btagSF_down',getattr(o,'btagSF_down'))
                #setattr(x, 'btagSF_shape',getattr(o,'btagSF_shape'))
                #setattr(x, 'btagSF_shape_up_jes',getattr(o,'btagSF_shape_up_jes'))
                #setattr(x, 'btagSF_shape_down_jes',getattr(o,'btagSF_shape_down_jes'))
                #setattr(x, 'btagSF_shape_up_lf',getattr(o,'btagSF_shape_up_lf'))
                #setattr(x, 'btagSF_shape_down_lf',getattr(o,'btagSF_shape_down_lf'))
                #setattr(x, 'btagSF_shape_up_hf',getattr(o,'btagSF_shape_up_hf'))
                #setattr(x, 'btagSF_shape_down_hf',getattr(o,'btagSF_shape_down_hf'))
                #setattr(x, 'btagSF_shape_up_hfstats1',getattr(o,'btagSF_shape_up_hfstats1'))
                #setattr(x, 'btagSF_shape_down_hfstats1',getattr(o,'btagSF_shape_down_hfstats1'))
                #setattr(x, 'btagSF_shape_up_hfstats2',getattr(o,'btagSF_shape_up_hfstats2'))
                #setattr(x, 'btagSF_shape_down_hfstats2',getattr(o,'btagSF_shape_down_hfstats2'))
                #setattr(x, 'btagSF_shape_up_lfstats1',getattr(o,'btagSF_shape_up_lfstats1'))
                #setattr(x, 'btagSF_shape_down_lfstats1',getattr(o,'btagSF_shape_down_lfstats1'))
                #setattr(x, 'btagSF_shape_up_lfstats2',getattr(o,'btagSF_shape_up_lfstats2'))
                #setattr(x, 'btagSF_shape_down_lfstats2',getattr(o,'btagSF_shape_down_lfstats2'))
                #setattr(x, 'btagSF_shape_up_cferr1',getattr(o,'btagSF_shape_up_cferr1'))
                #setattr(x, 'btagSF_shape_down_cferr1',getattr(o,'btagSF_shape_down_cferr1'))
                #setattr(x, 'btagSF_shape_up_cferr2',getattr(o,'btagSF_shape_up_cferr2'))
                #setattr(x, 'btagSF_shape_down_cferr2',getattr(o,'btagSF_shape_down_cferr2'))

                ts.append( x )

            # Set the btagFlags; order by decreasing btag, highest btag gets btagFlag=1.0
            ts = sorted( ts, key = lambda x: -x.btag )
            setattr( ts[0], 'btagFlag', 1.0 )
            setattr( ts[1], 'btagFlag', 0.0 )
            setattr( ts[2], 'btagFlag', 0.0 )

            for sj in ts:
                if sj.btagFlag == 1.0: setattr( sj, 'PDGID', 5 )
                if sj.btagFlag == 0.0: setattr( sj, 'PDGID', 1 )

            # Adding subjet transfer functions
            for subjet in ts:
                jet_eta_bin = 0
                if abs(subjet.eta)>1.0:
                    jet_eta_bin = 1

                # If True, TF [0] - reco, x - gen
                # If False, TF [0] - gen, x - reco
                eval_gen = False
                setattr( subjet, 'tf_b' ,
                    self.conf.tf_htt_matrix['b'][jet_eta_bin].Make_Formula(eval_gen) )
                setattr( subjet, 'tf_l' ,
                    self.conf.tf_htt_matrix['l'][jet_eta_bin].Make_Formula(eval_gen) )
                setattr( subjet, 'tf_b_lost' ,
                    self.conf.tf_htt_matrix['b'][jet_eta_bin].Make_CDF() )
                setattr( subjet, 'tf_l_lost' ,
                    self.conf.tf_htt_matrix['l'][jet_eta_bin].Make_CDF() )

                # Set jet pt threshold for CDF
                subjet.tf_b_lost.SetParameter(0, self.conf.jets["pt"])
                subjet.tf_l_lost.SetParameter(0, self.conf.jets["pt"])

                #PRELIMINARY - Add jet_corr 
                subjet.corr = subjet.corr
                subjet.corr_JER = subjet.corr_JER

            # Create a pointer in the top to its subjets
            setattr( top, 'subjets', ts )
            self.Attach_Subjets_To_Objects(top,ts)

            top_subjets[alltops.index(top)] = ts

        return top_subjets

    # ==============================================================================
    # Attaches subjets to top / Higgs candidate (needed in different NanoAOD format)
    def Attach_Subjets_To_Objects( self, o, subjets ):
        for i in subjets:
            setattr(o,"{}pt".format(i.prefix),i.pt)
            setattr(o,"{}eta".format(i.prefix),i.eta)
            setattr(o,"{}phi".format(i.prefix),i.phi)
            setattr(o,"{}mass".format(i.prefix),i.mass)
            setattr(o,"{}btag".format(i.prefix),i.btag)
            setattr(o,"{}corr".format(i.prefix),i.corr)
            setattr(o,"{}corr_JER".format(i.prefix),i.corr_JER)
            for cor in self.conf.mem["factorized_sources"]:
                for di in ["Up","Down"]:
                    setattr(o,"{}pt_corr_{}{}".format(i.prefix,cor,di),getattr(i,"pt_corr_{}{}".format(cor,di)))

    # ==============================================================================
    # Calculates angular distance between two objects (needs eta and phi as attr.)
    def Get_DeltaR_two_objects(self, obj1, obj2):

        for obj in [obj1, obj2]:
            if not (hasattr(obj, 'phi') or hasattr(obj, 'eta')):
                print "Can't calculate Delta R: objects don't have right attributes"
                return 0

        pi = math.pi

        del_phi = abs(obj1.phi - obj2.phi)
        if del_phi > pi: del_phi = 2*pi - del_phi

        delR = pow(pow(obj1.eta-obj2.eta,2) + pow(del_phi,2) , 0.5)

        return delR

    # ==============================================================================
    # Simple algorithm that matches the smallest delta R for two lists of objects
    def Get_min_delR(self, objs1, objs2, R_cut = 'def'):

        # Use self.R_cut if R_cut is not specified
        if R_cut == 'def':
            R_cut = self.R_cut

        n_objs1 = len(objs1)
        n_objs2 = len(objs2)

        Rmat = [[self.Get_DeltaR_two_objects(objs1[i], objs2[j]) \
            for j in range(n_objs2)] for i in range(n_objs1)]

        Rmin = 9999.0
        
        for i in range(n_objs1):
            for j in range(n_objs2):
                if Rmat[i][j] < Rmin and Rmat[i][j] < R_cut:
                    Rmin = Rmat[i][j]
                    i_min = i
                    j_min = j

        if Rmin == 9999.0: return ('No link', 0, 0)

        return (i_min, j_min, Rmin)

    # ==============================================================================
    def Match_two_lists(self,
                         objs1_orig, label1,
                         objs2_orig, label2,
                         R_cut = 'def'):

        # Check if object is not a list; if so, convert it to a list
        # (This allows to conveniently pass single objects to the function as well)
        if hasattr(objs1_orig, 'eta') and hasattr(objs1_orig, 'phi'):
            objs1_orig = [objs1_orig]
        if hasattr(objs2_orig, 'eta') and hasattr(objs2_orig, 'phi'):
            objs2_orig = [objs2_orig]

        # Create list of indices
        objs1 = range(len(objs1_orig))
        objs2 = range(len(objs2_orig))
            
        # Attempt matching until the shortest list is depleted, or until there are
        # no more matches with delR < delR_cut
        n_matches = min(len(objs1), len(objs2))

        for i_match in range(n_matches):

            # Attempt a match (map indices to objects first)
            tmp1 = [objs1_orig[i] for i in objs1]
            tmp2 = [objs2_orig[i] for i in objs2]
            (i1, i2, delR) = self.Get_min_delR(tmp1, tmp2, R_cut)

            # Return the attempt number if no more matches could be made
            if i1 == 'No link':
                return i_match

            # Pop the matched indices from the lists for the next iteration
            matched_obj1 = objs1.pop(i1)
            matched_obj2 = objs2.pop(i2)

            # Record the match in the original objs
            setattr(objs1_orig[matched_obj1],
                    'matched_{0}'.format(label2),
                    objs2_orig[matched_obj2])

            setattr(objs2_orig[matched_obj2],
                    'matched_{0}'.format(label1),
                    objs1_orig[matched_obj1])

            # Record the delR value in the original objs
            setattr(objs1_orig[matched_obj1],
                    'matched_{0}_delR'.format(label2),
                    delR)

            setattr(objs2_orig[matched_obj2],
                    'matched_{0}_delR'.format(label1),
                    delR)
            
        return n_matches

    # ==============================================================================
    # Print exactly 1 particle

    def Print_one_obj( self, q, extra_attrs=[], tab=False ):

        pt = '{0:.2f}'.format(q.pt)
        eta = '{0:.2f}'.format(q.eta)
        phi = '{0:.2f}'.format(q.phi)
        mass = '{0:.2f}'.format(q.mass)

        p4_str = '    [ pt: {0:6s} | eta: {1:5s} | phi: {2:5s} | mass: {3:6s} '.format( pt, eta, phi, mass )
    
        for a in extra_attrs:
            if hasattr( q, a ):
                value = getattr(q,a)
                if isinstance( value, float ): value = '{0:.2f}'.format(value)
                p4_str += '| {0}: {1} '.format( a, value )

        p4_str += ']'

        if tab: p4_str = '    ' + p4_str
        print p4_str

    # ==============================================================================
    # Print object or list of objects
    def Print_objs( self, objs, extra_attrs=[], tab=False ):

        # Check if only 1 object was passed; if so, convert to list
        if ( hasattr( objs, 'pt' ) and hasattr( objs, 'eta' ) and
             hasattr( objs, 'phi' ) and hasattr( objs, 'mass' ) ):
            objs = [ objs ]
        
        for obj in objs: self.Print_one_obj( obj, extra_attrs, tab )


    # ==============================================================================
    # Get Lorentz Vector for systematic variation
    def lvsyst(self,obj,syst):

        lv = ROOT.TLorentzVector()
        if syst == "nominal":
            lv.SetPtEtaPhiM(obj.pt, obj.eta, obj.phi, obj.mass)
        else:
            #Reconstruct mass from correction factor
            corrfactor = getattr(obj,"pt_corr_{}".format(syst))/obj.pt
            masscor = obj.mass*corrfactor
            lv.SetPtEtaPhiM(getattr(obj,"pt_corr_{}".format(syst)), obj.eta, obj.phi, masscor)
        return lv


    # ==============================================================================
    # Deletes duplicate WZ Quarks
    def CompareWZQuarks(self, event ):

        if len(event.GenWZQuark) < 4:
            return 0

        quarks = event.GenWZQuark

        Is_Duplicate = ( quarks[-1].pt==quarks[1].pt and \
            quarks[-2].pt==quarks[0].pt )

        if Is_Duplicate:
            event.GenWZQuark = event.GenWZQuark[0:-2]

        return 0

    # ==============================================================================
    # Tag one of the bquarks as hadronic, based on mass difference with top
    def Tag_GenB_as_hadronic(self, event ):

        # Make list of TLorentzVector objects for the 2 light quarks
        tl_GenWZQuarks = []
        for l in event.GenWZQuark:
            tl_l = ROOT.TLorentzVector()
            tl_l.SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass )
            tl_GenWZQuarks.append( tl_l )

        tl_Combined = []
        for (b_i, b) in enumerate(event.GenBQuarkFromTop):
            tl_b = ROOT.TLorentzVector()
            tl_b.SetPtEtaPhiM( b.pt, b.eta, b.phi, b.mass )
            tl_Combined.append( tl_b + tl_GenWZQuarks[0] + tl_GenWZQuarks[1] )

        # Calculate mass difference from top mass
        delmass0 = abs(tl_Combined[0].M() - self.top_mass)
        delmass1 = abs(tl_Combined[1].M() - self.top_mass)

        # Make sure the B quark with lowest del mass to top mass is at index 0
        if delmass0 < delmass1:
            setattr( event.GenBQuarkFromTop[0], 'is_hadr', 1 )
            setattr( event.GenBQuarkFromTop[1], 'is_hadr', 0 )
        else:
            setattr( event.GenBQuarkFromTop[1], 'is_hadr', 1 )
            setattr( event.GenBQuarkFromTop[0], 'is_hadr', 0 )

        event.GenBQuarkFromTop = sorted( event.GenBQuarkFromTop,
                                         key=lambda x: -x.is_hadr )

    # ==============================================================================
    # Writes matching statistics to event for matching (sub)jets to quarks
    def Do_Quark_Matching(self, event):

        # Necessary to remove duplicates in GenWZQuark branch
        # This step can be removed for V12 samples <---- Check it
        # self.CompareWZQuarks( event )

        # Check if event contains the right number of quarks
        # (Only used to do truth-level comparisons)
        genquarks_top_present = False
        if len(event.GenWZQuark)==2 and len(event.GenBQuarkFromTop)==2:
            genquarks_top_present = True
       
      
            
        genquarks_higgs_present = False
        if len(event.GenBQuarkFromH)==2:
            genquarks_higgs_present = True

      

        # Convenient list names
        if genquarks_top_present:
            # Sorts event.GenBQuarkFromTop
            self.Tag_GenB_as_hadronic(event)
            # Get the hadronic & leptonic b-quark and the two light quarks
            hadr_bquark = event.GenBQuarkFromTop[0]
            lept_bquark = event.GenBQuarkFromTop[1]
            lquarks = event.GenWZQuark
        if genquarks_higgs_present:
            higgs_bquarks = event.GenBQuarkFromH

        reco_btagged_jets = event.selected_btagged_jets_high
        reco_ltagged_jets = list( event.wquark_candidate_jets )

        top = event.topCandidate[0]
        other_tops = event.othertopCandidate


        # Quark matching
        # ==============

        # Quark matching is only done to compare events to truth level.
        # Events are not selected based on successful quark matching.
        # This entire part can be commented out if so desired.

        # Matching GenBQuarkFromTop and GenWZQuark
        if genquarks_top_present:

            # To reco_btagged_jets
            n_hadr_bquark_matched_to_bjet = self.Match_two_lists(
                hadr_bquark, 'hadr_bquark',
                reco_btagged_jets, 'bjet' )

            n_lept_bquark_matched_to_bjet = self.Match_two_lists(
                lept_bquark, 'lept_bquark',
                reco_btagged_jets, 'bjet' )

            n_lquarks_matched_to_bjet = self.Match_two_lists(
                lquarks, 'lquark',
                reco_btagged_jets, 'bjet' )

            # To reco_ltagged_jets
            n_hadr_bquark_matched_to_ljet = self.Match_two_lists(
                hadr_bquark, 'hadr_bquark',
                reco_ltagged_jets, 'ljet' )

            n_lept_bquark_matched_to_ljet = self.Match_two_lists(
                lept_bquark, 'lept_bquark',
                reco_ltagged_jets, 'ljet' )

            n_lquarks_matched_to_ljet = self.Match_two_lists(
                lquarks, 'lquark',
                reco_ltagged_jets, 'ljet' )

            # To subjets from chosen top
            n_hadr_bquark_matched_to_top_subjet = self.Match_two_lists(
                hadr_bquark, 'hadr_bquark',
                top.subjets, 'top_subjet' )

            n_lept_bquark_matched_to_top_subjet = self.Match_two_lists(
                lept_bquark, 'lept_bquark',
                top.subjets, 'top_subjet' )

            n_lquarks_matched_to_top_subjet = self.Match_two_lists(
                lquarks, 'lquark',
                top.subjets, 'top_subjet' )

            # To subjets from other top
            if len(other_tops) == 0:
                n_hadr_bquark_matched_to_otop_subjet = -1
                n_lept_bquark_matched_to_otop_subjet = -1
                n_lquarks_matched_to_otop_subjet = -1
            else:
                n_hadr_bquark_matched_to_otop_subjet = 0
                n_lept_bquark_matched_to_otop_subjet = 0
                n_lquarks_matched_to_otop_subjet = 0
                for top in other_tops:

                    n_hadr_bquark_matched_to_otop_subjet += self.Match_two_lists(
                        hadr_bquark, 'hadr_bquark',
                        top.subjets, 'other_top_subjet' )

                    n_lept_bquark_matched_to_otop_subjet += self.Match_two_lists(
                        lept_bquark, 'lept_bquark',
                        top.subjets, 'other_top_subjet' )

                    n_lquarks_matched_to_otop_subjet += self.Match_two_lists(
                        lquarks, 'lquark',
                        top.subjets, 'other_top_subjet' )


        if genquarks_higgs_present:

            # To reco_btagged_jets
            n_higgs_bquarks_matched_to_bjet = self.Match_two_lists(
                higgs_bquarks, 'higgs_bquark',
                reco_btagged_jets, 'bjet' )

            # To reco_ltagged_jets
            n_higgs_bquarks_matched_to_ljet = self.Match_two_lists(
                higgs_bquarks, 'higgs_bquark',
                reco_ltagged_jets, 'ljet' )

            # To subjets from chosen top
            n_higgs_bquarks_matched_to_top_subjet = self.Match_two_lists(
                higgs_bquarks, 'higgs_bquark',
                top.subjets, 'top_subjet' )

            # To subjets from other top
            if len(other_tops) == 0:
                n_higgs_bquarks_matched_to_otop_subjet = -1
            else:
                n_higgs_bquarks_matched_to_otop_subjet = 0
                for top in other_tops:
                    n_higgs_bquarks_matched_to_otop_subjet += self.Match_two_lists(
                        higgs_bquarks, 'higgs_bquark',
                        top.subjets, 'other_top_subjet' )


        # Write to event
        # ==============

        setattr( event, 'QMatching_t_attempted', genquarks_top_present )
        setattr( event, 'QMatching_H_attempted', genquarks_higgs_present )

        if genquarks_top_present:

            event.QMatching_n_hadr_bquark_matched_to_bjet = \
                n_hadr_bquark_matched_to_bjet
            event.QMatching_n_lept_bquark_matched_to_bjet = \
                n_lept_bquark_matched_to_bjet
            event.QMatching_n_lquarks_matched_to_bjet = \
                n_lquarks_matched_to_bjet

            event.QMatching_n_hadr_bquark_matched_to_ljet = \
                n_hadr_bquark_matched_to_ljet
            event.QMatching_n_lept_bquark_matched_to_ljet = \
                n_lept_bquark_matched_to_ljet
            event.QMatching_n_lquarks_matched_to_ljet = \
                n_lquarks_matched_to_ljet

            event.QMatching_n_hadr_bquark_matched_to_top_subjet = \
                n_hadr_bquark_matched_to_top_subjet
            event.QMatching_n_lept_bquark_matched_to_top_subjet = \
                n_lept_bquark_matched_to_top_subjet
            event.QMatching_n_lquarks_matched_to_top_subjet = \
                n_lquarks_matched_to_top_subjet

            event.QMatching_n_hadr_bquark_matched_to_otop_subjet = \
                n_hadr_bquark_matched_to_otop_subjet
            event.QMatching_n_lept_bquark_matched_to_otop_subjet = \
                n_lept_bquark_matched_to_otop_subjet
            event.QMatching_n_lquarks_matched_to_otop_subjet = \
                n_lquarks_matched_to_otop_subjet

        if genquarks_higgs_present:

            event.QMatching_n_higgs_bquarks_matched_to_bjet = \
                n_higgs_bquarks_matched_to_bjet
            event.QMatching_n_higgs_bquarks_matched_to_ljet = \
                n_higgs_bquarks_matched_to_ljet
            event.QMatching_n_higgs_bquarks_matched_to_top_subjet = \
                n_higgs_bquarks_matched_to_top_subjet
            event.QMatching_n_higgs_bquarks_matched_to_otop_subjet = \
                n_higgs_bquarks_matched_to_otop_subjet

    # ==============================================================================
    # Writes matching statistics to event for matching (sub)jets to quarks
    def Do_GenTop_Matching(self, event, topsubjets):
      
        gentops = []
        for l in event.GenTop:
            if l.pt>self.GenTop_pt_cut:
                gentops.append(l)

        # Loosely match the top candidate to the gen tops
        n_matched_gentop = self.Match_two_lists(
            event.topCandidate, 'topcand',
            gentops, 'gentop',
            R_cut = self.R_cut_fatjets)

        for l in gentops:
            if hasattr(l, 'matched_topcand'):
                event.matched_TTgentop_pt= l.pt
        
        event.n_matched_TTgentop = n_matched_gentop
        

        #if there is a match: try to match also the subjets
        if (n_matched_gentop>0):
            
            top_subjets = self.Get_Subjets_Top([event.topCandidate[0]],topsubjets)
            top_subjets_b = []
            top_subjets_W = []
            for s in top_subjets[0]:
                if s.btagFlag == 1.0: 
                    top_subjets_b.append(s)
                else:
                    top_subjets_W.append(s)
                
            
            # match the b subjet to GenBQuarkFromTop
            n_matched_genb = self.Match_two_lists(
                top_subjets_b, 'top_subjet_b',
                event.GenBQuarkFromTop, 'genb',
                R_cut = self.R_cut )

            # match the W subjets to GenWZQuark
            n_matched_genW = self.Match_two_lists(
                top_subjets_W, 'top_subjet_W',
                event.GenWZQuark, 'genW',
                R_cut = self.R_cut )

            event.n_matched_TTgenb = n_matched_genb
            event.n_matched_TTgenW = n_matched_genW
                        
#==========================END OF SUBJET ANALYZER==========================#
