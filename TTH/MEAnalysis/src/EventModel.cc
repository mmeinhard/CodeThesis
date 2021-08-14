#include "TTH/MEAnalysis/interface/EventModel.h"

namespace TTH_MEAnalysis {

template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}

bool Systematic::is_jec(Systematic::SystId syst_id) {
    bool ret = false;
    ret = (syst_id.first == CMS_scale_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteMPFBias_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteStat_j) | ret;
    ret = (syst_id.first == CMS_scaleAbsoluteScale_j) | ret;
    ret = (syst_id.first == CMS_scaleFlavorQCD_j) | ret;
    ret = (syst_id.first == CMS_scaleFragmentation_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpDataMC_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtBB_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtEC1_j) | ret;
    //ret = (syst_id.first == CMS_scalePileUpPtEC2_j) | ret;
    //ret = (syst_id.first == CMS_scalePileUpPtHF_j) | ret;
    ret = (syst_id.first == CMS_scalePileUpPtRef_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeBal_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeFSR_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeJEREC1_j) | ret;
    //ret = (syst_id.first == CMS_scaleRelativeJEREC2_j) | ret;
    //ret = (syst_id.first == CMS_scaleRelativeJERHF_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativePtBB_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativePtEC1_j) | ret;
    //ret = (syst_id.first == CMS_scaleRelativePtEC2_j) | ret;
    //ret = (syst_id.first == CMS_scaleRelativePtHF_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeStatFSR_j) | ret;
    ret = (syst_id.first == CMS_scaleRelativeStatEC_j) | ret;
    //ret = (syst_id.first == CMS_scaleRelativeStatHF_j) | ret;
    ret = (syst_id.first == CMS_scaleSinglePionECAL_j) | ret;
    ret = (syst_id.first == CMS_scaleSinglePionHCAL_j) | ret;
    ret = (syst_id.first == CMS_scaleTimePtEta_j) | ret;
    return ret;
}

bool Systematic::is_jer(Systematic::SystId syst_id) {
    return syst_id.first == CMS_res_j;
}

bool Systematic::is_nominal(Systematic::SystId syst_id) {
    return syst_id.first == Nominal;
}

Systematic::SystId Systematic::make_id(Systematic::Event e, Systematic::Direction d) {
    return std::make_pair(e, d);
}

template <typename T>
EventDescription TreeDescriptionMCSystematic<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription<T>::create_event(syst_id);
    event.ttCls = *ttCls;
    event.genHiggsDecayMode = *genHiggsDecayMode;
    event.Pileup_nTrueInt = *Pileup_nTrueInt;
    event.genTopHad_pt = *genTopHad_pt;
    event.genTopLep_pt = *genTopLep_pt;
    event.weights[std::make_pair(Systematic::CMS_btag, Systematic::None)] = 1.0;
    event.weights[std::make_pair(Systematic::CMS_btag_boosted, Systematic::None)] = 1.0;
    event.weights[std::make_pair(Systematic::CMS_pu, Systematic::None)] = 1.0;
    event.weights[std::make_pair(Systematic::gen, Systematic::None)] = (*genWeight);
    return event;
}

float recomputeMem(float p0, float p1, float sf=0.1) {
    if (p0 == 0 && p1 == 0) {
        return 0.0;
    }
    return p0/(p0+sf*p1);
}

template <typename T>
EventDescription TreeDescriptionMCBOOSTED<T>::create_event(Systematic::SystId syst_id) {
    std::vector<Jet> boosted_bjets(this->build_boosted_bjets(syst_id));
    std::vector<Jet> boosted_ljets(this->build_boosted_ljets(syst_id));
    std::vector<Jet> boosted_jets;
    boosted_jets.reserve( boosted_bjets.size() + boosted_ljets.size() ); // preallocate memory
    boosted_jets.insert( boosted_jets.end(), boosted_bjets.begin(), boosted_bjets.end() );
    boosted_jets.insert( boosted_jets.end(), boosted_ljets.begin(), boosted_ljets.end() );

    auto event = TreeDescriptionMC<T>::create_event(syst_id, boosted_jets);

    event.n_boosted_bjets =  *(this->n_boosted_bjets);
    event.n_boosted_ljets =  *(this->n_boosted_ljets);
    event.boosted = *(this->boosted);
    event.resolved = *(this->resolved);

    for (auto njet=0; njet < event.n_boosted_bjets; njet++) {
        event.boosted_bjets_hadronFlavour.push_back(this->boosted_bjets_hadronFlavour[njet]);
    }
    for (auto njet=0; njet < event.n_boosted_ljets; njet++) {
        event.boosted_ljets_hadronFlavour.push_back(this->boosted_ljets_hadronFlavour[njet]);
    }


    event.higgsCandidate = build_higgsCandidate(syst_id);
    event.topCandidate = build_topCandidate(syst_id);


    if (Systematic::is_nominal(syst_id) || Systematic::is_jec(syst_id) || Systematic::is_jer(syst_id)) {
        event.mem_DL_0w2h2t_sj_p = this->mem_DL_0w2h2t_sj_p.GetValue(syst_id);
        event.mem_SL_0w2h2t_sj_p = this->mem_SL_0w2h2t_sj_p.GetValue(syst_id);
        event.mem_SL_1w2h2t_sj_p = this->mem_SL_1w2h2t_sj_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_sj_p = this->mem_SL_2w2h2t_sj_p.GetValue(syst_id);
        event.mem_DL_0w2h2t_sj_perm_higgs_p = this->mem_DL_0w2h2t_sj_perm_higgs_p.GetValue(syst_id);
        event.mem_SL_0w2h2t_sj_perm_higgs_p = this->mem_SL_0w2h2t_sj_perm_higgs_p.GetValue(syst_id);
        event.mem_SL_1w2h2t_sj_perm_higgs_p = this->mem_SL_1w2h2t_sj_perm_higgs_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_sj_perm_higgs_p = this->mem_SL_2w2h2t_sj_perm_higgs_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_sj_perm_tophiggs_p = this->mem_SL_2w2h2t_sj_perm_tophiggs_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_sj_perm_top_p = this->mem_SL_2w2h2t_sj_perm_top_p.GetValue(syst_id);
    }
    
    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Up)] = LHE_weights_scale_wgt[4];
    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Down)] = LHE_weights_scale_wgt[5];
    return event;
}

template <typename T>
EventDescription TreeDescriptionMC<T>::create_event(Systematic::SystId syst_id, std::vector<Jet> boosted_jets) {
    auto event = TreeDescription<T>::create_event(syst_id);

    for (auto njet=0; njet < *(this->njets); njet++) {
        event.jets_hadronFlavour.push_back(this->jets_hadronFlavour[njet]);
    }

    event.ttCls = *ttCls;
    event.genHiggsDecayMode = *genHiggsDecayMode;
    event.Pileup_nTrueInt = *Pileup_nTrueInt;
    event.numJets = numJets.GetValue(syst_id);
    event.nBDeepCSVM = nBDeepCSVM.GetValue(syst_id);
    event.nBDeepFlavM = nBDeepFlavM.GetValue(syst_id);
    //event.nBCSVM = nBCSVM.GetValue(syst_id);

    std::vector<Jet> jetstouse;
    if (boosted_jets.size()>0) jetstouse = boosted_jets;
    else jetstouse = event.jets;

    if (BCalibInitialized == true){
        //Recalculate nominal btag Correction
        event.weights[std::make_pair(Systematic::CMS_btag, Systematic::None)] = this->calcBTagCorr("central", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted, Systematic::None)] = this->calcBTagCorr("central", jetstouse, BTagCalibType);
    }

    //if (Systematic::is_nominal(syst_id)) {
    //    std::cout <<  event.jets.size() << " " << boosted_jets.size() <<  " " << event.weights[std::make_pair(Systematic::CMS_btag, Systematic::None)] <<  " " << event.weights[std::make_pair(Systematic::CMS_btag_boosted, Systematic::None)] << std::endl;
    //    for( auto jet : event.jets){
    //        std::cout << "----- C++ ----- JET: " << "Passing (" << jet.flav << " " << abs(jet.lv.Eta()) << " " << jet.lv.Pt() << " " << jet.btagDeepCSV << std::endl;
    //    }
    //    for( auto jet : boosted_jets){
    //        std::cout << "----- C++ ----- BOOSTED JET: " << "Passing (" << jet.flav << " " << abs(jet.lv.Eta()) << " " << jet.lv.Pt() << " " << jet.btagDeepCSV << std::endl;
    //    }
    //}
    //else {
    //    event.weights[std::make_pair(Systematic::CMS_btag, Systematic::None)] = (*btagWeight_shape);
    //}

    event.weights[std::make_pair(Systematic::gen, Systematic::None)] = (*genWeight);
    //event.weights[std::make_pair(Systematic::CMS_btag, Systematic::None)] = (*btagWeight_shape);
    event.weights[std::make_pair(Systematic::CMS_pu, Systematic::None)] = (*puWeight);
    event.weights[std::make_pair(Systematic::CMS_L1Prefiring, Systematic::None)] = (*L1PrefireWeight);
    event.weights[std::make_pair(Systematic::CMS_ttHbb_PDF, Systematic::None)] = (this->LHEPDFWeights[0]);


    if (Systematic::is_nominal(syst_id) || Systematic::is_jec(syst_id)) {
        // std::cout << "------" << std::endl;
        // std::cout << this->calcBTagCorr("up_jesAbsoluteMPFBias", event.jets, BTagCalibType) << std::endl;
        // std::cout << this->calcBTagCorr("down_jesAbsoluteMPFBias", event.jets, BTagCalibType) << std::endl;
        // std::cout << "------" << std::endl;
        event.weights[std::make_pair(Systematic::CMS_btag_jesAbsoluteMPFBias, Systematic::Up)] = this->calcBTagCorr("up_jesAbsoluteMPFBias", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesAbsoluteScale, Systematic::Up)] = this->calcBTagCorr("up_jesAbsoluteScale", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesAbsoluteStat, Systematic::Up)] = this->calcBTagCorr("up_jesAbsoluteStat", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesFlavorQCD, Systematic::Up)] = this->calcBTagCorr("up_jesFlavorQCD", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesFragmentation, Systematic::Up)] = this->calcBTagCorr("up_jesFragmentation", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpDataMC, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpDataMC", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtBB, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtBB", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtEC1, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtEC1", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtEC2, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtEC2", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtHF, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtRef, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtRef", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeBal, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeBal", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeFSR, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeFSR", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeJEREC1, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeJEREC1", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeJEREC2, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeJEREC2", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeJERHF, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeJERHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtBB, Systematic::Up)] = this->calcBTagCorr("up_jesRelativePtBB", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtEC1, Systematic::Up)] = this->calcBTagCorr("up_jesRelativePtEC1", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtEC2, Systematic::Up)] = this->calcBTagCorr("up_jesRelativePtEC2", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtHF, Systematic::Up)] = this->calcBTagCorr("up_jesRelativePtHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeStatFSR, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeStatFSR", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeStatEC, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeStatEC", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeStatHF, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeStatHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesSinglePionECAL, Systematic::Up)] = this->calcBTagCorr("up_jesSinglePionECAL", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesSinglePionHCAL, Systematic::Up)] = this->calcBTagCorr("up_jesSinglePionHCAL", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesTimePtEta, Systematic::Up)] = this->calcBTagCorr("up_jesTimePtEta", event.jets, BTagCalibType);
    
        event.weights[std::make_pair(Systematic::CMS_btag_jesAbsoluteMPFBias, Systematic::Down)] = this->calcBTagCorr("down_jesAbsoluteMPFBias", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesAbsoluteScale, Systematic::Down)] = this->calcBTagCorr("down_jesAbsoluteScale", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesAbsoluteStat, Systematic::Down)] = this->calcBTagCorr("down_jesAbsoluteStat", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesFlavorQCD, Systematic::Down)] = this->calcBTagCorr("down_jesFlavorQCD", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesFragmentation, Systematic::Down)] = this->calcBTagCorr("down_jesFragmentation", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpDataMC, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpDataMC", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtBB, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtBB", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtEC1, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtEC1", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtEC2, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtEC2", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtHF, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesPileUpPtRef, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtRef", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeBal, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeBal", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeFSR, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeFSR", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeJEREC1, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeJEREC1", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeJEREC2, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeJEREC2", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeJERHF, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeJERHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtBB, Systematic::Down)] = this->calcBTagCorr("down_jesRelativePtBB", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtEC1, Systematic::Down)] = this->calcBTagCorr("down_jesRelativePtEC1", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtEC2, Systematic::Down)] = this->calcBTagCorr("down_jesRelativePtEC2", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativePtHF, Systematic::Down)] = this->calcBTagCorr("down_jesRelativePtHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeStatFSR, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeStatFSR", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeStatEC, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeStatEC", event.jets, BTagCalibType);
        //event.weights[std::make_pair(Systematic::CMS_btag_jesRelativeStatHF, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeStatHF", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesSinglePionECAL, Systematic::Down)] = this->calcBTagCorr("down_jesSinglePionECAL", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesSinglePionHCAL, Systematic::Down)] = this->calcBTagCorr("down_jesSinglePionHCAL", event.jets, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_jesTimePtEta, Systematic::Down)] = this->calcBTagCorr("down_jesTimePtEta", event.jets, BTagCalibType);
     

        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesAbsoluteMPFBias, Systematic::Up)] = this->calcBTagCorr("up_jesAbsoluteMPFBias", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesAbsoluteScale, Systematic::Up)] = this->calcBTagCorr("up_jesAbsoluteScale", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesAbsoluteStat, Systematic::Up)] = this->calcBTagCorr("up_jesAbsoluteStat", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesFlavorQCD, Systematic::Up)] = this->calcBTagCorr("up_jesFlavorQCD", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesFragmentation, Systematic::Up)] = this->calcBTagCorr("up_jesFragmentation", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpDataMC, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpDataMC", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpPtBB, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtBB", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpPtEC1, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtEC1", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpPtRef, Systematic::Up)] = this->calcBTagCorr("up_jesPileUpPtRef", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeBal, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeBal", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeFSR, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeFSR", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeJEREC1, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeJEREC1", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativePtBB, Systematic::Up)] = this->calcBTagCorr("up_jesRelativePtBB", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativePtEC1, Systematic::Up)] = this->calcBTagCorr("up_jesRelativePtEC1", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeStatFSR, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeStatFSR", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeStatEC, Systematic::Up)] = this->calcBTagCorr("up_jesRelativeStatEC", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesSinglePionECAL, Systematic::Up)] = this->calcBTagCorr("up_jesSinglePionECAL", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesSinglePionHCAL, Systematic::Up)] = this->calcBTagCorr("up_jesSinglePionHCAL", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesTimePtEta, Systematic::Up)] = this->calcBTagCorr("up_jesTimePtEta", jetstouse, BTagCalibType);

        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesAbsoluteMPFBias, Systematic::Down)] = this->calcBTagCorr("down_jesAbsoluteMPFBias", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesAbsoluteScale, Systematic::Down)] = this->calcBTagCorr("down_jesAbsoluteScale", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesAbsoluteStat, Systematic::Down)] = this->calcBTagCorr("down_jesAbsoluteStat", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesFlavorQCD, Systematic::Down)] = this->calcBTagCorr("down_jesFlavorQCD", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesFragmentation, Systematic::Down)] = this->calcBTagCorr("down_jesFragmentation", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpDataMC, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpDataMC", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpPtBB, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtBB", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpPtEC1, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtEC1", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesPileUpPtRef, Systematic::Down)] = this->calcBTagCorr("down_jesPileUpPtRef", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeBal, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeBal", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeFSR, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeFSR", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeJEREC1, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeJEREC1", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativePtBB, Systematic::Down)] = this->calcBTagCorr("down_jesRelativePtBB", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativePtEC1, Systematic::Down)] = this->calcBTagCorr("down_jesRelativePtEC1", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeStatFSR, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeStatFSR", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesRelativeStatEC, Systematic::Down)] = this->calcBTagCorr("down_jesRelativeStatEC", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesSinglePionECAL, Systematic::Down)] = this->calcBTagCorr("down_jesSinglePionECAL", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesSinglePionHCAL, Systematic::Down)] = this->calcBTagCorr("down_jesSinglePionHCAL", jetstouse, BTagCalibType);
        event.weights[std::make_pair(Systematic::CMS_btag_boosted_jesTimePtEta, Systematic::Down)] = this->calcBTagCorr("down_jesTimePtEta", jetstouse, BTagCalibType);

    }
    
    
    if (Systematic::is_nominal(syst_id)) {
        if (BCalibInitialized == true){
            //this->calcBTagCorr("up_cferr1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_cferr1, Systematic::Up)] = this->calcBTagCorr("up_cferr1", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_cferr2, Systematic::Up)] = this->calcBTagCorr("up_cferr2", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_hf, Systematic::Up)] = this->calcBTagCorr("up_hf", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_hfstats1, Systematic::Up)] = this->calcBTagCorr("up_hfstats1", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_hfstats2, Systematic::Up)] = this->calcBTagCorr("up_hfstats2", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_lf, Systematic::Up)] = this->calcBTagCorr("up_lf", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_lfstats1, Systematic::Up)] = this->calcBTagCorr("up_lfstats1", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_lfstats2, Systematic::Up)] = this->calcBTagCorr("up_lfstats2", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_cferr1, Systematic::Down)] = this->calcBTagCorr("down_cferr1", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_cferr2, Systematic::Down)] = this->calcBTagCorr("down_cferr2", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_hf, Systematic::Down)] = this->calcBTagCorr("down_hf", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_hfstats1, Systematic::Down)] = this->calcBTagCorr("down_hfstats1", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_hfstats2, Systematic::Down)] = this->calcBTagCorr("down_hfstats2", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_lf, Systematic::Down)] = this->calcBTagCorr("down_lf", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_lfstats1, Systematic::Down)] = this->calcBTagCorr("down_lfstats1", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_boosted_lfstats2, Systematic::Down)] = this->calcBTagCorr("down_lfstats2", jetstouse, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_cferr1, Systematic::Up)] = this->calcBTagCorr("up_cferr1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_cferr2, Systematic::Up)] = this->calcBTagCorr("up_cferr2", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_hf, Systematic::Up)] = this->calcBTagCorr("up_hf", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_hfstats1, Systematic::Up)] = this->calcBTagCorr("up_hfstats1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_hfstats2, Systematic::Up)] = this->calcBTagCorr("up_hfstats2", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_lf, Systematic::Up)] = this->calcBTagCorr("up_lf", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_lfstats1, Systematic::Up)] = this->calcBTagCorr("up_lfstats1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_lfstats2, Systematic::Up)] = this->calcBTagCorr("up_lfstats2", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_cferr1, Systematic::Down)] = this->calcBTagCorr("down_cferr1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_cferr2, Systematic::Down)] = this->calcBTagCorr("down_cferr2", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_hf, Systematic::Down)] = this->calcBTagCorr("down_hf", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_hfstats1, Systematic::Down)] = this->calcBTagCorr("down_hfstats1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_hfstats2, Systematic::Down)] = this->calcBTagCorr("down_hfstats2", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_lf, Systematic::Down)] = this->calcBTagCorr("down_lf", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_lfstats1, Systematic::Down)] = this->calcBTagCorr("down_lfstats1", event.jets, BTagCalibType);
            event.weights[std::make_pair(Systematic::CMS_btag_lfstats2, Systematic::Down)] = this->calcBTagCorr("down_lfstats2", event.jets, BTagCalibType);
        }
        //else {
        //    event.weights[std::make_pair(Systematic::CMS_btag_cferr1, Systematic::Up)] = (*btagWeight_shape_cferr1Up);
        //    event.weights[std::make_pair(Systematic::CMS_btag_cferr2, Systematic::Up)] = (*btagWeight_shape_cferr2Up);
        //    event.weights[std::make_pair(Systematic::CMS_btag_hf, Systematic::Up)] = (*btagWeight_shape_hfUp);
        //    event.weights[std::make_pair(Systematic::CMS_btag_hfstats1, Systematic::Up)] = (*btagWeight_shape_hfstats1Up);
        //    event.weights[std::make_pair(Systematic::CMS_btag_hfstats2, Systematic::Up)] = (*btagWeight_shape_hfstats2Up);
        //    event.weights[std::make_pair(Systematic::CMS_btag_jes, Systematic::Up)] = (*btagWeight_shape_jesUp);
        //    event.weights[std::make_pair(Systematic::CMS_btag_lf, Systematic::Up)] = (*btagWeight_shape_lfUp);
        //    event.weights[std::make_pair(Systematic::CMS_btag_lfstats1, Systematic::Up)] = (*btagWeight_shape_lfstats1Up);
        //    event.weights[std::make_pair(Systematic::CMS_btag_lfstats2, Systematic::Up)] = (*btagWeight_shape_lfstats2Up);
    
        //    event.weights[std::make_pair(Systematic::CMS_btag_cferr1, Systematic::Down)] = (*btagWeight_shape_cferr1Down);
        //    event.weights[std::make_pair(Systematic::CMS_btag_cferr2, Systematic::Down)] = (*btagWeight_shape_cferr2Down);
        //    event.weights[std::make_pair(Systematic::CMS_btag_hf, Systematic::Down)] = (*btagWeight_shape_hfDown);
        //    event.weights[std::make_pair(Systematic::CMS_btag_hfstats1, Systematic::Down)] = (*btagWeight_shape_hfstats1Down);
        //    event.weights[std::make_pair(Systematic::CMS_btag_hfstats2, Systematic::Down)] = (*btagWeight_shape_hfstats2Down);
        //    event.weights[std::make_pair(Systematic::CMS_btag_jes, Systematic::Down)] = (*btagWeight_shape_jesDown);
        //    event.weights[std::make_pair(Systematic::CMS_btag_lf, Systematic::Down)] = (*btagWeight_shape_lfDown);
        //    event.weights[std::make_pair(Systematic::CMS_btag_lfstats1, Systematic::Down)] = (*btagWeight_shape_lfstats1Down);
        //    event.weights[std::make_pair(Systematic::CMS_btag_lfstats2, Systematic::Down)] = (*btagWeight_shape_lfstats2Down);
        //}

        
        event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Up)] = (*puWeightUp);
        event.weights[std::make_pair(Systematic::CMS_pu, Systematic::Down)] = (*puWeightDown);

        event.weights[std::make_pair(Systematic::CMS_L1Prefiring, Systematic::Up)] = (*L1PrefireWeightUp);
        event.weights[std::make_pair(Systematic::CMS_L1Prefiring, Systematic::Down)] = (*L1PrefireWeightDown);

    }

    if (Systematic::is_jec(syst_id) || Systematic::is_jer(syst_id)) {

        event.mem_DL_0w2h2t_p = this->mem_DL_0w2h2t_p.GetValue(syst_id);
        event.mem_SL_0w2h2t_p = this->mem_SL_0w2h2t_p.GetValue(syst_id);
        event.mem_SL_1w2h2t_p = this->mem_SL_1w2h2t_p.GetValue(syst_id);
        event.mem_SL_2w2h2t_p = this->mem_SL_2w2h2t_p.GetValue(syst_id);
    }

    std::vector<double> pdfWeights;
    for(int iWeight = 1; iWeight <  (*nLHEPDFWeights); iWeight++){
        pdfWeights.push_back(this->LHEPDFWeights[iWeight]);
    }
    //std::cout << "PDFVec.size() = " << pdfWeights.size() << std::endl;
    float weightUp = 1.0;
    float weightDown = 1.0;
    
    if (pdfWeights.size() > 0){
        pdfWeights.insert(pdfWeights.begin(), 1.); //Since we reweight the nominal event this this PDF here needs to go a 1 otherwise the 0th element
//std::cout << "pdfWeights = " << pdfWeights.size() << std::endl; 
        if (pdfWeights.size() != 103){
            //std::cout << "Skipping PDF weight" << std::endl;
            weightUp = 1.0; //pdfUnc.central + pdfUnc.errplus;
            weightDown = 1.0; //pdfUnc.central - pdfUnc.errminus;
        }
        else {
            //std::cout << "NNPDF31_nnlo_hessian_pdfas" << std::endl;
            LHAPDF::PDFSet nnpdfSet("NNPDF31_nnlo_hessian_pdfas");
            const LHAPDF::PDFUncertainty pdfUnc = nnpdfSet.uncertainty(pdfWeights, 68.268949); //68.268949 to get 1 sigma deviation
            weightUp = pdfUnc.central + pdfUnc.errplus;
            weightDown = pdfUnc.central - pdfUnc.errminus;
        }

    }


    event.weights[std::make_pair(Systematic::CMS_ttHbb_PDF, Systematic::Up)] = (weightUp);
    event.weights[std::make_pair(Systematic::CMS_ttHbb_PDF, Systematic::Down)] = (weightDown);
    event.weights[std::make_pair(Systematic::CMS_ttHbb_scaleMuR, Systematic::Down)] = (this->LHEScaleWeights[1]);//7
    event.weights[std::make_pair(Systematic::CMS_ttHbb_scaleMuR, Systematic::Up)] = (this->LHEScaleWeights[7]);
    event.weights[std::make_pair(Systematic::CMS_ttHbb_scaleMuF, Systematic::Down)] = (this->LHEScaleWeights[3]);//5
    event.weights[std::make_pair(Systematic::CMS_ttHbb_scaleMuF, Systematic::Up)] = (this->LHEScaleWeights[5]);

    event.weights[std::make_pair(Systematic::CMS_ttHbb_FSR, Systematic::Down)] = *PSWeight_FSR_Down;
    event.weights[std::make_pair(Systematic::CMS_ttHbb_ISR, Systematic::Down)] = *PSWeight_ISR_Down;
    event.weights[std::make_pair(Systematic::CMS_ttHbb_FSR, Systematic::Up)] = *PSWeight_FSR_Up;
    event.weights[std::make_pair(Systematic::CMS_ttHbb_ISR, Systematic::Up)] = *PSWeight_ISR_Up;

    event.genTopHad_pt = *genTopHad_pt;
    event.genTopLep_pt = *genTopLep_pt;

    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Up)] = LHE_weights_scale_wgt[4];
    //event.weights[std::make_pair(Systematic::CMS_ttH_scaleME, Systematic::Down)] = LHE_weights_scale_wgt[5];
    return event;
}

template <typename T>
EventDescription TreeDescription<T>::create_event(Systematic::SystId syst_id) {
    std::vector<Jet> jets(this->build_jets(syst_id));
    
    EventDescription event;

    event.run = *(this->run);
    event.lumi = *(this->lumi);
    //event.evt = *(this->evt);
    //event.evt1 = *(this->evt1);
    //event.evt2 = *(this->evt2);
    event.json = *(this->json);
    event.passMETFilters = *(this->passMETFilters);

    event.is_sl = *(this->is_sl);
    event.is_dl = *(this->is_dl);
    event.is_fh = *(this->is_fh);

    event.passPV = *(this->passPV);

    event.HLT_ttH_SL_mu = *(this->HLT_ttH_SL_mu);
    event.HLT_ttH_SL_el = *(this->HLT_ttH_SL_el);
    event.HLT_ttH_DL_mumu = *(this->HLT_ttH_DL_mumu);
    event.HLT_ttH_DL_elmu = *(this->HLT_ttH_DL_elmu);
    event.HLT_ttH_DL_elel = *(this->HLT_ttH_DL_elel);
    //disabled in May1-2 
    //event.HLT_ttH_FH = *(this->HLT_ttH_FH);
    event.HLT_ttH_FH = 1;
    
    event.numJets = *(this->numJets);
    event.nBDeepCSVM = *(this->nBDeepCSVM);
    event.nBDeepFlavM= *(this->nBDeepFlavM);
    //event.nBCSVM = *(this->nBCSVM);
    event.jets = jets;
    event.syst_id = syst_id;
    event.leptons = build_leptons(syst_id);
    
    event.nPVs = *(this->nPVs);
    
    for (int ilep=0; ilep < *(this->nleps); ilep++) {
        event.leps_superclustereta.push_back(this->leps_scEta[ilep]);
    }

    event.btag_LR_4b_2b_btagCSV = *(this->btag_LR_4b_2b_btagCSV);
    event.mem_DL_0w2h2t_p = *(this->mem_DL_0w2h2t_p);
    event.mem_SL_0w2h2t_p = *(this->mem_SL_0w2h2t_p);
    event.mem_SL_1w2h2t_p = *(this->mem_SL_1w2h2t_p);
    event.mem_SL_2w2h2t_p = *(this->mem_SL_2w2h2t_p);

    event.Wmass = *(this->Wmass);
    event.met_pt = *(this->met_pt);
    event.met_phi = *(this->met_phi);

    event.weights[Systematic::syst_id_nominal] = 1.0;
    return event;
}


template <typename T>
EventDescription TreeDescriptionBOOSTED<T>::create_event(Systematic::SystId syst_id) {
    auto event = TreeDescription<T>::create_event(syst_id);
    std::vector<Jet> boosted_bjets(this->build_boosted_bjets(syst_id));
    std::vector<Jet> boosted_ljets(this->build_boosted_ljets(syst_id));


    event.n_boosted_bjets = *(this->n_boosted_bjets);
    event.n_boosted_ljets = *(this->n_boosted_ljets);
    event.boosted = *(this->boosted);
    event.resolved = *(this->resolved);
    //for (auto njet=0; njet < *(this->n_boosted_bjets); njet++) {
    //    event.boosted_bjets_hadronFlavour.push_back(this->boosted_bjets_hadronFlavour[njet]);
    //}
    //for (auto njet=0; njet < *(this->n_boosted_ljets); njet++) {
    //    event.boosted_ljets_hadronFlavour.push_back(this->boosted_ljets_hadronFlavour[njet]);
    //}


    event.higgsCandidate = build_higgsCandidate(syst_id);
    event.topCandidate = build_topCandidate(syst_id);

    event.mem_DL_0w2h2t_sj_p = *(this->mem_DL_0w2h2t_sj_p);
    event.mem_SL_0w2h2t_sj_p = *(this->mem_SL_0w2h2t_sj_p);
    event.mem_SL_1w2h2t_sj_p = *(this->mem_SL_1w2h2t_sj_p);
    event.mem_SL_2w2h2t_sj_p = *(this->mem_SL_2w2h2t_sj_p);
    event.mem_DL_0w2h2t_sj_perm_higgs_p = *(this->mem_DL_0w2h2t_sj_perm_higgs_p);
    event.mem_SL_0w2h2t_sj_perm_higgs_p = *(this->mem_SL_0w2h2t_sj_perm_higgs_p);
    event.mem_SL_1w2h2t_sj_perm_higgs_p = *(this->mem_SL_1w2h2t_sj_perm_higgs_p);
    event.mem_SL_2w2h2t_sj_perm_higgs_p = *(this->mem_SL_2w2h2t_sj_perm_higgs_p);
    event.mem_SL_2w2h2t_sj_perm_tophiggs_p = *(this->mem_SL_2w2h2t_sj_perm_tophiggs_p);
    event.mem_SL_2w2h2t_sj_perm_top_p = *(this->mem_SL_2w2h2t_sj_perm_top_p);


    return event;
}

template <typename T>
std::vector<Lepton> TreeDescription<T>::build_leptons(Systematic::SystId syst_id) {
    std::vector<Lepton> leps;

    for (int ilep = 0; ilep < *(this->nleps); ilep++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->leps_pt[ilep],
            this->leps_eta[ilep],
            this->leps_phi[ilep],
            this->leps_mass[ilep]
        );
        leps.push_back(Lepton(lv, sgn(this->leps_pdgId[ilep]), this->leps_pdgId[ilep]));
    }
    return leps;
}

template <typename T>
std::vector<higgsCandidates> TreeDescriptionBOOSTED<T>::build_higgsCandidate(Systematic::SystId syst_id) {
    std::vector<higgsCandidates> hc;

    for (int ih = 0; ih < *(this->nhiggsCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->higgsCandidate_pt[ih],
            this->higgsCandidate_eta[ih],
            this->higgsCandidate_phi[ih],
            this->higgsCandidate_mass[ih]
        );

        float m_softdrop = this->higgsCandidate_msoftdrop[ih];
        float tau21 = this->higgsCandidate_tau21[ih];
        float bbtag = this->higgsCandidate_bbtag[ih];
        float sj1btag = this->higgsCandidate_sj1btag[ih];
        float sj2btag = this->higgsCandidate_sj2btag[ih];
        float sj1pt = this->higgsCandidate_sj1pt[ih];
        float sj2pt = this->higgsCandidate_sj2pt[ih];
        hc.push_back(higgsCandidates(lv, m_softdrop,tau21,bbtag,sj1btag,sj2btag,sj1pt,sj2pt));
    }
    return hc;
}

template <typename T>
std::vector<topCandidates> TreeDescriptionBOOSTED<T>::build_topCandidate(Systematic::SystId syst_id) {
    std::vector<topCandidates> hc;

    for (int ih = 0; ih < *(this->ntopCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->topCandidate_pt[ih],
            this->topCandidate_eta[ih],
            this->topCandidate_phi[ih],
            this->topCandidate_mass[ih]
        );

        float tau32SD = this->topCandidate_tau32SD[ih];
        float fRec = this->topCandidate_fRec[ih];
        float delRopt = this->topCandidate_delRopt[ih];
        float sj1btag = this->topCandidate_sj1btag[ih];
        float sj2btag = this->topCandidate_sj2btag[ih];
        float sj3btag = this->topCandidate_sj3btag[ih];
        float sj1pt = this->topCandidate_sj1pt[ih];
        float sj2pt = this->topCandidate_sj2pt[ih];
        float sj3pt = this->topCandidate_sj3pt[ih];
        hc.push_back(topCandidates(lv, tau32SD,fRec,delRopt,sj1btag,sj2btag,sj3btag,sj1pt,sj2pt,sj3pt));
    }
    return hc;
}

template <typename T>
std::vector<higgsCandidates> TreeDescriptionMCBOOSTED<T>::build_higgsCandidate(Systematic::SystId syst_id) {
    std::vector<higgsCandidates> hc;

    for (int ih = 0; ih < *(this->nhiggsCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->higgsCandidate_pt[ih],
            this->higgsCandidate_eta[ih],
            this->higgsCandidate_phi[ih],
            this->higgsCandidate_mass[ih]
        );

        float m_softdrop = this->higgsCandidate_msoftdrop[ih];
        float tau21 = this->higgsCandidate_tau21[ih];
        float bbtag = this->higgsCandidate_bbtag[ih];
        float sj1btag = this->higgsCandidate_sj1btag[ih];
        float sj2btag = this->higgsCandidate_sj2btag[ih];
        float sj1pt = this->higgsCandidate_sj1pt[ih];
        float sj2pt = this->higgsCandidate_sj2pt[ih];
        hc.push_back(higgsCandidates(lv, m_softdrop,tau21,bbtag,sj1btag,sj2btag,sj1pt,sj2pt));
    }
    return hc;
}

template <typename T>
std::vector<topCandidates> TreeDescriptionMCBOOSTED<T>::build_topCandidate(Systematic::SystId syst_id) {
    std::vector<topCandidates> hc;

    for (int ih = 0; ih < *(this->ntopCandidate); ih++) {
        TLorentzVector lv;
        lv.SetPtEtaPhiM(
            this->topCandidate_pt[ih],
            this->topCandidate_eta[ih],
            this->topCandidate_phi[ih],
            this->topCandidate_mass[ih]
        );

        float tau32SD = this->topCandidate_tau32SD[ih];
        float fRec = this->topCandidate_fRec[ih];
        float delRopt = this->topCandidate_delRopt[ih];
        float sj1btag = this->topCandidate_sj1btag[ih];
        float sj2btag = this->topCandidate_sj2btag[ih];
        float sj3btag = this->topCandidate_sj3btag[ih];
        float sj1pt = this->topCandidate_sj1pt[ih];
        float sj2pt = this->topCandidate_sj2pt[ih];
        float sj3pt = this->topCandidate_sj3pt[ih];
        hc.push_back(topCandidates(lv, tau32SD,fRec,delRopt,sj1btag,sj2btag,sj3btag,sj1pt,sj2pt,sj3pt));
    }
    return hc;
}

template <typename T>
std::vector<Jet> TreeDescriptionBOOSTED<T>::build_boosted_bjets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->n_boosted_bjets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(this->boosted_bjets_pt[njet] * corr/base_corr, this->boosted_bjets_eta[njet], this->boosted_bjets_phi[njet], this->boosted_bjets_mass[njet]);
        Jet jet(lv, -3, this->boosted_bjets_btag[njet], -3);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
std::vector<Jet> TreeDescriptionBOOSTED<T>::build_boosted_ljets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->n_boosted_ljets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(this->boosted_ljets_pt[njet] * corr/base_corr, this->boosted_ljets_eta[njet], this->boosted_ljets_phi[njet], this->boosted_ljets_mass[njet]);
        Jet jet(lv, -3, this->boosted_ljets_btag[njet], -3);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
std::vector<Jet> TreeDescriptionMCBOOSTED<T>::build_boosted_bjets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->n_boosted_bjets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(this->boosted_bjets_pt[njet] * corr/base_corr, this->boosted_bjets_eta[njet], this->boosted_bjets_phi[njet], this->boosted_bjets_mass[njet]);
        Jet jet(lv, -3, this->boosted_bjets_btag[njet], -3, this->boosted_bjets_hadronFlavour[njet], 1, -3);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
std::vector<Jet> TreeDescriptionMCBOOSTED<T>::build_boosted_ljets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->n_boosted_ljets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(this->boosted_ljets_pt[njet] * corr/base_corr, this->boosted_ljets_eta[njet], this->boosted_ljets_phi[njet], this->boosted_ljets_mass[njet]);
        Jet jet(lv, -3, this->boosted_ljets_btag[njet], -3, this->boosted_ljets_hadronFlavour[njet], 0, -3);
        jets.push_back(jet);
    }
    return jets;
}


template <typename T>
std::vector<Jet> TreeDescription<T>::build_jets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->njets); njet++) {
        TLorentzVector lv;

        double corr = 1.0;
        double base_corr = 1.0;

        lv.SetPtEtaPhiM(this->jets_pt[njet] * corr/base_corr, this->jets_eta[njet], this->jets_phi[njet], this->jets_mass[njet]);
        Jet jet(lv, this->jets_btagCSV[njet], this->jets_btagDeepCSV[njet], this->jets_btagDeepFlav[njet]);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T>
std::vector<Jet> TreeDescriptionMC<T>::build_jets(Systematic::SystId syst_id) {
    std::vector<Jet> jets;
    for (auto njet=0; njet < *(this->njets); njet++) {
        TLorentzVector lv;

        double pt = this->jets_pt[njet];
        if (Systematic::is_jec(syst_id) || Systematic::is_jer(syst_id)) {
            pt = (*get_correction_branch(syst_id))[njet];
        }

        lv.SetPtEtaPhiM(pt, this->jets_eta[njet], this->jets_phi[njet], this->jets_mass[njet]);
        Jet jet(lv, this->jets_btagCSV[njet], this->jets_btagDeepCSV[njet], this->jets_btagDeepFlav[njet], this->jets_hadronFlavour[njet], this->jets_btagFlag[njet], this->jets_dRmin[njet]);
        jets.push_back(jet);
    }
    return jets;
}

template <typename T> 
void TreeDescriptionMC<T>::initBCalibration(std::string Calib_file, std::string type) {
  //std::cout << "----- C++ -----" << "Initializing b calibration"  <<  std::endl; //Temp
  //std::cout << "----- C++ -----" << "File "  <<  Calib_file << std::endl; //Temp
  BTagCalibration calib("DeepCSV", Calib_file);
  //calib = BTagCalibration("DeepCSV", Calib_file);
  std::vector<std::string> bSystematics = {
    "up_lf", "down_lf",
    "up_hf", "down_hf",
    "up_hfstats1", "down_hfstats1",
    "up_hfstats2", "down_hfstats2",
    "up_lfstats1", "down_lfstats1",
    "up_lfstats2", "down_lfstats2",
    "up_cferr1", "down_cferr1",
    "up_cferr2", "down_cferr2",
  };
  shapeCorr_jes = {
    /*"up_jesAbsoluteMPFBias", "down_jesAbsoluteMPFBias",
    "up_jesAbsoluteScale", "down_jesAbsoluteScale",
    "up_jesAbsoluteStat", "down_jesAbsoluteStat",
    "up_jesFlavorQCD", "down_jesFlavorQCD",
    "up_jesFragmentation", "down_jesFragmentation",
    "up_jesPileUpDataMC", "down_jesPileUpDataMC",
    "up_jesPileUpPtBB", "down_jesPileUpPtBB",
    "up_jesPileUpPtEC1", "down_jesPileUpPtEC1",
    "up_jesPileUpPtEC2", "down_jesPileUpPtEC2",
    "up_jesPileUpPtHF", "down_jesPileUpPtHF",
    "up_jesPileUpPtRef", "down_jesPileUpPtRef",
    "up_jesRelativeBal", "down_jesRelativeBal",
    "up_jesRelativeFSR", "down_jesRelativeFSR",
    "up_jesRelativeJEREC1", "down_jesRelativeJEREC1",
    "up_jesRelativeJEREC2", "down_jesRelativeJEREC2",
    "up_jesRelativeJERHF", "down_jesRelativeJERHF",
    "up_jesRelativePtBB", "down_jesRelativePtBB",
    "up_jesRelativePtEC1", "down_jesRelativePtEC1",
    "up_jesRelativePtEC2", "down_jesRelativePtEC2",
    "up_jesRelativePtHF", "down_jesRelativePtHF",
    "up_jesRelativeStatFSR", "down_jesRelativeStatFSR",
    "up_jesRelativeStatEC", "down_jesRelativeStatEC",
    "up_jesRelativeStatHF", "down_jesRelativeStatHF",
    "up_jesSinglePionECAL", "down_jesSinglePionECAL",
    "up_jesSinglePionHCAL", "down_jesSinglePionHCAL",
    "up_jesTimePtEta", "down_jesTimePtEta"*/
  };

  for( auto jesSys : shapeCorr_jes){
    bSystematics.push_back(jesSys);
  }

  std::string cSys = "central";
  
  BCalibReader = BTagCalibrationReader(BTagEntry::OP_RESHAPING, cSys, bSystematics);
 
  BCalibReader.load(calib,  BTagEntry::FLAV_B, "iterativefit");
  BCalibReader.load(calib,  BTagEntry::FLAV_C, "iterativefit");
  BCalibReader.load(calib,  BTagEntry::FLAV_UDSG, "iterativefit");

  BCalibInitialized = true;
  BTagCalibType = type;
}

template <typename T>
float TreeDescriptionMC<T>::calcBTagCorr(std::string thisSystematic, std::vector<Jet> jets, std::string disc){
  float correction = 1;
  float tmpCorr = 1;
  BTagEntry::JetFlavor BTV_flav;
  std::string useSyst = thisSystematic;
  //std::cout << "----- C++ -----" << "Starting btag correction with systeamtic " << thisSystematic  <<  std::endl; //Temp DEBUG
  for( auto jet : jets){
    //std::cout << "----- C++ -----" << jet.flav << std::endl; //Temp DEBUG
    useSyst = thisSystematic;
    //Get the flavour expected by the BTagCalibrationReader
    if (abs(jet.flav) == 5 ){ //b-Jets
      //std::cout << "----- C++ -----" << "found b" << std::endl; //Temp DEBUG
      BTV_flav = BTagEntry::FLAV_B;
      //If the systematic is not in the vector if "normal" systemtics and jes systemtics, use nomina
      if (shapeCorr_bFlav.find(thisSystematic) == shapeCorr_bFlav.end() && shapeCorr_jes.find(thisSystematic)  == shapeCorr_jes.end()){
    //std::cout << "----- C++ -----" << "Falling back to central (b)" << std::endl; //Temp DEBUG
    useSyst = "central";
      }
    }
    else if (abs(jet.flav) == 4 ){ //c-Jets
      //std::cout << "----- C++ -----" << "found c" << std::endl; //Temp DEBUG
      BTV_flav = BTagEntry::FLAV_C;
      //if (shapeCorr_cFlav.find(thisSystematic) == shapeCorr_cFlav.end() && shapeCorr_jes.find(thisSystematic)  == shapeCorr_jes.end()){
      if (shapeCorr_cFlav.find(thisSystematic) == shapeCorr_cFlav.end()){
    //std::cout << "----- C++ -----" << "Falling back to central (c)" << std::endl; //Temp DEBUG
    useSyst = "central";
      }
    }
    else if (abs(jet.flav) == 0){ //udsg-Jets
      //std::cout << "----- C++ -----" << "found udsg" << std::endl; //Temp DEBUG
      BTV_flav = BTagEntry::FLAV_UDSG;
      if (shapeCorr_udsgFlav.find(thisSystematic) == shapeCorr_udsgFlav.end() && shapeCorr_jes.find(thisSystematic)  == shapeCorr_jes.end()){
    //std::cout << "----- C++ -----" << "Falling back to central (udsg)" << std::endl; //Temp DEBUG
    useSyst = "central";
      }
    }
    else {
      std::cout << "Unknown flavour" << std::endl;
      BTV_flav =  BTagEntry::FLAV_UDSG;
      break;
    }
    
    float bDisc = -1;
    if (disc == "csv"){ bDisc = jet.btagCSV; }
    else if (disc == "deepcsv"){ bDisc = jet.btagDeepCSV; }
    //else if (disc == "deepflav"){ bDisc = jet.btagDeepFlav; }
    else {
      std::cout << "Invalid discriminator";
      break;
    }
    //std::cout << "----- C++ -----" << "Passing (" << useSyst << " " << BTV_flav << " " << abs(jet.lv.Eta()) << " " << jet.lv.Pt() << " " << bDisc << std::endl; //Temp DEBUG
    tmpCorr = BCalibReader.eval_auto_bounds(useSyst, BTV_flav, abs(jet.lv.Eta()), jet.lv.Pt(), bDisc);
    //std::cout << "calculated correction" << std::endl;
    correction *= tmpCorr;
    //std::cout << "----- C++ -----" << "This jet correction " << tmpCorr << std::endl;//Temp DEBUG

    //Now add Ntrack reweighting
    /*if (jet.btagDeepCSV > 0.8001) {
        //if (jet.nVertexTracks == 0) correction *= 0.7093;
        //else if (jet.nVertexTracks == 1) correction *= 0.9225;
        if (jet.nVertexTracks == 2) correction *= 0.9554;
        else if (jet.nVertexTracks == 3) correction *= 1.0245;
        else if (jet.nVertexTracks == 4) correction *= 1.0581;
        else if (jet.nVertexTracks == 5) correction *= 1.0703;
        else if (jet.nVertexTracks >= 6) correction *= 1.0604;
    }
    else if (jet.btagDeepCSV < 0.8001 && jet.btagDeepCSV > 0.4941) {
        //if (jet.nVertexTracks == 0) correction *= 0.8008;
        //else if (jet.nVertexTracks == 1) correction *= 0.9834;
        if (jet.nVertexTracks == 2) correction *= 1.0112;
        else if (jet.nVertexTracks == 3) correction *= 1.0543;
        else if (jet.nVertexTracks == 4) correction *= 1.0717;
        else if (jet.nVertexTracks == 5) correction *= 1.0728;
        else if (jet.nVertexTracks >= 6) correction *= 1.0801;
    }
    else if (jet.btagDeepCSV < 0.4941 && jet.btagDeepCSV > 0.1522) {
        //if (jet.nVertexTracks == 0) correction *= 0.9431;
        //else if (jet.nVertexTracks == 1) correction *= 1.0433;
        if (jet.nVertexTracks == 2) correction *= 1.0570;
        else if (jet.nVertexTracks == 3) correction *= 1.0798;
        else if (jet.nVertexTracks == 4) correction *= 1.0867;
        else if (jet.nVertexTracks == 5) correction *= 1.0906;
        else if (jet.nVertexTracks >= 6) correction *= 1.0917;
    };*/


  }
  //std::cout << "----- C++ -----" << "Total correction correction " << correction << std::endl;//Temp DEBUG
  //std::cin.get();//Temp DEBUG
  return correction;
}



template <typename T>
TTreeReaderArray<T>* TreeDescriptionMC<T>::get_correction_branch(Systematic::SystId syst_id) {
    return this->jets_pt_corr.GetValue(syst_id);
}

template class TreeDescription<float>;
template class TreeDescription<double>;

template class TreeDescriptionMC<float>;
template class TreeDescriptionMC<double>;

template class TreeDescriptionMCSystematic<float>;
template class TreeDescriptionMCSystematic<double>;

template class TreeDescriptionMCBOOSTED<float>;
template class TreeDescriptionMCBOOSTED<double>;

template class TreeDescriptionBOOSTED<float>;
template class TreeDescriptionBOOSTED<double>;

} //namespace TTH_MEAnalysis
