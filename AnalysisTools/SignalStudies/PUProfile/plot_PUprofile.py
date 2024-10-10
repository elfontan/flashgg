####################################################                                                                                            
# Very low mass diphoton analysis: Pileup profile  #                                                                   
# ------------------------------------------------ #                                                                     
# python3 plot_PUprofile.py --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Objects/

import CMS_lumi, CMSGraphics                                                                                                                        
import ROOT, array, random, copy                                                                                                                        
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TTree, TList                                                                                  
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray                                           
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText              
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack                                                                                     
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan                                  
from array import array                                                                                                 
from collections import OrderedDict                                                                                                          
import argparse                                                                                                                                                   
import sys                                                                                                                                                
import os                                                                                                                              
import math

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--norm', dest='norm', default='True', help='Normalizing to data')
#argparser.add_argument('--log', dest='log', default='False', help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
normAU = args.norm
#logScale = args.log
logScale=False

# ----------------------
# Obtain histogram files                                    
# ----------------------                                                   
f_UL18 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/ttBar_UL18.root","READ")
f_Leg18 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/ttBar_Leg18.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
t_UL18 = f_UL18.Get("Events")
t_Leg18 = f_Leg18.Get("Events")

# Create histograms
# -----------------
h_UL18 = TH1F("h_UL18", "h_UL18", 100, 0., 100)
h_Leg18 = TH1F("h_Leg18", "h_Leg18", 100, 0., 100)

t_UL18.Draw("PV_npvs>>h_UL18", "PV_npvs>0")                                        
t_Leg18.Draw("PV_npvs>>h_Leg18", "PV_npvs>0")                                        

# ------ #
# Plot #
# ------ #
canvasname = "c_pu"
c1 = TCanvas(canvasname,canvasname,1200,1000)
c1.cd()
c1.SetLeftMargin(0.19)

h_UL18.GetXaxis().SetTitle("Number of primary vertices")
h_UL18.GetYaxis().SetTitle("Events")
h_UL18.SetLineWidth(2)
h_UL18.SetLineColor(kAzure-4)
h_UL18.SetFillColorAlpha(kAzure-9,0.35)
h_UL18.SetFillStyle(3011)
h_UL18.Scale(h_Leg18.Integral() / h_UL18.Integral())
h_UL18.GetYaxis().SetRangeUser(0,1.2*h_Leg18.GetMaximum())
h_Leg18.SetLineColor(kPink-8)
h_Leg18.SetLineWidth(3)
h_UL18.Draw("eh")

legend = ROOT.TLegend (0.45 ,0.7 ,0.89 ,0.87) 
legend.SetTextFont(42)
legend.SetTextSize(0.032)
legend.SetHeader ("TTToHadronic MC sample @ 13TeV")
#legend.AddEntry (h_Leg18, "Legacy 2018", "L")
legend.AddEntry (h_UL18, "UL2018 MC Campaign", "L")
legend.SetLineWidth (0)

#h_Leg18.Draw("same he")
legend.Draw ("same")

# CMS and lumi text
# -----------------
CMS_lumi.writeExtraText = True
CMS_lumi.lumi_sqrtS     = "2018 (13 TeV)"
CMS_lumi.extraText      = "   Simulation Preliminary"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)
c1.Update()

c1.SaveAs(outputdir + "/puProfile_UL18.png")
c1.SaveAs(outputdir + "/puProfile_UL18.pdf")
