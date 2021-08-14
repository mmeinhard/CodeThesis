import glob, os

#NB: these cross-sections are now in the config file
#Cross-sections from
# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
xsec = {}
xsec[("ttjets", "8TeV")] = 252.89
xsec[("ttjets", "13TeV")] = 831.76
#http://pdg.lbl.gov/2013/reviews/rpp2013-rev-top-quark.pdf page 3, A-C
br_tt_to_ll = 0.105
br_tt_to_lj = 0.438

xsec[("ttjets", "tt_to_ll", "13TeV")] = xsec[("ttjets", "13TeV")] * br_tt_to_ll
xsec[("ttjets", "tt_to_lj", "13TeV")] = xsec[("ttjets", "13TeV")] * br_tt_to_lj

br_h_to_bb = 0.577
xsec[("tth", "8TeV")] = 0.1302
xsec[("tthbb", "8TeV")] = xsec[("tth", "8TeV")] * br_h_to_bb

#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
xsec[("tth", "13TeV")] = 0.5085
xsec[("tthbb", "13TeV")] = xsec[("tth", "13TeV")] * br_h_to_bb
xsec[("tth_nonhbb", "13TeV")] = xsec[("tth", "13TeV")] * (1.0 - br_h_to_bb)

xsec[("qcd_ht300to500", "13TeV")] = 366800.0
xsec[("qcd_ht500to700", "13TeV")] = 29370.0
xsec[("qcd_ht700to1000", "13TeV")] = 6524.0
xsec[("qcd_ht1000to1500", "13TeV")] = 1064.0
xsec[("qcd_ht1500to2000", "13TeV")] = 121.5
xsec[("qcd_ht2000toinf", "13TeV")] = 25.42

#From the AN
xsec[("wjets", "13TeV")] = 61526.7

xsec[("ttw_wqq", "13TeV")] = 0.435
xsec[("ttw_wlnu", "13TeV")] = 0.21
xsec[("ttz_zqq", "13TeV")] = 0.611

xsec[("stop_tW", "13TeV")] = 35.6
xsec[("stop_tbarW", "13TeV")] = 35.6
xsec[("stop_t", "13TeV")] = 45.34
xsec[("stop_tbar", "13TeV")] = 26.98 
xsec[("stop_s", "13TeV")] = 3.44

xsec[("ww", "13TeV")] = 118.7
xsec[("wz", "13TeV")] = 47.13
xsec[("zz", "13TeV")] = 16.523

xsec[("stop_tW", "13TeV")] = 35.6
xsec[("stop_tbarW", "13TeV")] = 35.6
xsec[("stop_t", "13TeV")] = 45.34
xsec[("stop_tbar", "13TeV")] = 26.98 
xsec[("stop_s", "13TeV")] = 3.44

#used to assign a number that you can cut on to events in different trigger paths
TRIGGERPATH_MAP = {
    "m": 1,
    "e": 2,
    "mm": 3,
    "em": 4,
    "ee": 5,
#    "fh": 6,
#    "bt": 7,
}

#Configure the site-specific file path
hn = os.environ.get("HOSTNAME", "")
vo = os.environ.get("VO_CMS_DEFAULT_SE", "")

def pfn_to_lfn(fn):
    """
    Converts a PFN to a LFN. Filename must be of
    /store/XYZ type.
    """
    return fn[fn.find("/store"):]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_files(fname):
    # Expect fname relative to CMSSW BASE
    fname = fname.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
    
    lines = [fname]

    #Load list of file names from textfile
    if fname.endswith(".txt"):
        lines = open(fname).readlines()
        lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: "root" in x, lines)
        lines = map(lambda x: x.split()[0], lines)
    
    #Filename is a globstring
    elif fname.endswith("*.root"):
        #Files in T3_CH_PSI storage element
        if "/pnfs/" in fname:
            lines = ["root://t3dcachedb.psi.ch/" + f for f in glob.glob(fname)]
        #Files are really on local filesystem
        else:
            lines = ["file://" + f for f in glob.glob(fname)]
    if len(lines) == 0:
        raise Exception("Could not match any files for {0}".format(fname))
    return lines

# This function is used everywher to translate LFN /store to PFN root://
# currently all files are assumed to reside at CSCS
#site_prefix = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat"
site_prefix = "root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat"
def getSitePrefix(fn=""):
    if fn.startswith("/store"):
        return site_prefix  + fn
    elif fn.startswith("file://") or fn.startswith("root://"):
        return fn
    else:
        return fn

def get_prefix_sample(datasetpath):
    spl = datasetpath.split("__")
    if len(spl) == 2:
        prefix = spl[0]
        sample = spl[1]
    elif len(spl) == 1:
        prefix = ""
        sample = datasetpath
    else:
        raise Exception("could not parse DATASETPATH: {0}".format(datasetpath))
    return (prefix, sample)

def getSampleNGen(sample):
    import ROOT
    n = 0
    nneg = 0
    npos = 0
    nw = 0
    for f in sample.subFiles:
        tfn = lfn_to_pfn(f)
        tf = ROOT.TFile.Open(tfn)
        hc = tf.Get("Count")
        hneg = tf.Get("CountNegWeight")
        hpos = tf.Get("CountPosWeight")
        hw = tf.Get("CountWeighted")
        n += hc.GetBinContent(1)
        nneg += hneg.GetBinContent(1)
        npos += hpos.GetBinContent(1)
        nw += hw.GetBinContent(1)
        tf.Close()
        del tf
        print tfn, npos, nneg, nw
    return int(nw)
