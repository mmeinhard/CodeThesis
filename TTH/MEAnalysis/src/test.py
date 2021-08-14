import ROOT

# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTauObjects') 
ROOT.gSystem.Load('libCondToolsBTau') 

# OR using standalone code:
#ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+') 


print "here we are "

# get the sf data loaded
calib = ROOT.BTagCalibration("deepcsv", "/shome/mameinha/TTH/CMSSW_9_4_9/CMSSW_9_4_9/src/TTH/MEAnalysis/data/sfs_deepcsv_2017.csv");

# making a std::vector<std::string>> in python is a bit awkward, 
# but works with root (needed to load other sys types):
v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')

print "here we are "
#load(calib,  BTagEntry::FLAV_B, "iterativefit");
# make a reader instance and load the sf data
reader = ROOT.BTagCalibrationReader(
    0,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
    "central",      # central systematic type
    v_sys,          # vector of other sys. types
)    
reader.load(    calib,     BTagEntry::FLAV_B, "iterativefit" )
# reader.load(...)     # for FLAV_C
# reader.load(...)     # for FLAV_UDSG

# in your event loop
sf = reader.eval_auto_bounds(
    'central',      # systematic (here also 'up'/'down' possible)
    0,              # jet flavor
    1.2,            # absolute value of eta
    31.             # pt
)
