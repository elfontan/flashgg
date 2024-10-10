####################################################                                                                                            
# Very low mass diphoton analysis: Pileup profile  #                                                                   
# ------------------------------------------------ #                                                                     
# python3 plot_PUprofile_gghComparison.py --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Objects/

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
argparser.add_argument('--m', dest='mass', default='35', help='Mass Hypothesis')
#argparser.add_argument('--log', dest='log', default='False', help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
logScale=False

# ----------------------
# Obtain histogram files                                    
# ----------------------                                                   
f_UL18 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_ggH_M70_newSamplesFlat.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
t_UL18 = f_UL18.Get("tagsDumper/trees/ggh_70_13TeV_UntaggedTag_0")

# Create histograms
# -----------------
h_wPuRew = TH1F("h_wPuRew", "h_wPuRew", 50, 0., 100)
h_noPuRew = TH1F("h_noPuRew", "h_noPuRew", 50, 0., 100)

t_UL18.Draw("nvtx>>h_wPuRew", "weight*nvtx * (CMS_hgg_mass>0)")                                        
t_UL18.Draw("nvtx>>h_noPuRew", "weight/puweight * nvtx * (CMS_hgg_mass>0)")                                        


# ------ #
# Plot #
# ------ #
canvasname = "c_pu"
c1 = TCanvas(canvasname,canvasname,1200,1000)
c1.cd()
c1.SetLeftMargin(0.15)

h_wPuRew.GetXaxis().SetTitle("Number of primary vertices")
h_wPuRew.GetYaxis().SetTitle("Events")
h_wPuRew.SetLineWidth(2)
h_wPuRew.SetLineColor(kAzure-4)
h_wPuRew.SetFillColorAlpha(kAzure-9,0.35)
h_wPuRew.SetFillStyle(3011)
h_wPuRew.GetYaxis().SetRangeUser(0,1.2*h_wPuRew.GetMaximum())
h_noPuRew.SetLineWidth(3)
h_noPuRew.SetLineColor(kPink-8)
h_wPuRew.Draw("eh")
h_noPuRew.Draw("eh same")

legend = ROOT.TLegend (0.45 ,0.7 ,0.89 ,0.87) 
legend.SetTextFont(42)
legend.SetTextSize(0.032)
legend.SetHeader ("ggH(70) MC sample @ 13TeV (UL18)")
legend.AddEntry (h_wPuRew, "with PU reweighting", "L")
legend.AddEntry (h_noPuRew, "w/o PU reweighting", "L")
legend.SetLineWidth (0)

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

c1.SaveAs(outputdir + "/puProfile_UL18_gghComparison_M70.png")
c1.SaveAs(outputdir + "/puProfile_UL18_gghComparison_M70.pdf")
