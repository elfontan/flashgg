####################################################                                                                                            
# Very low mass diphoton analysis: Pileup profile  #                                                                   
# ------------------------------------------------ #                                                                     
# python3 1dScan_plot.py --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Syst

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
argparser.add_argument('--infile', dest='infile', default='./higgsCombineTest.MultiDimFit.mH50.root', help='Input file')
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')

args = argparser.parse_args()
inputfile = args.infile
outputdir = args.outdir

def extract_1d_deltanll_tree(filename, parametername, treename='limit'):
    ''' Extract negative log likelihood values from combine limit tree.'''
    dnll = root2array(filename, treename, [parametername, 'deltaNLL'])
    dnll = dnll.view((np.float32, len(dnll.dtype.names)))
    # -2*DLL
    dnll[:,1] *= 2
    # return sorted array
    return dnll[np.lexsort((dnll[:,1], dnll[:,0]))]

# ----------------------
# Obtain histogram files                                    
# ----------------------                                                   
f = TFile(inputfile,"READ")

# Get trees and get the likelihood scan
# -------------------------------------
t_lim = f.Get("limit")
t_lim.Print()
#h = TH1F("h", "h",100,-10,10)
h = TGraph(100,-10,10)
t_lim.Draw("2*deltaNLL:r>>h(100, -10, 10)")

# ------ #
# Plot #
# ------ #
canvasname = "c_scan"
c1 = TCanvas(canvasname,canvasname,1000,800)
c1.cd()
c1.SetLeftMargin(0.19)

h.GetXaxis().SetTitle("r")
h.GetYaxis().SetTitle("2 * #Delta NLL")
h.SetMarkerSize(0.3)
h.SetMarkerColor(kAzure-4)
#h.GetYaxis().SetRangeUser(0,1.2*h.GetMaximum())
h.Draw()

#legend = ROOT.TLegend (0.45 ,0.7 ,0.89 ,0.87) 
#legend.SetTextFont(42)
#legend.SetTextSize(0.032)
#legend.SetHeader ("TTToHadronic MC sample @ 13TeV")
#legend.AddEntry (h, "UL 2018", "L")
#legend.SetLineWidth (0)
#legend.Draw ("same")

# CMS and lumi text
# -----------------
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "   Preliminary"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)
c1.Update()

c1.SaveAs(outputdir + "/test_scan_m50.png")
c1.SaveAs(outputdir + "/test_scan_m50.pdf")
