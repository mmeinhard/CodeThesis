import sys
import ROOT
from math import *

#rootfile=sys.argv[1]
#rootfile_nom = "/work/mameinha/tth/gc/sparse/Jul30_2DFactor_SLDLResolved_NegativeNorm.root"
#rootfile_nom = "/work/mameinha/tth/gc/sparse/Aug8_2DFactor_Boosted.root"
#rootfile_nom = "/work/mameinha/tth/gc/sparse/Aug10_2DFactor_Unboosted.root"
#rootfile_down = "/work/mameinha/tth/gc/sparse/Aug8_2DFactor_Systs/tunedown.root"
#rootfile_up = "/work/mameinha/tth/gc/sparse/Aug8_2DFactor_Systs/tuneup.root"
rootfile_nom = "/work/mameinha/tth/gc/sparse/Aug17_2DFactor_BoostedV2.root"

rootfile_down = "/work/mameinha/tth/gc/sparse/Aug17_2DFactor_Systs3/tunedown.root"
rootfile_up = "/work/mameinha/tth/gc/sparse/Aug17_2DFactor_Systs3/tuneup.root"

systematic="CMS_ttHbb_UE"
#systematic="CMS_ttHbb_HDAMP"

#discrname="jetsByPt_0_pt"
discrnames = {}
discrnames["sl_jge6_tge4"] = "mem_SL_2w2h2t_p"
discrnames["sl_jge6_t3"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["sl_j5_tge4"] = "mem_SL_1w2h2t_p"
discrnames["sl_j5_t3"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["sl_j4_tge4"] = "mem_SL_0w2h2t_p"
discrnames["sl_j4_t3"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["dl_jge4_tge4"] =  "mem_DL_0w2h2t_p"
discrnames["dl_jge4_t3"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["sl_jge6_tge4_sj"] = "mem_SL_2w2h2t_sj_p"
discrnames["sl_j5_tge4_sj"] = "mem_SL_1w2h2t_sj_p"
discrnames["sl_j4_tge4_sj"] = "mem_SL_0w2h2t_sj_p"
discrnames["dl_jge4_tge4_sj"] = "mem_DL_0w2h2t_sj_p"
discrnames["sl_jge6_tge4_sj_only"] = "mem_SL_2w2h2t_sj_p"
discrnames["sl_j5_tge4_sj_only"] = "mem_SL_1w2h2t_sj_p"
discrnames["sl_j4_tge4_sj_only"] = "mem_SL_0w2h2t_sj_p"
discrnames["dl_jge4_tge4_sj_only"] = "mem_DL_0w2h2t_sj_p"


discrnames["sl_jge6_tge4_noboost"] = "mem_SL_2w2h2t_p"
discrnames["sl_jge6_t3_noboost"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["sl_j5_tge4_noboost"] = "mem_SL_1w2h2t_p"
discrnames["sl_j5_t3_noboost"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["sl_j4_tge4_noboost"] = "mem_SL_0w2h2t_p"
discrnames["sl_j4_t3_noboost"] = "btag_LR_4b_2b_btagCSV_logit"
discrnames["dl_jge4_tge4_noboost"] =  "mem_DL_0w2h2t_p"
discrnames["dl_jge4_t3_noboost"] = "btag_LR_4b_2b_btagCSV_logit"

#systematics=["CMS_ttHbb_HDAMP","CMS_ttHbb_UE"]

f=ROOT.TFile(rootfile_nom,"READ")
fDown = ROOT.TFile(rootfile_down, "READ")
fUp = ROOT.TFile(rootfile_up, "READ")


processes = ["ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar", "ttbarOther"]
#categories = ["fh_j7_t3__mem_FH_4w2h1t_p", "fh_j8_t3__mem_FH_4w2h1t_p", "fh_j9_t3__mem_FH_4w2h1t_p",
#              "fh_j7_t4__mem_FH_3w2h2t_p", "fh_j8_t4__mem_FH_3w2h2t_p", "fh_j9_t4__mem_FH_4w2h2t_p"]
#categories = ["sl_jge6_tge4","sl_jge6_t3","sl_j5_tge4","sl_j5_t3","sl_j4_tge4","sl_j4_t3","dl_jge4_tge4","dl_jge4_t3"]
#categories = ["sl_jge6_tge4_sj","sl_j5_tge4_sj","sl_j4_tge4_sj","dl_jge4_tge4_sj"]
#categories = ["sl_jge6_tge4_noboost","sl_jge6_t3_noboost","sl_j5_tge4_noboost","sl_j5_t3_noboost","sl_j4_tge4_noboost","sl_j4_t3_noboost","dl_jge4_tge4_noboost","dl_jge4_t3_noboost"]
categories = ["sl_jge6_tge4_sj_only","sl_j5_tge4_sj_only","sl_j4_tge4_sj_only","dl_jge4_tge4_sj_only"]

def round_to_sign(x):
    x=float(x)
    strx=str(x)
    afterDecimal=float("0."+strx.split(".")[1])
    if afterDecimal==0.0:
        return x
    minNDigs=3
    actualNDigs=-int(floor(log10(abs(afterDecimal))))
    nDigs=max(actualNDigs,minNDigs)
    return round(x, nDigs)

def getNumbersSchemeOne(nomInt,downInt,upInt):
    upRatio=upInt/nomInt
    downRatio=downInt/nomInt
    
    if upRatio > 0:
        up_relerr = ((upRatio if upRatio>=1.0 else (1.0/upRatio)) -1.0)
    else:
        print "zero"
        up_relerr = 1
    if downRatio > 0:
        down_relerr = ((downRatio if downRatio>=1.0 else (1.0/downRatio)) -1.0)
    else: 
        print "zero"
        down_relerr = 1
    
    #average absolute up/down variation
    avg_err = 0.5*(up_relerr+down_relerr)
    
    # use avg abs error as symmetric error
    # example : up=1.2 down=1.1 => up=1.15, down 0.85
    upRatio_new=upRatio
    downRatio_new=downRatio
    if (upRatio>=downRatio):
        upRatio_new = (1.0 + avg_err)
        downRatio_new = 1.0/(1.0+avg_err)
    else:
        downRatio_new = (1.0 + avg_err)
        upRatio_new = 1.0/(1.0+avg_err)
    
    return downRatio_new, upRatio_new

result = {}
print "proc__cat__syst: nomInt downInt upInt down_naive up_naive downRatio upRatio"
for proc in processes:
    result[proc] = {}
    for cat in categories:
        result[proc][cat] = {}
        print proc+"__"+cat
        discrname = discrnames[cat]
	hnom = f.Get(proc+"__"+cat+"__"+discrname)
        
        result[proc][cat][systematic] = {}
        hup = fUp.Get(proc+"__"+cat+"__"+discrname)
        hdown = fDown.Get(proc+"__"+cat+"__"+discrname)
        if hnom==None or hup==None or hdown==None:
            print "ERROR did not find histos", proc+"__"+cat+"_"#+histprefix
            exit(1)
        nomInt=hnom.Integral()
        upInt=hup.Integral()
        downInt=hdown.Integral()
        if nomInt==0:
            print "WARNING NO NOM"
            nomInt=0.001
        if (upInt>nomInt and downInt>nomInt) or (upInt<nomInt and downInt<nomInt):
            print "WARNING same sided ! "
        downRatio, upRatio = getNumbersSchemeOne(nomInt,downInt,upInt)
        upRatio_naive=upInt/nomInt
        downRatio_naive=downInt/nomInt
        #print nomInt, upInt, downInt, upRatio, downRatio
        downRatio=round_to_sign(downRatio)
        upRatio=round_to_sign(upRatio)
        print proc+"__"+cat+"__"+systematic+":", nomInt, downInt, upInt, round_to_sign(downRatio_naive), round_to_sign(upRatio_naive),  downRatio, upRatio
        if (upInt>nomInt and upRatio<1) or (upInt<nomInt and upRatio>1):
            print "warning direction Flip UP", (upInt>nomInt and upRatio<1), (upInt<nomInt and upRatio>1)
        if (downInt>nomInt and downRatio<1) or (downInt<nomInt and downRatio>1):
            print "warning direction Flip DOWN", (downInt>nomInt and downRatio<1), (downInt<nomInt and downRatio>1)
        result[proc][cat][systematic]["nomInt"] = nomInt
        result[proc][cat][systematic]["upInt"] = upInt
        result[proc][cat][systematic]["downInt"] = downInt
        result[proc][cat][systematic]["upRatio"] = upRatio     
        result[proc][cat][systematic]["downRatio"] = downRatio

print ""
print "********** SUMMARY **********"

# print "////////", systematic, "////////"
# for cat in categories:
#     print "\""+cat+"__"+systematic+"\": {",
#     for proc in processes:
#         #print "--- ", proc
#         ratio_up = max(result[proc][cat][systematic]["upRatio"], result[proc][cat][systematic]["downRatio"])
#         ratio_down = min(result[proc][cat][systematic]["upRatio"], result[proc][cat][systematic]["downRatio"])
#         #print proc+"__"+cat+"__"+syst+":", "{0}/{1}".format(ratio_up, ratio_down)
#         #print cat+"__"+syst+":", "{0}/{1}".format(ratio_up, ratio_down)
#         print "\""+proc+"\":[{0},{1}],".format(ratio_up, ratio_down),
#     print "},"


print "////////", systematic, "////////"
for cat in categories:
    for proc in processes:
        print "\""+cat+"__"+systematic+"_"+proc+"_2017\": {",
        #print "--- ", proc
        ratio_up = max(result[proc][cat][systematic]["upRatio"], result[proc][cat][systematic]["downRatio"])
        ratio_down = min(result[proc][cat][systematic]["upRatio"], result[proc][cat][systematic]["downRatio"])
        #print proc+"__"+cat+"__"+syst+":", "{0}/{1}".format(ratio_up, ratio_down)
        #print cat+"__"+syst+":", "{0}/{1}".format(ratio_up, ratio_down)
        print "\""+proc+"\":[{0},{1}],".format(ratio_up, ratio_down),
        print "},"


print "////////", systematic, "////////"
for cat in categories:
    print "[Systematics__{0}]".format(cat)
    for proc in processes:
        ratio_up = max(result[proc][cat][systematic]["upRatio"], result[proc][cat][systematic]["downRatio"])
        ratio_down = min(result[proc][cat][systematic]["upRatio"], result[proc][cat][systematic]["downRatio"])
        print systematic+"_"+proc+"_2017: \n  "+proc+" : {0}/{1}".format(ratio_up,  ratio_down)
        
