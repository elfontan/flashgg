import FWCore.ParameterSet.Config as cms

diPhotonSelector = cms.EDFilter("FLASHggDiPhotonSelector",
                                src = cms.InputTag("flashggDiPhotons"),
                                cut = cms.string("leadingPhoton().pt > 0. && subLeadingPhoton().pt > 0.")
                                )

diPhotonFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("diPhotonSelector"),
    minNumber = cms.uint32(1)
)
