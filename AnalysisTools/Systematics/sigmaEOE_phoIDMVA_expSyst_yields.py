#!/usr/bin/env python3                                                                                                                                                     
##############################################################                                                                           
# Very low mass diphoton analysis: Systematic Uncertainties  #             
# ---------------------------------------------------------- #                                                              
# python3 sigmaEOE_phoIDMVA_expSyst_yields.py --cat cat0 

import CMS_lumi, CMSGraphics
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TTree, TList
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan, kMagenta
from array import array
from collections import OrderedDict
import argparse
import sys
import os
import math

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

argparser = argparse.ArgumentParser(description='Parser used for non-default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--cat', dest='cat', default='cat0', help='Category')
args = argparser.parse_args()
cat = args.cat

outputdir = "/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Syst/UpDnVariations/fixedSyst/5CAT"

systematics = ["SigmaEOverEShift", "MvaShift"]

for syst in systematics:
    uncList = []
    for mass in range(10, 75, 5):
        mass_str = str(mass)
        f_ggH_UL18 = TFile.Open("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/gghSig_Systematics_5Cat/ggh_m" + mass_str + ".root")
        #f_ggH_UL18 = TFile.Open("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/gghSig_Systematics_4Cat_withNNLOPS/ggh_m" + mass_str + ".root")
        if cat == "cat0":
            tree_UL18 = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_0") 
            if (syst == "SigmaEOverEShift"):
                tree_UL18_up = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_0_SigmaEOverEShiftUp01sigma")
                tree_UL18_dn = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_0_SigmaEOverEShiftDown01sigma")
            elif (syst == "MvaShift"):
                tree_UL18_up = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_0_MvaShiftUp01sigma")
                tree_UL18_dn = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_0_MvaShiftDown01sigma")
        elif cat == "cat1":
            tree_UL18 = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_1")
            if (syst == "SigmaEOverEShift"):
                tree_UL18_up = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_1_SigmaEOverEShiftUp01sigma")
                tree_UL18_dn = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_1_SigmaEOverEShiftDown01sigma")
            elif (syst == "MvaShift"):
                tree_UL18_up = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_1_MvaShiftUp01sigma")
                tree_UL18_dn = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_1_MvaShiftDown01sigma")
        elif cat == "cat2":
            tree_UL18 = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_2")
            if (syst == "SigmaEOverEShift"):
                tree_UL18_up = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_2_SigmaEOverEShiftUp01sigma")
                tree_UL18_dn = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_2_SigmaEOverEShiftDown01sigma")
            elif (syst == "MvaShift"):
                tree_UL18_up = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_2_MvaShiftUp01sigma")
                tree_UL18_dn = f_ggH_UL18.Get("tagsDumper/trees/ggh_" + mass_str + "_13TeV_UntaggedTag_2_MvaShiftDown01sigma")

        M = float(mass)
        minM = M - (M * 10 / 100)
        maxM = M + (M * 10 / 100)
        nbins = 50
        nsize = (maxM - minM) / nbins

        #############################
        # Plotting expected nEvents #
        #############################
        h_UL18_ref = TH1F("h_UL18_ref", "h_UL18_ref", nbins, minM, maxM)
        h_UL18_up = TH1F("h_UL18_up", "h_UL18_up", nbins, minM, maxM)
        h_UL18_dn = TH1F("h_UL18_dn", "h_UL18_dn", nbins, minM, maxM)

        for ev in tree_UL18:
            h_UL18_ref.Fill(ev.CMS_hgg_mass, ev.weight)
        for ev in tree_UL18_dn:
            h_UL18_dn.Fill(ev.CMS_hgg_mass, ev.weight )
        for ev in tree_UL18_up:
            h_UL18_up.Fill(ev.CMS_hgg_mass, ev.weight )
            #if syst == "MvaShift":
                #h_UL18_dn.Fill(ev.CMS_hgg_mass, ev.weight )
                #h_UL18_up.Fill(ev.CMS_hgg_mass, ev.weight )
            #elif syst == "SigmaEOverEShift":
                #h_UL18_dn.Fill(ev.CMS_hgg_mass, ev.weight )
                #h_UL18_up.Fill(ev.CMS_hgg_mass, ev.weight )

            h_UL18_ref.SetLineColor(kAzure - 3)
            h_UL18_dn.SetLineColor(kMagenta - 7)
            h_UL18_up.SetLineColor(kOrange - 3)
            h_UL18_ref.SetFillColorAlpha(kAzure - 3, 0.35)

        canvasname = "c_sumw_" + syst + "_M" + mass_str
        c = ROOT.TCanvas(canvasname, canvasname, 1000, 800)
        c.cd()
        c.SetLeftMargin(2.3)
        h_UL18_ref.GetXaxis().SetLabelSize(0.04)
        h_UL18_ref.GetYaxis().SetLabelSize(0.04)
        h_UL18_ref.GetXaxis().SetTitle("m_{#gamma#gamma} [GeV]")
        text_yAxis = "Events / " + str(nsize) + "  GeV"
        h_UL18_ref.GetYaxis().SetTitle(text_yAxis)
        h_UL18_ref.GetXaxis().SetTitleSize(0.035)
        h_UL18_ref.GetYaxis().SetTitleSize(0.04)
        h_UL18_ref.GetYaxis().SetRangeUser(0., 1.2 * h_UL18_ref.GetMaximum())
        h_UL18_ref.GetXaxis().SetTitleOffset(1.2)
        h_UL18_ref.GetYaxis().SetTitleOffset(1.1)
        h_UL18_ref.SetLineWidth(2)
        h_UL18_dn.SetLineWidth(2)
        h_UL18_up.SetLineWidth(2)
        h_UL18_ref.SetFillStyle(3011)

        legend = ROOT.TLegend(0.15, 0.63, 0.45, 0.88)
        legend.SetHeader("Systematics: " + syst)
        legend.AddEntry(h_UL18_ref, "Nominal", "L")
        legend.AddEntry(h_UL18_dn, "Dn variation", "L")
        legend.AddEntry(h_UL18_up, "Up variation", "L")
        legend.SetLineColor(0)
        legend.SetFillColor(0)
        h_UL18_ref.Draw("h")
        h_UL18_dn.Draw("h same")
        h_UL18_up.Draw("h same")
        legend.Draw("same")

        # Draw integral value
        integral_value_dn = h_UL18_dn.Integral()
        integral_value = h_UL18_ref.Integral()
        integral_value_up = h_UL18_up.Integral()

        latexDn = ROOT.TLatex()
        latexDn.SetTextFont(42)
        latexDn.SetTextSize(0.03)
        latexDn.SetTextColor(ROOT.kBlack)
        latexDn.SetTextAlign(22)  # Center alignment
        latexDn.DrawLatexNDC(0.75, 0.65, "Integral (Dn): %.3f" % integral_value_dn)
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.03)
        latex.SetTextColor(ROOT.kBlack)
        latex.SetTextAlign(22)  # Center alignment
        latex.DrawLatexNDC(0.75, 0.6, "Integral: %.3f" % integral_value)
        latexUp = ROOT.TLatex()
        latexUp.SetTextFont(42)
        latexUp.SetTextSize(0.03)
        latexUp.SetTextColor(ROOT.kBlack)
        latexUp.SetTextAlign(22)  # Center alignment
        latexUp.DrawLatexNDC(0.75, 0.55, "Integral (Up): %.3f" % integral_value_up)

        upVar = (abs(integral_value_up - integral_value) / integral_value * 100)
        dnVar = (abs(integral_value_dn - integral_value) / integral_value * 100)

        if upVar > dnVar:
            uncList.append(upVar)
        elif upVar < dnVar:
            uncList.append(dnVar)
        uncTextUp = ("UpVar: %.2f" % upVar + "%")
        uncTextDn = ("DnVar: %.2f" % dnVar + "%")

        latexUncDn = ROOT.TLatex()
        latexUncDn.SetTextFont(42)
        latexUncDn.SetTextSize(0.04)
        latexUncDn.SetTextColor(ROOT.kBlack)
        latexUncDn.SetTextAlign(22)  # Center alignment
        latexUncDn.DrawLatexNDC(0.75, 0.45, uncTextDn)

        latexUncUp = ROOT.TLatex()
        latexUncUp.SetTextFont(42)
        latexUncUp.SetTextSize(0.04)
        latexUncUp.SetTextColor(ROOT.kBlack)
        latexUncUp.SetTextAlign(22)  # Center alignment
        latexUncUp.DrawLatexNDC(0.75, 0.4, uncTextUp)

        # draw CMS and lumi text
        CMS_lumi.writeExtraText = True
        CMS_lumi.extraText = " Simulation Preliminary"
        CMS_lumi.lumi_sqrtS = "2018 (13 TeV)"
        CMS_lumi.cmsTextSize = 0.6
        CMS_lumi.lumiTextSize = 0.46
        CMS_lumi.extraOverCmsTextSize = 0.75
        CMS_lumi.relPosX = 0.12
        CMS_lumi.CMS_lumi(c, 0, 0)
        c.Update()

        c.SaveAs(outputdir + "/sumw_syst" + syst + "_UL18_M" + mass_str + "_" + cat + ".png")
        c.SaveAs(outputdir + "/sumw_syst" + syst + "_UL18_M" + mass_str + "_" + cat + ".pdf")

    print(syst+"_"+cat+" = np.array(")
    print(uncList)
