import ROOT
import numpy as np
from ROOT import RooStats


def uncertainties(result, workspace):

    # Load file
    f = ROOT.TFile(result)
    fit = f.Get("fit_mdf")

    # Read in covariance matrix
    cov = fit.covarianceMatrix()
    err_ttH = np.sqrt(cov[0][0])
    err_ttbb = np.sqrt(cov[1][1])

    f = ROOT.TFile(workspace)
    w = f.Get("w")
    #w.Print()
    data = w.data("data_obs")
    model = w.obj("ModelConfig")
    model.Print()
    pdf = model.GetPdf()
    POI = model.GetParametersOfInterest()
    print POI

    
    nll = model.createNLL(data) 
    
    """#snapshot = w.loadSnapshot("MultiDimFit")

    #POI = model.GetParametersOfInterest()
    #print POI
    #w.var("r_ttH").Print()

    pl = ROOT.RooStats.ProfileLikelihoodCalculator(data, model)
    #pl = ROOT.RooStats.ProfileLikelihoodCalculator(data, model)
    pl.SetConfidenceLevel(0.683)

    interval = pl.GetInterval()

    ttH = model.GetParametersOfInterest().first()
    ttH_low = interval.LowerLimit(ttH)
    ttH_up = interval.UpperLimit(ttH)

       
    #ttbb = model.GetParametersOfInterest().second()
    #ttbb_low = interval.LowerLimit(ttbb)
    #ttbb_up = interval.UpperLimit(ttbb)
 
    print "68% interval on {0} is [{1},{2}]".format(ttH.GetName(),ttH_low,ttH_up)
    #print "68% interval on {0} is [{1},{2}]".format(ttbb.GetName(),ttbb_low,ttbb_up)

    plot = ROOT.RooStats.LikelihoodIntervalPlot(interval)
    plot.SetRange(0,2)
    #plot.SetYRange(0.5,1.5)
    c = ROOT.TCanvas()
    #ROOT.gPad.SetLogy(True)
    plot.Draw()
    c.Draw()

       
    import time
    time.sleep(60)"""

    return err_ttH, err_ttbb

if __name__ == "__main__":

    err = uncertainties("multidimfit_frozen_all.root", "higgsCombine_frozen_all.MultiDimFit.mH120.root")

    print "stat-only error ttH", err[0]
    print "stat-only error ttbb", err[1]
