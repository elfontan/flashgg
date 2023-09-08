#!/usr/bin/env python3

# ********************************
# usage: 
#    python checkWeights.py
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
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M5_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M10_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M15_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M20_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M25_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M30_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M35_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M40_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M45_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M50_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M55_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M60_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M65_20220701.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/Jun2022_massPoints/Summer20UL18_ggH_M70_20220701.root"
]

# Data Sample
datafile = TFile("/eos/user/a/atsatsos/UL18_Data_Lowmassxml_v1/output_EGamma_alesauva-UL2018_0-10_6_4-v0-Run2018-12Nov2019_UL2018-981b04a73c9458401b9ffd78fdd24189_USER.root","READ")

# NOTE: Weight computation
#       1) Event weight after lumi weight = xsec_ggh_M70 * br_hgg_M70 * kf_M70 / nEvents_M70
#       2) * w0 = Event weight after weight 0  
target_lumi = 1000.0 #pb

masspoints = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
xs = [1.0, 1900.0, 1203.0, 845.8, 632.2, 492.3, 394.9, 324.0, 270.6, 229.4, 196.8, 170.6, 149.2, 131.5]
br = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0006871]
#xs = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] #assume to be 1 for limit estimates
#br = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] #assume to be 1 for limit estimates

kf = [1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06]
nEvents = [100226.0, 98926.0, 98377.0, 101077.0, 101758.0, 102829.0, 63522.0, 100223.0, 23156.0, 100752.0, 100581.0, 99832.0, 232630.0, 190139.0]
w0 = [3683.64, 2866.86, 2247.3, 1832.06, 1548.75, 1345.64, 1153.35, 1003.56, 881.80, 775.896, 683.22, 614.566, 560.66, 505.814]

v_eff = []
v_sigFract_cat0 = []
v_sigFract_cat1 = []
v_sigFract_cat2 = []
v_sigFract = []
v_sigEffFract_cat0 = []
v_sigEffFract_cat1 = []
v_sigEffFract_cat2 = []
v_sigEffFract = []

for m in range(len(filelist)):
    f_ggH = TFile.Open(filelist[m]) 
    #filename = "f_ggH_M"+str(masspoints[m])
    treename_cat0 = "t_ggH_M" + str(masspoints[m]) + "cat0"
    treename_cat1 = "t_ggH_M" + str(masspoints[m]) + "cat1"
    treename_cat2 = "t_ggH_M" + str(masspoints[m]) + "cat2"
    treename_cat3 = "t_ggH_M" + str(masspoints[m]) + "cat3"

    print("Reading file", filelist[m],"...")
    
    treename_cat0 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_0")
    treename_cat1 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_1")
    treename_cat2 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_2")
    treename_cat3 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_3")
    
    datatree_cat0 = datafile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
    datatree_cat1 = datafile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
    datatree_cat2 = datafile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
    datatree_cat3 = datafile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

    ggh_cat0 = TH1F("ggh_M"+str(masspoints[m])+"_cat0", "ggh_M"+str(masspoints[m])+"_cat0", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])
    ggh_cat1 = TH1F("ggh_M"+str(masspoints[m])+"_cat1", "ggh_M"+str(masspoints[m])+"_cat1", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])
    ggh_cat2 = TH1F("ggh_M"+str(masspoints[m])+"_cat2", "ggh_M"+str(masspoints[m])+"_cat2", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])
    ggh_cat3 = TH1F("ggh_M"+str(masspoints[m])+"_cat3", "ggh_M"+str(masspoints[m])+"_cat3", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])

    data_cat0 = TH1F("data_M"+str(masspoints[m])+"_cat0", "data_M"+str(masspoints[m])+"_cat0", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])
    data_cat1 = TH1F("data_M"+str(masspoints[m])+"_cat1", "data_M"+str(masspoints[m])+"_cat1", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])
    data_cat2 = TH1F("data_M"+str(masspoints[m])+"_cat2", "data_M"+str(masspoints[m])+"_cat2", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])
    data_cat3 = TH1F("data_M"+str(masspoints[m])+"_cat3", "data_M"+str(masspoints[m])+"_cat3", masspoints[m], 0.9*masspoints[m], 1.1*masspoints[m])

    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat0", "abs(weight)*(CMS_hgg_mass>0)")
    treename_cat1.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat1", "abs(weight)*(CMS_hgg_mass>0)")
    treename_cat2.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat2", "abs(weight)*(CMS_hgg_mass>0)")
    treename_cat3.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat3", "abs(weight)*(CMS_hgg_mass>0)")
    
    datatree_cat0.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat0", "abs(weight)*(CMS_hgg_mass>0) && event%20==0")
    datatree_cat1.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat1", "abs(weight)*(CMS_hgg_mass>0) && event%20==0")
    datatree_cat2.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat2", "abs(weight)*(CMS_hgg_mass>0) && event%20==0")
    datatree_cat3.Draw("CMS_hgg_mass>>data_M"+str(masspoints[m])+"_cat3", "abs(weight)*(CMS_hgg_mass>0) && event%20==0")
    
    ev_cat0 = ggh_cat0.Integral()
    ev_cat1 = ggh_cat1.Integral()
    ev_cat2 = ggh_cat2.Integral()
    ev_cat3 = ggh_cat3.Integral()
    ev_sumCat012 = ev_cat0 + ev_cat1 + ev_cat2

    v_sigFract_cat0.append(ev_cat0/ev_sumCat012*100)
    v_sigFract_cat1.append(ev_cat1/ev_sumCat012*100)
    v_sigFract_cat2.append(ev_cat2/ev_sumCat012*100)

    eff = round((ev_sumCat012)/(xs[m] * br[m] * kf[m] * target_lumi * w0[m]) , 4)
    eff0 = round((ev_cat0)/(xs[m] * br[m] * kf[m] * target_lumi * w0[m]) , 4)
    eff1 = round((ev_cat1)/(xs[m] * br[m] * kf[m] * target_lumi * w0[m]) , 4)
    eff2 = round((ev_cat2)/(xs[m] * br[m] * kf[m] * target_lumi * w0[m]) , 4)
    v_eff.append(eff*100)

    v_sigEffFract_cat0.append(round(ev_cat0/ev_sumCat012*eff,4))
    v_sigEffFract_cat1.append(round(ev_cat1/ev_sumCat012*eff,4))
    v_sigEffFract_cat2.append(round(ev_cat2/ev_sumCat012*eff,4))

    c0 = TCanvas("c0","c0",800,800)
    c0.cd()

    data_cat0.SetLineColor(1)
    data_cat0.Scale(20.0)
    data_cat0.Draw("ehist")
    data_cat0.SetXTitle("CMS Hgg Mass")
    data_cat0.SaveAs("histogramtest_data_"+str(masspoints[m])+"_cat0.root")

    ggh_cat0.SetLineColor(2)
    if ggh_cat0.Integral() != 0:
        ggh_cat0.Scale(59970.0*1.0*1.0*eff0/ggh_cat0.Integral())
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
    data_cat1.Scale(20.0)
    data_cat1.Draw("ehist")
    data_cat1.SetXTitle("CMS Hgg Mass")
    data_cat1.SaveAs("histogramtest_data_"+str(masspoints[m])+"_cat1.root")

    ggh_cat1.SetLineColor(2)
    if ggh_cat1.Integral() != 0:
        ggh_cat1.Scale(59970.0*1.0*1.0*eff1/ggh_cat1.Integral())
    ggh_cat1.Draw("ehistsame")
    ggh_cat1.SetXTitle("CMS Hgg Mass")
    ggh_cat1.SaveAs("histogramtest_sig_"+str(masspoints[m])+"_cat1.root")

    leg = TLegend(0.7,0.8,0.88,0.88)
    leg.AddEntry(data_cat1,"Untagged Data Files")
    leg.AddEntry(ggh_cat1,"Untagged"+str(masspoints[m])+" GeV Sample")
    leg.Draw("same")

    c1.SaveAs("mass_file_"+str(masspoints[m])+"_cat1.png")
    c1.SaveAs("mass_file_"+str(masspoints[m])+"_cat1.pdf")

    c2 = TCanvas("c2","c2",800,800)
    c2.cd()

    data_cat2.SetLineColor(1)
    data_cat2.Scale(20.0)
    data_cat2.Draw("ehist")
    data_cat2.SetXTitle("CMS Hgg Mass")
    data_cat2.SaveAs("histogramtest_data_"+str(masspoints[m])+"_cat2.root")

    ggh_cat2.SetLineColor(2)
    if ggh_cat2.Integral() != 0:
        ggh_cat2.Scale(59970.0*1.0*1.0*eff2/ggh_cat2.Integral())
    ggh_cat2.Draw("ehistsame")
    ggh_cat2.SetXTitle("CMS Hgg Mass")
    ggh_cat2.SaveAs("histogramtest_sig_"+str(masspoints[m])+"_cat2.root")

    leg = TLegend(0.7,0.8,0.88,0.88)
    leg.AddEntry(data_cat2,"Untagged Data Files")
    leg.AddEntry(ggh_cat2,"Untagged"+str(masspoints[m])+" GeV Sample")
    leg.Draw("same")

    c2.SaveAs("mass_file_"+str(masspoints[m])+"_cat2.png")
    c2.SaveAs("mass_file_"+str(masspoints[m])+"_cat2.pdf")
