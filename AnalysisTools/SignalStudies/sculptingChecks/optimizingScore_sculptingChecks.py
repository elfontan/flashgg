############################################
#     Very low mass diphoton analysis      #
############################################
#python3  optimizingScore_sculptingChecks.py --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/paramNN/nearest_flat/postPreapprTESTS/evaluateAt30GeV/ --hyp nearest_flat_evaluateAt30GeV --norm True

import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain, TLegend, TLine
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList, kCyan, kAzure, kGreen
from collections import OrderedDict
import argparse
import sys
import os
from ROOT import  gStyle

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--minV', dest='minV', default='-0.9', help='Minimum Value for maxPhoId')
argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Maximum Value for maxPhoId')
argparser.add_argument('--log', dest='log', default=False, help='Log scale in the y axis')
argparser.add_argument('--norm', dest='norm', default=False, help='Norm factor')
argparser.add_argument('--sb', dest='sb', default=False, help='Norm factor')
argparser.add_argument('--hyp', dest='hyp', default='NEAREST', help='Strategy for building the mass hypothesis')
argparser.add_argument('--c', dest='c', default='cat0', help='Category')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log
normFactor = args.norm
sbScenario = args.sb
massHyp = args.hyp
cat = args.c

# 
# /eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat_evaluateAt30GeV
# /eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat_evaluateAt60GeV

# ----------------------
# Obtain histogram files
# ----------------------
# All 2018 data
f_data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+massHyp+"/out_all2018Data_bkg_newSamplesFlat.root","READ") 
# Data from the sideband
f_sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+massHyp+"/out_sbData_bkg_newSamplesFlat.root","READ") 


# Get trees and create histograms for data
# ----------------------------------------
if (cat == "cat0"):
    t_dat0 = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
    t_sb0 = f_sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
elif (cat == "cat1"):
    t_dat0 = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
    t_sb0 = f_sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")

h_diphoMass_pre0 = TH1F("h_diphoMass_pre0", "h_diphoMass_pre0", 50, 0, 100)
h_diphoMass_pre1 = TH1F("h_diphoMass_pre1", "h_diphoMass_pre1", 50, 0, 100)
h_diphoMass_pre2 = TH1F("h_diphoMass_pre2", "h_diphoMass_pre2", 50, 0, 100)

h_diphoMass_mgg0 = TH1F("h_diphoMass_mgg0", "h_diphoMass_mgg0", 50, 0, 100)
h_diphoMass_sba0 = TH1F("h_diphoMass_sba0", "h_diphoMass_sba0", 50, 0, 100)

c_dat0 = 0
if (sbScenario):
    for ev_dat0 in t_sb0:        
        #if (ev_dat0.NNScore > 0.74 and min(ev_dat0.dipho_leadIDMVA*ev_dat0.weight_allDD, ev_dat0.dipho_subleadIDMVA*ev_dat0.weight_allDD) > -0.7):
        if (ev_dat0.NNScore > 0.9 and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA) > -0.7):
            h_diphoMass_pre0.Fill(ev_dat0.dipho_mass,ev_dat0.weight_allDD)    
        if ((ev_dat0.NNScore >= 0.8 and ev_dat0.NNScore < 0.9) and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA) > -0.7):
            h_diphoMass_pre1.Fill(ev_dat0.dipho_mass,ev_dat0.weight_allDD)    
        if ((ev_dat0.NNScore >= 0.6 and ev_dat0.NNScore < 0.8) and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA) > -0.7):
            h_diphoMass_pre2.Fill(ev_dat0.dipho_mass,ev_dat0.weight_allDD)    

else:
    for ev_dat0 in t_dat0:
        #if (c_dat0 == 1000): break                                               
        #print ("######################## Event ", c_dat0)
        c_dat0 += 1
        if (not(sbScenario) and not(c_dat0%10==0)): continue
        #print ("ev_dat0.NNScore", ev_dat0.NNScore)
        if (sbScenario and (min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA) > -0.7)): 
            continue
        #print("Minimum is = ", min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA))
        if (not(sbScenario) and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA) < -0.7):
            continue
        if (ev_dat0.NNScore > 0.9):
            h_diphoMass_pre0.Fill(ev_dat0.dipho_mass)    
        if (ev_dat0.NNScore >= 0.8 and ev_dat0.NNScore < 0.9):
            h_diphoMass_pre1.Fill(ev_dat0.dipho_mass)    
        if (ev_dat0.NNScore >= 0.6 and ev_dat0.NNScore < 0.8):
            h_diphoMass_pre2.Fill(ev_dat0.dipho_mass)    

    
# Plotting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

canvasname = "c_sculpting"
c1 = TCanvas(canvasname,canvasname,1000,700)
c1.cd()
#c1.SetLeftMargin(0.15)

# Upper plot pad - Data histos
c1.SetBottomMargin(0.1)
c1.SetLeftMargin(1.9)

h_diphoMass_pre0.GetXaxis().SetTitle("m_{#gamma#gamma}")
if (normFactor):
    h_diphoMass_pre0.GetYaxis().SetTitle("A.U.")
    h_diphoMass_pre0.GetYaxis().SetTitleOffset(1.6)
else:
    h_diphoMass_pre0.GetYaxis().SetTitle("Events")
    h_diphoMass_pre0.GetYaxis().SetTitleOffset(1.9)
h_diphoMass_pre0.GetYaxis().SetTitleSize(25)
h_diphoMass_pre0.GetYaxis().SetTitleFont(43)
h_diphoMass_pre0.GetYaxis().SetLabelFont(43)
h_diphoMass_pre0.GetYaxis().SetLabelOffset(0.01)
h_diphoMass_pre0.GetYaxis().SetLabelSize(25)
h_diphoMass_pre0.SetLineWidth(2)
h_diphoMass_pre0.SetLineColor(kCyan-3)
h_diphoMass_pre0.GetYaxis().SetRangeUser(0,2200)

h_diphoMass_pre1.SetLineWidth(2)
h_diphoMass_pre1.SetLineColor(kAzure+1)
h_diphoMass_pre2.SetLineWidth(2)
h_diphoMass_pre2.SetLineColor(kGreen-8)


if (normFactor):
    h_diphoMass_pre1.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre1.Integral())
    h_diphoMass_pre2.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre2.Integral())
    h_diphoMass_pre0.SetMaximum(1.8*h_diphoMass_pre0.GetMaximum())
    
else:
    h_diphoMass_pre1.SetMaximum(1.5*h_diphoMass_pre0.GetMaximum())
    h_diphoMass_pre2.SetMaximum(1.5*h_diphoMass_pre0.GetMaximum())

h_diphoMass_pre0.Draw("hist")
h_diphoMass_pre1.Draw("hist same")
h_diphoMass_pre2.Draw("hist same")

leg = TLegend(0.15,0.6,0.55,0.85)
if (sbScenario):
    leg.AddEntry(h_diphoMass_pre0,"sb events: NN score > 0.9")
    leg.AddEntry(h_diphoMass_pre1,"sb events: NN score = [0.8,0.9]")
    leg.AddEntry(h_diphoMass_pre2,"sb events: NN score = [0.6,0.8]")
else:
    #leg.AddEntry(h_diphoMass_pre0,"All data (presel): NN score > 0.74")
    #leg.AddEntry(h_diphoMass_pre1,"All data (presel): NN score > 0.8")
    #leg.AddEntry(h_diphoMass_pre2,"All data (presel): NN score > 0.907")
    leg.AddEntry(h_diphoMass_pre0,"10% data (presel): NN score > 0.9")
    leg.AddEntry(h_diphoMass_pre1,"10% data (presel): NN score = [0.8,0.9]")
    leg.AddEntry(h_diphoMass_pre2,"10% data (presel): NN score = [0.6,0.8]")

leg.SetLineWidth(0)
leg.Draw("same")

line = TLine(70, 0, 70, h_diphoMass_pre0.GetMaximum())
line.SetLineStyle(2)
line.Draw("same")

#CMS Title and Lumi info
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
#CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)

c1.Update()
if (sbScenario and normFactor):
    #c1.SaveAs(outputdir+"/diphoMass_sb_nnScoreOpt_norm1_"+cat+".png")
    #c1.SaveAs(outputdir+"/diphoMass_sb_nnScoreOpt_norm1"+cat+".pdf")
    c1.SaveAs(outputdir+"/diphoMass_sb_nnScoreOpt_norm1.png")
    c1.SaveAs(outputdir+"/diphoMass_sb_nnScoreOpt_norm1.pdf")
elif (normFactor):
    #c1.SaveAs(outputdir+"/diphoMass_allDataPreselOnly_nnScoreOpt_norm1"+cat+".png")
    #c1.SaveAs(outputdir+"/diphoMass_allDataPreselOnly_nnScoreOpt_norm1"+cat+".pdf")
    c1.SaveAs(outputdir+"/diphoMass_10percentDataPreselOnly_nnScoreOpt_norm1.png")
    c1.SaveAs(outputdir+"/diphoMass_10percentDataPreselOnly_nnScoreOpt_norm1.pdf")
elif(sbScenario):
    c1.SaveAs(outputdir+"/diphoMass_sb_nnScoreOpt.png")
    c1.SaveAs(outputdir+"/diphoMass_sb_nnScoreOpt.pdf")
else:
    c1.SaveAs(outputdir+"/diphoMass_10percentDataPreselOnly_sculptingCheck.png")
    c1.SaveAs(outputdir+"/diphoMass_10percentDataPreselOnly_sculptingCheck.pdf")
