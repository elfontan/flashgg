minimalVariables = ["CMS_hgg_mass[1500,0.0,150.0]:=diPhoton().mass",
                    "sigmaMoM_decorr:=diPhotonMVA().decorrSigmarv",
                    "dZ[40,-20.,20.]:=(tagTruth().genPV().z-diPhoton().vtx().z)", # store actual value
                                                                                  #when doing systematics, variables need to have a binning
                                                                                  #specified, otherwise the rooDataHist end up empty.
            								          #an assert in the code prevents you from doing this.
                    "genZ:=tagTruth().genPV().z",
                    "centralObjectWeight[1,-999999.,999999.] := centralWeight"
]

minimalHistograms = []

minimalNonSignalVariables = ["CMS_hgg_mass[1500,0.0,150.0]:=diPhoton().mass",
                             "sigmaRV:=diPhotonMVA().sigmarv",
                             "sigmaWV:=diPhotonMVA().sigmawv",
                             "sigmaMoM_decorr:=diPhotonMVA().decorrSigmarv"]#,"centralObjectWeight[1,-999999.,999999.] := centralWeight"]

minimalVariablesHTXS = minimalVariables+["stage0bin[72,9.5,81.5] := tagTruth().HTXSstage0bin"]

defaultVariables=["CMS_hgg_mass[10000,0.0,100000.0]:=diPhoton().mass", 
#Weights
                  "centralObjectWeight[1,-999999.,999999.] := centralWeight",
                  "weight_electronVetoSF[1,-999999.,999999.]:=weight(\"electronVetoSFCentral\")",
                  "weight_PreselSF[1,-999999.,999999.]:=weight(\"PreselSFCentral\")",
                  "weight_TriggerWeight[1,-999999.,999999.]:=weight(\"TriggerWeightCentral\")",
                  "weight_LooseMvaSF[1,-999999.,999999.]:=weight(\"LooseMvaSFCentral\")",
                  "weight_FracRVWeight[1,-999999.,999999.]:=weight(\"FracRVWeightCentral\")",
                  "weight_FracRVNvtxWeight[1,-999999.,999999.]:=weight(\"FracRVNvtxWeightCentral\")",
                  "weight_SigmaEOverESmearing[1,-999999.,999999.]:=weight(\"SigmaEOverESmearingCentral\")",
                                    "diphoMVA                 :=diPhotonMVA().result",
                                    "maxEta                   :=max(abs(diPhoton().leadingPhoton.superCluster.eta),abs(diPhoton().leadingPhoton.superCluster.eta))",
                                    "vtxZ                     :=diPhoton().vtx().z",
                                    "dZ0                      :=0",
                                    "leadPt                   :=diPhoton().leadingPhoton.pt",
                                    "subleadPt                :=diPhoton().subLeadingPhoton.pt",
                                    "leadEta                   :=diPhoton().leadingPhoton.superCluster.eta",
                                    "subleadEta                :=diPhoton().subLeadingPhoton.superCluster.eta",
                                    "leadPhi                   :=diPhoton().leadingPhoton.superCluster.phi",
                                    "subleadPhi                :=diPhoton().subLeadingPhoton.superCluster.phi",
#Vertex Variables
				    "vtxprob                := diPhotonMVA().vtxprob",
				    "ptbal                  := diPhoton().ptBal",
				    "ptasym                 := diPhoton().ptAsym",
				    "logspt2                := diPhoton().logSumPt2",
				    "p2conv                 := diPhoton().pullConv",
				    "nconv                  := diPhoton().nConv",
				    "vtxmva                 := diPhoton().vtxProbMVA",
				    "vtxdz                  := diPhoton().dZ1",
				    "vtx_x                  := diPhoton().vtx().x",
				    "vtx_y                  := diPhoton().vtx().y",
				    "vtx_z                  := diPhoton().vtx().z",


#Diphoton Variables
				    "dipho_sumpt            := diPhoton().sumPt",
				    "dipho_cosphi           := abs(cos(diPhoton().leadingPhoton.phi - diPhoton().subLeadingPhoton.phi))",
				    "dipho_mass             := diPhoton().mass",
				    "dipho_pt               := diPhoton().pt",
				    "dipho_phi              := diPhoton().phi",
				    "dipho_eta              := diPhoton().eta",
				    "dipho_e                := diPhoton().energy",
				    "dipho_PtoM             := diPhoton().pt/diPhoton().mass",
				    "cosphi                 := diPhotonMVA().CosPhi",
				    "sigmaMrvoM             := diPhotonMVA().sigmarv",
				    "sigmaMwvoM             := diPhotonMVA().sigmawv",
				    "w_signal               := diPhotonMVA().vtxprob/diPhotonMVA().sigmarv+(1.0-diPhotonMVA().vtxprob)/diPhotonMVA().sigmawv",

#Photon Variables, including corrected and uncorrected ones
				    #"leadMatchType          := diPhoton().leadingPhoton.genMatchType",
				    #"subleadMatchType       := diPhoton().subLeadingPhoton.genMatchType",
				    "dipho_lead_prompt      := diPhoton().leadingPhoton.genMatchType",
				    "dipho_sublead_prompt   := diPhoton().subLeadingPhoton.genMatchType",

				    "dipho_leadEt           := diPhoton().leadingPhoton.et",
				    "dipho_leadEt_corr      := ? diPhoton().leadingPhoton.hasUserFloat(\"afterDiffCorr_regr_E\")>0 ? diPhoton().leadingPhoton.userFloat(\"afterDiffCorr_regr_E\") : -1.",
				    "dipho_leadEt_uncorr    := ? diPhoton().leadingPhoton.hasUserFloat(\"reco_E\")>0 ? diPhoton().leadingPhoton.userFloat(\"reco_E\") : -1.",

				    "dipho_leadEta          := diPhoton().leadingPhoton.eta",
				    "dipho_leadPhi          := diPhoton().leadingPhoton.phi",
				    "dipho_lead_sieie       := diPhoton().leadingPhoton.full5x5_sigmaIetaIeta",
#				    "dipho_lead_sieie       := diPhoton().leadingPhoton.sigmaIetaIeta",
#				    "dipho_lead_sieie_corr  := diPhoton().leadingPhoton.full5x5_sigmaIetaIeta",
				    "dipho_lead_sieie_uncorr := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_sieie\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_sieie\") : -1",

				    "dipho_lead_hoe         := diPhoton().leadingPhoton.hadronicOverEm",
				    "dipho_lead_sigmaEoE    := diPhoton().leadingPhoton.sigEOverE",
				    "dipho_lead_ptoM        := diPhoton().leadingPhoton.pt/diPhoton().mass",
				    "dipho_leadR9           := diPhoton().leadingPhoton.full5x5_r9",
				    "dipho_leadR9_uncorr    := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_r9\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_r9\") : -1.",
				    "dipho_leadIDMVA        := diPhoton().leadingView.phoIdMvaWrtChosenVtx",
				    "dipho_lead_elveto      := diPhoton().leadingPhoton.passElectronVeto",
				    "dipho_lead_chiso       := diPhoton().leadingView.pfChIso03WrtChosenVtx",
				    "dipho_lead_chisow      := diPhoton().leadingPhoton.pfChgIsoWrtWorstVtx04",
				    "dipho_lead_phoiso      := diPhoton().leadingPhoton.pfPhoIso03",
				    "dipho_lead_phoiso_uncorr := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_pfPhoIso03\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_pfPhoIso03\") : -1",
				    "dipho_lead_phoiso04    := diPhoton().leadingPhoton.pfPhoIso04",
				    "dipho_lead_neutiso      := diPhoton().leadingPhoton.pfNeutIso03",
				    "dipho_lead_ecaliso03   := diPhoton().leadingPhoton.ecalRecHitSumEtConeDR03",
				    "dipho_lead_hcaliso03   := diPhoton().leadingPhoton.hcalTowerSumEtConeDR03",
				    "dipho_lead_pfcluecal03 := diPhoton().leadingPhoton.ecalPFClusterIso",
				    "dipho_lead_pfcluhcal03 := diPhoton().leadingPhoton.hcalPFClusterIso",
				    "dipho_lead_trkiso03    := diPhoton().leadingPhoton.trkSumPtHollowConeDR03",
				    "dipho_lead_pfchiso2    := diPhoton().leadingView.pfChIso02WrtChosenVtx",
				    "dipho_lead_haspixelseed:= diPhoton().leadingPhoton.hasPixelSeed",
				    "dipho_lead_sieip       := diPhoton().leadingPhoton.sieip",
				    "dipho_lead_sieip_uncorr := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_sieip\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_sieip\") : -1",

#				    "dipho_lead_etawidth    := diPhoton().leadingPhoton.superCluster.etaWidth",
#				    "dipho_lead_etawidth_corr := ? diPhoton().leadingPhoton.hasUserFloat(\"etaWidth\")>0 ? diPhoton().leadingPhoton.userFloat(\"etaWidth\") : -1",
				    "dipho_lead_etawidth := ? diPhoton().leadingPhoton.hasUserFloat(\"etaWidth\")>0 ? diPhoton().leadingPhoton.userFloat(\"etaWidth\") : diPhoton().leadingPhoton.superCluster.etaWidth",
				    "dipho_lead_etawidth_uncorr := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_etaWidth\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_etaWidth\") : -1",
				    "dipho_lead_scetawidth    := diPhoton().leadingPhoton.superCluster.etaWidth",

#				    "dipho_lead_phiwidth    := diPhoton().leadingPhoton.superCluster.phiWidth",
#				    "dipho_lead_phiwidth_corr := ? diPhoton().leadingPhoton.hasUserFloat(\"phiWidth\")>0 ? diPhoton().leadingPhoton.userFloat(\"phiWidth\") : -1",
				    "dipho_lead_phiwidth := ? diPhoton().leadingPhoton.hasUserFloat(\"phiWidth\")>0 ? diPhoton().leadingPhoton.userFloat(\"phiWidth\") : diPhoton().leadingPhoton.superCluster.phiWidth",
				    "dipho_lead_phiwidth_uncorr := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_phiWidth\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_phiWidth\") : -1",
				    "dipho_lead_scphiwidth    := diPhoton().leadingPhoton.superCluster.phiWidth",

				    "dipho_lead_regrerr     := diPhoton().leadingPhoton.sigEOverE * diPhoton().leadingPhoton.energy",
				    "dipho_lead_s4ratio     := diPhoton().leadingPhoton.s4",
				    "dipho_lead_s4ratio_uncorr := ? diPhoton().leadingPhoton.hasUserFloat(\"uncorr_s4\")>0 ? diPhoton().leadingPhoton.userFloat(\"uncorr_s4\") : -1",

				    "dipho_lead_effSigma    :=  diPhoton().leadingPhoton.esEffSigmaRR",
				    "dipho_lead_scraw       :=  diPhoton().leadingPhoton.superCluster.rawEnergy",
				    "dipho_lead_ese         :=  diPhoton().leadingPhoton.superCluster.preshowerEnergy",

				    "dipho_subleadEt        := diPhoton().subLeadingPhoton.et",
				    "dipho_subleadEt_corr      := ? diPhoton().subLeadingPhoton.hasUserFloat(\"afterDiffCorr_regr_E\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"afterDiffCorr_regr_E\") : -1.",
				    "dipho_subleadEt_uncorr    := ? diPhoton().subLeadingPhoton.hasUserFloat(\"reco_E\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"reco_E\") : -1.",

				    "dipho_subleadEta       := diPhoton().subLeadingPhoton.eta",
				    "dipho_subleadPhi       := diPhoton().subLeadingPhoton.phi",
				    "dipho_sublead_sieie    := diPhoton().subLeadingPhoton.full5x5_sigmaIetaIeta",
#				    "dipho_sublead_sieie    := diPhoton().subLeadingPhoton.sigmaIetaIeta",
#				    "dipho_sublead_sieie_corr  := diPhoton().subLeadingPhoton.full5x5_sigmaIetaIeta",
				    "dipho_sublead_sieie_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_sieie\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_sieie\") : -1",

				    "dipho_sublead_hoe      := diPhoton().subLeadingPhoton.hadronicOverEm",
				    "dipho_sublead_sigmaEoE := diPhoton().subLeadingPhoton.sigEOverE",
				    "dipho_sublead_ptoM     := diPhoton().subLeadingPhoton.pt/diPhoton().mass",
				    "dipho_subleadR9        := diPhoton().subLeadingPhoton.full5x5_r9",
				    "dipho_subleadR9_uncorr    := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_r9\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_r9\") : -1.",

				    "dipho_subleadIDMVA     := diPhoton().subLeadingView.phoIdMvaWrtChosenVtx",
				    "dipho_sublead_elveto   := diPhoton().subLeadingPhoton.passElectronVeto",
				    "dipho_sublead_chiso    := diPhoton().subLeadingView.pfChIso03WrtChosenVtx",
				    "dipho_sublead_chisow   := diPhoton().subLeadingPhoton.pfChgIsoWrtWorstVtx04",
				    "dipho_sublead_phoiso   := diPhoton().subLeadingPhoton.pfPhoIso03",
				    "dipho_sublead_phoiso_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_pfPhoIso03\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_pfPhoIso03\") : -1",

				    "dipho_sublead_phoiso04 := diPhoton().subLeadingPhoton.pfPhoIso04",
				    "dipho_sublead_neutiso   := diPhoton().subLeadingPhoton.pfNeutIso03",
				    "dipho_sublead_ecaliso03:= diPhoton().subLeadingPhoton.ecalRecHitSumEtConeDR03",
				    "dipho_sublead_hcaliso03:= diPhoton().subLeadingPhoton.hcalTowerSumEtConeDR03",
				    "dipho_sublead_pfcluecal03 := diPhoton().subLeadingPhoton.ecalPFClusterIso",
				    "dipho_sublead_pfcluhcal03 := diPhoton().subLeadingPhoton.hcalPFClusterIso",
				    "dipho_sublead_trkiso03    := diPhoton().subLeadingPhoton.trkSumPtHollowConeDR03",
				    "dipho_sublead_pfchiso2    := diPhoton().subLeadingView.pfChIso02WrtChosenVtx",
				    "dipho_sublead_haspixelseed:= diPhoton().subLeadingPhoton.hasPixelSeed",
				    "dipho_sublead_sieip       := diPhoton().subLeadingPhoton.sieip",
				    "dipho_sublead_sieip_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_sieip\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_sieip\") : -1",

#				    "dipho_sublead_etawidth    := diPhoton().subLeadingPhoton.superCluster.etaWidth",
#				    "dipho_sublead_etawidth_corr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"etaWidth\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"etaWidth\") : -1",
				    "dipho_sublead_etawidth := ? diPhoton().subLeadingPhoton.hasUserFloat(\"etaWidth\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"etaWidth\") : diPhoton().subLeadingPhoton.superCluster.etaWidth",
				    "dipho_sublead_etawidth_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_etaWidth\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_etaWidth\") : -1",
				    "dipho_sublead_scetawidth    := diPhoton().subLeadingPhoton.superCluster.etaWidth",

#				    "dipho_sublead_phiwidth    := diPhoton().subLeadingPhoton.superCluster.phiWidth",
#				    "dipho_sublead_phiwidth_corr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"phiWidth\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"phiWidth\") : -1",
				    "dipho_sublead_phiwidth := ? diPhoton().subLeadingPhoton.hasUserFloat(\"phiWidth\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"phiWidth\") : diPhoton().subLeadingPhoton.superCluster.phiWidth",
				    "dipho_sublead_phiwidth_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_phiWidth\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_phiWidth\") : -1",
				    "dipho_sublead_scphiwidth    := diPhoton().subLeadingPhoton.superCluster.phiWidth",

				    "dipho_sublead_regrerr     := diPhoton().subLeadingPhoton.sigEOverE * diPhoton().subLeadingPhoton.energy",
				    "dipho_sublead_s4ratio     :=  diPhoton().subLeadingPhoton.s4",
				    "dipho_sublead_s4ratio_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat(\"uncorr_s4\")>0 ? diPhoton().subLeadingPhoton.userFloat(\"uncorr_s4\") : -1",

				    "dipho_sublead_effSigma    :=  diPhoton().subLeadingPhoton.esEffSigmaRR",
				    "dipho_sublead_scraw       :=  diPhoton().subLeadingPhoton.superCluster.rawEnergy",
				    "dipho_sublead_ese         :=  diPhoton().subLeadingPhoton.superCluster.preshowerEnergy"]

phoIDCorrectionVariables=[
                           'leadEnergy := diPhoton().leadingPhoton.p4.energy',
                           'leadInitialEnergy := diPhoton().leadingPhoton.energyAtStep("initial")',
                           'leadEnergy_corr := ? diPhoton().leadingPhoton.hasUserFloat("afterDiffCorr_regr_E")>0 ? diPhoton().leadingPhoton.userFloat("afterDiffCorr_regr_E") : -1.',
                           'leadEnergy_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("reco_E")>0 ? diPhoton().leadingPhoton.userFloat("reco_E") : -1.',
                           'leadPhoId := diPhoton().leadingView.phoIdMvaWrtChosenVtx',
                           'leadPt := diPhoton().leadingPhoton.pt',
                           'leadEta := diPhoton().leadingPhoton.superCluster().eta',
                           'leadPhi := diPhoton().leadingPhoton.phi',
                           'leadR9 := diPhoton().leadingPhoton.full5x5_r9',
                           'leadR9_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_r9")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_r9") : -1.',
                           'leadS4 := diPhoton().leadingPhoton.s4',
                           'leadS4_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_s4")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_s4") : -1',
                           'leadSieie := diPhoton().leadingPhoton.full5x5_sigmaIetaIeta',
                           'leadSieie_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_sieie")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_sieie") : -1',
                           'leadSieip := diPhoton().leadingPhoton.sieip',
                           'leadSieip_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_sieip")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_sieip") : -1',
                           'leadEtaWidth := ? diPhoton().leadingPhoton.hasUserFloat("etaWidth")>0 ? diPhoton().leadingPhoton.userFloat("etaWidth") : -1',
                           'leadEtaWidth_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_etaWidth")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_etaWidth") : -1',
                           'leadPhiWidth := ? diPhoton().leadingPhoton.hasUserFloat("phiWidth")>0 ? diPhoton().leadingPhoton.userFloat("phiWidth") : -1',
                           'leadPhiWidth_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_phiWidth")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_phiWidth") : -1',
                           'leadPhoIso := diPhoton().leadingPhoton.pfPhoIso03',
                           'leadPhoIso_uncorr := ? diPhoton().leadingPhoton.hasUserFloat("uncorr_pfPhoIso03")>0 ? diPhoton().leadingPhoton.userFloat("uncorr_pfPhoIso03") : -1',
                           'subleadEnergy := diPhoton().subLeadingPhoton.p4.energy',
                           'subleadInitialEnergy := diPhoton().subLeadingPhoton.energyAtStep("initial")',
                           'subleadEnergy_corr := ? diPhoton().subLeadingPhoton.hasUserFloat("afterDiffCorr_regr_E")>0 ? diPhoton().subLeadingPhoton.userFloat("afterDiffCorr_regr_E") : -1.',
                           'subleadEnergy_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("reco_E")>0 ? diPhoton().subLeadingPhoton.userFloat("reco_E") : -1.',
                           'subleadPhoId := diPhoton().subLeadingView.phoIdMvaWrtChosenVtx',
                           'subleadPt := diPhoton().subLeadingPhoton.pt',
                           'subleadEta := diPhoton().subLeadingPhoton.superCluster().eta',
                           'subleadPhi := diPhoton().subLeadingPhoton.phi',
                           'subleadR9 := diPhoton().subLeadingPhoton.full5x5_r9',
                           'subleadR9_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_r9")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_r9") : -1',
                           'subleadS4 := diPhoton().subLeadingPhoton.s4',
                           'subleadS4_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_s4")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_s4") : -1',
                           'subleadSieie := diPhoton().subLeadingPhoton.full5x5_sigmaIetaIeta',
                           'subleadSieie_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_sieie")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_sieie") : -1',
                           'subleadSieip := diPhoton().subLeadingPhoton.sieip',
                           'subleadSieip_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_sieip")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_sieip") : -1',
                           'subleadEtaWidth := ? diPhoton().subLeadingPhoton.hasUserFloat("etaWidth")>0 ? diPhoton().subLeadingPhoton.userFloat("etaWidth") : -1',
                           'subleadEtaWidth_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_etaWidth")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_etaWidth") : -1',
                           'subleadPhiWidth := ? diPhoton().subLeadingPhoton.hasUserFloat("phiWidth")>0 ? diPhoton().subLeadingPhoton.userFloat("phiWidth") : -1',
                           'subleadPhiWidth_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_phiWidth")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_phiWidth") : -1',
                           'subleadPhoIso := diPhoton().subLeadingPhoton.pfPhoIso03',
                           'subleadPhoIso_uncorr := ? diPhoton().subLeadingPhoton.hasUserFloat("uncorr_pfPhoIso03")>0 ? diPhoton().subLeadingPhoton.userFloat("uncorr_pfPhoIso03") : -1'
]


defaultHistograms=["CMS_hgg_mass>>mass(1500,0.0,150.0)",
                                     "subleadPt:leadPt>>ptLeadvsSub(180,20,200:180,20,200)",
                                     "diphoMVA>>diphoMVA(50,0,1)",
                                     "maxEta>>maxEta[0.,0.1,0.2,0.3,0.4,0.6,0.8,1.0,1.2,1.4442,1.566,1.7,1.8,2.,2.2,2.3,2.5]"
                                     ]

systematicVariables=["CMS_hgg_mass[1500,0.0,150.0]:=diPhoton().mass"]#,"centralObjectWeight[1,-999999.,999999.] := centralWeight"]
systematicHistograms=["CMS_hgg_mass>>mass(1500,0.0,150.0)"]

systematicVariablesHTXS = systematicVariables+["stage0bin[72,9.5,81.5] := tagTruth().HTXSstage0bin"]
