import os
import ROOT
import numpy as np

def run_fit(datacard):

    # create workspace
    os.system("text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO verbose --PO 'map=.*/ttH_hbb:r[1,-5,5]' --PO 'map=.*/ttH_nonhbb:r[1,-5,5]' " + datacard + " -o model.root")
    
    # run and save best-fit snapshot
    os.system("combine -M MultiDimFit --algo=cross --cl=0.68 --robustFit 0 --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 1 --saveWorkspace -n _myanalysis_bestfit model.root -v 3 --saveFitResult |& tee bestfit.log")

    # run with all nuisances frozen
    os.system("combine -M MultiDimFit --algo=cross --cl=0.68 --freezeNuisanceGroups exp,autoMCStats,theory --robustFit 0 --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 1 -d higgsCombine_myanalysis_bestfit.MultiDimFit.mH120.root -w w --snapshotName \"MultiDimFit\" -n _frozen_all --saveFitResult -v 3 --saveWorkspace |& tee frozen_all.log")

    # run with no frozen nuisances
    os.system("combine -M MultiDimFit --algo=cross --cl=0.68 --robustFit 0 --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 1 -d higgsCombine_myanalysis_bestfit.MultiDimFit.mH120.root -w w --snapshotName \"MultiDimFit\" -n _frozen_none -v 3 --saveFitResult |& tee frozen_none.log")



def calc_2d(frozen_none, frozen_all):

    # cacluate the systematic and statistical uncertainties
    f = ROOT.TFile(frozen_all)
    t = f.Get("limit")
    stat_ttH = []
    stat_ttbb = []
    for evt in t:
        stat_ttH.append(evt.r_ttH)
        stat_ttbb.append(evt.r_ttbb)
    f.Close()

    f = ROOT.TFile(frozen_none)
    t = f.Get("limit")
    tot_ttH = []
    tot_ttbb = []
    for evt in t:
        tot_ttH.append(evt.r_ttH)
        tot_ttbb.append(evt.r_ttbb)
    f.Close()

    tot_ttH.sort()
    tot_ttbb.sort()
    stat_ttH.sort()
    stat_ttbb.sort()  

    print tot_ttH
    print tot_ttbb
    print stat_ttH
    print stat_ttbb

    res = {"stat_ttH" : stat_ttH, "tot_ttH" : tot_ttH, "stat_ttbb" : stat_ttbb, "tot_ttbb" : tot_ttbb}

    for i in ["ttH", "ttbb"]:

        tot_up = res["tot_" + i][4] - res["tot_" + i][2]
        tot_down = res["tot_" + i][2] - res["tot_" + i][0]
        stat_up = res["stat_" + i][4] - res["stat_" + i][2]
        stat_down = res["stat_" + i][2] - res["stat_" + i][0]
        
        print "result %s  %f (- %f / + %f)" % (i, res["tot_"+i][2], tot_down, tot_up)

        print "%s statistical uncertainty (- %f / + %f)" % (i, stat_down, stat_up)

        syst_up = np.sqrt( tot_up **2 - stat_up **2 )
        syst_down = np.sqrt( tot_down **2 - stat_down **2)

        print "%s systematic uncertainty (- %f / + %f)" % (i, syst_down, syst_up)
   
def calc_1d(frozen_none, frozen_all):

    # cacluate the systematic and statistical uncertainties
    f = ROOT.TFile(frozen_all)
    t = f.Get("limit")
    stat = []
    for evt in t:
        stat.append(evt.r)
    f.Close()

    f = ROOT.TFile(frozen_none)
    t = f.Get("limit")
    tot = []
    for evt in t:
        tot.append(evt.r)
    f.Close()

    tot.sort()
    stat.sort()

    print stat
    print tot


    tot_up = tot[2] - tot[1]
    tot_down = tot[1] - tot[0]
    stat_up = stat[2] - stat[1]
    stat_down = stat[1] - stat[0]

    print "result %f (- %f / + %f)" % (tot[1], tot_down, tot_up)

    print "statistical uncertainty (- %f / + %f)" % (stat_down, stat_up)

    syst_up = np.sqrt( tot_up **2 - stat_up **2 )
    syst_down = np.sqrt( tot_down **2 - stat_down **2)

    print "systematic uncertainty (- %f / + %f)" % (syst_down, syst_up)

 
if __name__ == "__main__":

        run_fit("/work/creissel/dnn_datacards/shapes_sl_dnn__dnn.txt")
        calc_1d("/work/creissel/dnn_datacards/higgsCombine_frozen_none.MultiDimFit.mH120.root","/work/creissel/dnn_datacards/higgsCombine_frozen_all.MultiDimFit.mH120.root")
