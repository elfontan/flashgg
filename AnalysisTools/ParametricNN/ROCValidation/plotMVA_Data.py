import ROOT, array
import CMS_lumi, random, copy
from ROOT import gSystem, gStyle, gROOT
from ROOT import TCanvas, TFile, TTree, TH1, TH1F, TF1, TLegend, TChain, TList
from ROOT import kViolet, kBlue, kBlack, kAzure
from collections import OrderedDict

import argparse
import sys
import os

gROOT.SetBatch()                     
ROOT.gStyle.SetOptStat(0)                                                                                                                 
ROOT.gStyle.SetOptTitle(0)                                                                                                                                 

#Background
lmf = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Feb2024_LowMassBDT_MassHypInput/EGamma_Summer20UL.root","READ")
pnrf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/randomAssignment_twoRanges/out_all2018Data_bkg.root","READ")

lmt0 = lmf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
pnrt0 = pnrf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

lmr = TH1F("lmr","lmr",2000,-1.0,1.0)
lmr.Sumw2()
pnrr = TH1F("pnrr","pnrr",2000,-1.0,1.0)
pnrr.Sumw2()

#Weighted: weight*(CMS_hgg_mass>0)
lmt0.Draw("diphoMVA>>lmr","weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
pnrt0.Draw("NNScore>>pnrr","weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")

lmr.SaveAs("output/lm_data.root")
pnrr.SaveAs("output/pnr_data.root")

lm = TH1F("lm","lm",80,-1.0,1.0)
lm.Sumw2()
pnr = TH1F("pnr","pnr",80,-1.0,1.0)
pnr.Sumw2()

#Weighted: weight*(CMS_hgg_mass>0)
lmt0.Draw("diphoMVA>>lm","weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
pnrt0.Draw("NNScore>>pnr","weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")

#Now we draw it out
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()
c1.SetBottomMargin(0.11)
c1.SetLeftMargin(0.11)

lm.SetLineColor(kViolet-2)
lm.SetLineWidth(2)
lm.Draw("histsame")

lm.SetXTitle("Diphoton MVA")
lm.GetXaxis().SetTitleSize(25)
lm.GetXaxis().SetTitleFont(43)
lm.GetXaxis().SetTitleOffset(2.0)
lm.GetXaxis().SetLabelFont(43)
lm.GetXaxis().SetLabelSize(25)
lm.GetXaxis().SetLabelOffset(0.02)

lm.GetYaxis().SetTitle("Events")
lm.GetYaxis().SetTitleSize(25)
lm.GetYaxis().SetTitleFont(43)
lm.GetYaxis().SetTitleOffset(2.25)
lm.GetYaxis().SetLabelFont(43)
lm.GetYaxis().SetLabelSize(25)

pnr.SetLineColor(kAzure-2)
pnr.SetLineWidth(2)
pnr.Draw("histsame")

pnr.SetXTitle("Diphoton MVA")
pnr.GetXaxis().SetTitleSize(25)
pnr.GetXaxis().SetTitleFont(43)
pnr.GetXaxis().SetTitleOffset(2.0)
pnr.GetXaxis().SetLabelFont(43)
pnr.GetXaxis().SetLabelSize(25)
pnr.GetXaxis().SetLabelOffset(0.02)

pnr.GetYaxis().SetTitle("Events")
pnr.GetYaxis().SetTitleSize(25)
pnr.GetYaxis().SetTitleFont(43)
pnr.GetYaxis().SetTitleOffset(2.25)
pnr.GetYaxis().SetLabelFont(43)
pnr.GetYaxis().SetLabelSize(25)

leg = TLegend(0.35,0.65,0.6,0.85)
leg.SetBorderSize(0)
leg.SetTextSize(0.018)
leg.AddEntry(lm,"Lowmass BDT")
leg.AddEntry(pnr,"Parametric NN")
leg.Draw("same")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText= "Preliminary"
CMS_lumi.lumi_sqrtS = "2018 (13 TeV)"
CMS_lumi.cmsTextSize= 0.4
CMS_lumi.lumiTextSize = 0.3
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)
c1.Update()

c1.SaveAs("output/DiphoMVA_DataBkg.png")
c1.SaveAs("output/DiphoMVA_DataBkg.pdf")

print("Lowmass Data: ",lm.Integral())
print("PNN Data: ",pnr.Integral())
