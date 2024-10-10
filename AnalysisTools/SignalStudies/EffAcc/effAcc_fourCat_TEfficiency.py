#!/usr/bin/env python3

# ********************************
# usage: 
#  python3 effAcc_TEfficiency.py --outdir /eos/user/e/elfontan/www/LowMassDiPhoton/diphotonBDT/ParametricBDT/TensorFlow/SignalModeling/newNtuples_newTraining_NN0p66
#  (e.g. from CMSSW_12_4_0/src)
# ********************************

import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem
#from ROOT import *
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooDataHist, RooCBShape, RooNumConvPdf, RooFFTConvPdf
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TEfficiency, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan
from array import array
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#import mplhep as hep
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')

args = argparser.parse_args()
outputdir = args.outdir

# Histograms: numerator, denominator, efficiency plot for each category
# ---------------------------------------------------------------------
h_num_cat0 = TH1F("h_num_cat0", "h_num_cat0", 13, 7.5, 72.5)
h_num_cat1 = TH1F("h_num_cat1", "h_num_cat1", 13, 7.5, 72.5)
h_num_cat2 = TH1F("h_num_cat2", "h_num_cat2", 13, 7.5, 72.5)
h_num_cat3 = TH1F("h_num_cat3", "h_num_cat3", 13, 7.5, 72.5)
h_num_all = TH1F("h_num_all", "h_num_all", 13, 7.5, 72.5)
h_den = TH1F("h_den", "h_den", 13, 7.5, 72.5)

masses = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

for i in range(len(masses)):
    print("-----------------")
    print("MASS ", masses[i])
    filename = "masspoint_"+str(masses[i])+"_histograms.root"
    #filename = "masspoint_"+str(masses[i])+"_histograms_targetLumi54p4InvFb.root"
    inFile = TFile.Open(filename, "READ")
    if not inFile or inFile.IsZombie():
        print(f"Error: Unable to open input file '{filename}'.")
        continue

    h_selEvents_cat0 = inFile.Get("ggh_M"+str(masses[i])+"_cat0")
    h_selEvents_cat1 = inFile.Get("ggh_M"+str(masses[i])+"_cat1")
    h_selEvents_cat2 = inFile.Get("ggh_M"+str(masses[i])+"_cat2")
    h_selEvents_cat3 = inFile.Get("ggh_M"+str(masses[i])+"_cat3")
    h_denAll = inFile.Get("ggh_M"+str(masses[i])+"_den")

    #h_totEvents = inFile.Get("ggh_M"+str(masses[i])+"_den")
    #h_totW_0 = inFile.Get("ggh_M"+str(masses[i])+"_sumw0")
    #h_totW_1 = inFile.Get("ggh_M"+str(masses[i])+"_sumw1")
    #h_totW_2 = inFile.Get("ggh_M"+str(masses[i])+"_sumw2")
    #h_totW_3 = inFile.Get("ggh_M"+str(masses[i])+"_sumw3")
    #sumw = h_totEvents.Integral()
    #print("h_totW_0 Integral =", h_totW_0.Integral())
    #print("h_totW_1 Integral =", h_totW_1.Integral())
    #print("h_totW_2 Integral =", h_totW_2.Integral())
    #print("h_totW_3 Integral =", h_totW_3.Integral())
    
    massBin = (i+1)
    print("BIN ", massBin)
    h_num_cat0.SetBinContent(massBin, h_selEvents_cat0.Integral())
    h_num_cat1.SetBinContent(massBin, h_selEvents_cat1.Integral())
    h_num_cat2.SetBinContent(massBin, h_selEvents_cat2.Integral())
    h_num_cat3.SetBinContent(massBin, h_selEvents_cat3.Integral())
    h_num_all.SetBinContent(massBin, h_selEvents_cat0.Integral() + h_selEvents_cat1.Integral() + h_selEvents_cat2.Integral() + h_selEvents_cat3.Integral())
    totEvents=h_selEvents_cat0.Integral() + h_selEvents_cat1.Integral() + h_selEvents_cat2.Integral() + h_selEvents_cat3.Integral()

    h_den.SetBinContent(massBin,h_denAll.Integral())
    print("h_denAll.Integral()", h_denAll.Integral())

    print("h_selEvents_cat0 Integral =", h_selEvents_cat0.Integral())
    print("h_selEvents_cat1 Integral =", h_selEvents_cat1.Integral())
    print("h_selEvents_cat2 Integral =", h_selEvents_cat2.Integral())
    print("h_selEvents_cat3 Integral =", h_selEvents_cat3.Integral())

    inFile.Close()

output_file = TFile("effNumDen.root", "RECREATE")
h_num_cat0.Write()
h_num_cat1.Write()
h_num_cat2.Write()
h_num_cat3.Write()
h_num_all.Write()
h_den.Write()
output_file.Close()
    
# Fill TEfficiency objects
print("Filling TEfficiency Objects...")
print("------------------------------")
eff_cat0 = TEfficiency(h_num_cat0, h_den)
eff_cat1 = TEfficiency(h_num_cat1, h_den)
eff_cat2 = TEfficiency(h_num_cat2, h_den)
eff_cat3 = TEfficiency(h_num_cat3, h_den)
eff_all = TEfficiency(h_num_all, h_den)

# TEfficiency: error options
    #kCP: Clopper-Pearson (default)
    #kFNormal: Normal approximation
    #kFWilson: Wilson score interval
    #kFAC: Agresti-Coull
    #kFFC: Feldman-Cousins
    #kBBayesian: Bayesian 
#eff_cat0.SetStatisticOption(TEfficiency.kBBayesian)
#eff_cat1.SetStatisticOption(TEfficiency.kBBayesian)
#eff_cat2.SetStatisticOption(TEfficiency.kBBayesian)
#eff_cat3.SetStatisticOption(TEfficiency.kBBayesian)
#eff_all.SetStatisticOption(TEfficiency.kBBayesian) 
eff_cat0.SetStatisticOption(TEfficiency.kFNormal)
eff_cat1.SetStatisticOption(TEfficiency.kFNormal)
eff_cat2.SetStatisticOption(TEfficiency.kFNormal)
eff_cat3.SetStatisticOption(TEfficiency.kFNormal)
eff_all.SetStatisticOption(TEfficiency.kFNormal) 
eff_cat0.SetUseWeightedEvents()
eff_cat1.SetUseWeightedEvents()
eff_cat2.SetUseWeightedEvents()
eff_cat3.SetUseWeightedEvents()
eff_all.SetUseWeightedEvents()

# Function to convert TEfficiency to TGraphAsymmErrors
def efficiency_to_graph(efficiency):
    n_points = efficiency.GetTotalHistogram().GetNbinsX()
    graph = ROOT.TGraphAsymmErrors(n_points)
    for i in range(n_points):
        x = efficiency.GetTotalHistogram().GetBinCenter(i + 1)
        y = efficiency.GetEfficiency(i + 1)
        ey_low = efficiency.GetEfficiencyErrorLow(i + 1)
        ey_high = efficiency.GetEfficiencyErrorUp(i + 1)
        ex_low = efficiency.GetTotalHistogram().GetBinWidth(i + 1) / 2.0
        ex_high = efficiency.GetTotalHistogram().GetBinWidth(i + 1) / 2.0
        print("---------------", i)
        print("y = ", y*100)
        print("yLow = ", ey_low*100)
        print("yHigh = ", ey_high*100)
        graph.SetPoint(i, x, y*100)
        graph.SetPointError(i, ex_low, ex_high, ey_low*100, ey_high*100)
    return graph

# Convert TEfficiency objects to TGraph
#graph_0 = ROOT.TGraphAsymmErrors(eff_cat0)
#graph_1 = ROOT.TGraphAsymmErrors(eff_cat1)
#graph_2 = ROOT.TGraphAsymmErrors(eff_all)
graph_cat0 = efficiency_to_graph(eff_cat0)
graph_cat1 = efficiency_to_graph(eff_cat1)
graph_cat2 = efficiency_to_graph(eff_cat2)
graph_cat3 = efficiency_to_graph(eff_cat3)
graph_all = efficiency_to_graph(eff_all)
#graph_0 = eff_cat0.CreateGraph()
#graph_1 = eff_cat1.CreateGraph()
#graph_all = eff_all.CreateGraph()

# ------------ #
#   PLOTTING   #
# ------------ #
c_graph_all = TCanvas("c_graph_all", "c_graph_all", 1000, 800)
c_graph_all.cd()
c_graph_all.SetLeftMargin(0.14)
c_graph_all.SetGrid()

# Plot TGraph for efficiency vs mass
graph_all.SetTitle("")
graph_all.GetXaxis().SetTitle("Mass [GeV]")
graph_all.GetYaxis().SetTitle("Efficiency x Acceptance [%]")
graph_all.SetMarkerStyle(20)
graph_all.SetMarkerColor(kCyan+1)
graph_all.SetLineColor(kCyan+1)
graph_all.Draw("AP")
    
# CMS lumi info
CMS_lumi.writeExtraText = True
CMS_lumi.extraText = "  Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV"
CMS_lumi.cmsTextSize = 0.6
CMS_lumi.lumiTextSize = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_graph_all, 0, 0)

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextFont(52)
latex.SetTextSize(0.04)
latex.DrawLatex(0.2, 0.75, "H #rightarrow #gamma#gamma (Inclusive)")

c_graph_all.Update()
c_graph_all.SaveAs(outputdir + "/effAcc_all_TEfficiency_Normal.png")
c_graph_all.SaveAs(outputdir + "/effAcc_all_TEfficiency_Normal.pdf")

# Plot TGraph for category 0
c_graph_cat0 = TCanvas("c_graph_cat0", "c_graph_cat0", 1000, 800)
c_graph_cat0.cd()
c_graph_cat0.SetGrid()
c_graph_cat0.SetLeftMargin(0.14)

graph_cat0.SetTitle("")
graph_cat0.GetXaxis().SetTitle("Mass [GeV]")
graph_cat0.GetYaxis().SetTitle("Efficiency x Acceptance [%]")
graph_cat0.SetMarkerStyle(20)
graph_cat0.SetMarkerColor(kAzure+1)
graph_cat0.SetLineColor(kAzure+1)
graph_cat0.Draw("AP")
CMS_lumi.CMS_lumi(c_graph_cat0, 0, 0)
latex.SetTextFont(52)
latex.SetTextSize(0.04)
latex.DrawLatex(0.2, 0.75, "H #rightarrow #gamma#gamma (Category 0)")

c_graph_cat0.Update()
c_graph_cat0.SaveAs(outputdir + "/effAcc_cat0_TEfficiency_Normal.png")
c_graph_cat0.SaveAs(outputdir + "/effAcc_cat0_TEfficiency_Normal.pdf")

# Plot TGraph for category 1
c_graph_cat1 = TCanvas("c_graph_cat1", "c_graph_cat1", 1000, 800)
c_graph_cat1.cd()
c_graph_cat1.SetLeftMargin(0.14)
c_graph_cat1.SetGrid()

graph_cat1.GetXaxis().SetTitle("Mass [GeV]")
graph_cat1.GetYaxis().SetTitle("Efficiency x Acceptance [%]")
graph_cat1.SetMarkerStyle(20)
graph_cat1.SetMarkerStyle(20)
graph_cat1.SetMarkerColor(kOrange-3)
graph_cat1.SetLineColor(kOrange-3)
graph_cat1.Draw("AP")
CMS_lumi.CMS_lumi(c_graph_cat1, 0, 0)
latex.SetTextFont(52)
latex.SetTextSize(0.04)
latex.DrawLatex(0.2, 0.75, "H #rightarrow #gamma#gamma (Category 1)")

c_graph_cat1.Update()
c_graph_cat1.SaveAs(outputdir + "/effAcc_cat1_TEfficiency_Normal.png")
c_graph_cat1.SaveAs(outputdir + "/effAcc_cat1_TEfficiency_Normal.pdf")

# Plot TGraph for category 2
c_graph_cat2 = TCanvas("c_graph_cat2", "c_graph_cat2", 1000, 800)
c_graph_cat2.cd()
c_graph_cat2.SetGrid()
c_graph_cat2.SetLeftMargin(0.14)

graph_cat2.SetTitle("")
graph_cat2.GetXaxis().SetTitle("Mass [GeV]")
graph_cat2.GetYaxis().SetTitle("Efficiency x Acceptance [%]")
graph_cat2.SetMarkerStyle(20)
graph_cat2.SetMarkerColor(kRed+1)
graph_cat2.SetLineColor(kRed+1)
graph_cat2.Draw("AP")
CMS_lumi.CMS_lumi(c_graph_cat2, 0, 0)
latex.SetTextFont(52)
latex.SetTextSize(0.04)
latex.DrawLatex(0.2, 0.75, "H #rightarrow #gamma#gamma (Category 2)")

c_graph_cat2.Update()
c_graph_cat2.SaveAs(outputdir + "/effAcc_cat2_TEfficiency_Normal.png")
c_graph_cat2.SaveAs(outputdir + "/effAcc_cat2_TEfficiency_Normal.pdf")

# Plot TGraph for category 3
c_graph_cat3 = TCanvas("c_graph_cat3", "c_graph_cat3", 1000, 800)
c_graph_cat3.cd()
c_graph_cat3.SetGrid()
c_graph_cat3.SetLeftMargin(0.14)

graph_cat3.SetTitle("")
graph_cat3.GetXaxis().SetTitle("Mass [GeV]")
graph_cat3.GetYaxis().SetTitle("Efficiency x Acceptance [%]")
graph_cat3.SetMarkerStyle(20)
graph_cat3.SetMarkerColor(kAzure+1)
graph_cat3.SetLineColor(kAzure+1)
graph_cat3.Draw("AP")
CMS_lumi.CMS_lumi(c_graph_cat3, 0, 0)
latex.SetTextFont(52)
latex.SetTextSize(0.04)
latex.DrawLatex(0.2, 0.75, "H #rightarrow #gamma#gamma (Category 3)")

c_graph_cat3.Update()
c_graph_cat3.SaveAs(outputdir + "/effAcc_cat3_TEfficiency_Normal.png")
c_graph_cat3.SaveAs(outputdir + "/effAcc_cat3_TEfficiency_Normal.pdf")


# Save efficiency histograms and different components to the output ROOT file
# ---------------------------------------------------------------------------
outFile = TFile("myGraph_TEfficiency_Normal.root", "RECREATE")
graph_cat0.Write("graph_cat0")
graph_cat1.Write("graph_cat1")
graph_cat2.Write("graph_cat2")
graph_cat3.Write("graph_cat3")
graph_all.Write("graph_all")
eff_cat0.Write("g_eff_cat0")
eff_cat1.Write("g_eff_cat1")
eff_cat2.Write("g_eff_cat2")
eff_cat3.Write("g_eff_cat3")
eff_all.Write("g_eff_cat2")
h_num_cat0.Write()
h_num_cat1.Write()
h_num_cat2.Write()
h_num_cat3.Write()
h_num_all.Write()
h_den.Write()
outFile.Close()
