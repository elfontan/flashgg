import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain, THStack, gStyle, TPad, TLegend
import ROOT, array, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList, kYellow, kOrange, kBlue, kBlack
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
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
logScale = args.log

# ----------------------
# Obtain histogram files
# ----------------------
para = TFile("output_ParaDDFullSigBkgNorms.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = para.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = para.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
sig0_10 = para.Get("tagsDumper/trees/ggh_10_13TeV_UntaggedTag_0")
sig0_15 = para.Get("tagsDumper/trees/ggh_15_13TeV_UntaggedTag_0")
sig0_20 = para.Get("tagsDumper/trees/ggh_20_13TeV_UntaggedTag_0")
#sig0_25 = para.Get("tagsDumper/trees/ggh_25_13TeV_UntaggedTag_0")
sig0_30 = para.Get("tagsDumper/trees/ggh_30_13TeV_UntaggedTag_0")
#sig0_35 = para.Get("tagsDumper/trees/ggh_35_13TeV_UntaggedTag_0")
sig0_40 = para.Get("tagsDumper/trees/ggh_40_13TeV_UntaggedTag_0")
#sig0_45 = para.Get("tagsDumper/trees/ggh_45_13TeV_UntaggedTag_0")
sig0_50 = para.Get("tagsDumper/trees/ggh_50_13TeV_UntaggedTag_0")
sig0_55 = para.Get("tagsDumper/trees/ggh_55_13TeV_UntaggedTag_0")
sig0_60 = para.Get("tagsDumper/trees/ggh_60_13TeV_UntaggedTag_0")
#sig0_65 = para.Get("tagsDumper/trees/ggh_65_13TeV_UntaggedTag_0")
sig0_70 = para.Get("tagsDumper/trees/ggh_70_13TeV_UntaggedTag_0")

var_list = ["dipho_masshyp_near"]
label_list = ["m_{hyp,near}"]

histo_dat0_list = OrderedDict()
histo_mgg0_list = OrderedDict()
histo_sig0_list = OrderedDict()

# Create a dictionary to store the binning information for each variable
# ----------------------------------------------------------------------
binning_info = { 
    var_list[0]: (32, 0., 80.),   #dipho_masshyp_near
}

for variable in var_list:
    nbins, xlow, xhigh = binning_info[variable]
    print("var_list[i]", variable)
    print("nbins = ", nbins)
    print("xlow = ", xlow)
    print("xhigh = ", xhigh)
    histo_dat0_list[variable + "_dat0"] = TH1F("h_" + variable + "_dat0", "h_" + variable + "_dat0", nbins, xlow, xhigh)
    histo_mgg0_list[variable + "_mgg0"] = TH1F("h_" + variable + "_mgg0", "h_" + variable + "_mgg0", nbins, xlow, xhigh)
    histo_sig0_list[variable + "_sig0"] = TH1F("h_" + variable + "_sig0", "h_" + variable + "_sig0", nbins, xlow, xhigh)


    # Fill the histograms
    dat0.Draw(variable + ">>h_" + variable + "_dat0", "weight*weight_allDD*dipho_hypnorm_near*dipho_hypSigBkgNorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")     
    mgg0.Draw(variable + ">>h_" + variable + "_mgg0", "weight*weight_allDD*dipho_hypnorm_near*dipho_hypSigBkgNorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")

    sig0_10.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_15.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_20.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    #sig0_25.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_30.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    #sig0_35.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_40.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    #sig0_45.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_50.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_55.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_60.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    #sig0_65.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    sig0_70.Draw(variable + ">>+h_" + variable + "_sig0", "weight*w_signal*dipho_hypwgt_near*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")

idx = 0
for variable in var_list:
    print(variable)

    # MC Scaling
    dat0 = histo_dat0_list[variable + "_dat0"]
    mgg0 = histo_mgg0_list[variable + "_mgg0"]
    sig0 = histo_sig0_list[variable + "_sig0"]
    bkg0 = THStack("bkg0","bkg0")
    
    # Plotting
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    canvasname = "c_"+variable
    c1 = TCanvas(canvasname,canvasname,1200,1200)
    c1.cd()
    #c1.SetLeftMargin(0.15)
    
    # Upper plot pad - Data histos
    pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
    pad1.Draw()
    pad1.cd()
    #pad1.SetLogy()                                                                                                  
    pad1.SetBottomMargin(0.01)
    pad1.SetLeftMargin(1.9)
    
    dat0.SetLineColor(kYellow-7)
    dat0.SetFillColorAlpha(kYellow-7,0.8)
    dat0.SetLineWidth(2)
    
    dat0.GetXaxis().SetLabelSize(0)
    
    dat0.GetYaxis().SetTitle("Events")
    dat0.GetYaxis().SetTitleSize(25)
    dat0.GetYaxis().SetTitleFont(43)
    dat0.GetYaxis().SetTitleOffset(2.25)
    dat0.GetYaxis().SetLabelFont(43)
    dat0.GetYaxis().SetLabelOffset(0.01)
    dat0.GetYaxis().SetLabelSize(25)
    
    mgg0.SetLineColor(kOrange-4)
    mgg0.SetFillColorAlpha(kOrange-4,0.8)
    mgg0.SetLineWidth(2)
        
    bkg0.Add(mgg0)
    bkg0.Add(dat0)

    dat0.SetMaximum(1.5*(bkg0.GetMaximum()))
    mgg0.SetMaximum(1.5*(bkg0.GetMaximum()))
    bkg0.SetMaximum(1.5*(bkg0.GetMaximum()))
    sig0.SetMaximum(1.5*(bkg0.GetMaximum()))

    bkg0.Draw("histo")
    
    sig0.SetLineColor(kBlue-1)
    sig0.SetLineWidth(2)
    sig0.Draw("histosame")
        
    leg = TLegend(0.45,0.65,0.85,0.85)
    leg.AddEntry(dat0,"Reweighted Data-Driven Sideband")
    leg.AddEntry(mgg0,"Diphoton MC")
    leg.AddEntry(sig0,"Signal MC")
    leg.SetLineWidth(0)
    leg.Draw("same")
    
    c1.Update()
    c1.cd()
    
    # Lower plot pad - Ratio plot
    pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.35)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    pad2.SetTopMargin(0.)
    pad2.SetBottomMargin(0.17)
    pad2.SetLeftMargin(0.11)
    
    # Define ratio plot
    rp = TH1F(sig0.Clone("rp")) #clone the preselection region
    rp.SetLineColor(kBlack)
    rp.SetMinimum(-0.1)
    rp.SetMaximum(2.1)
    rp.SetStats(0)
    rp.Divide(dat0+mgg0) #divide by sideband+mgg
    rp.SetMarkerStyle(24)
    rp.SetTitle("") 
    
    rp.SetYTitle("Signal/Background")
    rp.GetYaxis().SetNdivisions(505)
    rp.GetYaxis().SetTitleSize(25)
    rp.GetYaxis().SetTitleFont(43)
    rp.GetYaxis().SetTitleOffset(2.25)
    rp.GetYaxis().SetLabelFont(43)
    rp.GetYaxis().SetLabelSize(25)
    
    rp.SetXTitle(label_list[idx])
    rp.GetXaxis().SetTitleSize(25)
    rp.GetXaxis().SetTitleFont(43)
    rp.GetXaxis().SetTitleOffset(3.9)
    rp.GetXaxis().SetLabelFont(43)
    rp.GetXaxis().SetLabelSize(25)
    rp.GetXaxis().SetLabelOffset(0.02)
    
    rp.Draw("ep")
    
    c1.Update()
    c1.cd()
    
    #CMS Title and Lumi info
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText      = "Preliminary"
    CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
    CMS_lumi.cmsTextSize    = 0.6
    CMS_lumi.lumiTextSize   = 0.46
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12
    CMS_lumi.CMS_lumi(pad1, 0, 0)
    
    c1.Update()
    c1.SaveAs(outputdir+"/"+variable+"_SigBkgWgtNorm_flatteningBkg_gradualDiphoIncrease.png")
    c1.SaveAs(outputdir+"/"+variable+"_SigBkgWgtNorm_flatteningBkg_gradualDiphoIncrease.pdf")
    
    idx += 1
    print("MGG: ", mgg0.Integral())
    print("Data: ", dat0.Integral())
    print("Signal: ", sig0.Integral())
