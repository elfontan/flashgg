#from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
from collections import OrderedDict
import argparse
import sys
import os
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray                                            
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText                 
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack                                                                                                   
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan, kMagenta, kTeal, kSpring, kViolet

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')

args = argparser.parse_args()
outputdir = args.outdir

# Open the ROOT file
root_file = TFile.Open("histoFile_doublePeakChecks.root") 

# Define the list of masses and variables
# ---------------------------------------
masses = [30, 50, 70]                                                                                                           

# List of variables                                                                                                                       
# -----------------                                                                                                                                   
variables = ["dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt"]

label_list = ["Leading photon p_{T}/m_{#gamma#gamma}", "Subleading photon p_{T}/m_{#gamma#gamma}", "Leading photon #eta", "Sublead photon #eta", "cosphi", "Lead #gamma IDMVA", "Sublead #gamma IDMVA","#sigma_{RV}/m_{#gamma#gamma}", "#sigma_{WV}/m_{#gamma#gamma}", "Vtx probability", "Leading #gamma #sigma_{E}/E", "Subleading #gamma #sigma_{E}/E", "Diphoton p_{T}", "Diphoton sum p_{T}"]


# Loop through masses and variables to plot histograms
# ----------------------------------------------------
colors = [kRed-7, kPink-6, kMagenta-7, kViolet+6, kBlue, kAzure+7, kCyan-3 ]
#colors = [kRed - 7, kPink - 6, kMagenta - 7, kViolet + 6, kBlue, kAzure + 7, kCyan - 3, kTeal - 7, kGreen, kSpring - 7, kYellow, kOrange - 3, kRed - 3]

idx = 0
for var in variables:
    for mass in masses:
        canvas = TCanvas("c_m"+str(mass)+"_"+var, "c_m"+str(mass)+"_"+var, 1200, 800)
        canvas.SetLogy()
        histHigh_name = "h_high_"+var+"_ggh_M"+str(mass)
        histHigh = root_file.Get(histHigh_name)
        histLow_name = "h_low_"+var+"_ggh_M"+str(mass)
        histLow = root_file.Get(histLow_name)
        
        histHigh.SetLineWidth(2)
        histHigh.SetLineColor(kAzure+7)
        histHigh.SetFillStyle(3005)
        histHigh.SetFillColor(kAzure+7)
        histLow.SetLineWidth(3)            
        histLow.SetLineColor(kMagenta-7)
        histHigh.GetXaxis().SetTitleOffset(1.45)
        histHigh.GetXaxis().SetTitle(label_list[idx])
        histHigh.GetYaxis().SetTitle("A.U.")
        histHigh.SetTitle("")
        histHigh.Scale(histLow.Integral()/histHigh.Integral())
        if (var == "cosphi"):
            histHigh.GetYaxis().SetRangeUser(0.1, 8.0*histLow.GetMaximum())
        elif (var == "vtxProb" or var == "leadEta" or var == "subleadEta"):
            histHigh.GetYaxis().SetRangeUser(0.1, 50.*histLow.GetMaximum())
        else:
            histHigh.GetYaxis().SetRangeUser(0.1, 5.0*histLow.GetMaximum())
        histHigh.Draw("h")
        histLow.Draw("hsame")
        
        legend = TLegend(0.45, 0.7, 0.85, 0.88)
        #legend = TLegend(0.15, 0.63, 0.6, 0.88)
        legend.SetBorderSize(0)
        legend.AddEntry(histHigh, "High NN Score: [0.8, 1.0]", "l")
        legend.AddEntry(histLow, "Low NN Score: [0.5, 0.8]", "l")
        legend.Draw()
        
        # CMS Title and Lumi info                                                                                                         
        # -----------------------
        CMS_lumi.writeExtraText = True
        CMS_lumi.extraText      = " Simulation Preliminary"
        CMS_lumi.lumi_sqrtS     = str(mass)+" GeV (13 TeV)"
        #CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
        #CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"                                                        
        CMS_lumi.cmsTextSize    = 0.6
        CMS_lumi.lumiTextSize   = 0.46
        CMS_lumi.extraOverCmsTextSize = 0.75
        CMS_lumi.relPosX = 0.12
        CMS_lumi.CMS_lumi(canvas, 0, 0)
        canvas.Update()
        
        canvas.Draw()
        canvas.SaveAs(outputdir+"/"+var+"_m"+str(mass)+".png")
        canvas.SaveAs(outputdir+"/"+var+"_m"+str(mass)+".pdf")
    idx += 1
