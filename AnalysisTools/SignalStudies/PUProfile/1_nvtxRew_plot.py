#####################################################                                                                      
# Very low mass diphoton analysis: nvtx reweighting #                                                                                        
# ------------------------------------------------- #                                                                              

import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList, kBlue
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

# Open the input file
input_file = TFile("f_nvtx_reweighting_v2.root", "READ")
# Retrieve the weight histogram
h_ratio = input_file.Get("h_ratio_nvtx")

c_w1 = TCanvas("c_w1","c_w1",1200,800)
c_w1.cd()
#c_w1.SetLeftMargin(0.15)                     
h_ratio.GetYaxis().SetTitle("NVtx weights")
h_ratio.GetXaxis().SetTitle("Number of primary vertices")
h_ratio.SetLineWidth(3)                                       
h_ratio.SetLineColor(kBlue)                                       
h_ratio.Draw("EP")                                       

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_w1, 0, 0)

c_w1.Update()
c_w1.SaveAs("/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/ZeeVal/reweighting_nvtx.png")
c_w1.SaveAs("/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/ZeeVal/reweighting_nvtx.pdf")
