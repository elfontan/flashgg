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
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_0_711823.0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_10_711823.10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_11_711823.11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_12_711823.12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_13_711823.13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_14_711823.14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_15_711823.15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_16_711823.16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_17_711823.17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_18_711823.18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_19_711823.19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_1_711823.1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_20_711823.20.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_21_711823.21.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_22_711823.22.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_23_711823.23.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_24_711823.24.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_25_711823.25.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_26_711823.26.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_27_711823.27.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_28_711823.28.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_29_711823.29.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_2_711823.2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_30_711823.30.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_31_711823.31.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_32_711823.32.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_33_711823.33.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_34_711823.34.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_35_711823.35.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_36_711823.36.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_37_711823.37.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_38_711823.38.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_39_711823.39.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_3_711823.3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_40_711823.40.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_41_711823.41.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_42_711823.42.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_43_711823.43.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_44_711823.44.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_45_711823.45.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_46_711823.46.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_47_711823.47.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_48_711823.48.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_49_711823.49.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_4_711823.4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_50_711823.50.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_51_711823.51.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_52_711823.52.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_53_711823.53.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_54_711823.54.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_55_711823.55.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_56_711823.56.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_57_711823.57.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_58_711823.58.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_59_711823.59.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_5_711823.5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_60_711823.60.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_61_711823.61.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_62_711823.62.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_63_711823.63.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_64_711823.64.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_65_711823.65.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_66_711823.66.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_67_711823.67.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_68_711823.68.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_69_711823.69.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_6_711823.6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_70_711823.70.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_71_711823.71.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_72_711823.72.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_73_711823.73.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_74_711823.74.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_75_711823.75.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_76_711823.76.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_77_711823.77.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_78_711823.78.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_79_711823.79.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_7_711823.7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_80_711823.80.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_81_711823.81.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_82_711823.82.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_83_711823.83.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_84_711823.84.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_85_711823.85.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_86_711823.86.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_87_711823.87.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_88_711823.88.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_89_711823.89.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_8_711823.8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_90_711823.90.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_91_711823.91.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_92_711823.92.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_93_711823.93.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_94_711823.94.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_95_711823.95.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_96_711823.96.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_97_711823.97.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_98_711823.98.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_99_711823.99.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/gjets_mgg2to40_v1/wmLHEG_9_711823.9.root"])


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

gPad.SetLogy()

genmass.SetFillColor(4)
genmass.SetLineColor(1)
genmass.Draw("ehisto")
genmass.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass.SetYTitle("Gen Level Events")

leg = TLegend(0.55,0.75,0.85,0.85)
leg.AddEntry(genmass,"Photon+Jet Background Sample")
leg.Draw("same")

c1.SaveAs("bkg_gj240_gen.png")
c1.SaveAs("bkg_gj240_gen.pdf")
