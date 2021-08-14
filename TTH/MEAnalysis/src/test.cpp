// with CMSSW:
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

//// setup calibration + reader
//BTagCalibration calib("deepcsv", "/shome/mameinha/TTH/CMSSW_9_4_9/CMSSW_9_4_9/src/TTH/MEAnalysis/data/deepCSV_sfs.csv");
//BTagCalibrationReader reader(BTagEntry::OP_LOOSE,  // operating point
//                             "central",             // central sys type
//                             {"up", "down"});      // other sys types
//
//reader.load(calib, BTagEntry::FLAV_B,"comb")               // measurement type
//// reader.load(...)     // for FLAV_C
//// reader.load(...)     // for FLAV_UDSG
//
//// in your event loop
//for (const auto & event : events) {
//   
//  for (const auto & b_jet : event.b_jets) {
//
//      // Note: this is for b jets, for c jets (light jets) use FLAV_C (FLAV_UDSG)
//      double jet_scalefactor    = reader.eval_auto_bounds(
//          "central", 
//          BTagEntry::FLAV_B, 
//          b_jet.eta(), // absolute value of eta
//          b_jet.pt()
//      ); 
//      double jet_scalefactor_up = reader.eval_auto_bounds(
//          "up", BTagEntry::FLAV_B, b_jet.eta(), b_jet.pt());
//      double jet_scalefactor_do = reader.eval_auto_bounds(
//          "down", BTagEntry::FLAV_B, b_jet.eta(), b_jet.pt()); 
//
//
//    std::cout << jet_scalefactor << "  " << jet_scalefactor_up << " " << jet_scalefactor_down << endl;
//
//  }
//  ...
//}