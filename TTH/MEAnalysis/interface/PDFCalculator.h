#ifndef PDFCALCULATOR_H // header guards
#define PDFCALCULATOR_H

#include <iostream>
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH1D.h"
#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"


#include "LHAPDF/LHAPDF.h"


class PDFObject {
    private:
        float central;
        float errplus;
        float errminus;
    public:
        PDFObject(float c, float p, float m);
        PDFObject(std::vector<double> pdfWeights);
        void SetValues(float c, float p, float m);

};


#endif
