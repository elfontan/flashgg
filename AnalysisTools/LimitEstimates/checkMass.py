#!/usr/bin/env python3

# ********************************
# usage: 
#    python3 checkWeights.py
#    (e.g. from CMSSW_12_4_0/src)
# ********************************

import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem
from ROOT import *
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooDataHist, RooCBShape, RooNumConvPdf, RooFFTConvPdf, RooGlobalFunc
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan
from array import array
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# Signal Samples
filelist = [
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M5_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M10_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M15_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M20_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M25_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M30_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M35_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M40_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M45_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M50_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M55_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M60_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M65_cat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_Categories_NN0p907/ggH_M70_cat.root"
]


# Data Sample
datafile = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_ParametricNNNearest_BkgCat/all2018data.root","READ")


# NOTE: Weight computation
#       1) Gen weight: Number of events generated/sum of event counts (positively and negatively weighted) in MiniAOD
#       2) Lumi weight: xs* br * kf * target_lumi/sum of event weights (positive and negative)
#       3) w0 = gen weight * lumi weight
#       Event dependency begins here - the rest are sample dependent
#       4) PU weight - weight adjusted for PU
#       5) Tag central weight - need to check what this is/what it includes
#       6) Check if systematics (SFs of preselection, trigger, vertex, etc.) are included
#       Weight = gen weight * lumi weight * PU weight * tag central weight

target_lumi = 1000.0 #pb

masspoints = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
#xs = [1.0, 1900.0, 1203.0, 845.8, 632.2, 492.3, 394.9, 324.0, 270.6, 229.4, 196.8, 170.6, 149.2, 131.5]
#br = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0006871]
xs = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] #assume to be 1 for limit estimates
br = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] #assume to be 1 for limit estimates

kf = [1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06]
nEvents = [100226.0, 98926.0, 98377.0, 102177.0, 101758.0, 102829.0, 103448.0, 100223.0, 102755.0, 100752.0, 100581.0, 99832.0, 232630.0, 190139.0]
nEvents_sign = [46103.96, 45505.96, 49188.5, 49044.96, 46808.68, 47301.34, 49655.04, 48107.04, 49322.4, 56421.12, 58336.98, 59899.2, 144230.6, 117886.18]
gen = [3683.64, 2866.86, 2247.3, 1832.06, 1548.75, 1345.64, 1153.35, 1003.56, 881.80, 775.896, 683.22, 614.566, 560.66, 505.814] #can be assigned negatively to events

v_eff0 = []
v_eff1 = []
v_eff = []

for m in range(len(filelist)):
    f_ggH = TFile.Open(filelist[m]) 
    print("Reading file", filelist[m],"...")
    
    lumi_diff = nEvents[m]/nEvents_sign[m]
    print("Lumi Diff: ", lumi_diff)

    treename_cat0 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_0")    
    datatree_cat0 = datafile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

    treename_cat1 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_1")    
    datatree_cat1 = datafile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")

    ggh_cat0 = TH1F("ggh_M"+str(masspoints[m])+"_cat0", "ggh_M"+str(masspoints[m])+"_cat0", 80, 0.9*masspoints[m], 1.1*masspoints[m])
    data_cat0 = TH1F("data_M"+str(masspoints[m])+"_cat0", "data_M"+str(masspoints[m])+"_cat0", 80, 0.9*masspoints[m], 1.1*masspoints[m])

    ggh_cat1 = TH1F("ggh_M"+str(masspoints[m])+"_cat1", "ggh_M"+str(masspoints[m])+"_cat1", 80, 0.9*masspoints[m], 1.1*masspoints[m])
    data_cat1 = TH1F("data_M"+str(masspoints[m])+"_cat1", "data_M"+str(masspoints[m])+"_cat1", 80, 0.9*masspoints[m], 1.1*masspoints[m])

    ggh_cat = TH1F("ggh_M"+str(masspoints[m])+"_cat", "ggh_M"+str(masspoints[m])+"_cat", 80, 0.9*masspoints[m], 1.1*masspoints[m])
    data_cat = TH1F("data_M"+str(masspoints[m])+"_cat", "data_M"+str(masspoints[m])+"_cat", 80, 0.9*masspoints[m], 1.1*masspoints[m])

    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat0", "weight*(CMS_hgg_mass>0 && NNScore > 0.659)")    
    datatree_cat0.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat0", "weight*(CMS_hgg_mass>0 && event%20==0 && NNScore > 0.659)")
    treename_cat1.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_cat0", "weight*(CMS_hgg_mass>0 && NNScore > 0.659)")    
    datatree_cat1.Draw("CMS_hgg_mass>>+data_M"+str(masspoints[m])+"_cat0", "weight*(CMS_hgg_mass>0 && event%20==0 && NNScore > 0.659)")

    treename_cat1.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat1", "weight*(CMS_hgg_mass>0 && NNScore < 0.659)")    
    datatree_cat1.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat1", "weight*(CMS_hgg_mass>0 && event%20==0 && NNScore < 0.659)")

    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat", "weight*(CMS_hgg_mass>0)")    
    datatree_cat0.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat", "weight*(CMS_hgg_mass>0 && event%20==0)")
    treename_cat1.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_cat", "weight*(CMS_hgg_mass>0)")    
    datatree_cat1.Draw("CMS_hgg_mass>>+data_M"+str(masspoints[m])+"_cat", "weight*(CMS_hgg_mass>0 && event%20==0)")
    
    ggh_cat0.Scale(lumi_diff)
    ggh_cat1.Scale(lumi_diff)
    ggh_cat.Scale(lumi_diff)

    ev_cat0 = ggh_cat0.Integral()
    ev_cat1 = ggh_cat1.Integral()
    ev_cat = ggh_cat.Integral()

    eff0 = round(ev_cat0/(xs[m] * br[m] * kf[m] * target_lumi * gen[m]) , 4)
    eff1 = round(ev_cat1/(xs[m] * br[m] * kf[m] * target_lumi * gen[m]) , 4)
    eff = round(ev_cat/(xs[m] * br[m] * kf[m] * target_lumi * gen[m]) , 4)

    v_eff0.append(eff0*100)
    v_eff1.append(eff1*100)
    v_eff.append(eff*100)

    c0 = TCanvas("c0","c0",800,800)
    c0.cd()

    data_cat0.SetLineColor(1)
    data_cat0.Draw("ehist")
    data_cat0.SetXTitle("CMS Hgg Mass")
    data_cat0.SaveAs("histogramtest_data_"+str(masspoints[m])+"_cat0.root")

    ggh_cat0.SetLineColor(2)
    if ggh_cat0.Integral() != 0:
        ggh_cat0.Scale(2720.0*1.0*1.0*eff0/ggh_cat0.Integral())
    ggh_cat0.Draw("ehistsame")
    ggh_cat0.SetXTitle("CMS Hgg Mass")
    ggh_cat0.SaveAs("histogramtest_sig_"+str(masspoints[m])+"_cat0.root")

    leg = TLegend(0.7,0.8,0.88,0.88)
    leg.AddEntry(data_cat0,"Untagged Data Files")
    leg.AddEntry(ggh_cat0,"Untagged"+str(masspoints[m])+" GeV Sample")
    leg.Draw("same")

    c0.SaveAs("mass_file_"+str(masspoints[m])+"_cat0.png")
    c0.SaveAs("mass_file_"+str(masspoints[m])+"_cat0.pdf")

    c1 = TCanvas("c1","c1",800,800)
    c1.cd()

    data_cat1.SetLineColor(1)
    data_cat1.Draw("ehist")
    data_cat1.SetXTitle("CMS Hgg Mass")
    data_cat1.SaveAs("histogramtest_data_"+str(masspoints[m])+"_cat1.root")

    ggh_cat1.SetLineColor(2)
    if ggh_cat1.Integral() != 0:
        ggh_cat1.Scale(2720.0*1.0*1.0*eff1/ggh_cat1.Integral())
    ggh_cat1.Draw("ehistsame")
    ggh_cat1.SetXTitle("CMS Hgg Mass")
    ggh_cat1.SaveAs("histogramtest_sig_"+str(masspoints[m])+"_cat1.root")

    leg = TLegend(0.7,0.8,0.88,0.88)
    leg.AddEntry(data_cat1,"Untagged Data Files")
    leg.AddEntry(ggh_cat1,"Untagged"+str(masspoints[m])+" GeV Sample")
    leg.Draw("same")

    c1.SaveAs("mass_file_"+str(masspoints[m])+"_cat1.png")
    c1.SaveAs("mass_file_"+str(masspoints[m])+"_cat1.pdf")

    print("M"+str(masspoints[m])+" 0: ", ggh_cat0.Integral())
    print("M"+str(masspoints[m])+" 1: ", ggh_cat1.Integral())

print(v_eff0)
print(v_eff1)
print(v_eff)

