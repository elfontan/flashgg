from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
from collections import OrderedDict
import argparse
import sys
import os

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

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log
normFactor = args.norm
sbScenario = args.sb
massHyp = args.hyp

# ----------------------
# Obtain histogram files
# ----------------------
# All 2018 data
f_data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/"+massHyp+"/out_all2018Data_bkg_v1.root","READ") 
# Data from the sideband
f_sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/"+massHyp+"/out_sbData_bkg_v1.root","READ") 
# Data from the sideband
f_dipho = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/"+massHyp+"/out_reducedDipho_bkg_v1.root","READ") 


# Get trees and create histograms for data
# ----------------------------------------
t_dat0 = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
t_sb0 = f_sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
t_dipho = f_dipho.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

h_score = TH1F("h_score", "h_score", 100, 0, 1)

h_diphoMass_pre0 = TH1F("h_diphoMass_pre0", "h_diphoMass_pre0", 200, 0, 100)
h_diphoMass_pre1 = TH1F("h_diphoMass_pre1", "h_diphoMass_pre1", 200, 0, 100)
h_diphoMass_pre2 = TH1F("h_diphoMass_pre2", "h_diphoMass_pre2", 200, 0, 100)
h_diphoMass_pre3 = TH1F("h_diphoMass_pre3", "h_diphoMass_pre3", 200, 0, 100)
h_diphoMass_pre4 = TH1F("h_diphoMass_pre4", "h_diphoMass_pre4", 200, 0, 100)
h_diphoMass_pre5 = TH1F("h_diphoMass_pre5", "h_diphoMass_pre5", 200, 0, 100)
h_diphoMass_pre6 = TH1F("h_diphoMass_pre6", "h_diphoMass_pre6", 200, 0, 100)

h_diphoMass_mgg0 = TH1F("h_diphoMass_mgg0", "h_diphoMass_mgg0", 200, 0, 100)
h_diphoMass_sba0 = TH1F("h_diphoMass_sba0", "h_diphoMass_sba0", 200, 0, 100)


c_dipho = 0
for ev_dipho in t_dipho:
    #if (c_dat0 == 1000): break                                               
    #print ("######################## Event ", c_dat0)
    c_dipho += 1
    h_score.Fill(ev_dipho.NNScore, ev_dipho.weight*ev_dipho.weight_allDD)
    #if (min(ev_dipho.dipho_leadIDMVA, ev_dipho.dipho_subleadIDMVA) < -0.7):
    #    continue
    if (ev_dipho.NNScore > 0.0):
        h_diphoMass_pre0.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    
    if (ev_dipho.NNScore > 0.2):
        h_diphoMass_pre1.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    
    if (ev_dipho.NNScore > 0.4):
        h_diphoMass_pre2.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    
    if (ev_dipho.NNScore > 0.5):
        h_diphoMass_pre3.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    
    if (ev_dipho.NNScore > 0.6):
        h_diphoMass_pre4.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    
    if (ev_dipho.NNScore > 0.8):
        h_diphoMass_pre5.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    
    if (ev_dipho.NNScore > 0.9):
        h_diphoMass_pre6.Fill(ev_dipho.dipho_mass, ev_dipho.weight*ev_dipho.weight_allDD)    

    
# Plotting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c_score = TCanvas("c_score","c_score",1000,600)
c_score.cd()
c_score.SetBottomMargin(0.1)
c_score.SetLeftMargin(1.9)

h_score.GetXaxis().SetTitle("NN score")
h_score.GetYaxis().SetTitle("Events")
h_score.GetYaxis().SetTitleOffset(1.6)
h_score.GetYaxis().SetTitleSize(25)
h_score.GetYaxis().SetTitleFont(43)
h_score.GetYaxis().SetLabelFont(43)
h_score.GetYaxis().SetLabelOffset(0.01)
h_score.GetYaxis().SetLabelSize(25)
h_score.SetLineWidth(2)
h_score.SetLineColor(kCyan-3)
h_score.Draw("hist")

leg0 = TLegend(0.15,0.75,0.45,0.88)
leg0.AddEntry(h_score,"Diphoton MC")
leg0.SetLineWidth(0)
leg0.Draw("same")

#CMS Title and Lumi info
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary Simulation"
#CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
#CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.lumi_sqrtS     = "13 TeV"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_score, 0, 0)

c_score.Update()
c_score.SaveAs(outputdir+"/nnScore_MCdiphoton_trainingEvents_ddWeights.png")
c_score.SaveAs(outputdir+"/nnScore_MCdiphoton_trainingEvents_ddDefWeights.pdf")



canvasname = "c_sculpting"
c1 = TCanvas(canvasname,canvasname,1200,600)
c1.cd()
#c1.SetLeftMargin(0.15)

# Upper plot pad - Data histos
c1.SetBottomMargin(0.1)
c1.SetLeftMargin(1.9)
#c1.SetLogy()

h_diphoMass_pre0.GetXaxis().SetTitle("m_{#gamma#gamma}")
if (normFactor):
    h_diphoMass_pre0.GetYaxis().SetTitle("A.U.")
    h_diphoMass_pre0.GetYaxis().SetTitleOffset(1.9)
else:
    h_diphoMass_pre0.GetYaxis().SetTitle("Events")
    h_diphoMass_pre0.GetYaxis().SetTitleOffset(1.6)
h_diphoMass_pre0.GetYaxis().SetTitleSize(25)
h_diphoMass_pre0.GetYaxis().SetTitleFont(43)
h_diphoMass_pre0.GetYaxis().SetLabelFont(43)
h_diphoMass_pre0.GetYaxis().SetLabelOffset(0.01)
h_diphoMass_pre0.GetYaxis().SetLabelSize(25)
h_diphoMass_pre0.SetLineWidth(2)
h_diphoMass_pre0.SetLineColor(kCyan-3)

h_diphoMass_pre1.SetLineWidth(2)
h_diphoMass_pre1.SetLineColor(kAzure+1)
h_diphoMass_pre2.SetLineWidth(2)
h_diphoMass_pre2.SetLineColor(kGreen-8)
h_diphoMass_pre3.SetLineWidth(2)
h_diphoMass_pre3.SetLineColor(kBlue-7)
h_diphoMass_pre4.SetLineWidth(2)
h_diphoMass_pre4.SetLineColor(kViolet-4)
h_diphoMass_pre5.SetLineWidth(2)
h_diphoMass_pre5.SetLineColor(kMagenta-7)
h_diphoMass_pre6.SetLineWidth(2)
h_diphoMass_pre6.SetLineColor(kPink+4)

if (normFactor):
    h_diphoMass_pre1.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre1.Integral())
    h_diphoMass_pre2.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre2.Integral())
    h_diphoMass_pre3.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre3.Integral())
    h_diphoMass_pre4.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre4.Integral())
    h_diphoMass_pre5.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre5.Integral())
    h_diphoMass_pre6.Scale(h_diphoMass_pre0.Integral()/h_diphoMass_pre6.Integral())
    h_diphoMass_pre0.SetMaximum(2.0*h_diphoMass_pre0.GetMaximum())
    
else:
    h_diphoMass_pre1.SetMaximum(2.5*h_diphoMass_pre0.GetMaximum())
    h_diphoMass_pre2.SetMaximum(2.5*h_diphoMass_pre0.GetMaximum())
    h_diphoMass_pre3.SetMaximum(2.5*h_diphoMass_pre0.GetMaximum())
    h_diphoMass_pre4.SetMaximum(2.5*h_diphoMass_pre0.GetMaximum())
    h_diphoMass_pre5.SetMaximum(2.5*h_diphoMass_pre0.GetMaximum())
    h_diphoMass_pre6.SetMaximum(2.5*h_diphoMass_pre0.GetMaximum())

h_diphoMass_pre0.Draw("hist")
h_diphoMass_pre1.Draw("hist same")
h_diphoMass_pre2.Draw("hist same")
h_diphoMass_pre3.Draw("hist same")
h_diphoMass_pre4.Draw("hist same")
h_diphoMass_pre5.Draw("hist same")
h_diphoMass_pre6.Draw("hist same")

leg = TLegend(0.15,0.6,0.45,0.88)
leg.AddEntry(h_diphoMass_pre0,"Diphoton MC: NN score > 0.0")
leg.AddEntry(h_diphoMass_pre1,"Diphoton MC: NN score > 0.2")
leg.AddEntry(h_diphoMass_pre2,"Diphoton MC: NN score > 0.4")
leg.AddEntry(h_diphoMass_pre3,"Diphoton MC: NN score > 0.5")
leg.AddEntry(h_diphoMass_pre4,"Diphoton MC: NN score > 0.6")
leg.AddEntry(h_diphoMass_pre5,"Diphoton MC: NN score > 0.8")
leg.AddEntry(h_diphoMass_pre6,"Diphoton MC: NN score > 0.9")
leg.SetLineWidth(0)
leg.Draw("same")

line = TLine(70, 0, 70, h_diphoMass_pre0.GetMaximum())
line.SetLineStyle(2)
line.Draw("same")

#CMS Title and Lumi info
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary Simulation"
#CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
#CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.lumi_sqrtS     = "13 TeV"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)

c1.Update()
if (normFactor):
    c1.SaveAs(outputdir+"/diphoMass_MCdiphoton_sculptingCheck_norm1_trainingEvents_ddWeights.png")
    c1.SaveAs(outputdir+"/diphoMass_MCdiphoton_sculptingCheck_norm1_trainingEvents_ddWeights.pdf")
else:
    c1.SaveAs(outputdir+"/diphoMass_MCdiphoton_sculptingCheck_trainingEvents_ddWeights.png")
    c1.SaveAs(outputdir+"/diphoMass_MCdiphoton_sculptingCheck_trainingEvents_ddWeights.pdf")
