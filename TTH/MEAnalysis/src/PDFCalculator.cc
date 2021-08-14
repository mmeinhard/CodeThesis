#include "TTH/MEAnalysis/interface/PDFCalculator.h"
#include <iostream>
#include <iostream>
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH1D.h"
#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"


#include "LHAPDF/LHAPDF.h"


/*class PDFObject{
    public:
        float central;
        float errplus;
        float errminus;
        PDFObject(float c, float p, float m) { 
        central = c;
        errplus = p;
        errminus = m;
        } 

};*/

PDFObject::PDFObject(float c, float p, float m) { 
    SetValues(c,p,m);
} 

void PDFObject::SetValues(float c, float p, float m)
{
    central = c;
    errplus = p;
    errminus = m;
}

PDFObject::PDFObject(std::vector<double> pdfWeights) {
    float weightUp = 1.0;
    float weightDown = 1.0;
    float centre = 1.0;

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
            centre = pdfUnc.central;

        }
    }
    errplus = weightUp;
    errminus = weightDown;
    central = centre;

}

/*
PDFObject calcUncertainty(std::vector<double> pdfWeights) {
    float weightUp = 1.0;
    float weightDown = 1.0;
    float central = 1.0;

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
            central = pdfUnc.central;

        }

    }

    PDFObject result(central,weightUp,weightDown);

    return result;


}
*/
/*    std::vector<double> pdfWeights;
    for(int iWeight = 1; iWeight <  (*nLHEPDFWeights); iWeight++){
        pdfWeights.push_back(this->LHEPDFWeights[iWeight]);
    }
    //ttjets_powheg_hadronicstd::cout << "PDFVec.size() = " << pdfWeights.size() << std::endl;
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

    }*/