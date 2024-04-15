# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/diphoton_mgg0to40_cfg.py --python_filename wmLHEGS_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN --fileout file:wmLHEG.root --conditions 106X_upgrade2018_realistic_v15_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --no_exec --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=2 process.g4SimHits.Physics.G4GeneralProcess=cms.bool(False) --mc -n 25000
import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

process = cms.Process('MINIAOD',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.source = cms.Source ("PoolSource",
                fileNames=cms.untracked.vstring(
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_0.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_1.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_10.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_11.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_12.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_13.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_14.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_15.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_16.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_17.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_18.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_19.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_2.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_21.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_22.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_23.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_24.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_25.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_26.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_27.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_28.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_29.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_3.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_30.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_31.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_32.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_33.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_34.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_35.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_36.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_37.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_38.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_39.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_4.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_40.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_41.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_42.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_43.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_44.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_45.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_46.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_47.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_48.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_49.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_5.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_51.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_52.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_53.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_54.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_55.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_56.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_57.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_58.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_59.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_6.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_60.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_61.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_62.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_63.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_64.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_65.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_66.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_67.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_68.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_69.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_7.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_70.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_71.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_72.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_73.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_74.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_75.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_76.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_77.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_78.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_79.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_8.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_80.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_81.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_82.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_83.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_84.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_85.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_86.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_87.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_88.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_89.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_9.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_90.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_91.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_92.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_93.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_94.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_95.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_96.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_97.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_98.root',
                        'file:/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/MiniAOD_99.root'
                ),
                eventsToProcess = cms.untracked.VEventRange('1:182595','1:165954','1:971161','1:547713','1:497636','1:283318','1:481094','1:581558','1:47122','1:558171','1:16764','1:106650','1:819408','1:325718','1:519565','1:489594','1:332782','1:929036','1:919195','1:836936','1:860205','1:55006','1:264546','1:216201','1:192819','1:248442','1:355187','1:562083'))
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

# Output definition
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/BkgMCCutFlowPlots_v2/GenLevel/extractedMiniAOD.root'),
)

process.output_step = cms.EndPath(process.output)

# Schedule definition
process.schedule = cms.Schedule(process.output_step)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 
process = addMonitoring(process)
# End of customisation functions

# Add early deletion of temporary data products to reduce peak memory need
#from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
#process = customiseEarlyDelete(process)
# End adding early deletion

