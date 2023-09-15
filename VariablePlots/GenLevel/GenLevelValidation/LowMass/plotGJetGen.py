# Gen Plots

import numpy as np
from array import array

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

xmin = 0.1
xmax = 100

xbins = [xmin]
while (xbins[-1]<xmax):
  xbins.append(1.01*xbins[-1])

genmasslog = TH1F("genmasslog","genmasslog",len(xbins)-1,array('f',xbins)); genmasslog.Sumw2()

events = Events([
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_0_697389.0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_10_697389.10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_11_697389.11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_12_697389.12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_13_697389.13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_14_697389.14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_15_697389.15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_16_697389.16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_17_697389.17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_18_697389.18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_19_697389.19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_1_697389.1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_20_697389.20.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_21_697389.21.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_22_697389.22.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_23_697389.23.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_24_697389.24.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_25_697389.25.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_26_697389.26.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_27_697389.27.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_28_697389.28.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_29_697389.29.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_2_697389.2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_30_697389.30.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_31_697389.31.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_32_697389.32.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_33_697389.33.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_34_697389.34.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_35_697389.35.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_36_697389.36.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_37_697389.37.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_38_697389.38.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_39_697389.39.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_3_697389.3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_40_697389.40.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_41_697389.41.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_42_697389.42.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_43_697389.43.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_44_697389.44.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_45_697389.45.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_46_697389.46.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_47_697389.47.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_48_697389.48.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_49_697389.49.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_4_697389.4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_5_697389.5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_6_697389.6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_7_697389.7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_8_697389.8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg0to40_v1/wmLHEG_9_697389.9.root"])


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
    genmasslog.Fill(phom.M(),w)

print genmasslog.Integral()

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1000,800)
c1.cd()
c1.SetLeftMargin(0.15)

gPad.SetLogx()
gPad.SetLogy()

genmasslog.SetFillColor(4)
genmasslog.SetLineColor(1)
genmasslog.Draw("ehisto")
genmasslog.SetXTitle("m_{#gamma#gamma} [GeV]")
genmasslog.SetYTitle("Gen Level Events")

leg = TLegend(0.55,0.75,0.85,0.85)
leg.AddEntry(genmasslog,"Photon+Jet Background Sample")
leg.Draw("same")

c1.SaveAs("bkg_gj040_gen_lowmass.png")
c1.SaveAs("bkg_gj040_gen_lowmass.pdf")
