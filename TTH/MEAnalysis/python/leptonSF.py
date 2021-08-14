import ROOT, os, sys
ROOT.gSystem.Load("libTTHMEAnalysis")
import ROOT.TTH_MEAnalysis
dummy = ROOT.TTH_MEAnalysis.TreeDescription
import logging
LOG_MODULE_NAME = logging.getLogger("leptonSF")

tfile_ele_trig = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/SingleEG_JetHT_Trigger_Scale_Factors_ttHbb_Data_MC_v5.root")
hist_ele_trig = tfile_ele_trig.Get("SFs_ele_pt_ele_sceta_ele28_ht150_OR_ele35_2017BCDEF")

def calcTriggerSF_el(pt, eta, hist=hist_ele_trig):
    if pt < 25:
        pt = 25
    if pt > 500:
        pt = 499
    b = hist.FindBin(pt, eta)
    w = hist.GetBinContent(b)
    #print "trigger el", w
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("el trig sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_ll_trig = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/tth_dileptonic_2DscaleFactors_withSysts_2017BCDEF_18-08-19.root")
hist_ee_trig = tfile_ll_trig.Get("h_DoubleEl_OR__X__allMET_el0_pt_vs_el1_pt_withSysts")
hist_em_trig = tfile_ll_trig.Get("h_EMu_OR__X__allMET_mu0_pt_vs_el0_pt_withSysts")
hist_mm_trig = tfile_ll_trig.Get("h_DoubleMu_OR__X__allMET_mu0_pt_vs_mu1_pt_withSysts") 

def calcDileptonSF(pt1, pt2, hist):
    b = hist.FindBin(pt1, pt2)
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    return w, wup, wdown

def calcTriggerSF_dilepton(pt1, pt2, pdgId1, pdgId2, hlt_ee, hlt_em, hlt_mm):
    if hlt_ee:
        if pt1 < 30:
            pt1 = 31
        if pt1 > 200:
            pt1 = 199
        if pt2 < 20:
            pt2 = 21
        if pt2 > 200:
            pt2 = 199
        return calcDileptonSF(pt1, pt2, hist_ee_trig)
    elif hlt_em:
        if abs(pdgId2) == 13 and abs(pdgId1) == 11:
            ptmuon = pt2
            ptelectron = pt1
        else:
            ptmuon = pt1
            ptelectron = pt2
        if ptmuon < 20:
            ptmuon = 21
        if ptmuon > 200:
            ptmuon = 199
        if ptelectron < 20:
            ptelectron = 21
        if ptelectron > 200:
            ptelectron = 199
        return calcDileptonSF(ptmuon, ptelectron, hist_em_trig)
    elif hlt_mm:
        if pt1 < 30:
            pt1 = 31
        if pt1 > 200:
            pt1 = 199
        if pt2 < 20:
            pt2 = 21
        if pt2 > 200:
            pt2 = 199
        return calcDileptonSF(pt1, pt2, hist_mm_trig)
    else:
        return (1.0, 1.0, 1.0)

tfile_ele_id = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/2017_ElectronTight.root")
hist_ele_id = tfile_ele_id.Get("EGamma_SF2D")

def calcIDSF_el(pt, eta, hist=hist_ele_id):
    if pt > 500:
        pt = 499
    b = hist.FindBin(eta, pt)
    w = hist.GetBinContent(b)
    #print "id e", w
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("el ID sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_ele_reco = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/egammaEffi_EGM2D_runBCDEF_passingRECO_v2.root")
hist_ele_reco = tfile_ele_reco.Get("EGamma_SF2D")
def calcRecoSF_el(pt, eta, hist=hist_ele_reco):
    if pt < 25:
        pt = 25
    if pt > 500:
        pt = 499
    b = hist.FindBin(eta, pt)
    w = hist.GetBinContent(b)
    #print "reco el", w
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("el reco sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

#https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults#Results_on_the_full_2016_data
tfile_mu_trig1 = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root")
hist_mu_trig1 = tfile_mu_trig1.Get("IsoMu27_PtEtaBins/pt_abseta_ratio")

def calcTriggerSF_mu(pt, eta, hist=hist_mu_trig1):
    if pt < 2:
        pt = 2.1
    if pt > 1200:
        pt = 1199
    b = hist.FindBin(pt, abs(eta))
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("mu trig sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_mu_id = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/RunBCDEF_SF_ID.root")
hist_mu_id = tfile_mu_id.Get("NUM_TightID_DEN_genTracks_pt_abseta")

def calcIDSF_mu(pt, eta, hist=hist_mu_id):
    if pt < 26:
        pt = 26
    if pt > 120:
        pt = 119
    b = hist.FindBin(pt, abs(eta))
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("mu ID sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

tfile_mu_iso = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/RunBCDEF_SF_ISO.root")
hist_mu_iso = tfile_mu_iso.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")
hist_mu_iso_loose = tfile_mu_iso.Get("NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta")

def calcIsoSF_mu(pt, eta, hist=hist_mu_iso):
    if pt < 26:
        pt = 26
    if pt > 120:
        pt = 119
    b = hist.FindBin(pt, abs(eta))
    w = hist.GetBinContent(b)
    wup = hist.GetBinContent(b) + hist.GetBinError(b)
    wdown = hist.GetBinContent(b) - hist.GetBinError(b)
    LOG_MODULE_NAME.debug("mu iso sf pt={0} eta={1} w={2} wup={3} wdown={4}".format(pt, eta, w, wup, wdown))
    return w, wup, wdown

# Mu tracking SF is 1 in 2017
#tfile_mu_track = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/sf/mu_tracking_bcdef.root")
#hist_mu_track = tfile_mu_track.Get("ratio_eff_aeta_dr030e030_corr")

# helper function to find the first occurance of a point whose x-error bars cover a certain value
def findGraphPoint(tgraph, x):
    x_, y_ = ROOT.Double(), ROOT.Double()
    for i in range(0, tgraph.GetN()):
        tgraph.GetPoint(i, x_, y_)
        # use same edge treatment as root histograms use, so inclusive at the left edge
        # and exclusive at the right edge
        l, r = x_ - tgraph.GetErrorXlow(i), x_ + tgraph.GetErrorXhigh(i)
        if float(l) <= x < float(r):
            return i
    return -1

# helper function to get the y-value of a point defined by it's x-value with optional error handling
def getGraphValue(tgraph, x, err="nominal"):
    assert(err in ("nominal", "up", "down"))

    i = findGraphPoint(tgraph, x)
    if i < 0:
        raise Exception("x-value %f cannot be assigned to a valid point" % x)

    x_, y_ = ROOT.Double(), ROOT.Double()
    tgraph.GetPoint(i, x_, y_)
    y = float(y_)

    if err == "up":
        return y + tgraph.GetErrorYhigh(i)
    elif err == "down":
        return y - tgraph.GetErrorYlow(i)
    else:
        return y

def calc_lepton_SF_mu(ev, syst="nominal"):
   
    ilep = 0
    pt = ev.leptons.at(ilep).lv.Pt()
    aeta = abs(ev.leptons.at(ilep).lv.Eta())

    w = 1.0
    weights_trigger = calcTriggerSF_mu(pt, aeta)
    if syst == "CMS_effTrigger_mUp":
        w *= weights_trigger[1]
    elif syst == "CMS_effTrigger_mDown":
        w *= weights_trigger[2]
    else:
        w *= weights_trigger[0]
        #print "Muon_triggerw", weights_trigger[0]

    weights_id = calcIDSF_mu(pt, aeta)
    weights_iso = calcIsoSF_mu(pt, aeta)

    if syst == "CMS_eff_mUp":
        w *= weights_id[1] * weights_iso[1]
    elif syst == "CMS_eff_mDown":
        w *= weights_id[2] * weights_iso[2]
    else:
        w *= weights_id[0] * weights_iso[0]
        #print "Muon_ id, iso", weights_id[0],  weights_iso[0]


    return w

def calc_lepton_SF_el(ev, syst="nominal"):
   
    ilep = 0
    pt = ev.leptons.at(ilep).lv.Pt()
    eta = ev.leps_superclustereta.at(ilep)

    w = 1.0
    weights_trigger = calcTriggerSF_el(pt, eta)
    if syst == "CMS_effTrigger_eUp":
        w *= weights_trigger[1]
    elif syst == "CMS_effTrigger_eDown":
        w *= weights_trigger[2]
    else:
        w *= weights_trigger[0]

    weights_id = calcIDSF_el(pt, eta)
    weights_reco = calcRecoSF_el(pt, eta)

    if syst == "CMS_eff_eUp":
        w *= weights_id[1] * weights_reco[1]
    elif syst == "CMS_eff_eDown":
        w *= weights_id[2] * weights_reco[2]
    else:
        w *= weights_id[0] * weights_reco[0]

    return w

def calc_lepton_SF_dilepton(event, syst="nominal"):
    w = 1.0
    
    weights_trigger = calcTriggerSF_dilepton(
        abs(event.leptons.at(0).lv.Pt()),
        abs(event.leptons.at(1).lv.Pt()),
        abs(event.leptons.at(0).pdgId),
        abs(event.leptons.at(1).pdgId),
        event.HLT_ttH_DL_elel,
        event.HLT_ttH_DL_elmu,
        event.HLT_ttH_DL_mumu
    )

    if event.HLT_ttH_DL_elel or event.HLT_ttH_DL_elmu or event.HLT_ttH_DL_mumu:
        if syst == "CMS_effTrigger_dlUp":
            w *= weights_trigger[1]
        elif syst == "CMS_effTrigger_dlDown":
            w *= weights_trigger[2]
        else:
            w *= weights_trigger[0]
    else:
        w *= weights_trigger[0]
    
    for ilep in range(2):
        pt = event.leptons.at(ilep).lv.Pt()
        if abs(event.leps_pdgId[ilep]) == 11:
            eta = event.leps_superclustereta.at(ilep)
            weights_id = calcIDSF_el(pt, eta)
            weights_reco = calcRecoSF_el(pt, eta)
            if syst == "CMS_eff_eUp":
                w *= weights_id[1] * weights_reco[1]
            elif syst == "CMS_eff_eDown":
                w *= weights_id[2] * weights_reco[2]
            else:
                w *= weights_id[0] * weights_reco[0]


        elif abs(event.leps_pdgId[ilep]) == 13:
            aeta = abs(event.leptons.at(ilep).lv.Eta())
            weights_id = calcIDSF_mu(pt, aeta)
            weights_iso = calcIsoSF_mu(pt, aeta, hist_mu_iso_loose)
            if syst == "CMS_eff_mUp":
                w *= weights_id[1] * weights_iso[1]
            elif syst == "CMS_eff_mDown":
                w *= weights_id[2] * weights_iso[2]
            else:
                w *= weights_id[0] * weights_iso[0]

    return w

def calc_lepton_SF(event, syst="nominal"):
    if event.is_sl:
        if abs(event.leps_pdgId[0]) == 13:
            w = calc_lepton_SF_mu(event, syst)
        elif abs(event.leps_pdgId[0]) == 11:
            w = calc_lepton_SF_el(event, syst)
    elif event.is_dl:
        w = calc_lepton_SF_dilepton(event, syst)
    #print syst, w
    return w

from PhysicsTools.HeppyCore.statistics.tree import Tree
if __name__ == "__main__":
    dummy = ROOT.TTH_MEAnalysis.TreeDescription
    
    tf = ROOT.TFile.Open(sys.argv[1])
    events = ROOT.TTH_MEAnalysis.TreeDescriptionMCFloat(
        tf,
        ROOT.TTH_MEAnalysis.SampleDescription(
            ROOT.TTH_MEAnalysis.SampleDescription.MC
        )
    )
    nom = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.Nominal, ROOT.TTH_MEAnalysis.Systematic.None)
   
    
    outfile = ROOT.TFile('out.root', 'recreate')
    tree = Tree('tree', 'MEM tree')
    tree.var('is_sl', the_type=int)
    tree.var('is_dl', the_type=int)
    tree.var('numJets', the_type=int)
    #tree.var('nBCSVM', the_type=int)
    tree.var('lep0_pdgId', the_type=int)
    tree.var('lep1_pdgId', the_type=int)
    tree.var('lep0_pt', the_type=float)
    tree.var('lep1_pt', the_type=float)
    tree.var('lep_trigger', the_type=float)
    tree.var('lep_id', the_type=float)
    tree.var('lep_track', the_type=float)
    tree.var('lep_iso', the_type=float)
    tree.var('lep_reco', the_type=float)
    
    iEv = 0
    systs = [
        "nominal",
        "CMS_effTrigger_eUp",
        "CMS_effTrigger_mUp",
        #"CMS_effTrigger_eeUp",
        #"CMS_effTrigger_emUp",
        #"CMS_effTrigger_mmUp",
        "CMS_effTrigger_dlUp",

        #CMS_effID_eUp",
        #CMS_effReco_eUp",
        "CMS_eff_eUp",
        

        #"CMS_effID_mUp",
        #"CMS_effIso_mUp",
        #"CMS_effTracking_mUp",
        "CMS_eff_mUp",
        
        "CMS_effTrigger_eDown",
        "CMS_effTrigger_mDown",
        #"CMS_effTrigger_eeDown",
        #"CMS_effTrigger_emDown",
        #"CMS_effTrigger_mmDown",
        "CMS_effTrigger_dlDown",

        #"CMS_effID_eDown",
        #"CMS_effReco_eDown",
        "CMS_eff_eDown",

        #"CMS_effID_mDown",
        #"CMS_effIso_mDown",
        #"CMS_effTracking_mDown",
        "CMS_eff_eDown",
    ]

    for syst in systs:
        tree.var('lep_weight_'+syst, the_type=float)

    while events.reader.Next():
        print iEv
        event = events.create_event(nom)
        event.leps_pdgId = [x.pdgId for x in event.leptons]

        w_trigger = 1.0
        w_id = 1.0
        w_track = 1.0
        w_iso = 1.0
        w_reco = 1.0
        lep0_pdgId = 0
        lep1_pdgId = 0
        lep0_pt = 0
        lep1_pt = 0
        
        for syst in systs:
            tree.fill('lep_weight_' + syst, 0)

        if event.is_sl or event.is_dl:
            if event.is_sl:
                lep0_pdgId = event.leps_pdgId[0]
                lep0_pt = event.leptons.at(0).lv.Pt()
            elif event.is_dl:
                lep0_pdgId = event.leps_pdgId[0]
                lep0_pt = event.leptons.at(0).lv.Pt()
                lep1_pdgId = event.leps_pdgId[1]
                lep1_pt = event.leptons.at(1).lv.Pt()

            for syst in systs:
                w = calc_lepton_SF(event, syst)
                tree.fill('lep_weight_' + syst, w)

        tree.fill('is_sl', event.is_sl)
        tree.fill('is_dl', event.is_dl)
        tree.fill('numJets', event.numJets)
        #tree.fill('nBCSVM', event.nBCSVM)
        tree.fill('lep0_pdgId', lep0_pdgId)
        tree.fill('lep1_pdgId', lep1_pdgId)
        tree.fill('lep0_pt', lep0_pt)
        tree.fill('lep1_pt', lep1_pt)
        tree.tree.Fill()
        iEv += 1

    outfile.Write()
    outfile.Close()
