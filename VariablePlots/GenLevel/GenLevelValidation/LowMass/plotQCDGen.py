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

xmin = 0.1
xmax = 100

xbins = [xmin]
while (xbins[-1]<xmax):
  xbins.append(1.01*xbins[-1])

genmasslog = TH1F("genmasslog","genmasslog",len(xbins)-1,array('f',xbins)); genmasslog.Sumw2()

events = Events([
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_0_708828.0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_10_708828.10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_11_708828.11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_12_708828.12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_13_708828.13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_14_708828.14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_15_708828.15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_16_708828.16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_17_708828.17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_18_708828.18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_19_708828.19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_1_708828.1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_20_708828.20.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_21_708828.21.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_22_708828.22.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_23_708828.23.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_24_708828.24.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_25_708828.25.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_26_708828.26.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_27_708828.27.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_28_708828.28.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_29_708828.29.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_2_708828.2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_3_708828.3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_4_708828.4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_5_708828.5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_6_708828.6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_7_708828.7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_8_708828.8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg0to40_v1/wmLHEG_9_708828.9.root"])


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

genmasslog.SetFillColor(5)
genmasslog.SetLineColor(1)
genmasslog.Draw("ehisto")
genmasslog.SetXTitle("m_{#gamma#gamma} [GeV]")
genmasslog.SetYTitle("Gen Level Events")

leg = TLegend(0.55,0.75,0.85,0.85)
leg.AddEntry(genmasslog,"QCD Background Sample")
leg.Draw("same")

c1.SaveAs("bkg_qcd040_gen_lowmass.png")
c1.SaveAs("bkg_qcd040_gen_lowmass.pdf")
