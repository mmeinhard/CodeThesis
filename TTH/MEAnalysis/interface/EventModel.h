#ifndef EVENTMODEL_H // header guards
#define EVENTMODEL_H

#include <iostream>
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH1D.h"
#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

#include "LHAPDF/LHAPDF.h"

namespace TTH_MEAnalysis {

class Jet {
public:
    TLorentzVector lv;
    double btagCSV;
    double btagDeepCSV;
    double btagDeepFlav;
    int flav;
    float btagFlag;
    float dRmin;
    //double nVertexTracks;
  
 Jet() : lv(TLorentzVector()), btagCSV(-10), btagDeepCSV(-10), btagDeepFlav(-10), flav(-10), btagFlag(-10), dRmin(-10){}

 Jet(TLorentzVector lv, double btagCSV, double btagDeepCSV, double btagDeepFlav) :
    lv(lv),
    btagCSV(btagCSV),
    btagDeepCSV(btagDeepCSV),
    btagDeepFlav(btagDeepFlav),
    flav(-10),
    btagFlag(-10),
    dRmin(-10)
    //nVertexTracks(-10)
    {
    }
 Jet(TLorentzVector lv, double btagCSV, double btagDeepCSV, double btagDeepFlav, int hadFlav) :
    lv(lv),
    btagCSV(btagCSV),
    btagDeepCSV(btagDeepCSV),
    btagDeepFlav(btagDeepFlav),
    flav(hadFlav),
    btagFlag(-10),
    dRmin(-10)
    //nVertexTracks(nVertexTracks)
    {
    }
  Jet(TLorentzVector lv, double btagCSV, double btagDeepCSV, double btagDeepFlav, int hadFlav, float bFlag, float dR) : //Full jet for MC
    lv(lv),
    btagCSV(btagCSV),
    btagDeepCSV(btagDeepCSV),
    btagDeepFlav(btagDeepFlav),
    flav(hadFlav),
    btagFlag(bFlag),
    dRmin(dR)
    //nVertexTracks(nVertexTracks)
    {
    }
  Jet(TLorentzVector lv, double btagCSV, double btagDeepCSV, double btagDeepFlav, float bFlag, float dR) : //Full jet for Data
    lv(lv),
    btagCSV(btagCSV),
    btagDeepCSV(btagDeepCSV),
    btagDeepFlav(btagDeepFlav),
    flav(-1),
    btagFlag(bFlag),
    dRmin(dR)
    //VertexTracks(-10)
    {
    }
};

class Lepton {
public:
    TLorentzVector lv;
    double charge;
    int pdgId;

    Lepton() : lv(TLorentzVector()), charge(0), pdgId(0) {}

    Lepton(TLorentzVector lv, double charge, int pdgId) :
    lv(lv),
    charge(charge),
    pdgId(pdgId)
    {
    }
};

class higgsCandidates {
public:
    TLorentzVector lv;
    float msoftdrop;
    float tau21;
    float bbtag;
    float sj1btag;
    float sj2btag;
    float sj1pt;
    float sj2pt;

    higgsCandidates() : lv(TLorentzVector()), msoftdrop(0),tau21(0),bbtag(0),sj1btag(0),sj2btag(0),sj1pt(0),sj2pt(0) {}

    higgsCandidates(TLorentzVector lv, float msoftdrop,float tau21,float bbtag,float sj1btag,float sj2btag,float sj1pt,float sj2pt) :
    lv(lv),
    msoftdrop(msoftdrop),
    tau21(tau21),
    bbtag(bbtag),
    sj1btag(sj1btag),
    sj2btag(sj2btag),
    sj1pt(sj1pt),
    sj2pt(sj2pt)
    {
    }
};

class topCandidates {
public:
    TLorentzVector lv;
    float tau32SD;
    float fRec;
    float delRopt;
    float sj1btag;
    float sj2btag;
    float sj3btag;
    float sj1pt;
    float sj2pt;
    float sj3pt;

    topCandidates() : lv(TLorentzVector()), tau32SD(0),fRec(0),delRopt(0),sj1btag(0),sj2btag(0),sj3btag(0),sj1pt(0),sj2pt(0),sj3pt(0) {}

    topCandidates(TLorentzVector lv,float tau32SD,float fRec,float delRopt,float sj1btag,float sj2btag,float sj3btag,float sj1pt,float sj2pt,float sj3pt) :
    lv(lv),
    tau32SD(tau32SD),
    fRec(fRec),
    delRopt(delRopt),
    sj1btag(sj1btag),
    sj2btag(sj2btag),
    sj3btag(sj3btag),
    sj1pt(sj1pt),
    sj2pt(sj2pt),
    sj3pt(sj3pt)
    {
    }
};


class SampleDescription {
public:
    enum Schema {
        MC,
        DATA,
        MCBOOSTED,
        DATABOOSTED,
    };

    Schema schema;

    SampleDescription(Schema _schema) : schema(_schema) {};

    bool isMC() const {
        return schema == MC;
    }


};

namespace Systematic {

    enum Event {
        Nominal,
        CMS_scale_j,
        CMS_res_j,
    
        CMS_scaleAbsoluteMPFBias_j,
        CMS_scaleAbsoluteStat_j,
        CMS_scaleAbsoluteScale_j,
        CMS_scaleFlavorQCD_j,
        CMS_scaleFragmentation_j,
        CMS_scalePileUpDataMC_j,
        CMS_scalePileUpPtBB_j,
        CMS_scalePileUpPtEC1_j,
        //CMS_scalePileUpPtEC2_j,
        //CMS_scalePileUpPtHF_j,
        CMS_scalePileUpPtRef_j,
        CMS_scaleRelativeBal_j,
        CMS_scaleRelativeFSR_j,
        CMS_scaleRelativeJEREC1_j,
        //CMS_scaleRelativeJEREC2_j,
        //CMS_scaleRelativeJERHF_j,
        CMS_scaleRelativePtBB_j,
        CMS_scaleRelativePtEC1_j,
        //CMS_scaleRelativePtEC2_j,
        //CMS_scaleRelativePtHF_j,
        CMS_scaleRelativeStatFSR_j,
        CMS_scaleRelativeStatEC_j,
        //CMS_scaleRelativeStatHF_j,
        CMS_scaleSinglePionECAL_j,
        CMS_scaleSinglePionHCAL_j,
        CMS_scaleTimePtEta_j,
    
        CMS_btag,
        CMS_btag_cferr1,
        CMS_btag_cferr2,
        CMS_btag_hf,
        CMS_btag_hfstats1,
        CMS_btag_hfstats2,
        CMS_btag_lf,
        CMS_btag_lfstats1,
        CMS_btag_lfstats2,

        CMS_btag_boosted,
        CMS_btag_boosted_cferr1,
        CMS_btag_boosted_cferr2,
        CMS_btag_boosted_hf,
        CMS_btag_boosted_hfstats1,
        CMS_btag_boosted_hfstats2,
        CMS_btag_boosted_lf,
        CMS_btag_boosted_lfstats1,
        CMS_btag_boosted_lfstats2,

        CMS_btag_jesAbsoluteMPFBias,
        CMS_btag_jesAbsoluteScale,
        CMS_btag_jesAbsoluteStat,
        CMS_btag_jesFlavorQCD,
        CMS_btag_jesFragmentation,
        CMS_btag_jesPileUpDataMC,
        CMS_btag_jesPileUpPtBB,
        CMS_btag_jesPileUpPtEC1,
        //CMS_btag_jesPileUpPtEC2,
        //CMS_btag_jesPileUpPtHF,
        CMS_btag_jesPileUpPtRef,
        CMS_btag_jesRelativeBal,
        CMS_btag_jesRelativeFSR,
        CMS_btag_jesRelativeJEREC1,
        //CMS_btag_jesRelativeJEREC2,
        //CMS_btag_jesRelativeJERHF,
        CMS_btag_jesRelativePtBB,
        CMS_btag_jesRelativePtEC1,
        //CMS_btag_jesRelativePtEC2,
        //CMS_btag_jesRelativePtHF,
        CMS_btag_jesRelativeStatFSR,
        CMS_btag_jesRelativeStatEC,
        //CMS_btag_jesRelativeStatHF,
        CMS_btag_jesSinglePionECAL,
        CMS_btag_jesSinglePionHCAL,
        CMS_btag_jesTimePtEta,

        CMS_btag_boosted_jesAbsoluteMPFBias,
        CMS_btag_boosted_jesAbsoluteScale,
        CMS_btag_boosted_jesAbsoluteStat,
        CMS_btag_boosted_jesFlavorQCD,
        CMS_btag_boosted_jesFragmentation,
        CMS_btag_boosted_jesPileUpDataMC,
        CMS_btag_boosted_jesPileUpPtBB,
        CMS_btag_boosted_jesPileUpPtEC1,
        CMS_btag_boosted_jesPileUpPtRef,
        CMS_btag_boosted_jesRelativeBal,
        CMS_btag_boosted_jesRelativeFSR,
        CMS_btag_boosted_jesRelativeJEREC1,
        CMS_btag_boosted_jesRelativePtBB,
        CMS_btag_boosted_jesRelativePtEC1,
        CMS_btag_boosted_jesRelativeStatFSR,
        CMS_btag_boosted_jesRelativeStatEC,
        CMS_btag_boosted_jesSinglePionECAL,
        CMS_btag_boosted_jesSinglePionHCAL,
        CMS_btag_boosted_jesTimePtEta,

        CMS_btag_jes, //OLD. Only used in current tree --> use factorized 
    
        CMS_ttHbb_PDF,
        CMS_ttHbb_scaleMuF,
        CMS_ttHbb_scaleMuR,
        CMS_ttHbb_scaleME,

        CMS_ttHbb_FSR,
        CMS_ttHbb_ISR,

        CMS_ttHbb_qgWeight,
    
        CMS_pu,
        CMS_L1Prefiring,
        gen,

    };

    enum Direction {
        None,
        Up,
        Down
    };

    typedef std::pair<Systematic::Event, Systematic::Direction> SystId;

    bool is_jec(SystId syst_id);
    bool is_jer(SystId syst_id);
    bool is_nominal(SystId syst_id);

    const static auto syst_id_nominal = std::make_pair(Systematic::Nominal, Systematic::None);

    SystId make_id(Systematic::Event e, Systematic::Direction d);
} // namespace Systematic

template <typename T>
void attachSystematics(TTreeReader& reader, std::map<Systematic::SystId, T*>& values, const char* branch_name, bool add_nominal) {
    if (add_nominal) {
        values[std::make_pair(Systematic::Nominal, Systematic::None)] = new T(reader, branch_name);
    }

    const std::string brname(branch_name);

    values[std::make_pair(Systematic::CMS_scale_j, Systematic::Up)] = new T(reader, (brname + std::string("_TotalUp")).c_str());
    values[std::make_pair(Systematic::CMS_res_j, Systematic::Up)] = new T(reader, (brname + std::string("_JERUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleAbsoluteMPFBias_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteMPFBiasUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleAbsoluteStat_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteStatUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleAbsoluteScale_j, Systematic::Up)] = new T(reader, (brname + std::string("_AbsoluteScaleUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleFlavorQCD_j, Systematic::Up)] = new T(reader, (brname + std::string("_FlavorQCDUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleFragmentation_j, Systematic::Up)] = new T(reader, (brname + std::string("_FragmentationUp")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpDataMC_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpDataMCUp")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpPtBB_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtBBUp")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpPtEC1_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtEC1Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtEC2_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtEC2Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpPtRef_j, Systematic::Up)] = new T(reader, (brname + std::string("_PileUpPtRefUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeBal_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeBalUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeFSR_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeFSRUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeJEREC1_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeJEREC1Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJEREC2_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeJEREC2Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJERHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeJERHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativePtBB_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtBBUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativePtEC1_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtEC1Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtEC2_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtEC2Up")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativePtHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeStatFSR_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeStatFSRUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeStatEC_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeStatECUp")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatHF_j, Systematic::Up)] = new T(reader, (brname + std::string("_RelativeStatHFUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleSinglePionECAL_j, Systematic::Up)] = new T(reader, (brname + std::string("_SinglePionECALUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleSinglePionHCAL_j, Systematic::Up)] = new T(reader, (brname + std::string("_SinglePionHCALUp")).c_str());
    values[std::make_pair(Systematic::CMS_scaleTimePtEta_j, Systematic::Up)] = new T(reader, (brname + std::string("_TimePtEtaUp")).c_str());

    values[std::make_pair(Systematic::CMS_scale_j, Systematic::Down)] = new T(reader, (brname + std::string("_TotalDown")).c_str());
    values[std::make_pair(Systematic::CMS_res_j, Systematic::Down)] = new T(reader, (brname + std::string("_JERDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleAbsoluteMPFBias_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteMPFBiasDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleAbsoluteStat_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteStatDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleAbsoluteScale_j, Systematic::Down)] = new T(reader, (brname + std::string("_AbsoluteScaleDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleFlavorQCD_j, Systematic::Down)] = new T(reader, (brname + std::string("_FlavorQCDDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleFragmentation_j, Systematic::Down)] = new T(reader, (brname + std::string("_FragmentationDown")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpDataMC_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpDataMCDown")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpPtBB_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtBBDown")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpPtEC1_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtEC1Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtEC2_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtEC2Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scalePileUpPtHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_scalePileUpPtRef_j, Systematic::Down)] = new T(reader, (brname + std::string("_PileUpPtRefDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeBal_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeBalDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeFSR_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeFSRDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeJEREC1_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeJEREC1Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJEREC2_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeJEREC2Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeJERHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeJERHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativePtBB_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtBBDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativePtEC1_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtEC1Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtEC2_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtEC2Down")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativePtHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativePtHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeStatFSR_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeStatFSRDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleRelativeStatEC_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeStatECDown")).c_str());
    //values[std::make_pair(Systematic::CMS_scaleRelativeStatHF_j, Systematic::Down)] = new T(reader, (brname + std::string("_RelativeStatHFDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleSinglePionECAL_j, Systematic::Down)] = new T(reader, (brname + std::string("_SinglePionECALDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleSinglePionHCAL_j, Systematic::Down)] = new T(reader, (brname + std::string("_SinglePionHCALDown")).c_str());
    values[std::make_pair(Systematic::CMS_scaleTimePtEta_j, Systematic::Down)] = new T(reader, (brname + std::string("_TimePtEtaDown")).c_str());
}

template <typename T>
class TTreeReaderValueSystematic {
public:
    std::map<Systematic::SystId, TTreeReaderValue<T>* > values;

    TTreeReaderValueSystematic(TTreeReader& reader, const char* branch_name, bool add_nominal = true) {
        attachSystematics<TTreeReaderValue<T>>(reader, values, branch_name, add_nominal); 
    }

    T GetValue(Systematic::SystId syst_id) {
        if (!values.count(syst_id)) {
            std::cerr << "could not find key " << syst_id.first << " " << syst_id.second << std::endl;
            throw std::exception();
        }
        return **values.at(syst_id);
    }

};

template <typename T>
class TTreeReaderArraySystematic {
public:
    std::map<Systematic::SystId, TTreeReaderArray<T>* > values;

    TTreeReaderArraySystematic(TTreeReader& reader, const char* branch_name, bool add_nominal = true) {
        attachSystematics<TTreeReaderArray<T>>(reader, values, branch_name, add_nominal); 
    }

    TTreeReaderArray<T>* GetValue(Systematic::SystId syst_id) {
        return values.at(syst_id);
    }
};

//Static (unchangin) data type that represents the event content
class EventDescription {
public:
    //int evt1;
    //int evt2;
    //float evt;
    unsigned int run;
    unsigned int lumi;
    int json;
    int passMETFilters;

    std::vector<Lepton> leptons;
    std::vector<Jet> jets;
    std::vector<int> jets_hadronFlavour;
    //std::vector<double> jets_nVertexTracks;
    std::vector<Jet> boosted_bjets;
    std::vector<Jet> boosted_ljets;
    std::vector<int> boosted_bjets_hadronFlavour;
    std::vector<int> boosted_ljets_hadronFlavour;
    
    
    std::vector<float> leps_superclustereta;

    int ttCls;
    int genHiggsDecayMode;
    float Pileup_nTrueInt;
    float genTopLep_pt;
    float genTopHad_pt;
    int is_sl;
    int is_dl;
    int is_fh;
    int passPV;
    int numJets;
    int nBDeepCSVM;
    int nBDeepFlavM;
    //int nBCSVM;
    int nPVs;

    int HLT_ttH_SL_mu;
    int HLT_ttH_SL_el;
    int HLT_ttH_DL_mumu;
    int HLT_ttH_DL_elmu;
    int HLT_ttH_DL_elel;
    int HLT_ttH_FH;

    double btag_LR_4b_2b_btagCSV;
    double mem_DL_0w2h2t_p;
    double mem_SL_0w2h2t_p;
    double mem_SL_1w2h2t_p;
    double mem_SL_2w2h2t_p;

    double Wmass;
    double met_pt;
    double met_phi;

    Systematic::SystId syst_id;
    std::map<Systematic::SystId, double> weights;


    float n_boosted_bjets;
    float n_boosted_ljets;
    float boosted;
    int resolved; 

    std::vector<higgsCandidates> higgsCandidate;
    std::vector<topCandidates> topCandidate;

    double mem_DL_0w2h2t_sj_p;
    double mem_SL_0w2h2t_sj_p;
    double mem_SL_1w2h2t_sj_p;
    double mem_SL_2w2h2t_sj_p;
    double mem_DL_0w2h2t_sj_perm_higgs_p;
    double mem_SL_0w2h2t_sj_perm_higgs_p;
    double mem_SL_1w2h2t_sj_perm_higgs_p;
    double mem_SL_2w2h2t_sj_perm_higgs_p;
    double mem_SL_2w2h2t_sj_perm_top_p;
    double mem_SL_2w2h2t_sj_perm_tophiggs_p;
};

//Translates a tthbb13 TTree to an EventDescription
template <typename T>
class TreeDescription {
public:

    TTreeReader reader;

    //TTreeReaderValue<float> evt;
    //TTreeReaderValue<int> evt1;
    //TTreeReaderValue<int> evt2;
    TTreeReaderValue<int> run;
    TTreeReaderValue<int> lumi;
    TTreeReaderValue<int> json;
    TTreeReaderValue<int> passMETFilters;

    TTreeReaderValue<int> is_sl;
    TTreeReaderValue<int> is_dl;
    TTreeReaderValue<int> is_fh;

    TTreeReaderValue<int> passPV;
    
    TTreeReaderValue<int> HLT_ttH_SL_mu;
    TTreeReaderValue<int> HLT_ttH_SL_el;
    TTreeReaderValue<int> HLT_ttH_DL_elmu;
    TTreeReaderValue<int> HLT_ttH_DL_elel;
    TTreeReaderValue<int> HLT_ttH_DL_mumu;
    //TTreeReaderValue<int> HLT_ttH_FH;

    TTreeReaderValue<int> numJets;
    TTreeReaderValue<int> nBDeepCSVM;
    TTreeReaderValue<int> nBDeepFlavM;
    //TTreeReaderValue<int> nBCSVM;
    TTreeReaderValue<T> nPVs;
    
    TTreeReaderValue<int> nleps;
    TTreeReaderArray<T> leps_pdgId;
    TTreeReaderArray<T> leps_pt;
    TTreeReaderArray<T> leps_eta;
    TTreeReaderArray<T> leps_phi;
    TTreeReaderArray<T> leps_mass;
    TTreeReaderArray<T> leps_scEta;

    TTreeReaderValue<int> njets;
    TTreeReaderArray<T> jets_pt;
    TTreeReaderArray<T> jets_eta;
    TTreeReaderArray<T> jets_phi;
    TTreeReaderArray<T> jets_mass;
    TTreeReaderArray<T> jets_btagCSV;
    TTreeReaderArray<T> jets_btagDeepCSV;
    TTreeReaderArray<T> jets_btagDeepFlav;
    TTreeReaderArray<T> jets_btagFlag;
    TTreeReaderArray<T> jets_dRmin;
    //TTreeReaderArray<T> jets_nVertexTracks;



    TTreeReaderValue<T> btag_LR_4b_2b_btagCSV;
    TTreeReaderValue<T> mem_DL_0w2h2t_p;
    TTreeReaderValue<T> mem_SL_0w2h2t_p;
    TTreeReaderValue<T> mem_SL_1w2h2t_p;
    TTreeReaderValue<T> mem_SL_2w2h2t_p;

    TTreeReaderValue<T> Wmass;
    TTreeReaderValue<T> met_pt;
    TTreeReaderValue<T> met_phi;

    std::map<Systematic::SystId, TTreeReaderArray<T>*> correction_branches;

    SampleDescription sample;

    TreeDescription(TFile* file, SampleDescription sample) :
        reader("tree", file),
        //evt(reader, "evt"),
        //evt1(reader, "evt1"),
        //evt2(reader, "evt2"),
        run(reader, "run"),
        lumi(reader, "lumi"),
        json(reader, "json"),
        passMETFilters(reader, "passMETFilters"),

        is_sl(reader, "is_sl"),
        is_dl(reader, "is_dl"),
        is_fh(reader, "is_fh"),

        passPV(reader, "passPV"),
       
        HLT_ttH_SL_mu(reader, "HLT_ttH_SL_mu"),
        HLT_ttH_SL_el(reader, "HLT_ttH_SL_el"),
        HLT_ttH_DL_elmu(reader, "HLT_ttH_DL_elmu"),
        HLT_ttH_DL_elel(reader, "HLT_ttH_DL_elel"),
        HLT_ttH_DL_mumu(reader, "HLT_ttH_DL_mumu"),
        //HLT_ttH_FH(reader, "HLT_ttH_FH"),
        
        numJets(reader, "numJets"),
        nBDeepCSVM(reader, "nBDeepCSVM"),
        nBDeepFlavM(reader, "nBDeepFlavM"),
        //nBCSVM(reader, "nBCSVM"),
        nPVs(reader, "nPVs"),
        
        nleps(reader, "nleps"),
        leps_pdgId(reader, "leps_pdgId"),
        leps_pt(reader, "leps_pt"),
        leps_eta(reader, "leps_eta"),
        leps_phi(reader, "leps_phi"),
        leps_mass(reader, "leps_mass"),
        //FIXME: add scEta to tthbb13 tree
        leps_scEta(reader, "leps_eta"),

        njets(reader, "njets"),
        jets_pt(reader, "jets_pt"),
        jets_eta(reader, "jets_eta"),
        jets_phi(reader, "jets_phi"),
        jets_mass(reader, "jets_mass"),
        jets_btagCSV(reader, "jets_btagCSV"),
        jets_btagDeepCSV(reader, "jets_btagDeepCSV"),
        jets_btagDeepFlav(reader, "jets_btagDeepFlav"),
        jets_btagFlag(reader, "jets_btagFlag"),
        jets_dRmin(reader, "jets_dRmin"),
        //jets_nVertexTracks(reader, "jets_nVertexTracks"),




        btag_LR_4b_2b_btagCSV(reader, "btag_LR_4b_2b_btagCSV"),
        mem_DL_0w2h2t_p(reader, "mem_DL_0w2h2t_p"),
        mem_SL_0w2h2t_p(reader, "mem_SL_0w2h2t_p"),
        mem_SL_1w2h2t_p(reader, "mem_SL_1w2h2t_p"),
        mem_SL_2w2h2t_p(reader, "mem_SL_2w2h2t_p"),
 
        Wmass(reader, "Wmass"),
        met_pt(reader, "met_pt"),
        met_phi(reader, "met_phi"),


        sample(sample) {
    }
    virtual ~TreeDescription() {}

    std::vector<Lepton> build_leptons(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_jets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

template <typename T>
class TreeDescriptionBOOSTED : public TreeDescription<T> {
public:


    TTreeReaderValue<float>  n_boosted_bjets;
    TTreeReaderValue<float>  n_boosted_ljets;
    TTreeReaderValue<float>  boosted;
    TTreeReaderValue<int> resolved;

    //TTreeReaderArray<int> boosted_bjets_hadronFlavour;
    //TTreeReaderArray<int> boosted_ljets_hadronFlavour;

    TTreeReaderArray<T> boosted_bjets_pt;
    TTreeReaderArray<T> boosted_bjets_eta;
    TTreeReaderArray<T> boosted_bjets_phi;
    TTreeReaderArray<T> boosted_bjets_mass;
    TTreeReaderArray<T> boosted_bjets_btag;

    TTreeReaderArray<T> boosted_ljets_pt;
    TTreeReaderArray<T> boosted_ljets_eta;
    TTreeReaderArray<T> boosted_ljets_phi;
    TTreeReaderArray<T> boosted_ljets_mass;
    TTreeReaderArray<T> boosted_ljets_btag;

    TTreeReaderValue<int> nhiggsCandidate;
    TTreeReaderArray<T> higgsCandidate_pt;
    TTreeReaderArray<T> higgsCandidate_eta;
    TTreeReaderArray<T> higgsCandidate_phi;
    TTreeReaderArray<T> higgsCandidate_mass;
    TTreeReaderArray<T> higgsCandidate_msoftdrop; 
    TTreeReaderArray<T> higgsCandidate_tau21;
    TTreeReaderArray<T> higgsCandidate_bbtag;
    TTreeReaderArray<T> higgsCandidate_sj1btag;
    TTreeReaderArray<T> higgsCandidate_sj2btag;
    TTreeReaderArray<T> higgsCandidate_sj1pt;
    TTreeReaderArray<T> higgsCandidate_sj2pt;

    TTreeReaderValue<int> ntopCandidate;
    TTreeReaderArray<T> topCandidate_pt;
    TTreeReaderArray<T> topCandidate_eta;
    TTreeReaderArray<T> topCandidate_phi;
    TTreeReaderArray<T> topCandidate_mass;
    TTreeReaderArray<T> topCandidate_tau32SD;
    TTreeReaderArray<T> topCandidate_fRec;
    TTreeReaderArray<T> topCandidate_delRopt; 
    TTreeReaderArray<T> topCandidate_sj1btag;
    TTreeReaderArray<T> topCandidate_sj2btag;
    TTreeReaderArray<T> topCandidate_sj3btag;
    TTreeReaderArray<T> topCandidate_sj1pt;
    TTreeReaderArray<T> topCandidate_sj2pt;
    TTreeReaderArray<T> topCandidate_sj3pt;

    TTreeReaderValue<T> mem_DL_0w2h2t_sj_p;
    TTreeReaderValue<T> mem_SL_0w2h2t_sj_p;
    TTreeReaderValue<T> mem_SL_1w2h2t_sj_p;
    TTreeReaderValue<T> mem_SL_2w2h2t_sj_p;
    TTreeReaderValue<T> mem_DL_0w2h2t_sj_perm_higgs_p;
    TTreeReaderValue<T> mem_SL_0w2h2t_sj_perm_higgs_p;
    TTreeReaderValue<T> mem_SL_1w2h2t_sj_perm_higgs_p;
    TTreeReaderValue<T> mem_SL_2w2h2t_sj_perm_higgs_p;
    TTreeReaderValue<T> mem_SL_2w2h2t_sj_perm_top_p;
    TTreeReaderValue<T> mem_SL_2w2h2t_sj_perm_tophiggs_p;


    TreeDescriptionBOOSTED(TFile* file, SampleDescription sample) :
        TreeDescription<T>(file, sample),
        n_boosted_bjets(TreeDescription<T>::reader, "n_boosted_bjets"),
        n_boosted_ljets(TreeDescription<T>::reader, "n_boosted_ljets"),
        boosted(TreeDescription<T>::reader, "boosted"),
	resolved(TreeDescription<T>::reader, "resolved"),

        //boosted_bjets_hadronFlavour(TreeDescription<T>::reader, "boosted_bjets_hadronFlavour"),
        //boosted_ljets_hadronFlavour(TreeDescription<T>::reader, "boosted_ljets_hadronFlavour"),


        boosted_bjets_pt(TreeDescription<T>::reader, "boosted_bjets_pt"),
        boosted_bjets_eta(TreeDescription<T>::reader, "boosted_bjets_eta"),
        boosted_bjets_phi(TreeDescription<T>::reader, "boosted_bjets_phi"),
        boosted_bjets_mass(TreeDescription<T>::reader, "boosted_bjets_mass"),
        boosted_bjets_btag(TreeDescription<T>::reader, "boosted_bjets_btag"),

        boosted_ljets_pt(TreeDescription<T>::reader, "boosted_ljets_pt"),
        boosted_ljets_eta(TreeDescription<T>::reader, "boosted_ljets_eta"),
        boosted_ljets_phi(TreeDescription<T>::reader, "boosted_ljets_phi"),
        boosted_ljets_mass(TreeDescription<T>::reader, "boosted_ljets_mass"),
        boosted_ljets_btag(TreeDescription<T>::reader, "boosted_ljets_btag"),

        nhiggsCandidate(TreeDescription<T>::reader, "nhiggsCandidate"),
        higgsCandidate_pt(TreeDescription<T>::reader, "higgsCandidate_pt"),
        higgsCandidate_eta(TreeDescription<T>::reader, "higgsCandidate_eta"),
        higgsCandidate_phi(TreeDescription<T>::reader, "higgsCandidate_phi"),
        higgsCandidate_mass(TreeDescription<T>::reader, "higgsCandidate_mass"),
        higgsCandidate_msoftdrop(TreeDescription<T>::reader, "higgsCandidate_msoftdrop"),
        higgsCandidate_tau21(TreeDescription<T>::reader, "higgsCandidate_tau21"),
        higgsCandidate_bbtag(TreeDescription<T>::reader, "higgsCandidate_bbtag"),
        higgsCandidate_sj1btag(TreeDescription<T>::reader, "higgsCandidate_sj1btag"),
        higgsCandidate_sj2btag(TreeDescription<T>::reader, "higgsCandidate_sj2btag"),
        higgsCandidate_sj1pt(TreeDescription<T>::reader, "higgsCandidate_sj1pt"),
        higgsCandidate_sj2pt(TreeDescription<T>::reader, "higgsCandidate_sj2pt"),

        ntopCandidate(TreeDescription<T>::reader, "ntopCandidate"),
        topCandidate_pt(TreeDescription<T>::reader, "topCandidate_pt"),
        topCandidate_eta(TreeDescription<T>::reader, "topCandidate_eta"),
        topCandidate_phi(TreeDescription<T>::reader, "topCandidate_phi"),
        topCandidate_mass(TreeDescription<T>::reader, "topCandidate_mass"),
        topCandidate_tau32SD(TreeDescription<T>::reader, "topCandidate_tau32SD"),
        topCandidate_fRec(TreeDescription<T>::reader, "topCandidate_fRec"),
        topCandidate_delRopt(TreeDescription<T>::reader, "topCandidate_delRopt"),
        topCandidate_sj1btag(TreeDescription<T>::reader, "topCandidate_sj1btag"),
        topCandidate_sj2btag(TreeDescription<T>::reader, "topCandidate_sj2btag"),
        topCandidate_sj3btag(TreeDescription<T>::reader, "topCandidate_sj3btag"),
        topCandidate_sj1pt(TreeDescription<T>::reader, "topCandidate_sj1pt"),
        topCandidate_sj2pt(TreeDescription<T>::reader, "topCandidate_sj2pt"),
        topCandidate_sj3pt(TreeDescription<T>::reader, "topCandidate_sj3pt"),

        mem_DL_0w2h2t_sj_p(TreeDescription<T>::reader, "mem_DL_0w2h2t_sj_p"),
        mem_SL_0w2h2t_sj_p(TreeDescription<T>::reader, "mem_SL_0w2h2t_sj_p"),
        mem_SL_1w2h2t_sj_p(TreeDescription<T>::reader, "mem_SL_1w2h2t_sj_p"),
        mem_SL_2w2h2t_sj_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_p"),
        mem_DL_0w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_DL_0w2h2t_sj_perm_higgs_p"),
        mem_SL_0w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_SL_0w2h2t_sj_perm_higgs_p"),
        mem_SL_1w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_SL_1w2h2t_sj_perm_higgs_p"),
        mem_SL_2w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_perm_higgs_p"),
        mem_SL_2w2h2t_sj_perm_top_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_perm_top_p"),
        mem_SL_2w2h2t_sj_perm_tophiggs_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_perm_tophiggs_p")
    {}
    ~TreeDescriptionBOOSTED() {}

    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_boosted_bjets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_boosted_ljets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    std::vector<higgsCandidates> build_higgsCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    std::vector<topCandidates> build_topCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
 };

template <typename T>
class TreeDescriptionMCSystematic : public TreeDescription<T> {
public:

    TTreeReaderValue<int> ttCls;
    TTreeReaderValue<int> genHiggsDecayMode;
    TTreeReaderValue<float> Pileup_nTrueInt;
    TTreeReaderValue<T> genTopHad_pt;
    TTreeReaderValue<T> genTopLep_pt;
    
    TTreeReaderValue<T> genWeight;
    TTreeReaderValue<T> puWeight;
    TTreeReaderValue<T> L1PrefireWeight;
    //TTreeReaderValue<T> btagWeight_shape;
    
    TreeDescriptionMCSystematic(TFile* file, SampleDescription sample) :
        TreeDescription<T>(file, sample),
        ttCls(TreeDescription<T>::reader, "ttCls"),
        genHiggsDecayMode(TreeDescription<T>::reader, "genHiggsDecayMode"),
        Pileup_nTrueInt(TreeDescription<T>::reader, "Pileup_nTrueInt"),
        genTopHad_pt(TreeDescription<T>::reader, "genTopHad_pt"),
        genTopLep_pt(TreeDescription<T>::reader, "genTopLep_pt"),
        genWeight(TreeDescription<T>::reader, "genWeight"),
        puWeight(TreeDescription<T>::reader, "puWeight"),
        L1PrefireWeight(TreeDescription<T>::reader, "L1PrefireWeight")
        //btagWeight_shape(TreeDescription<T>::reader, "btagWeight_shape")
    {}
    
    ~TreeDescriptionMCSystematic() {}
    
    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

template <typename T>
class TreeDescriptionMC : public TreeDescription<T> {
public:

    TTreeReaderValue<int> ttCls;
    TTreeReaderValue<int> genHiggsDecayMode;
    TTreeReaderValue<float> Pileup_nTrueInt;
    TTreeReaderValue<T> genTopHad_pt;
    TTreeReaderValue<T> genTopLep_pt;

    TTreeReaderValueSystematic<int> numJets;
    TTreeReaderValueSystematic<int> nBDeepCSVM;
    TTreeReaderValueSystematic<int> nBDeepFlavM;
    //TTreeReaderValueSystematic<int> nBCSVM;

    TTreeReaderArray<int> jets_hadronFlavour;
    //TTreeReaderArray<T> jets_nVertexTracks;
    TTreeReaderArraySystematic<T> jets_pt_corr;

    TTreeReaderValueSystematic<T> mem_DL_0w2h2t_p;
    TTreeReaderValueSystematic<T> mem_SL_0w2h2t_p;
    TTreeReaderValueSystematic<T> mem_SL_1w2h2t_p;
    TTreeReaderValueSystematic<T> mem_SL_2w2h2t_p;

    TTreeReaderValue<T> genWeight;
    
    TTreeReaderValue<T> puWeight;
    TTreeReaderValue<T> puWeightUp;
    TTreeReaderValue<T> puWeightDown;

    TTreeReaderValue<T> L1PrefireWeight;
    TTreeReaderValue<T> L1PrefireWeightUp;
    TTreeReaderValue<T> L1PrefireWeightDown;

    
    TTreeReaderArray<T> LHEPDFWeights;
    TTreeReaderArray<T> LHEScaleWeights;
    TTreeReaderValue<int> nLHEPDFWeights;
    TTreeReaderValue<int> nLHEScaleWeights;


    TTreeReaderValue<T> PSWeight_FSR_Down;
    TTreeReaderValue<T> PSWeight_FSR_Up;
    TTreeReaderValue<T> PSWeight_ISR_Down;
    TTreeReaderValue<T> PSWeight_ISR_Up;

    
    //TTreeReaderValue<T> btagWeight_shape;
    //TTreeReaderValue<T> btagWeight_shape_cferr1Up;
    //TTreeReaderValue<T> btagWeight_shape_cferr2Up;
    //TTreeReaderValue<T> btagWeight_shape_hfUp;
    //TTreeReaderValue<T> btagWeight_shape_hfstats1Up;
    //TTreeReaderValue<T> btagWeight_shape_hfstats2Up;
    //TTreeReaderValue<T> btagWeight_shape_jesUp;
    //TTreeReaderValue<T> btagWeight_shape_lfUp;
    //TTreeReaderValue<T> btagWeight_shape_lfstats1Up;
    //TTreeReaderValue<T> btagWeight_shape_lfstats2Up;
    //
    //TTreeReaderValue<T> btagWeight_shape_cferr1Down;
    //TTreeReaderValue<T> btagWeight_shape_cferr2Down;
    //TTreeReaderValue<T> btagWeight_shape_hfDown;
    //TTreeReaderValue<T> btagWeight_shape_hfstats1Down;
    //TTreeReaderValue<T> btagWeight_shape_hfstats2Down;
    //TTreeReaderValue<T> btagWeight_shape_jesDown;
    //TTreeReaderValue<T> btagWeight_shape_lfDown;
    //TTreeReaderValue<T> btagWeight_shape_lfstats1Down;
    //TTreeReaderValue<T> btagWeight_shape_lfstats2Down;


    BTagCalibrationReader BCalibReader;
    BTagCalibration calib;
    std::set<std::string> shapeCorr_bFlav;
    std::set<std::string> shapeCorr_cFlav;
    std::set<std::string> shapeCorr_udsgFlav;
    std::set<std::string> shapeCorr_jes;

    bool BCalibInitialized;
    std::string BTagCalibType;
    virtual void initBCalibration(std::string Calib_file, std::string type);
    virtual float calcBTagCorr(std::string thisSystematic, std::vector<Jet> jets, std::string disc);


    //TTreeReaderArray<T> LHE_weights_scale_wgt;
    
    TreeDescriptionMC(TFile* file, SampleDescription sample) :
        TreeDescription<T>(file, sample),
        ttCls(TreeDescription<T>::reader, "ttCls"),
        genHiggsDecayMode(TreeDescription<T>::reader, "genHiggsDecayMode"),
        Pileup_nTrueInt(TreeDescription<T>::reader, "Pileup_nTrueInt"),
        genTopHad_pt(TreeDescription<T>::reader, "genTopHad_pt"),
        genTopLep_pt(TreeDescription<T>::reader, "genTopLep_pt"),
        
        numJets(TreeDescription<T>::reader, "numJets"),
        nBDeepCSVM(TreeDescription<T>::reader, "nBDeepCSVM"),
        nBDeepFlavM(TreeDescription<T>::reader, "nBDeepFlavM"),
        //nBCSVM(TreeDescription<T>::reader, "nBCSVM"),

        jets_hadronFlavour(TreeDescription<T>::reader, "jets_hadronFlavour"),
        //jets_nVertexTracks(TreeDescription<T>::reader, "jets_nVertexTracks"),
        jets_pt_corr(TreeDescription<T>::reader, "jets_pt_corr", false),

        mem_DL_0w2h2t_p(TreeDescription<T>::reader, "mem_DL_0w2h2t_p"),
        mem_SL_0w2h2t_p(TreeDescription<T>::reader, "mem_SL_0w2h2t_p"),
        mem_SL_1w2h2t_p(TreeDescription<T>::reader, "mem_SL_1w2h2t_p"),
        mem_SL_2w2h2t_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_p"),

        genWeight(TreeDescription<T>::reader, "genWeight"),

        puWeight(TreeDescription<T>::reader, "puWeight"),
        puWeightUp(TreeDescription<T>::reader, "puWeightUp"),
        puWeightDown(TreeDescription<T>::reader, "puWeightDown"),

        L1PrefireWeight(TreeDescription<T>::reader, "L1PrefireWeight"),
        L1PrefireWeightUp(TreeDescription<T>::reader, "L1PrefireWeight_Up"),
        L1PrefireWeightDown(TreeDescription<T>::reader, "L1PrefireWeight_Down"),

        
        LHEPDFWeights(TreeDescription<T>::reader, "LHEPDFWeights_wgt"),
        LHEScaleWeights(TreeDescription<T>::reader, "LHEScaleWeights_wgt"),
        nLHEPDFWeights(TreeDescription<T>::reader, "nLHEPDFWeights"),
        nLHEScaleWeights(TreeDescription<T>::reader, "nLHEScaleWeights"),



        PSWeight_FSR_Down(TreeDescription<T>::reader, "PSWeight_FSR_Down"),
        PSWeight_FSR_Up(TreeDescription<T>::reader, "PSWeight_FSR_Up"),
        PSWeight_ISR_Down(TreeDescription<T>::reader, "PSWeight_ISR_Down"),
        PSWeight_ISR_Up(TreeDescription<T>::reader, "PSWeight_ISR_Up"),
      
        //btagWeight_shape(TreeDescription<T>::reader, "btagWeight_shape"),

        //btagWeight_shape_cferr1Up(TreeDescription<T>::reader, "btagWeight_shapeCFERR1Up"),
        //btagWeight_shape_cferr2Up(TreeDescription<T>::reader, "btagWeight_shapeCFERR2Up"),
        //btagWeight_shape_hfUp(TreeDescription<T>::reader, "btagWeight_shapeHFUp"),
        //btagWeight_shape_hfstats1Up(TreeDescription<T>::reader, "btagWeight_shapeHFSTATS1Up"),
        //btagWeight_shape_hfstats2Up(TreeDescription<T>::reader, "btagWeight_shapeHFSTATS2Up"),
        //btagWeight_shape_jesUp(TreeDescription<T>::reader, "btagWeight_shapeJESUp"),
        //btagWeight_shape_lfUp(TreeDescription<T>::reader, "btagWeight_shapeLFUp"),
        //btagWeight_shape_lfstats1Up(TreeDescription<T>::reader, "btagWeight_shapeLFSTATS1Up"),
        //btagWeight_shape_lfstats2Up(TreeDescription<T>::reader, "btagWeight_shapeLFSTATS2Up"),
        //
        //btagWeight_shape_cferr1Down(TreeDescription<T>::reader, "btagWeight_shapeCFERR1Down"),
        //btagWeight_shape_cferr2Down(TreeDescription<T>::reader, "btagWeight_shapeCFERR2Down"),
        //btagWeight_shape_hfDown(TreeDescription<T>::reader, "btagWeight_shapeHFDown"),
        //btagWeight_shape_hfstats1Down(TreeDescription<T>::reader, "btagWeight_shapeHFSTATS1Down"),
        //btagWeight_shape_hfstats2Down(TreeDescription<T>::reader, "btagWeight_shapeHFSTATS2Down"),
        //btagWeight_shape_jesDown(TreeDescription<T>::reader, "btagWeight_shapeJESDown"),
        //btagWeight_shape_lfDown(TreeDescription<T>::reader, "btagWeight_shapeLFDown"),
        //btagWeight_shape_lfstats1Down(TreeDescription<T>::reader, "btagWeight_shapeLFSTATS1Down"),
        //btagWeight_shape_lfstats2Down(TreeDescription<T>::reader, "btagWeight_shapeLFSTATS2Down"),
        shapeCorr_bFlav({"up_lf", "down_lf", "up_hfstats1", "down_hfstats1", "up_hfstats2", "down_hfstats2"}),
        shapeCorr_cFlav({"up_cferr1", "down_cferr1",  "up_cferr2", "down_cferr2"}),
        shapeCorr_udsgFlav({"up_hf", "down_hf", "up_lfstats1", "down_lfstats1", "up_lfstats2", "down_lfstats2"}),
        BCalibInitialized(true),
        BTagCalibType("deepcsv")


        //LHE_weights_scale_wgt(TreeDescription<T>::reader, "LHE_weights_scale_wgt")
    {}
    
    ~TreeDescriptionMC() {}

    TTreeReaderArray<T>* get_correction_branch(Systematic::SystId syst_id = Systematic::syst_id_nominal);

    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal, std::vector<Jet> boosted_jets = std::vector<Jet>());
    virtual std::vector<Jet> build_jets(Systematic::SystId syst_id = Systematic::syst_id_nominal);

};

template <typename T>
class TreeDescriptionMCBOOSTED : public TreeDescriptionMC<T> {
public:

    TTreeReaderValue<float>  n_boosted_bjets;
    TTreeReaderValue<float>  n_boosted_ljets;
    TTreeReaderValue<float>  boosted;
    TTreeReaderValue<int> resolved;

    TTreeReaderArray<int> boosted_bjets_hadronFlavour;
    TTreeReaderArray<int> boosted_ljets_hadronFlavour;

    TTreeReaderArray<T> boosted_bjets_pt;
    TTreeReaderArray<T> boosted_bjets_eta;
    TTreeReaderArray<T> boosted_bjets_phi;
    TTreeReaderArray<T> boosted_bjets_mass;
    TTreeReaderArray<T> boosted_bjets_btag;

    TTreeReaderArray<T> boosted_ljets_pt;
    TTreeReaderArray<T> boosted_ljets_eta;
    TTreeReaderArray<T> boosted_ljets_phi;
    TTreeReaderArray<T> boosted_ljets_mass;
    TTreeReaderArray<T> boosted_ljets_btag;

    TTreeReaderValue<int> nhiggsCandidate;
    TTreeReaderArray<T> higgsCandidate_pt;
    TTreeReaderArray<T> higgsCandidate_eta;
    TTreeReaderArray<T> higgsCandidate_phi;
    TTreeReaderArray<T> higgsCandidate_mass;
    TTreeReaderArray<T> higgsCandidate_msoftdrop; 
    TTreeReaderArray<T> higgsCandidate_tau21;
    TTreeReaderArray<T> higgsCandidate_bbtag;
    TTreeReaderArray<T> higgsCandidate_sj1btag;
    TTreeReaderArray<T> higgsCandidate_sj2btag;
    TTreeReaderArray<T> higgsCandidate_sj1pt;
    TTreeReaderArray<T> higgsCandidate_sj2pt;

    TTreeReaderValue<int> ntopCandidate;
    TTreeReaderArray<T> topCandidate_pt;
    TTreeReaderArray<T> topCandidate_eta;
    TTreeReaderArray<T> topCandidate_phi;
    TTreeReaderArray<T> topCandidate_mass;
    TTreeReaderArray<T> topCandidate_tau32SD;
    TTreeReaderArray<T> topCandidate_fRec;
    TTreeReaderArray<T> topCandidate_delRopt; 
    TTreeReaderArray<T> topCandidate_sj1btag;
    TTreeReaderArray<T> topCandidate_sj2btag;
    TTreeReaderArray<T> topCandidate_sj3btag;
    TTreeReaderArray<T> topCandidate_sj1pt;
    TTreeReaderArray<T> topCandidate_sj2pt;
    TTreeReaderArray<T> topCandidate_sj3pt;

    TTreeReaderValueSystematic<T> mem_DL_0w2h2t_sj_p;
    TTreeReaderValueSystematic<T> mem_SL_0w2h2t_sj_p;
    TTreeReaderValueSystematic<T> mem_SL_1w2h2t_sj_p;
    TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_p;
    TTreeReaderValueSystematic<T> mem_DL_0w2h2t_sj_perm_higgs_p;
    TTreeReaderValueSystematic<T> mem_SL_0w2h2t_sj_perm_higgs_p;
    TTreeReaderValueSystematic<T> mem_SL_1w2h2t_sj_perm_higgs_p;
    TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_perm_higgs_p;
    TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_perm_top_p;
    TTreeReaderValueSystematic<T> mem_SL_2w2h2t_sj_perm_tophiggs_p;
    
    TreeDescriptionMCBOOSTED(TFile* file, SampleDescription sample) :
        TreeDescriptionMC<T>(file, sample),

        n_boosted_bjets(TreeDescription<T>::reader, "n_boosted_bjets"),
        n_boosted_ljets(TreeDescription<T>::reader, "n_boosted_ljets"),
        boosted(TreeDescription<T>::reader, "boosted"),
	resolved(TreeDescription<T>::reader, "resolved"),

        boosted_bjets_hadronFlavour(TreeDescription<T>::reader, "boosted_bjets_hadronFlavour"),
        boosted_ljets_hadronFlavour(TreeDescription<T>::reader, "boosted_ljets_hadronFlavour"),

        boosted_bjets_pt(TreeDescription<T>::reader, "boosted_bjets_pt"),
        boosted_bjets_eta(TreeDescription<T>::reader, "boosted_bjets_eta"),
        boosted_bjets_phi(TreeDescription<T>::reader, "boosted_bjets_phi"),
        boosted_bjets_mass(TreeDescription<T>::reader, "boosted_bjets_mass"),
        boosted_bjets_btag(TreeDescription<T>::reader, "boosted_bjets_btag"),

        boosted_ljets_pt(TreeDescription<T>::reader, "boosted_ljets_pt"),
        boosted_ljets_eta(TreeDescription<T>::reader, "boosted_ljets_eta"),
        boosted_ljets_phi(TreeDescription<T>::reader, "boosted_ljets_phi"),
        boosted_ljets_mass(TreeDescription<T>::reader, "boosted_ljets_mass"),
        boosted_ljets_btag(TreeDescription<T>::reader, "boosted_ljets_btag"),

        nhiggsCandidate(TreeDescription<T>::reader, "nhiggsCandidate"),
        higgsCandidate_pt(TreeDescription<T>::reader, "higgsCandidate_pt"),
        higgsCandidate_eta(TreeDescription<T>::reader, "higgsCandidate_eta"),
        higgsCandidate_phi(TreeDescription<T>::reader, "higgsCandidate_phi"),
        higgsCandidate_mass(TreeDescription<T>::reader, "higgsCandidate_mass"),
        higgsCandidate_msoftdrop(TreeDescription<T>::reader, "higgsCandidate_msoftdrop"),
        higgsCandidate_tau21(TreeDescription<T>::reader, "higgsCandidate_tau21"),
        higgsCandidate_bbtag(TreeDescription<T>::reader, "higgsCandidate_bbtag"),
        higgsCandidate_sj1btag(TreeDescription<T>::reader, "higgsCandidate_sj1btag"),
        higgsCandidate_sj2btag(TreeDescription<T>::reader, "higgsCandidate_sj2btag"),
        higgsCandidate_sj1pt(TreeDescription<T>::reader, "higgsCandidate_sj1pt"),
        higgsCandidate_sj2pt(TreeDescription<T>::reader, "higgsCandidate_sj2pt"),

        ntopCandidate(TreeDescription<T>::reader, "ntopCandidate"),
        topCandidate_pt(TreeDescription<T>::reader, "topCandidate_pt"),
        topCandidate_eta(TreeDescription<T>::reader, "topCandidate_eta"),
        topCandidate_phi(TreeDescription<T>::reader, "topCandidate_phi"),
        topCandidate_mass(TreeDescription<T>::reader, "topCandidate_mass"),
        topCandidate_tau32SD(TreeDescription<T>::reader, "topCandidate_tau32SD"),
        topCandidate_fRec(TreeDescription<T>::reader, "topCandidate_fRec"),
        topCandidate_delRopt(TreeDescription<T>::reader, "topCandidate_delRopt"),
        topCandidate_sj1btag(TreeDescription<T>::reader, "topCandidate_sj1btag"),
        topCandidate_sj2btag(TreeDescription<T>::reader, "topCandidate_sj2btag"),
        topCandidate_sj3btag(TreeDescription<T>::reader, "topCandidate_sj3btag"),
        topCandidate_sj1pt(TreeDescription<T>::reader, "topCandidate_sj1pt"),
        topCandidate_sj2pt(TreeDescription<T>::reader, "topCandidate_sj2pt"),
        topCandidate_sj3pt(TreeDescription<T>::reader, "topCandidate_sj3pt"),

        mem_DL_0w2h2t_sj_p(TreeDescription<T>::reader, "mem_DL_0w2h2t_sj_p"),
        mem_SL_0w2h2t_sj_p(TreeDescription<T>::reader, "mem_SL_0w2h2t_sj_p"),
        mem_SL_1w2h2t_sj_p(TreeDescription<T>::reader, "mem_SL_1w2h2t_sj_p"),
        mem_SL_2w2h2t_sj_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_p"),
        mem_DL_0w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_DL_0w2h2t_sj_perm_higgs_p"),
        mem_SL_0w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_SL_0w2h2t_sj_perm_higgs_p"),
        mem_SL_1w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_SL_1w2h2t_sj_perm_higgs_p"),
        mem_SL_2w2h2t_sj_perm_higgs_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_perm_higgs_p"),
        mem_SL_2w2h2t_sj_perm_top_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_perm_top_p"),
        mem_SL_2w2h2t_sj_perm_tophiggs_p(TreeDescription<T>::reader, "mem_SL_2w2h2t_sj_perm_tophiggs_p")


        //LHE_weights_scale_wgt(TreeDescription<T>::reader, "LHE_weights_scale_wgt")
    {}
    
    ~TreeDescriptionMCBOOSTED() {}

    TTreeReaderArray<T>* get_correction_branch(Systematic::SystId syst_id = Systematic::syst_id_nominal);

    std::vector<higgsCandidates> build_higgsCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    std::vector<topCandidates> build_topCandidate(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_boosted_bjets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual std::vector<Jet> build_boosted_ljets(Systematic::SystId syst_id = Systematic::syst_id_nominal);
    virtual EventDescription create_event(Systematic::SystId syst_id = Systematic::syst_id_nominal);
};

typedef TreeDescription<float> TreeDescriptionFloat;
typedef TreeDescriptionBOOSTED<float> TreeDescriptionBOOSTEDFloat;
typedef TreeDescriptionMC<float> TreeDescriptionMCFloat;
typedef TreeDescriptionMCBOOSTED<float> TreeDescriptionMCBOOSTEDFloat;
typedef TreeDescriptionMCSystematic<float> TreeDescriptionMCSystematicFloat;

typedef TreeDescription<double> TreeDescriptionDouble;
typedef TreeDescriptionBOOSTED<double> TreeDescriptionBOOSTEDDouble;
typedef TreeDescriptionMC<double> TreeDescriptionMCDouble;
typedef TreeDescriptionMCBOOSTED<double> TreeDescriptionMCBOOSTEDDouble;
typedef TreeDescriptionMCSystematic<double> TreeDescriptionMCSystematicDouble;

} //namespace TTH_MEAnalysis
#endif
