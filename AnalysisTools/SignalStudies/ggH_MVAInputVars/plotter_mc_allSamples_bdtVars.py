#########################################################   
# Very low mass diphoton analysis: Signal MC variables  #                                                                                                     
# ----------------------------------------------------- #                                                                                                               
# python3 plotter_mc_allSamples_bdtVars.py  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/gghMC/

import CMS_lumi, CMSGraphics                                                                                                                                             
import ROOT, array, random, copy                                                                                                                 
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TTree, TList                                                                                                    
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray                                                  
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText                   
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack                                                                                    
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan, kMagenta, kTeal, kSpring
from array import array                                                                                                                                                  
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

args = argparser.parse_args()
outputdir = args.outdir

# Open the ROOT file
root_file = TFile.Open("histoFile_allMasses_v4.root") 

# Define the list of masses and variables
# ---------------------------------------
#masses = [15, 25, 35, 45, 55, 65]                                                                                                           
masses = [15, 20, 30, 40, 50, 60, 70]                                                                                                           
#masses = [70, 60, 50, 40, 30, 20, 15]                                                                                                           
#masses = [10, 20, 30, 40, 50, 60, 70]                                               
#masses = [30, 45, 50, 55, 60, 65, 70]                                                                                                           
#masses = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

# List of variables                                                                                                                       
# -----------------                                                                                                                                   
variables = ["dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt", "NNScore", "leadPt", "subleadPt"]

label_list = ["Leading photon p_{T}/m_{#gamma#gamma}", "Subleading photon p_{T}/m_{#gamma#gamma}", "Leading photon #eta", "Sublead photon #eta", "cosphi", "Lead #gamma IDMVA", "Sublead #gamma IDMVA","#sigma_{RV}/m_{#gamma#gamma}", "#sigma_{WV}/m_{#gamma#gamma}", "Vtx probability", "Leading #gamma #sigma_{E}/E", "Subleading #gamma #sigma_{E}/E", "Diphoton p_{T}", "Diphoton sum p_{T}", "NN score", "Leading photon p_{T}", "Subleading photon p_{T}"]


# Loop through masses and variables to plot histograms
# ----------------------------------------------------
colors = [kMagenta-7, kOrange - 3,  kBlue, kAzure+7, kCyan-3, kTeal - 7, kSpring - 7]
#colors = [kRed - 7, kPink - 6, kMagenta - 7, kViolet + 6, kBlue, kAzure + 7, kCyan - 3, kTeal - 7, kGreen, kSpring - 7, kYellow, kOrange - 3, kRed - 3]

idx = 0
for var in variables:
    canvas = TCanvas("c_"+var, "c_"+var, 1000, 800)
    #canvas.SetGrid()
    canvas.SetLogy()  # Set log scale for y-axis
    
    legend = TLegend(0.65, 0.45, 0.89, 0.88)
    if (var == "NNScore" or var =="vtxprob"):
        legend = TLegend(0.15, 0.45, 0.6, 0.88)
    legend.SetBorderSize(0)

    for i, mass in enumerate(masses):
        hist_name = "h_"+var+"_ggh_M"+str(mass)
        hist = root_file.Get(hist_name)
        if hist:
            hist.SetLineWidth(3)
            hist.SetLineColor(colors[i])
            if (var == "leadPt" or var == "subleadPt"):
                hist.Rebin(4)
            if (var == "dipho_lead_ptoM" or var == "dipho_sublead_ptoM"):
                hist.Rebin(20)
            if i == 0:
                if (var == "dipho_lead_ptoM" or var == "dipho_sublead_ptoM"):
                    hist.GetYaxis().SetRangeUser(0.1, 200.0*hist.GetMaximum())
                elif (var == "dipho_sumpt"):
                    hist.GetYaxis().SetRangeUser(0.1, 50.0*hist.GetMaximum())
                elif (var == "leadPt" or var == "subleadPt"):
                    hist.GetYaxis().SetRangeUser(0.1, 3.0*hist.GetMaximum())
                elif (var == "dipho_leadIDMVA" or var == "dipho_subleadIDMVA"):
                    hist.GetYaxis().SetRangeUser(0.1, 500*hist.GetMaximum())
                elif (var == "cosphi"):
                    hist.GetYaxis().SetRangeUser(0.1, 1500*hist.GetMaximum())
                #elif (var == "dipho_sumpt"):
                #    hist.GetYaxis().SetRangeUser(0., 3.0*hist.GetMaximum())
                #if (var == "dipho_lead_ptoM" or var == "dipho_sublead_ptoM"):
                #    hist.GetYaxis().SetRangeUser(0., 5.1*hist.GetMaximum())
                #elif (var == "dipho_sumpt" or var == "sigmaMwvoM"):
                #    hist.GetYaxis().SetRangeUser(0., 3.2*hist.GetMaximum())
                else:
                    hist.GetYaxis().SetRangeUser(0.1, 100.0*hist.GetMaximum())
                hist.GetXaxis().SetTitleOffset(1.45)
                hist.GetXaxis().SetTitle(label_list[idx])
                hist.GetYaxis().SetTitle("A.U.")
                #hist.SetMaximum(1000*hist.GetMaximum())
                hist.SetMinimum(0.01)
                hist.SetTitle("")
                hist.DrawNormalized("h")
            else:
                hist.DrawNormalized("hsame")
                #if (str(mass) == "70"):
                #    hist.GetYaxis().SetRangeUser(0., 1.3*hist.GetMaximum())
            legend.AddEntry(hist, "m="+str(mass)+" GeV", "l")

    legend.Draw()

    # CMS Title and Lumi info                                                                                                         
    # -----------------------
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText      = " Simulation Preliminary"
    CMS_lumi.lumi_sqrtS     = "2018 (13 TeV)"
    #CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
    #CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"                                                        
    CMS_lumi.cmsTextSize    = 0.6
    CMS_lumi.lumiTextSize   = 0.46
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12
    CMS_lumi.CMS_lumi(canvas, 0, 0)
    canvas.Update()

    canvas.Draw()
    canvas.SaveAs(outputdir+"/"+var+"_log.png")
    canvas.SaveAs(outputdir+"/"+var+"_log.pdf")
    idx += 1
