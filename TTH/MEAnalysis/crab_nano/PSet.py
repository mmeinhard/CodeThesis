import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #"/store/data/Run2018A/JetHT/NANOAOD/Nano14Dec2018-v1/280000/A1BDED36-C1E6-8448-885A-EBC383E10E28.root",
        #"/store/mc/RunIIAutumn18NanoAODv4/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/30000/F5EF6FF0-B722-A544-AFCB-5F125A8409E3.root",
        "/store/mc/RunIIFall17MiniAODv2/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/FEA474B7-2594-E811-968D-1866DA8F75C0.root ",
        #"/store/mc/RunIIAutumn18NanoAODv4/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/30000/F54FC57A-AECE-1248-8B4F-4671C50A958D.root"
        
    ),
    lumisToProcess = cms.untracked.VLuminosityBlockRange(
        #"315974:25-315974:27","315973:860-315973:860",
        #"1:3141-1:3141"
        "1:1195565-1:1195568"
        #,"1:29-1:29"
    )
)

from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValTTbarPileUpMINIAODSIM
#process.source.fileNames = filesRelValTTbarPileUpMINIAODSIM

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.output = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('tree.root'),
    logicalFileName = cms.untracked.string('')
)


process.out = cms.EndPath(process.output)
