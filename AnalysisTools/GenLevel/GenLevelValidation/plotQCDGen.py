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
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_0_712468.0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_10_712468.10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_11_712468.11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_12_712468.12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_13_712468.13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_14_712468.14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_15_712468.15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_16_712468.16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_17_712468.17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_18_712468.18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_19_712468.19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_1_712468.1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_20_712468.20.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_21_712468.21.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_22_712468.22.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_23_712468.23.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_24_712468.24.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_25_712468.25.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_26_712468.26.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_27_712468.27.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_28_712468.28.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_29_712468.29.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_2_712468.2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_30_712468.30.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_31_712468.31.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_32_712468.32.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_33_712468.33.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_34_712468.34.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_35_712468.35.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_36_712468.36.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_37_712468.37.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_38_712468.38.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_39_712468.39.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_3_712468.3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_40_712468.40.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_41_712468.41.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_42_712468.42.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_43_712468.43.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_44_712468.44.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_45_712468.45.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_46_712468.46.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_47_712468.47.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_48_712468.48.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_49_712468.49.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_4_712468.4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_50_712468.50.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_51_712468.51.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_52_712468.52.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_53_712468.53.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_54_712468.54.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_55_712468.55.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_56_712468.56.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_57_712468.57.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_58_712468.58.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_59_712468.59.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_5_712468.5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_60_712468.60.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_61_712468.61.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_62_712468.62.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_63_712468.63.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_64_712468.64.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_65_712468.65.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_66_712468.66.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_67_712468.67.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_68_712468.68.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_69_712468.69.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_6_712468.6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_70_712468.70.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_71_712468.71.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_72_712468.72.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_73_712468.73.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_74_712468.74.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_75_712468.75.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_76_712468.76.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_77_712468.77.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_78_712468.78.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_79_712468.79.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_7_712468.7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_80_712468.80.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_81_712468.81.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_82_712468.82.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_83_712468.83.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_84_712468.84.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_85_712468.85.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_86_712468.86.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_87_712468.87.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_88_712468.88.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_89_712468.89.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_8_712468.8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_90_712468.90.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_91_712468.91.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_92_712468.92.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_93_712468.93.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_94_712468.94.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_95_712468.95.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_96_712468.96.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_97_712468.97.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_98_712468.98.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_99_712468.99.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/qcd_mgg5to40_v1/wmLHEG_9_712468.9.root"])


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

genmass.SetFillColor(5)
genmass.SetLineColor(1)
genmass.Draw("ehisto")
genmass.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass.SetYTitle("Gen Level Events")

leg = TLegend(0.55,0.75,0.85,0.85)
leg.AddEntry(genmass,"QCD Background Sample")
leg.Draw("same")

c1.SaveAs("bkg_qcd540_gen.png")
c1.SaveAs("bkg_qcd540_gen.pdf")
