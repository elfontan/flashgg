# ------------------------------------------------------ #
# Use this script within an environment allowing python: #
# ------------------------------------------------------ #
from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain, TH1F, TCanvas, TLegend, TProfile
from ROOT import kBlack, kRed, kPink, kMagenta, kViolet, kBlue, kAzure, kCyan, kTeal, kGreen, kSpring, kYellow, kOrange
import random, copy
import ROOT, array, CMSGraphics, CMS_lumi
import argparse
import sys
import os

gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--o', dest='o', default='/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/paramNN/', help='Output dir')

args = argparser.parse_args()
outdir  = args.o

print("Data File Processing...")
f_histos = ROOT.TFile.Open("histoFile_nnScores_allMC_data.root")
h_nnScore_data = f_histos.Get("h_nnScore_data")

#masses = [15,25,30,35,45,50,55,60,70]
#col_list = [kBlue, kAzure + 7, kCyan + 3, kCyan - 3, kTeal - 7, kGreen - 6, kOrange - 3, kPink - 6, kMagenta - 7, kViolet + 6,kRed - 3]
masses = [10,15,20,25,30,35,40,45,50,55,60,65,70]
col_list = [kSpring - 7,kBlue, kOrange + 7, kAzure + 7, kCyan + 3, kCyan - 3, kTeal - 7, kGreen - 6, kOrange - 3, kPink - 6, kMagenta - 7, kViolet + 6,kRed - 3, kPink - 6, kMagenta - 7, kViolet + 6,kRed - 3]


canvas = TCanvas("canvas", "canvas", 1200, 1000)
canvas.SetLogy()
canvas.SetBottomMargin(0.12)
canvas.SetLeftMargin(0.15)

h_nnScore_data.GetXaxis().SetTitleOffset(1.25)
h_nnScore_data.GetXaxis().SetTitleSize(0.045)
h_nnScore_data.GetYaxis().SetTitleSize(0.045)
h_nnScore_data.GetXaxis().SetTitle("PNN Score")
h_nnScore_data.GetYaxis().SetTitle("Events (#sigma_{ggH} = 1 pb)")
h_nnScore_data.SetTitle("")
h_nnScore_data.SetMarkerColor(kBlack)
h_nnScore_data.SetMarkerStyle(20)
h_nnScore_data.SetMarkerSize(1.1)
h_nnScore_data.Scale(0.5)
h_nnScore_data.SetMinimum(10)
h_nnScore_data.SetMaximum(50.0*h_nnScore_data.GetMaximum())
h_nnScore_data.Draw("EPX")

legend = TLegend(0.4, 0.58, 0.88, 0.88)
legend.SetBorderSize(0)
legend.SetNColumns(2)
legend.AddEntry(h_nnScore_data, "SR Data", "P")


idx = 0
mass_medians = []

for mass in masses:
    histoname = "h_nnScoreW_M"+str(mass)
    h = f_histos.Get(histoname)
    print("Integral for mass ", str(mass), " = ", h.Integral())

    h.SetLineWidth(2)            
    h.SetLineColor(col_list[idx])
    h.Scale(1000)
    h.Draw("hist same")
    canvas.Update()
    legend.AddEntry(h, "M = "+str(mass)+" GeV", "l")

    # Calculate the median PNN score for this mass
    median = 0
    cumulative = 0
    total = h.Integral()
    for bin in range(1, h.GetNbinsX() + 1):
        cumulative += h.GetBinContent(bin)
        if cumulative >= total / 2.0:
            median = h.GetBinCenter(bin)
            break
    # Calculate median PNN score for this mass and store it
    #profile = h.ProfileX()
    #median = profile.GetBinContent(profile.GetMaximumBin())

    mass_medians.append((mass, median))
    idx += 1

legend.Draw()

# CMS Title and Lumi info
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "  Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.13
CMS_lumi.CMS_lumi(canvas, 0, 11)
canvas.Update()

canvas.Draw()
#canvas.SaveAs(outdir+"/nnScore_allSig_data_paperDraft.png")
#canvas.SaveAs(outdir+"/nnScore_allSig_data_paperDraft.pdf")


############################
# PNN Profile plot VS mass #
############################
canvas2 = TCanvas("canvas2", "canvas2", 1200, 1000)
#canvas2 = TCanvas("canvas2", "canvas2", 1200, 600)
canvas2.SetBottomMargin(0.12)
canvas2.SetLeftMargin(0.12)

g_medians = ROOT.TGraph(len(mass_medians))
g_medians.SetMarkerStyle(22)
g_medians.SetMarkerColor(kAzure+7)
g_medians.SetMarkerSize(1.9)
g_medians.SetLineStyle(2)
g_medians.SetLineColor(kBlack)

for i, (mass, median) in enumerate(mass_medians):
    g_medians.SetPoint(i, mass, median)

g_medians.GetXaxis().SetTitleOffset(1.25)
g_medians.GetXaxis().SetTitleSize(0.045)
g_medians.GetYaxis().SetTitleSize(0.045)
g_medians.GetYaxis().SetRangeUser(0.6,0.9)
g_medians.GetXaxis().SetTitle("m_{#gamma#gamma} [GeV]")
g_medians.GetYaxis().SetTitle("Median PNN Score")
g_medians.SetTitle("")
g_medians.Draw("APL")

# CMS Title and Lumi info
CMS_lumi.CMS_lumi(canvas2, 0, 11)
canvas2.Update()

canvas2.Draw()
canvas2.SaveAs(outdir+"/profilePNN_vs_mass_v2.png")
canvas2.SaveAs(outdir+"/profilePNN_vs_mass_v2.pdf")

