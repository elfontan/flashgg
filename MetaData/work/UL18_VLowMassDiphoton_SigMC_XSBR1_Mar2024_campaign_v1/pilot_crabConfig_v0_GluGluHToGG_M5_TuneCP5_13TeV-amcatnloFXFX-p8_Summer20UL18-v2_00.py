# CRAB3 config template for flashgg
# More options available on the twiki :
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial
# To actually prepare the jobs, please execute prepareCrabJobs.py

from WMCore.Configuration import Configuration
config = Configuration()
import os

config.section_("General")
config.General.requestName = "v0_GluGluHToGG_M5_TuneCP5_13TeV-amcatnloFXFX-p8_Summer20UL18-v2_00"
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "microAODstd.py"

## to include local file in the sendbox, this will put the file in the directory where cmsRun runs
config.JobType.inputFiles = ['QGL_AK4chs_94X.db']

## incrase jobs time wall, maximum 2750 minutes (~46 hours)
#config.JobType.maxJobRuntimeMin = 2750

#config.JobType.maxMemoryMB = 2500 # For memory leaks. NB. will block jobs on many sites
## config.JobType.scriptExe = "cmsWrapper.sh"
config.JobType.pyCfgParams = ['datasetName=/GluGluHToGG_M5_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 'processType=signal', 'conditionsJSON=/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_29/src/flashgg/MetaData/data/MetaConditions/Era2018_UL_lowMassDiphotonAnalysis_noDiphotonBoundaries_DataBDT.json']
config.JobType.sendExternalFolder = True

config.section_("Data")
config.Data.inputDataset = "/GluGluHToGG_M5_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
config.Data.inputDBS = 'global'
config.Data.splitting = "FileBased"
config.Data.unitsPerJob = 1
config.Data.publication = True
config.Data.publishDBS = 'phys03'
config.Data.outputDatasetTag = 'UL18_VLowMassDiphoton_SigMC_XSBR1_Mar2024_campaign_v1-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2'
config.Data.outLFNDirBase = "/store/user/atsatsos/UL18_VLowMassDiphoton_SigMC_XSBR1_Mar2024_campaign_v1/v0"

config.section_("Site")
config.Site.storageSite = "T2_US_MIT"
#config.Site.blacklist = ["T2_US_Nebraska"]
#config.Site.blacklist = ["T2_UK_London_Brunel","T1_US_FNAL","T2_US_MIT"]

config.Data.totalUnits = 25000
config.Data.publication = False
config.General.requestName = "pilot_v0_GluGluHToGG_M5_TuneCP5_13TeV-amcatnloFXFX-p8_Summer20UL18-v2_00"
