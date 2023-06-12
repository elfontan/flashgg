import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("FLASHggMicroAOD")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff") # gives deprecated message in 80X but still runs
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( -1 ) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

import os
### 2016
process.GlobalTag = GlobalTag(process.GlobalTag, '' , '')
#process.source = cms.Source("PoolSource",

###############
# Legacy 2018 #
###############
#                             fileNames=cms.untracked.vstring("/store/mc/RunIIAutumn18MiniAOD/GluGluHToGG_M70_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/00000/1359F11B-F51C-4F47-8D70-8CFC55E77A64.root"))
#                             fileNames=cms.untracked.vstring("/store/mc/RunIIAutumn18MiniAOD/DiPhotonJetsBox_M40_80-Sherpa/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v1/00000/042DFFF7-80E4-E04D-B9F7-DE117C3BA50A.root",
#                                                             "/store/mc/RunIIAutumn18MiniAOD/DiPhotonJetsBox_M40_80-Sherpa/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v1/00000/1C95D4F9-16C2-734C-A27D-8E4DA3546E10.root",
#                                                             "/store/mc/RunIIAutumn18MiniAOD/DiPhotonJetsBox_M40_80-Sherpa/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v1/00000/15C2B929-9CEF-F54D-9C1D-F392F7E8F131.root",
#                                                             "/store/mc/RunIIAutumn18MiniAOD/DiPhotonJetsBox_M40_80-Sherpa/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v1/00000/207FF7E5-7843-B943-927B-A1086E997D66.root"))
##########
# UL2018 #
##########
#                             fileNames=cms.untracked.vstring("/store/mc/RunIISummer20UL18MiniAODv2/GluGluHToGG_M30_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/ED2522A0-D644-1E41-BCCE-55DD7B12053A.root","))
#                             fileNames=cms.untracked.vstring("/store/mc/RunIISummer20UL18MiniAODv2/GluGluHToGG_M70_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2430000/5326E7F7-2C04-F84F-932F-85644569548C.root","))
#
#                             fileNames=cms.untracked.vstring("/store/mc/RunIISummer16MiniAODv3/VBFHToGG_M125_13TeV_amcatnlo_pythia8_v2/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/50000/38128C3C-892D-E911-AC8E-008CFA0087C4.root","))
#    process.GlobalTag = GlobalTag(process.GlobalTag,'80X_dataRun2_2016LegacyRepro_v4','')
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2016B/SingleElectron/MINIAOD/07Aug17_ver1-v1/110000/0248293E-578B-E711-A639-44A842CFC9D9.root","))
### 2017
#    process.GlobalTag = GlobalTag(process.GlobalTag,'','')
#    process.source = cms.Source("PoolSource",
#                             fileNames=cms.untracked.vstring("/store/mc/RunIIFall17MiniAODv2/GluGluHToGG_M-125_13TeV_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/0866D1A8-1941-E811-B61F-0CC47AF9B2E6.root","))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring('/store/mc/RunIISummer16MiniAODv2/GluGluHToGG_M-125_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/024E4FA3-8BBC-E611-8E3D-00266CFFBE88.root",'))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/mc/RunIIFall17MiniAOD/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/40000/4A2ACB0A-1BD9-E711-AF54-141877410316.root",'))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/mc/RunIIFall17MiniAOD/GluGluToHHTo2B2G_node_SM_13TeV-madgraph/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/2E0E165D-8E05-E811-909C-FA163E80AE1F.root'))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring('file:/afs/cern.ch/user/s/sethzenz/work/public/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_94X_mc2017_realistic_v10-v1.root'))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/RunIIFall17MiniAODv2/THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/6E58A5DD-BF43-E811-8946-0023AEEEB538.root"))

### 2018
#    process.GlobalTag = GlobalTag(process.GlobalTag,'100X_upgrade2018_realistic_v10','')
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2018B/DoubleMuon/MINIAOD/PromptReco-v1/000/317/080/00000/4E78B565-8464-E811-BF54-02163E01A0FC.root"))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2018D/EGamma/MINIAOD/PromptReco-v2/000/322/106/00000/9A1C4C91-1EB3-E811-A238-02163E0150CE.root"))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2018D/DoubleMuon/MINIAOD/PromptReco-v2/000/320/673/00000/0A83E8DF-EB97-E811-AE18-FA163E192E5D.root"))
#    process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/100X_upgrade2018_realistic_v10-v2/10000/F24C5C06-FF47-E811-9C2F-FA163EC3CAD1.root"))

#process.GlobalTag = GlobalTag(process.GlobalTag,'92X_upgrade2017_realistic_v10','')
#process.source.fileNames=cms.untracked.vstring("/store/mc/RunIISummer17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10_ext1-v2/10000/00F9D855-E293-E711-B625-02163E014200.root")

# 2017 Data

# Legacy ReReco
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2016B/SingleElectron/MINIAOD/18Apr2017_ver1-v1/120000/40167FB6-6237-E711-934A-001E67E69E05.root"))

#Moriond17 MC
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/RunIISummer16MiniAODv2/GluGluHToGG_M-125_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/024E4FA3-8BBC-E611-8E3D-00266CFFBE88.root"))
#80x reminiAOD data
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2016G/DoubleEG/MINIAOD/03Feb2017-v1/100000/002F14FF-D0EA-E611-952E-008CFA197AF4.root"))

#80x signal
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/RunIISpring16MiniAODv2/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext2-v1/10000/6A31A211-063B-E611-98EC-001E67F8F727.root")) # ggH 125 miniAODv2
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/RunIISpring16MiniAODv2/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_v2/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/80000/267A1DB4-3D3B-E611-9AD2-003048C559C4.root")) # ttH 125 miniAODv2

#80x data
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/data/Run2016B/DoubleEG/MINIAOD/PromptReco-v2/000/273/158/00000/1E5ABF54-E019-E611-AAED-02163E01293F.root")) # /DoubleEG/Run2016B-PromptReco-v2/MINIAOD

#Background MC for Diphoton Mass 0 to 40
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_0142b42052c9aead8f71a3bd834f96dc.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_81749d13125f85adac6c11fdade0965a.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_027ca3f2873f6a1c1a36f84d99bcc3ef.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_860102ed46b46864103e4d902ff2482c.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_03da9024112a7ac87d15c3fefafed3d5.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_88d2daac4f269618c4a33a4ee8ff62cf.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_04e74e19b22c8bb4a968cda301138a19.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_894c04c210091f62bc26a27e3f6acf65.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_07357811954a150052bde5c52b5ed6d0.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_89a99fe14fe4b49a6103bd52ee2427e6.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_0c92bf0d59c8d126b6884cece57354dd.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_8ab3ae6ca308fa5e81e90b8c6792979b.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_0e47aad90b11a37d33b7a69f493068b3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_8d10437ad207d2e2b3df6e63c2b0f9d4.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_103ebe42121220c09b2c83ea0b79bbe1.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_922228e86b46d34cfb2327a6065e5c45.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_14cb5a1ba4660c5a58cfd89a1ff83f09.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_940e7832493e0fcc3f72e0ffe2d6aa80.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_1c60417bcf9d7ee4647bda6f15c7ebab.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_9a9a59420f83474a087ac0d40a502c2c.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_1e866a0a4460a21e2258acea31dfdd00.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_9b6ceb4d2257e68ec3579c4afadbcdd8.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_21d2fb08ffefeb0e43bf698cca1e33e3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_9eab516671afec482c8a3e9d8dc6d65f.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_246c5202a8101c7b959d20a0760ef2fb.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_a1fbc3d99e9922340be5ec5dcf92f6e3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_24705e2ed662baefe21a238e366767cf.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_a35785647220e548e8d1c2421a6efefd.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_26fe6800d849f5103140fec729db8d52.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_a4a46267f96287c7496880f15215501e.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_29177247c01ccbf373fc8cff8e642349.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_a52fbaa89d1c1cc3dd5b06496492f0ce.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_29c376269ae0a9a203977f028d5c5b71.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_a5a54c1ec64f801e7c4104ebe52486f4.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_2a4b160881c8f08d3a4f9b23a539d4ae.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_aed4cf389a87f214795fbd98909fde3a.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_2a9d6e6c5898832acf0ffa0a1dffdf73.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_b00c3a025a5769b132e13efb17bbb894.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_2b3af8f1b3a85e320e00c85ed38cabe9.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_b0c2068e68e3fc6b93d2f43f5cd16e87.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_2ccc92742c10ace52e9c2bbacfe86887.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_b0d12287d50f608776862fefacd9833d.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_3065ffa0600d1d49e5c12a7023f772dc.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_b6fad1ea0f96525efad7bf6de318e80c.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_330fb9cef1fb835eba03ff1caacb21d6.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_b7734c1eff3cd8bde07f4e401ecf77af.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_34e06c54c6245ef09ca69fc3cc105178.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_bb3895c2e7071d992925e650d0c31ef6.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_36a90031d16894dd4262910086fc3d39.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_bc875238482180181a091a3d0829e0c3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_38de7978ad1e5ba28618e572815063ae.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_c1973a55011960a9090cce3b5e795ecd.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_3a23bb776ff9dff74c7fb0c568ac75c9.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_c568fcef240b883dd56c0e1d57682c62.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_3a2b29f2b9d2d6117c5f903f6baf5eea.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_c5b1290fcaab43c72a8ec51beb0687c3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_4259adf4e2ae808c9987f0c8171390d7.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_ca0177298d6e065e0112f43974001cd2.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_43d54a7d3d352b14541abbccfbd7089a.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_cec7ee27c0875ffe209afc6e53dbb462.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_468275d66ca898a11aa89c0a63e2911a.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d05a2a4b057220832a634798a07b7d35.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_48aa16a82ead41505894021391864d52.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d0c0b41db65658aceccf850f351e2713.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_49df42a662ae361b0e1e7858489057ec.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d15f756dd9f846194f67c13d2a34a4f6.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_4a405187d50e008ce9a4665b6756c1e1.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d31a154b4aa05b3e8fed5c7fb486f2e8.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_4bc42ee215585b280cc277189927c587.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d40f0a19ae3e1cae8b19d8cab4d381a3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_50313e2e2eb8c84d9c7603c5d646472a.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d81983d4e06b10716c6401a994c1da47.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_52812c04e35580ceb15f2223ac6e9f8f.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d882d2f031a25eaa3327c29c40e17c87.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_5aaded3f721b275bf182b7fefc920aee.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_d9dadb3e49cd9ef855c7b6205c58fa8e.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_5dbd53555791378e845c5f03fcc8de99.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_da98820ea29a971905294e3317a6a58f.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_5f4d320fa677344d61a2836f86f83856.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_dd39176b8f6f3b1b91896b98ea0a6170.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_6596659d24b0a0042168137a47a13c75.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_de2c2b2f5ef9a33b0f8c53753ce66be8.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_6671d197ca57a36bbf3705a8590d84ce.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_e01a8afbf3d673318f9aaddd04f83d78.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_67709fedd8772eb9b54cfc57449b6a2d.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_e4521d27ca865f3b885faf3ff75ac9f4.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_6ae390df8baec2cd99a1d6ec3eb45d55.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_eb28ca7fd5530f987b271e7aea3e399d.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_6ec179e875c387b73fc5b46a1bc32282.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_f2ead4f6173884981455440208fd2e56.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_72b3aa3e968ab648839e7df83d3c9ac3.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_f411afd20aa2fbaac94bc350f7f8e2ed.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_74012c6fcedbb2a7030cd99d63492859.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_f5229ec333fa9256e69de42352b49bb8.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_74aba82fd8792765eaee734b7c931511.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_f650b52f9185ccb2ac1d957ea36a9f0b.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_7a71907a66d355a48f3d401b7d3eb466.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_f97563945d89500c56fa31a01833d505.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_8031b8b2a54ff1653a292e080f71e1dc.root",
#                                                                         "file:/eos/user/d/dsperka/mc/lowmassdiphoton/diphoton_mgg0to40/MiniAOD_fab626c996663247df95cfd1fcdab242.root"))

#Background MC for Photon+Jets
#process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_0.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_1.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_2.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_3.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_4.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_5.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_6.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_7.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_8.root",
#                                                                         "file:/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_pt10_m5_v1/MiniAOD_9.root"))

#Background MC Test for Diphoton 80-Inf
process.source = cms.Source("PoolSource",fileNames=cms.untracked.vstring("/store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/50000/C036CAF3-46AB-DC48-A8CF-16D680818D41.root",
                                                                         "/store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/50000/42509035-6D9D-F041-B91E-D05A5B5E0D57.root",
                                                                         "/store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/50000/B2A608C1-3594-5145-8689-27ECDC21DB94.root"))

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")
process.RandomNumberGeneratorService.flashggRandomizedPhotons = cms.PSet(
          initialSeed = cms.untracked.uint32(16253245)
        )

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

process.MessageLogger.cerr.threshold = 'ERROR' # can't get suppressWarning to work: disable all warnings for now
# process.MessageLogger.suppressWarning.extend(['SimpleMemoryCheck','MemoryCheck']) # this would have been better...

# Uncomment the following if you notice you have a memory leak
# This is a lightweight tool to digg further
#process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
#                                        ignoreTotal = cms.untracked.int32(1),
#                                        monitorPssAndPrivate = cms.untracked.bool(True)
#                                       )

process.load("flashgg/MicroAOD/flashggMicroAODSequence_cff")

# NEEDED FOR ANYTHING PRIOR TO reMiniAOD
#process.weightsCount.pileupInfo = "addPileupInfo"

from flashgg.MicroAOD.flashggMicroAODOutputCommands_cff import microAODDefaultOutputCommand
process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('myMicroAODOutputFile.root'),
                               outputCommands = microAODDefaultOutputCommand
                               )

# All jets are now handled in MicroAODCustomize.py
# Switch from PFCHS to PUPPI with puppi=1 argument (both if puppi=2)

process.p = cms.Path(process.flashggMicroAODSequence)
process.e = cms.EndPath(process.out)

# Uncomment these lines to run the example commissioning module and send its output to root
#process.commissioning = cms.EDAnalyzer('flashggCommissioning',
#                                       PhotonTag=cms.untracked.InputTag('flashggPhotons'),
#                                       DiPhotonTag = cms.untracked.InputTag('flashggDiPhotons'),
#                                       VertexTag=cms.untracked.InputTag('offlineSlimmedPrimaryVertices')
#)
#process.TFileService = cms.Service("TFileService",
#                                   fileName = cms.string("commissioningTree.root")
#)
#process.p *= process.commissioning

from flashgg.MicroAOD.MicroAODCustomize import customize
customize(process)

if "DY" in customize.datasetName or "SingleElectron" in customize.datasetName or "DoubleEG" in customize.datasetName or "EGamma" in customize.datasetName:
    customize.customizeHLT(process)

open('dump.py', 'w').write(process.dumpPython())
