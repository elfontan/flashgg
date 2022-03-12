import FWCore.ParameterSet.Config as cms
from flashgg.MicroAOD.flashggJets_cfi import flashggUnpackedJets
from flashgg.Taggers.flashggDiPhotonMVA_cfi import flashggDiPhotonMVA
from flashgg.Taggers.flashggVBFMVA_cff import flashggVBFMVA,flashggVBFDiPhoDiJetMVA
from flashgg.Taggers.flashggVHhadMVA_cff import flashggVHhadMVA
from flashgg.Taggers.flashggGluGluHMVA_cff import flashggGluGluHMVA
from flashgg.Taggers.flashggPrefireDiPhotons_cff import flashggPrefireDiPhotons
from flashgg.Taggers.flashggTags_cff import *
from flashgg.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
from flashgg.Taggers.flashggTagSorter_cfi import flashggTagSorter
from flashgg.Taggers.flashggDifferentialPhoIdInputsCorrection_cfi import flashggDifferentialPhoIdInputsCorrection, setup_flashggDifferentialPhoIdInputsCorrection
flashggUntagged.Boundaries     = cms.vdouble(-0.364,0.334,0.753)
#flashggUntagged.Boundaries     = cms.vdouble(-1.0,0.334,0.792)

flashggTagSorter.TagPriorityRanges = cms.VPSet(
#  cms.PSet(TagName = cms.InputTag('flashggVBFTag')),
  cms.PSet(TagName = cms.InputTag('flashggUntagged'))
)
flashggTagSorter.MassCutUpper=cms.double(120.)
flashggTagSorter.MassCutLower=cms.double(65.)
def flashggPrepareTagSequence(process, options):


    setup_flashggDifferentialPhoIdInputsCorrection(process, options)
    flashggPreselectedDiPhotons.src = "flashggPrefireDiPhotons"

    if "flashggDiPhotonMVA" in options:
        flashggDiPhotonMVA.diphotonMVAweightfile = cms.FileInPath(str(options["flashggDiPhotonMVA"]["weightFile"]))
        flashggDiPhotonMVA.Version = cms.string(str(options["flashggDiPhotonMVA"]["version"]))
    if "flashggVBFMVA" in options:
        flashggVBFMVA.vbfMVAweightfile = cms.FileInPath(str(options["flashggVBFMVA"]["weightFile"]))
        flashggVBFMVA.JetIDLevel = cms.string(str(options["flashggVBFMVA"]["jetID"]))
    if "flashggVHhadMVA" in options:
        flashggVHhadMVA.vhHadMVAweightfile = cms.FileInPath(str(options["flashggVHhadMVA"]["weightFile"]))
        flashggVHhadMVA.JetIDLevel = cms.string(str(options["flashggVHhadMVA"]["jetID"]))
    if "flashggGluGluHMVA" in options:
        flashggGluGluHMVA.ggHMVAweightfile = cms.FileInPath(str(options["flashggGluGluHMVA"]["weightFile"]))
        flashggGluGluHMVA.JetIDLevel = cms.string(str(options["flashggGluGluHMVA"]["jetID"]))

    flashggTHQLeptonicTag.MVAweight_tHqVsNonHiggsBkg = cms.FileInPath(str(options['THQLeptonicTag']['MVAweights_VsAllBkg']))
    flashggTHQLeptonicTag.MVAThreshold_tHqVsNonHiggsBkg = cms.double(options['THQLeptonicTag']['MVAThreshold_VsAllBkg'])
    flashggTHQLeptonicTag.MVAweight_tHqVsttHBDT = cms.FileInPath(str(options['THQLeptonicTag']['MVAweights_VsttH']))
    flashggTHQLeptonicTag.MVAThreshold_tHqVsttHBDT = cms.double(options['THQLeptonicTag']['MVAThreshold_VsttH'])

    flashggTagSequence = cms.Sequence(flashggDifferentialPhoIdInputsCorrection
                                      * flashggPrefireDiPhotons
                                      * flashggPreselectedDiPhotons
                                      * flashggDiPhotonMVA
                                      * flashggUnpackedJets
#                                      * flashggVBFMVA
#                                      * flashggVBFDiPhoDiJetMVA
                                      * ( flashggUntagged
                                      #                                  *( flashggSigmaMoMpToMTag
#                                          + flashggVBFTag
#                                          + flashggTTHDiLeptonTag
#                                          + flashggTTHLeptonicTag
#					  + flashggTHQLeptonicTag
#                                     + flashggTTHHadronicTTag                                      
#                                     + flashggTTHHadronicLTag                                      
#                                          + flashggTTHHadronicTag
                                      #############old VH tags##############
                                      #                  + flashggVHEtTag
                                      #                  + flashggVHLooseTag
                                      #                  + flashggVHTightTag
 #                                     ###########updated VH tags############
 #                                         + flashggVHMetTag
 #                                         + flashggWHLeptonicTag
 #                                         + flashggZHLeptonicTag
  #                                        + flashggVHLeptonicLooseTag
 #                                         + flashggVHHadronicTag
                                      )
                                      * flashggTagSorter
                                  )

    return flashggTagSequence
