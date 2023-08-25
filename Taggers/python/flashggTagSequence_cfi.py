import FWCore.ParameterSet.Config as cms
from flashgg.Taggers.flashggDiPhotonMVA_cfi import flashggDiPhotonMVA
from flashgg.Taggers.flashggVBFMVA_cff import flashggVBFMVA,flashggVBFDiPhoDiJetMVA
from flashgg.Taggers.flashggTags_cff import *
from flashgg.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
from flashgg.Taggers.flashggTagSorter_cfi import flashggTagSorter
from flashgg.Taggers.flashggDifferentialPhoIdInputsCorrection_cfi import flashggDifferentialPhoIdInputsCorrection, setup_flashggDifferentialPhoIdInputsCorrection
from flashgg.MetaData.MetaConditionsReader import *

flashggUntagged.Boundaries     = cms.vdouble(-999.0)
#flashggUntagged.Boundaries     = cms.vdouble(-999.0,-0.364,0.334,0.753)

flashggTagSorter.TagPriorityRanges = cms.VPSet(
  cms.PSet(TagName = cms.InputTag('flashggUntagged'))
)
flashggTagSorter.MassCutUpper=cms.double(100000.)
flashggTagSorter.MassCutLower=cms.double(0.0)

def flashggPrepareTagSequence(process, options):
    setup_flashggDifferentialPhoIdInputsCorrection(process, options)
    flashggPreselectedDiPhotons.src = "flashggDifferentialPhoIdInputsCorrection"

    if flashggDiPhotonMVA in options:
        flashggDiPhotonMVA.diphotonMVAweightfile           = cms.FileInPath(str(options["flashggDiPhotonMVA"]["weightFile"]))
        flashggDiPhotonMVA.diphotonMVAweightfileDefLowMass = cms.FileInPath(str(options["flashggDiPhotonMVA"]["weightFileDefLowMass"]))
        flashggDiPhotonMVA.diphotonMVAweightfileNewMcBdt   = cms.FileInPath(str(options["flashggDiPhotonMVA"]["weightFileNewMcBdt"]))
        flashggDiPhotonMVA.diphotonMVAweightfileDataBdt    = cms.FileInPath(str(options["flashggDiPhotonMVA"]["weightFileDataBdt"]))
        flashggDiPhotonMVA.Version                         = cms.string(str(options["flashggDiPhotonMVA"]["version"]))

    flashggTagSequence = cms.Sequence(flashggDifferentialPhoIdInputsCorrection
                                      * flashggPreselectedDiPhotons
                                      * flashggDiPhotonMVA
                                      * flashggUnpackedJets
                                      * ( flashggUntagged
                                      )
                                      * flashggTagSorter
                                  )

    return flashggTagSequence
