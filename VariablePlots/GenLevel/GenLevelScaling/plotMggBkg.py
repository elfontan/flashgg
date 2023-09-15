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
genmass040 = TH1F("genmass040","genmass040",120,0,120); genmass040.Sumw2()
genmass040zoomed = TH1F("genmass040zoomed","genmass040zoomed",16,36,44); genmass040zoomed.Sumw2()

events040 = Events([
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_0/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_1/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_2/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_3/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_4/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_5/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_6/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_7/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_8/MiniAOD_9.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_0.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_1.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_10.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_11.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_12.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_13.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_14.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_15.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_16.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_17.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_18.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_19.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_2.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_3.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_4.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_5.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_6.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_7.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_8.root",
"/eos/user/a/atsatsos/mc/BkgMCGeneration/diphoton_mgg0to40_v2/GEN_9/MiniAOD_9.root"])

for i,event in enumerate(events040):
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  if (i==200000):
    print i
    break

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
    if ((pho[0].Pt()>30.0 and pho[1].Pt()>18.0) or (pho[0].Pt()>18.0 and pho[1].Pt()>30.0)):
      if (abs(pho[0].Eta())<2.5 and abs(pho[1].Eta())<2.5):
        genmass040.Fill(phom.M(),w) #FGG ntuple cuts
        genmass040zoomed.Fill(phom.M(),w)

# 40-80 Histograms
genmass4080 = TH1F("genmass4080","genmass4080",120,0,120); genmass4080.Sumw2()
genmass4080zoomed = TH1F("genmass4080zoomed","genmass4080zoomed",16,36,44); genmass4080zoomed.Sumw2()
genmass4080zoomed2 = TH1F("genmass4080zoomed2","genmass4080zoomed2",16,76,84); genmass4080zoomed2.Sumw2()

events4080 = Events([
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/113DBEC9-4937-FE41-BE16-DB99DAFF9CEF.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/2FD81CCC-7D2C-8B45-B891-B0F0AEA34CD0.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/418A05AB-734B-684E-A844-2911DC5B54E3.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/38E8CB9F-ADC4-D846-BEE8-2828A5BB3F7D.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/F5DB57F3-BE28-A246-BC3F-CCE63CCD8008.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/16B0EC73-076D-C940-82A6-2754F0E080DB.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/2A96D112-AE4D-744E-AA79-F37BA9F92D93.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/435132D1-CA9B-B64D-98FF-AD17F1F0A9E5.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/A2EDE8E9-B19E-C241-984D-EE809CB07E86.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/5510241F-0F68-F842-8FCA-51AB9E70DDCA.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/8C477610-A468-A941-A078-549803C31849.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/2A9BFBD1-E227-1D4E-8C6A-80FDEB86BF72.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/958E2A80-609F-8346-A1A6-52C30F68B7CA.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/9655C6E3-3584-BD4A-BFCA-467A28F271D0.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/1A7D9C8C-3143-4C43-B6C0-915659DED1C5.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/8659DAB8-87E4-A84A-A56B-7AB628ED166E.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/7B33038A-F4FE-4C48-AE1F-DA21A0669584.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/E80A355C-2562-AF4C-A746-C3D3838391DF.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/45EAE516-CC29-9941-A6DA-FE65586318D2.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/02CC7998-8BB7-F248-AB3F-FF4A94E5884E.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/D9291B6C-DF36-9845-9C40-8AB24FC37BF9.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/85BFFDC7-069D-3D4B-B10B-4669B83A1654.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/C43DAB23-0E37-644B-9657-67B5CF099245.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/6CF6F52E-6B14-0A4D-A4E2-063CDD5D8C75.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/3B2CC70D-F8EF-BA48-B7D2-265076DB4509.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/4DAE971B-B04D-4D41-8A42-1E87698F6941.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/BD47CDC5-8D8C-9542-B813-97C1FF4FF303.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/1DFCB7C3-F2BF-914E-B1D0-87E6AAD82892.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/62D77DC9-1B81-1240-8FE0-6BB8AADE9A58.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/BEEA360B-8348-0F4B-AA58-46EB802CBCA2.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/B71EC6D5-936A-7A4A-A1C5-FEF841BD76D8.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/5140DB2B-4D6D-AD49-8D13-973E8E587D3C.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/36CC9223-F3CD-154D-ABF6-BC7BCAF4164F.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/D991F185-0D55-EB40-BFEF-0735815C0290.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/E86FA7DA-E20D-C14E-B51C-608D4E84DE70.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/5EAACAD5-916C-5D46-9EFB-87967290129F.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/3F3A7E6C-ECA9-AC46-9DD3-B15EBBD109E9.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/FCF831C3-27EB-CF4F-B0E2-BEE69FC67911.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/9CF55D32-B961-F143-8D38-C050D83240B5.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/D119CD9A-B97F-A946-81D6-F6141E0536FF.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/039FD5F4-392C-DF4E-9499-AC199B966B0C.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/657405C9-4AED-D245-A62B-FE0B11FA2306.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/C074DCA0-9EF7-3943-8CBB-E5CD30B71EE7.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/ABC42C27-7170-B141-A9F2-ED6D4D0A4F34.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/E3D32F7D-CD78-A046-A09A-84800F6BF555.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/E9D015BD-0DAB-0C46-BBE9-C6FB9E6C78F9.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/EABCB87A-DEE0-7B4E-BC5F-593520F94FB3.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/8B1FEAA7-2BD4-1443-9970-24DFC6897E6E.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/256CD542-FCF4-BF4D-ADE6-4710A939F9E0.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/4485FEAD-2675-9F4D-AF88-F1B03FB9F6E4.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/1E5ACE28-ADBE-204B-97D4-7278CF3034FE.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/8B6D5CD3-858B-664C-BF2F-5885CAE3D2D3.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/CB4C1F4E-3BED-2D4E-BF3B-A5FC64AF42C1.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/4FDFD534-970F-5B44-A555-023D026055BE.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/E524EAB1-5F95-0A4E-B380-A096EC3870AB.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/827515CB-AF2A-DC4C-B24C-7B30076FC072.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/5B4E04E1-5D51-9E4E-803C-AC5872089D88.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/1F35288D-6E7C-9B42-A850-DBEAB38E3ABB.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/B2B7FB73-0B2C-2E4D-877C-1DF53203508B.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/26FA84B5-692B-7245-9C0C-83965764B032.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/7FF71AF2-2422-5942-84D3-07FBF2D8BED2.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/43AD27B0-7315-6B40-AB93-06CDAD3F7C84.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/A8919B25-10B0-8B4F-881D-2FAF97C33A68.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/432421D3-B0FE-D042-9A8A-115F7630E0AA.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/91E8B3EF-636F-E048-8B74-7EE21CAB0AB2.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/BED0D40A-8C5A-9146-ADE5-E25202EC28BD.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/5CDF721B-F021-EF45-A384-1EDC0AE28993.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/94D3B344-F637-0541-9721-4F636DFE9261.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/5329ADC0-2544-CA48-952F-7DABFD5DE652.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/95119398-D747-D64F-8F9F-E650F58238EC.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/787A9DB3-FEF3-624A-B9B7-EF4C3873A5EF.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/C6A5F4B1-FAF5-094B-B521-546AD337E561.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/D80C44BA-DA5D-224C-A019-5A9E3FAAA9C8.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/E0C6676E-9101-3B47-83FE-0729A6F6E657.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/4AE34A12-22CE-134F-8169-6623A87B1028.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/178B7412-B22A-E746-905A-0FDF27FEF18E.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/AD6BCA24-4173-3D4D-8606-85FCF02D8F18.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/CEA48C4D-FA93-D948-8F83-34EB91577FDC.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/AA180FDF-CB12-B747-9E49-56601CCD8AC1.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/BD6CB798-336D-044A-8BD7-1E6776E3145F.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/5E2D6FAA-0318-6942-94E2-391C623DB488.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/403713BD-FCB6-1841-A4BB-12DC3E2EE9AC.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/61D6D1BE-3F85-7847-99C1-50108262C697.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/7A322A88-60CA-864A-BAED-033C4804B733.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/9C114597-C9F4-3F4A-9422-CE2672E08FCC.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/7691EC86-19DD-874C-B27E-BEB2D65C465D.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/A3D69618-296B-7848-96A5-E51D53AE4F5F.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/D1606A3A-E22C-6E43-AF5E-65EBEDFA8446.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/D20A703E-B7AD-3A4D-BFFC-F87D8078735E.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/290ECA80-56A2-2941-A472-0DC48CDF3F7A.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/A1ACD2B7-BEA5-4D47-93AF-DE4826CCA524.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/2D974D01-A766-E54A-8AD4-9FBE2F2BA89C.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/5FAD0E29-1E98-2F4C-A99F-50A2584E326B.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/8124D34A-C912-9C4A-9ADC-AE3C079E8368.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/E2E9F3DE-008E-8F4E-96E0-CD5755766ED7.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/AACDB2C5-6C52-FB48-94EF-A9FF951D1F72.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/AA33F81D-4DED-3944-A022-21429896D27D.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/EE51714F-BFDE-B043-ADC7-1181B8A37065.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/CD392D73-4976-AB41-81A1-E313FBCB2CB3.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/F1EDAA3B-CD76-E24A-90EE-EB43BCBBFE85.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/FF15F260-521C-3C40-A618-6697CCA18007.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/AD00597F-7FE1-C048-AE5A-F0EC843300E5.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/5BC52330-E1EE-3F49-AE31-77036B998853.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/0E81A79B-D954-2347-935B-CB1BA761EB14.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/365450F9-D9A5-8946-94F0-8AEE6DF71CAD.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/D99AB933-F894-734C-8A30-D26B075EF11F.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/9E5F5788-2FC5-9840-A3F8-1BE80E0B57DA.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/09131F03-0A98-524E-A133-91DCF11964B3.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/F2869145-C702-E642-B53A-BD013F42537A.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_M40_80-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/AFCBCDA8-34D2-2245-9CD0-C14B7983976C.root"])

nbtw=0
for i,event in enumerate(events4080):
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  if (i==200000):
    print i
    break

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
    if ((pho[0].Pt()>30.0 and pho[1].Pt()>18.0) or (pho[0].Pt()>18.0 and pho[1].Pt()>30.0)):
      if (abs(pho[0].Eta())<2.5 and abs(pho[1].Eta())<2.5):
        genmass4080.Fill(phom.M(),w) #FGG ntuple cuts
        genmass4080zoomed.Fill(phom.M(),w)
        genmass4080zoomed2.Fill(phom.M(),w)
  if (phom.M()>40.0 and phom.M()<80.0):
    nbtw+=1
print "40-80 dipho: ",nbtw

# 80-Inf Histograms
genmass80inf = TH1F("genmass80inf","genmass80inf",120,0,120); genmass80inf.Sumw2()
genmass80infzoomed = TH1F("genmass80infzoomed","genmass80infzoomed",16,76,84); genmass80infzoomed.Sumw2()

events80inf = Events([
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/AB65FCB3-DE53-8846-9E7B-F481CCBC155D.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/B231847C-C00D-7E40-9646-431B3D0B9AA2.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/E3A55628-262D-3A48-9E29-555E2AEAB33E.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/A0BEF426-9BA9-D44A-BF39-8F14E38F8F1D.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/706B9748-A245-7040-87D7-AF4955FAD8F6.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/FEF35EBB-9A42-7E46-8921-33E1F30632D7.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/095D4FCC-6678-354D-9C7E-D58EF79888F1.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/444C83D3-3526-0946-8D82-EF36FAA9B295.root",
"root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/DB17D4DA-8F33-8C48-AC96-45D5B3527C01.root"])

nbtw=0
ndipho=0

for i,event in enumerate(events80inf):
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

#  if (i==200000): break

  if (nbtw==200000):
    print "80infevents surveyed:",i
    break

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
    ndipho+=1
    phom = pho[0]+pho[1]
    if ((pho[0].Pt()>30.0 and pho[1].Pt()>18.0) or (pho[0].Pt()>18.0 and pho[1].Pt()>30.0)):
      if (abs(pho[0].Eta())<2.5 and abs(pho[1].Eta())<2.5):
        genmass80inf.Fill(phom.M(),w) #FGG ntuple cuts
        genmass80infzoomed.Fill(phom.M(),w)
  if (phom.M()>80.0 and phom.M()<120.0):
    nbtw+=1

print "dipho events between 80 and 120:",nbtw
print "all dipho events: ",ndipho

print "pT and eta cuts: ",genmass040.Integral()
print "pT and eta cuts: ",genmass4080.Integral()
print "pT and eta cuts: ",genmass80inf.Integral()

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",800,800)
c1.cd()
c1.SetLeftMargin(0.15)

#norm040norm4080 = genmass4080.Integral()/genmass040.Integral()
#norm80infnorm4080 = genmass4080.Integral()/genmass80inf.Integral()

genmass4080.SetFillColor(6)
genmass4080.SetLineColor(1)
genmass4080.Scale(311.2)
genmass4080.Draw("histo")
genmass4080.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass4080.SetYTitle("Gen Level Events * XS [pb]")

genmass040.SetFillColor(2)
genmass040.SetLineColor(1)
genmass040.Scale(755.0)
#genmass040.Scale(norm040norm4080)
genmass040.Draw("histosame")
genmass040.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass040.SetYTitle("Gen Level Events * XS [pb]")

genmass80inf.SetFillColor(9)
genmass80inf.SetLineColor(1)
genmass80inf.Scale(56.0) #also, check xs for 80-120
#genmass80inf.Scale(norm80infnorm4080)
genmass80inf.Draw("histosame")
genmass80inf.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass80inf.SetYTitle("Gen Level Events * XS [pb]")

leg = TLegend(0.2,0.8,0.5,0.9)
leg.AddEntry(genmass040,"0-40 Diphoton Background")
leg.AddEntry(genmass4080,"40-80 Diphoton Background")
leg.AddEntry(genmass80inf,"80-Inf Diphoton Background")
leg.Draw("same")

c1.SaveAs("mass_mggbkg_gen_norm_v7.png")
c1.SaveAs("mass_mggbkg_gen_norm_v7.pdf")

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c2 = TCanvas("c2","c2",800,800)
c2.cd()
c2.SetLeftMargin(0.15)

genmass4080zoomed.SetLineColor(6)
genmass4080zoomed.Scale(311.2*1.3)
genmass4080zoomed.Draw("ehisto")
genmass4080zoomed.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass4080zoomed.SetYTitle("Gen Level Events * XS [pb]")

genmass040zoomed.SetLineColor(2)
genmass040zoomed.Scale(755.0*1.3)
genmass040zoomed.Draw("ehistosame")
genmass040zoomed.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass040zoomed.SetYTitle("Gen Level Events * XS [pb]")

leg = TLegend(0.6,0.8,0.9,0.9)
leg.AddEntry(genmass040zoomed,"0-40 Diphoton Background")
leg.AddEntry(genmass4080zoomed,"40-80 Diphoton Background")
leg.Draw("same")

c2.SaveAs("mass_mggbkg_gen_zoomed40_v7.png")
c2.SaveAs("mass_mggbkg_gen_zoomed40_v7.pdf")

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c3 = TCanvas("c3","c3",800,800)
c3.cd()
c3.SetLeftMargin(0.15)

genmass4080zoomed2.SetLineColor(6)
genmass4080zoomed2.Scale(311.2*1.3)
genmass4080zoomed2.Draw("ehisto")
genmass4080zoomed2.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass4080zoomed2.SetYTitle("Gen Level Events * XS [pb]")

genmass80infzoomed.SetLineColor(9)
genmass80infzoomed.Scale(56.0)
genmass80infzoomed.Draw("ehistosame")
genmass80infzoomed.SetXTitle("m_{#gamma#gamma} [GeV]")
genmass80infzoomed.SetYTitle("Gen Level Events * XS [pb]")

leg = TLegend(0.6,0.8,0.9,0.9)
leg.AddEntry(genmass4080zoomed2,"40-80 Diphoton Background")
leg.AddEntry(genmass80infzoomed,"80-Inf Diphoton Background")
leg.Draw("same")

c3.SaveAs("mass_mggbkg_gen_zoomed80_v7.png")
c3.SaveAs("mass_mggbkg_gen_zoomed80_v7.pdf")
