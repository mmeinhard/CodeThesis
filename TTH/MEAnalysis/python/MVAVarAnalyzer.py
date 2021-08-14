from TTH.MEAnalysis.vhbb_utils import lvec
import copy
import numpy as np

import math
import scipy
import scipy.special
from scipy.special import eval_legendre

#for some reason, root imports need to be after scipy
import ROOT
ROOT.gSystem.Load("libTTHMEAnalysis")

mva_enabled = False
from TTH.MEAnalysis.Analyzer import FilterAnalyzer
if mva_enabled:
    try:
        from sklearn.externals import joblib
    except Exception as e:
        print "Could not load scikit-learn. Please configure PYTHONPATH=/path/to/anaconda/lib/python2.7/site-packages:$PYTHONPATH PATH=/path/to/anaconda/bin/:$PATH"
        mva_enabled = False

CvectorTLorentzVector = getattr(ROOT, "std::vector<TLorentzVector>")
EventShapeVariables = getattr(ROOT, "EventShapeVariables")
TMatrixDSym = getattr(ROOT, "TMatrixDSym")
TMatrixDSymEigen = getattr(ROOT, "TMatrixDSymEigen")

class FoxWolfram:

    @staticmethod
    def w_s(objs, lv1, lv2):
        return (lv1.Vect().Mag() * lv2.Vect().Mag()) / (sum(objs, ROOT.TLorentzVector())).Mag2()

    @staticmethod
    def calcFoxWolfram(objects, orders, weight_func):
        """
        http://arxiv.org/pdf/1212.4436v1.pdf
        """
        lvecs = [lvec(o) for o in objects]

        h = np.zeros(len(orders))
        for i in range(len(lvecs)):
            for j in range(len(lvecs)):
                cos_omega_ij = (lvecs[i].CosTheta() * lvecs[j].CosTheta() +
                    math.sqrt((1.0 - lvecs[i].CosTheta()**2) * (1.0 - lvecs[j].CosTheta()**2)) *
                    (math.cos(lvecs[i].Phi() - lvecs[j].Phi()))
                )
                w_ij = weight_func(lvecs, lvecs[i], lvecs[j])
                vals = np.array([cos_omega_ij]*len(orders))

                p_l = np.array(eval_legendre(orders, vals))
                h += w_ij * p_l
        return h

class MVAVarAnalyzer(FilterAnalyzer):
    """
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MVAVarAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        if mva_enabled:
            self.cls = joblib.load(self.conf.tth_mva["filename"])

    def beginLoop(self, setup):
        super(MVAVarAnalyzer, self).beginLoop(setup)

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            #vector variables must always be present!
            setattr(event_syst, 'Detaj', [])
            #print syst, event_syst.__dict__
            if event_syst.passes_btag:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mva = False
        return self.conf.general["passall"] or np.any([v.passes_mva for v in event.systResults.values()])

    def _process(self, event):
        #FIXME: NEED COMMENTS HERE
        sumP2 = 0.0
        sumPxx = 0.0
        sumPxy = 0.0
        sumPxz = 0.0
        sumPyy = 0.0
        sumPyz = 0.0
        sumPzz = 0.0
        vecs = CvectorTLorentzVector()
        lvtot = ROOT.TLorentzVector()
        for jet in event.good_jets:
            obj = lvec(jet)
            lvtot += obj
            vecs.push_back(lvec(jet))
            sumP2  += obj.P() * obj.P()
            sumPxx += obj.Px() * obj.Px()
            sumPxy += obj.Px() * obj.Py()
            sumPxz += obj.Px() * obj.Pz()
            sumPyy += obj.Py() * obj.Py()
            sumPyz += obj.Py() * obj.Pz()
            sumPzz += obj.Pz() * obj.Pz()
        evshape = EventShapeVariables(vecs)
        eigs = evshape.compEigenValues(2.0) #difference: this takes T^2-x^2-y^2-z^2 for P2
        event.momentum_eig0 = eigs[0]
        event.momentum_eig1 = eigs[1]
        event.momentum_eig2 = eigs[2]

        event.isotropy = evshape.isotropy()
        event.invmass = lvtot.M()
        event.centralitymass = -99.0 if event.invmass<=0 else (event.ht / event.invmass)


        
        ##---- compute sphericity --------------------#DS
        if sumP2 > 0:
            Txx = sumPxx/sumP2
            Tyy = sumPyy/sumP2
            Tzz = sumPzz/sumP2
            Txy = sumPxy/sumP2
            Txz = sumPxz/sumP2
            Tyz = sumPyz/sumP2
            T = TMatrixDSym(3)
            T[0,0] = Txx
            T[0,1] = Txy
            T[0,2] = Txz
            T[1,0] = Txy
            T[1,1] = Tyy
            T[1,2] = Tyz
            T[2,0] = Txz
            T[2,1] = Tyz
            T[2,2] = Tzz
            TEigen = TMatrixDSymEigen(T)
            eigenValues = TEigen.GetEigenValues()
            event.sphericity = 1.5*(eigenValues(1)+eigenValues(2))
            event.aplanarity = 1.5*eigenValues(2)
            event.C = 3.0*(eigenValues(0)*eigenValues(1) + eigenValues(0)*eigenValues(2) + eigenValues(1)*eigenValues(2))
            event.D = 27.*eigenValues(0)*eigenValues(1)*eigenValues(2) #---------DS 

            event.isotropy = evshape.isotropy()
            event.sphericity = 1.5*(eigs[1]+eigs[2]) #evshape.sphericity(eigs) #DS
            event.aplanarity = 1.5*eigs[2] #evshape.aplanarity(eigs) #DS
            event.C = 3.0*(eigs[0]*eigs[1] + eigs[0]*eigs[2] + eigs[1]*eigs[2]) #evshape.C(eigs) #DS
            event.D = 27.*eigs[0]*eigs[1]*eigs[2] #evshape.D(eigs) #DS
        else:
            event.sphericity = -99.0
            event.aplanarity = -99.0
            event.C = -99.0
            event.D = -99.0

            event.isotropy = -99.0
            event.sphericity = -99.0
            event.aplanarity = -99.0
            event.C = -99.0
            event.D = -99.0
            
        event.mean_bdisc = np.mean([j.btagCSV for j in event.good_jets])
        event.mean_bdisc_btag = np.mean([j.btagCSV for j in event.selected_btagged_jets_high])
        event.std_bdisc = np.std([j.btagCSV for j in event.good_jets])
        event.std_bdisc_btag = np.std([j.btagCSV for j in event.selected_btagged_jets_high])
        drs = []
        hmass = -99.0
        bigHmass = 9999.0
        for j1 in event.selected_btagged_jets_high:
            for j2 in event.selected_btagged_jets_high:
                if j1==j2:
                    continue
                l1 = lvec(j1)
                l2 = lvec(j2)
                drs += [(l1.DeltaR(l2), l1, l2)]
                mass = (l1+l2).M()
                if abs(mass-125.0)<bigHmass:
                    bigHmass = abs(mass-125.0)
                    hmass = mass

        drs = sorted(drs, key=lambda x: x[0])
        if len(drs)>0:
            lv = drs[0][1] + drs[0][2]
            event.mass_drpair_btag = lv.M()
            event.eta_drpair_btag = abs(lv.Eta())
            event.pt_drpair_btag = lv.Pt()
            event.min_dr_btag = drs[0][0]
            event.mean_dr_btag = np.mean([dr[0] for dr in drs], -1)
            event.std_dr_btag = np.std([dr[0] for dr in drs], -1)
        else:
            event.min_dr_btag = -1.0
            event.mean_dr_btag = -1.0
            event.std_dr_btag = -1.0
            event.mass_drpair_btag = -1.0
            event.eta_drpair_btag = -99
            event.pt_drpair_btag = -1.0
        event.hmass = hmass
        
        #light jet variables for background validation
        bigWmass = 9999.0
        bigQdr = 9999.0
        drqq = -99.0
        mqq = -99.0
        wmass = -99.0
        ljets = sorted(event.buntagged_jets+event.selected_btagged_jets_low, key=lambda x: x.pt, reverse=True)
        light_jets = ljets[0:5] #at most 5 lquarks considered for MEM    
        for j1 in light_jets:
            for j2 in light_jets:
                if j1==j2:
                    continue
                l1 = lvec(j1)
                l2 = lvec(j2)
                dr = l1.DeltaR(l2)
                mass = (l1+l2).M()
                if abs(mass-80.4)<bigWmass:
                    bigWmass = abs(mass-80.4)
                    wmass = mass
                if dr<bigQdr:
                    bigQdr = dr
                    drqq = dr
                    mqq = mass
        event.min_dr_untag = drqq
        event.mass_drpair_untag = mqq
        event.wmass = wmass

        #all jet variables
        bigJmass = 9999.0
        mjjmin = -99.0
        njets = len(event.good_jets)
        Detaj = [0.0 for x in range(njets)]
        for j1 in event.good_jets:
            detamin = [99 for x in range(njets-1)]
            for j2 in event.good_jets:
                if j1==j2:
                    continue
                #calculate minimum dijet mass
                l1 = lvec(j1)
                l2 = lvec(j2)
                mass = (l1+l2).M()
                if mass<bigJmass:
                    bigJmass = mass
                    mjjmin = mass
                #calcualte delta Eta variables
                deta = abs(j1.eta - j2.eta)
                for x in range(njets-1):
                    if deta < detamin[x]:
                        for k in range((njets-2),(x-1),-1):
                            if k==x:
                                detamin[k] = deta
                            else:
                                detamin[k] = detamin[k-1]
                        break
            for k in range(njets-1):
                Detaj[k] += detamin[k]
        for k in range(njets-1):
            Detaj[k] = Detaj[k] / njets
        event.Detaj = Detaj
        event.mjjmin = mjjmin

        #csv rank variables (nominal only)
        if event.systematic=="nominal":
            for i in range(njets):
                maxCSV = -99.0
                maxjet = -99
                for j in range(njets):
                    if hasattr(event.good_jets[j], "CSVrank"):
                        continue
                    if event.good_jets[j].btagCSV>maxCSV:
                        maxCSV = event.good_jets[j].btagCSV
                        maxjet = j
                if maxjet >= njets:
                    print "maxjet={0} njets={1} j={2}".format(maxjet, njets, j)
                if hasattr(event.good_jets[i], "CSVindex"):
                    jet = event.good_jets[i]
                    print "jet already has CSVindex: njets={0} i={1} pt={2} eta={3} csv={4} maxCSV={5} maxjet={6} rank={7} index={8} syst={9}".format(njets, i, jet.pt, jet.eta, jet.btagCSV, maxCSV, maxjet, jet.CSVrank, jet.CSVindex, event.systematic )
                elif maxjet > -1:
                    event.good_jets[maxjet].CSVrank = i
                    event.good_jets[i].CSVindex = maxjet
                else:
                    jet = event.good_jets[i]
                    print "jet has no CSVindex: njets={0} i={1} pt={2} eta={3} csv={4} maxCSV={5} maxjet={6} rank={7} syst={8}".format(njets, i, jet.pt, jet.eta, jet.btagCSV, maxCSV, maxjet, jet.CSVrank, event.systematic )
            #if event.good_jets[1].CSVindex >= njets: #testing
            #    print "maxjet={0}".format(maxjet)
            #    for i in range(njets):
            #        print "jets_CSVindex[{2}]={0} njets={1}".format(event.good_jets[i].CSVindex, njets, i)
            if njets > 1:
                lv0 = lvec(event.good_jets[event.good_jets[0].CSVindex])
                lv1 = lvec(event.good_jets[event.good_jets[1].CSVindex])
                for i in range(njets):
                    lv = lvec(event.good_jets[i])
                    dr0 = lv.DeltaR(lv0)
                    dr1 = lv.DeltaR(lv1)
                    event.good_jets[i].dRmax = max(dr0,dr1)
                    event.good_jets[i].dRmin = min(dr0,dr1)
                    event.good_jets[i].dRave = 0.5*(dr0+dr1)
            else:
                for i in range(njets):
                    event.good_jets[i].dRmax = -99
                    event.good_jets[i].dRmin = -99
                    event.good_jets[i].dRave = -99



            
        for i in range(min(4, len(event.selected_btagged_jets_high))):
            setattr(event, "jet_btag_{0}".format(i), event.selected_btagged_jets_high[i])

        lvecs = [lvec(x) for x in event.good_jets + event.good_leptons]
        if len(lvecs) != 0:
            event.centrality = np.sum([l.Pt() for l in lvecs])/np.sum([l.E() for l in lvecs])
        else: event.centrality = -999

        #orders of momenta to calculate
        orders = np.array([0, 1, 2, 3, 4, 5, 6, 7])
        event.fw_h_alljets = FoxWolfram.calcFoxWolfram(event.good_jets, orders, FoxWolfram.w_s)
        event.fw_h_btagjets = FoxWolfram.calcFoxWolfram(event.selected_btagged_jets_high, orders, FoxWolfram.w_s)
        event.fw_h_untagjets = FoxWolfram.calcFoxWolfram(event.buntagged_jets, orders, FoxWolfram.w_s)
        
        for ij in range(6):
            setattr(event, "jet{0}_pt".format(ij), 0)
            setattr(event, "jet{0}_aeta".format(ij), 0)
            setattr(event, "jet{0}_btag".format(ij), 0)

        for ij, jet in enumerate(event.good_jets):
            setattr(event, "jet{0}_pt".format(ij), jet.pt)
            setattr(event, "jet{0}_aeta".format(ij), abs(jet.eta))
            setattr(event, "jet{0}_btag".format(ij), jet.btagCSV)
       
        for i in range(2):
            setattr(event, "lep{0}_pt".format(i), 0.0)
            setattr(event, "lep{0}_aeta".format(i), 0.0)

        for ij, lep in enumerate(event.good_leptons):
            setattr(event, "lep{0}_pt".format(ij), lep.pt)
            setattr(event, "lep{0}_aeta".format(ij), abs(lep.eta))
        
        for io in orders:
            setattr(event, "fw_h{0}".format(io), event.fw_h_alljets[io])
        
        #vararray = np.array([getattr(event, vname) for vname in self.conf.tth_mva["varlist"]])
        #vararray[np.isnan(vararray)] = 0
        
        event.tth_mva = 0
        if mva_enabled:
            event.tth_mva = self.cls.predict_proba(vararray)[0,1]
        event.passes_mva = True

        return event
