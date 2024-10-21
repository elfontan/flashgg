######################################################                                                                                            
# Very low mass diphoton analysis: ZToEE validation  #                                                                   
# -------------------------------------------------- #                                                                     
# python3 plot_nVtx_PUReweighting.py --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/ZeeVal/M80_M100_AU/

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

args = argparser.parse_args()
outputdir = args.outdir
normAU = args.norm

# Reweighting function
# --------------------
def reweighting(inputFile_weights, rootFile_weights, var):
    # Open the input file
    input_file = TFile(inputFile_weights, "READ")
    if input_file.IsZombie():
        print("Error: Unable to open the input file.")
        return

    # Retrieve the weight histogram
    weight_histogram = input_file.Get(rootFile_weights)
    if not weight_histogram or not isinstance(weight_histogram, TH1):
        print("Error: Unable to retrieve the weight histogram.")
        return

    # Get the bin number for the variable                                                                           
    bin_number = weight_histogram.GetXaxis().FindBin(var)
    if bin_number < 1 or bin_number > weight_histogram.GetNbinsX():
        input_file.Close()
        return 1.  # Default weight is 1 if the value is not found

    w = weight_histogram.GetBinContent(bin_number)

    # Close the input file
    input_file.Close()

    return w

# ----------------------
# Obtain histogram files                                    
# ----------------------                                                   
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/Jun30_data2018ABCD_zeeVal.root","READ")
dy = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/Jun30_dyJets2018_zeeVal.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
dy0 = dy.Get("tagsDumper/trees/DYToLL_13TeV_UntaggedTag_0")

# Create histograms
# -----------------
h_data_nvtx = TH1F("h_data_nvtx", "h_data_nvtx", 60, 0., 60.)
h_data_nvtx_noPUw = TH1F("h_data_nvtx_noPUw", "h_data_nvtx_noPUw", 60, 0., 60.)
h_DY_nvtx = TH1F("h_DY_nvtx", "h_DY_nvtx", 60, 0., 60.)
h_DY_nvtx_noPUw = TH1F("h_DY_nvtx_noPUw", "h_DY_nvtx_noPUw", 60, 0., 60.)
h_DY_nvtx_final = TH1F("h_DY_nvtx_final", "h_DY_nvtx_final", 60, 0., 60.)

dat0.Draw("nvtx>>+h_data_nvtx", "(CMS_hgg_mass>0)*weight")          
dat0.Draw("nvtx>>+h_data_nvtx_noPUw", "(CMS_hgg_mass>0)*weight/puweight")          
dy0.Draw("nvtx>>+h_DY_nvtx", "(CMS_hgg_mass>0)*weight")          
dy0.Draw("nvtx>>+h_DY_nvtx_noPUw", "(CMS_hgg_mass>0)*weight/puweight")          

n=0
for ev in dy0:
   #n+=1
   #if (n==1000):break
   w_nvtx = reweighting("f_nvtx_reweighting_v2.root", "h_ratio_nvtx", ev.nvtx)
   #print( w_nvtx)
   h_DY_nvtx_final.Fill(ev.nvtx, ev.weight * w_nvtx)
        
# DY MC sample: lumi scaling
# --------------------------
if (normAU):
    h_DY_nvtx.Scale(h_data_nvtx.Integral()/h_DY_nvtx.Integral())
    h_DY_nvtx_noPUw.Scale(h_data_nvtx.Integral()/h_DY_nvtx_noPUw.Integral())
    h_DY_nvtx_final.Scale(h_data_nvtx.Integral()/h_DY_nvtx_final.Integral())
else:
    h_DY_nvtx.Scale(54.4)
    h_DY_nvtx_noPUw.Scale(54.4)

# Divide the DY MC by the data distribution to compute the ratio                                                                                                            
# --------------------------------------------------------------                                                                                                             
#h_ratio_nvtx = h_data_nvtx.Clone("h_ratio_nvtx")    
#h_ratio_nvtx.Divide(h_DY_nvtx)                                                                                                                         
#outfile = TFile("f_nvtx_reweighting_v2.root", "RECREATE")
#h_ratio_nvtx.Write()
#outfile.Close()


# --------------- #
# With PU Weights #
# --------------- #
canvasname = "c_PUw"
c1 = TCanvas(canvasname,canvasname,1200,1200)
c1.cd()

pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
pad1.Draw()
pad1.cd()
#pad1.SetBottomMargin(0.9)
pad1.SetLeftMargin(1.9)

h_DY_nvtx.SetLineColor(kBlue-10)
h_DY_nvtx.SetFillColorAlpha(kBlue-10,0.8)
h_DY_nvtx.SetLineWidth(2)

h_DY_nvtx.GetXaxis().SetLabelSize(0)

if (normAU):
    h_DY_nvtx.GetYaxis().SetTitle("A.U.")
else:
    h_DY_nvtx.GetYaxis().SetTitle("Events")

h_DY_nvtx.SetMaximum(1.8*h_DY_nvtx.GetMaximum())

h_DY_nvtx.GetYaxis().SetTitleSize(25)
h_DY_nvtx.GetYaxis().SetTitleFont(43)
h_DY_nvtx.GetYaxis().SetTitleOffset(2.25)
h_DY_nvtx.GetYaxis().SetLabelFont(43)
h_DY_nvtx.GetYaxis().SetLabelOffset(0.01)
h_DY_nvtx.GetYaxis().SetLabelSize(25)
h_DY_nvtx.Draw("histo")

h_data_nvtx.SetMarkerStyle(20)
h_data_nvtx.SetMarkerSize(1.2)
h_data_nvtx.SetLineColorAlpha(kBlack,0.8)
h_data_nvtx.Draw("epsame")

leg = TLegend(0.35,0.65,0.88,0.78)
leg.AddEntry(h_DY_nvtx,"DYJetsToLL MC (with PU weights)")
leg.AddEntry(h_data_nvtx,"Z #rightarrow ee Data", "P")
leg.SetLineWidth(0)
leg.Draw("same")

latexBin = ROOT.TLatex()                                                                                                    
latexBin.SetTextFont(52)                                                                                                                              
latexBin.SetTextSize(0.03)                                                                                                    
latexBin.SetTextColor(ROOT.kBlack)                                                                                                   
latexBin.SetTextAlign(22)  # Center alignment                                                                             
#if (r9Bins==True):
#    latexBin.DrawLatexNDC(0.65, 0.55, "High R9 (> 0.96) EB") 

c1.Update()
c1.cd()

pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.345)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.24)
#pad2.SetBottomMargin(0.19)

rp = TH1F(h_data_nvtx.Clone("rp")) 
rp.SetLineColor(kBlack)
rp.SetMinimum(0.7)
rp.SetMaximum(1.3)
rp.SetStats(0)
rp.Divide(h_DY_nvtx) 
rp.SetMarkerStyle(20)
rp.SetTitle("") 

rp.SetYTitle("Data / DY MC")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(27)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.0)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Number of primary vertices")
rp.GetXaxis().SetTitleSize(27)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(1.2)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()
c1.cd()

latex = TLatex();                                                                                     
latex.SetTextSize(0.04);                                                                                                          
latex.SetTextAlign(13);                                                                                                              
latex.SetTextFont(62)                                                                                                   
#latex.DrawLatexNDC(.12,.95,"CMS"); OutOfFrame                                                                            
latex.DrawLatexNDC(.14,.9,"CMS");                                                                                        
latex.SetTextFont(52)                                                                                                                
#latex.DrawLatexNDC(.20,.95, " Preliminary") #OutOfFrame     
latex.DrawLatexNDC(.235, .9, " Preliminary")                                                                                                                   
latex.SetTextFont(42)                                                                                                                        
latex.SetTextSize(0.035)                                                                                                       
latex.DrawLatexNDC(.64,.98, "54.4 fb^{-1} (13 TeV)")
c1.Update()
if (normAU):
    c1.SaveAs(outputdir+"/nvtx.png")
    c1.SaveAs(outputdir+"/nvtx.pdf")
else:
    c1.SaveAs(outputdir+"/nvtx_noNorm.png")
    c1.SaveAs(outputdir+"/nvtx_noNorm.pdf")

print("DY MC: ", h_DY_nvtx.Integral())
print("Data Z->ee: ", h_data_nvtx.Integral())


# -------------- #
# W/o PU Weights #
# -------------- #
canvasname = "c_noPUw"
c2 = TCanvas(canvasname,canvasname,1200,1200)
c2.cd()

pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
pad1.Draw()
pad1.cd()
pad1.SetLeftMargin(1.9)

h_DY_nvtx_noPUw.SetLineColor(kBlue-10)
h_DY_nvtx_noPUw.SetFillColorAlpha(kBlue-10,0.8)
h_DY_nvtx_noPUw.SetLineWidth(2)

h_DY_nvtx_noPUw.GetXaxis().SetLabelSize(0)

if (normAU):
    h_DY_nvtx_noPUw.GetYaxis().SetTitle("A.U.")
else:
    h_DY_nvtx_noPUw.GetYaxis().SetTitle("Events")

h_DY_nvtx_noPUw.SetMaximum(1.8*h_DY_nvtx_noPUw.GetMaximum())

h_DY_nvtx_noPUw.GetYaxis().SetTitleSize(25)
h_DY_nvtx_noPUw.GetYaxis().SetTitleFont(43)
h_DY_nvtx_noPUw.GetYaxis().SetTitleOffset(2.25)
h_DY_nvtx_noPUw.GetYaxis().SetLabelFont(43)
h_DY_nvtx_noPUw.GetYaxis().SetLabelOffset(0.01)
h_DY_nvtx_noPUw.GetYaxis().SetLabelSize(25)
h_DY_nvtx_noPUw.Draw("histo")

h_data_nvtx_noPUw.SetMarkerStyle(20)
h_data_nvtx_noPUw.SetMarkerSize(1.2)
h_data_nvtx_noPUw.SetLineColorAlpha(kBlack,0.8)
h_data_nvtx_noPUw.Draw("epsame")

leg = TLegend(0.35,0.65,0.88,0.78)
leg.AddEntry(h_DY_nvtx_noPUw,"DYJetsToLL MC (w/o PU weights)")
leg.AddEntry(h_data_nvtx_noPUw,"Z #rightarrow ee Data", "P")
leg.SetLineWidth(0)
leg.Draw("same")

latexBin = ROOT.TLatex()                                                                                                    
latexBin.SetTextFont(52)                                                                                                                              
latexBin.SetTextSize(0.03)                                                                                                    
latexBin.SetTextColor(ROOT.kBlack)                                                                                                   
latexBin.SetTextAlign(22)  # Center alignment                                                                             
#if (r9Bins==True):
#    latexBin.DrawLatexNDC(0.65, 0.55, "High R9 (> 0.96) EB") 

c2.Update()
c2.cd()

pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.345)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.01)
#pad2.SetBottomMargin(0.19)
pad2.SetBottomMargin(0.24)

rp = TH1F(h_data_nvtx_noPUw.Clone("rp")) 
rp.SetLineColor(kBlack)
rp.SetMinimum(0.7)
rp.SetMaximum(1.3)
rp.SetStats(0)
rp.Divide(h_DY_nvtx_noPUw) 
rp.SetMarkerStyle(20)
rp.SetTitle("") 

rp.SetYTitle("Data / DY MC")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(27)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.0)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Number of primary vertices")
rp.GetXaxis().SetTitleSize(27)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(1.2)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c2.Update()
c2.cd()

latex = TLatex();                                                                                     
latex.SetTextSize(0.04);                                                                                                          
latex.SetTextAlign(13);                                                                                                              
latex.SetTextFont(62)                                                                                                   
#latex.DrawLatexNDC(.12,.95,"CMS"); OutOfFrame                                                                            
latex.DrawLatexNDC(.14,.9,"CMS");                                                                                        
latex.SetTextFont(52)                                                                                                                
#latex.DrawLatexNDC(.20,.95, " Preliminary") #OutOfFrame     
latex.DrawLatexNDC(.235, .9, " Preliminary")                                                                                                                   
latex.SetTextFont(42)                                                                                                                        
latex.SetTextSize(0.035)                                                                                                       
latex.DrawLatexNDC(.64,.98, "54.4 fb^{-1} (13 TeV)")
c2.Update()
if (normAU):
    c2.SaveAs(outputdir+"/nvtx_noPUw.png")
    c2.SaveAs(outputdir+"/nvtx_noPUw.pdf")
else:
    c2.SaveAs(outputdir+"/nvtx_noPUw_noNorm.png")
    c2.SaveAs(outputdir+"/nvtx_noPUw_noNorm.pdf")

print("DY MC: ", h_DY_nvtx_noPUw.Integral())
print("Data Z->ee: ", h_data_nvtx_noPUw.Integral())

# ---------------------------- #
# With nVtx ReweightingWeights #
# -----------------------------#
canvasname = "c_NvtxRew"
c1 = TCanvas(canvasname,canvasname,1200,1200)
c1.cd()

pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
pad1.Draw()
pad1.cd()
pad1.SetLeftMargin(1.9)

h_DY_nvtx_final.SetLineColor(kBlue-10)
h_DY_nvtx_final.SetFillColorAlpha(kBlue-10,0.8)
h_DY_nvtx_final.SetLineWidth(2)

h_DY_nvtx_final.GetXaxis().SetLabelSize(0)

if (normAU):
    h_DY_nvtx_final.GetYaxis().SetTitle("A.U.")
else:
    h_DY_nvtx_final.GetYaxis().SetTitle("Events")

h_DY_nvtx_final.SetMaximum(1.8*h_DY_nvtx_final.GetMaximum())

h_DY_nvtx_final.GetYaxis().SetTitleSize(25)
h_DY_nvtx_final.GetYaxis().SetTitleFont(43)
h_DY_nvtx_final.GetYaxis().SetTitleOffset(2.25)
h_DY_nvtx_final.GetYaxis().SetLabelFont(43)
h_DY_nvtx_final.GetYaxis().SetLabelOffset(0.01)
h_DY_nvtx_final.GetYaxis().SetLabelSize(25)
h_DY_nvtx_final.Draw("histo")

h_data_nvtx.SetMarkerStyle(20)
h_data_nvtx.SetMarkerSize(1.2)
h_data_nvtx.SetLineColorAlpha(kBlack,0.8)
h_data_nvtx.Draw("epsame")

leg = TLegend(0.35,0.65,0.88,0.78)
leg.AddEntry(h_DY_nvtx_final,"DYJetsToLL MC (with PU weights)")
leg.AddEntry(h_data_nvtx,"Z #rightarrow ee Data", "P")
leg.SetLineWidth(0)
leg.Draw("same")

latexBin = ROOT.TLatex()                                                                                                    
latexBin.SetTextFont(52)                                                                                                                              
latexBin.SetTextSize(0.03)                                                                                                    
latexBin.SetTextColor(ROOT.kBlack)                                                                                                   
latexBin.SetTextAlign(22)  # Center alignment                                                                             
#if (r9Bins==True):
#    latexBin.DrawLatexNDC(0.65, 0.55, "High R9 (> 0.96) EB") 

c1.Update()
c1.cd()

pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.345)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.24)
#pad2.SetBottomMargin(0.19)

rp = TH1F(h_data_nvtx.Clone("rp")) 
rp.SetLineColor(kBlack)
rp.SetMinimum(0.7)
rp.SetMaximum(1.3)
rp.SetStats(0)
rp.Divide(h_DY_nvtx_final) 
rp.SetMarkerStyle(20)
rp.SetTitle("") 

rp.SetYTitle("Data / DY MC")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(27)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.0)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Number of primary vertices")
rp.GetXaxis().SetTitleSize(27)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(1.2)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()
c1.cd()

latex = TLatex();                                                                                     
latex.SetTextSize(0.04);                                                                                                          
latex.SetTextAlign(13);                                                                                                              
latex.SetTextFont(62)                                                                                                   
#latex.DrawLatexNDC(.12,.95,"CMS"); OutOfFrame                                                                            
latex.DrawLatexNDC(.14,.9,"CMS");                                                                                        
latex.SetTextFont(52)                                                                                                                
#latex.DrawLatexNDC(.20,.95, " Preliminary") #OutOfFrame     
latex.DrawLatexNDC(.235, .9, " Preliminary")                                                                                                                   
latex.SetTextFont(42)                                                                                                                        
latex.SetTextSize(0.035)                                                                                                       
latex.DrawLatexNDC(.64,.98, "54.4 fb^{-1} (13 TeV)")
c1.Update()
if (normAU):
    c1.SaveAs(outputdir+"/nvtx_withNvtxReweighting.png")
    c1.SaveAs(outputdir+"/nvtx_withNvtxReweighting.pdf")
else:
    c1.SaveAs(outputdir+"/nvtx_noNorm.png")
    c1.SaveAs(outputdir+"/nvtx_noNorm.pdf")

print("DY MC: ", h_DY_nvtx_final.Integral())
print("Data Z->ee: ", h_data_nvtx.Integral())

