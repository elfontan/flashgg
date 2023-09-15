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

handlePruned, prunedLabel  = Handle ("std::vector<reco::GenParticle>"), ("genParticles")

# Histograms

genmass = TH1F("genmass","genmass",120,0,60); genmass.Sumw2()

events = Events([
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_0_543502.0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_1_543502.1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_2_543502.2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_3_543502.3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_4_543502.4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_5_543502.5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_6_543502.6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_7_543502.7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_8_543502.8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/wmLHEG_9_543502.9.root"])


for i,event in enumerate(events):
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  if (gen.product().weight() != 0.0): w = 1.0
  pruned = handlePruned.product()

  npho=0; 
  pho={}
  phom=TLorentzVector(0,0,0,0)

  for p in pruned :
 
    if (abs(p.pdgId())==22 and p.status()==1):
      pho[npho]=TLorentzVector(p.px(),p.py(),p.pz(),p.energy())
      npho+=1

  if npho>=2: 
    phom = pho[0]+pho[1]
    genmass.Fill(phom.M(),w)

print genmass.Integral()

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1000,800)
c1.cd()
c1.SetLeftMargin(0.15)

genmass.SetFillColor(2)
genmass.SetLineColor(1)
genmass.Draw("ehisto")
genmass.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass.SetYTitle("Gen Level Events")

leg = TLegend(0.55,0.75,0.85,0.85)
leg.AddEntry(genmass,"Diphoton Background Sample")
leg.Draw("same")

c1.SaveAs("bkg_mgg040_gen.png")
c1.SaveAs("bkg_mgg040_gen.pdf")

