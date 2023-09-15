# Gen Plots

# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
from ROOT import *
gROOT.SetBatch(True)
sys.argv = oldargv
gStyle.SetOptStat(0)
gStyle.SetOptFit(1)
from array import array

# load FWLite C++ libraries
gSystem.Load("libFWCoreFWLite.so");
gSystem.Load("libDataFormatsFWLite.so");
#AutoLibraryLoader.enable()
FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

gen, genLabel = Handle("GenEventInfoProduct"), ("generator")

#handlePruned, prunedLabel  = Handle ("std::vector<reco::GenParticle>"), ("genParticles") # for GEN level
handlePruned, prunedLabel  = Handle ("std::vector<reco::GenParticle>"), ("prunedGenParticles") # for MiniAOD level

# 0-40 Histograms
genmass = TH1F("genmass","genmass",120,0,120); genmass.Sumw2()

events = Events(["/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/BkgMCCutFlowPlots_v2/GenLevel/extractedMiniAOD.root"])

for i,event in enumerate(events):
  print "Event: ",i

  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  if (gen.product().weight() != 0.0): w = 1.0
  
  pruned = handlePruned.product()

  npho=0; 

  pho={}
  phom=TLorentzVector(0,0,0,0)

  print " "
  for j,p in enumerate(pruned):
    print "Gen Particle:", j
    print "Particle ID: ", p.pdgId()
    if(p.pdgId()==22): print "This is a photon."
    print "Status: ", p.status()
#    print "Mother ID: ", p.mother().pdgId()
    print "pT: ", p.pt()
    print "Eta: ", p.eta()
    print "Phi: ", p.phi()
    print "Energy: ", p.energy()
    print " "
