from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
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

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV

# ----------------------
# Obtain histogram files
# ----------------------
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ")
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/sb_data2018.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")
f_gj080 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/gjets_080.root","READ")                              
f_qcd080 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/qcd_080.root","READ")                   

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
gj0 = f_gj080.Get("tagsDumper/trees/gjets_promptfake_13TeV_UntaggedTag_0")                                                    
qcd0 = f_qcd080.Get("tagsDumper/trees/qcd_fakefake_13TeV_UntaggedTag_0")

# ------------------------------------------------ #                            
# Preparing 2D templates for min and max photon ID #                                           
# ------------------------------------------------ #                                      
def fill_histograms_2d(histogram, value_x, value_y, weight=1):
    n_bins_x = histogram.GetNbinsX()
    n_bins_y = histogram.GetNbinsY()

    x = min(value_x, histogram.GetXaxis().GetXmax())
    y = min(value_y, histogram.GetYaxis().GetXmax())

    bin_x = histogram.GetXaxis().FindBin(x)
    bin_y = histogram.GetYaxis().FindBin(y)

    if value_x > histogram.GetXaxis().GetXmax():
        bin_x = n_bins_x

    if value_y > histogram.GetYaxis().GetXmax():
        bin_y = n_bins_y

    histogram.Fill(x, y, weight)

# Create a 2D histogram (data histogram)
# --------------------------------------
h_phoId_pre0 = TH2F("h_phoId_pre0", "h_phoId_pre0", 36, -0.8, 1., 36, -0.8, 1.)

# Create 2D histograms for background samples
# -------------------------------------------------
h_phoId_sba0 = TH2F("h_phoId_sba0", "h_phoId_sba0", 36, -0.8, 1., 36, -0.8, 1.)
h_phoId_mgg0 = TH2F("h_phoId_mgg0", "h_phoId_mgg0", 36, -0.8, 1., 36, -0.8, 1.)
h_phoId_bkg = TH2F("h_phoId_bkg", "h_phoId_bkg", 36, -0.8, 1., 36, -0.8, 1.)
h_phoId_qcd0 = TH2F("h_phoId_qcd0", "h_phoId_qcd0", 36, -0.8, 1., 36, -0.8, 1.)
h_phoId_gjets0 = TH2F("h_phoId_gjets0", "h_phoId_gjets0", 36, -0.8, 1., 36, -0.8, 1.)

# Fill the histograms with data and MC samples
# --------------------------------------------
sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_sba0", "weight*(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")
#sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_sba0", "weight*(CMS_hgg_mass<75 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")
dat0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_pre0", "CMS_hgg_mass<75 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7","goff")
mgg0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_mgg0", "weight*(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")
qcd0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_qcd0", "weight*(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")
gj0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_gjets0", "weight*(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")

# To inject a contribution of gJets+QCD similar to the MC expectation starting with all SB data
h_phoId_sba0.Scale(0.02190371141)

# Plot data and MC 2D templates 
# -----------------------------
c_sba0 = TCanvas("c_sba0","c_sba0",1200,800)
c_sba0.cd()
c_sba0.SetLeftMargin(0.12)
c_sba0.SetRightMargin(0.15)
h_phoId_sba0.Draw("COLZ")
h_phoId_sba0.GetXaxis().SetTitle("Min #gamma ID MVA")
h_phoId_sba0.GetYaxis().SetTitle("Max #gamma ID MVA")
# CMS lumi info                                                                                                              
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_sba0, 0, 0)
c_sba0.Update()
c_sba0.SaveAs(outputdir+"/2d_diphoMVAId_sba0_presel_allSB.png")
c_sba0.SaveAs(outputdir+"/2d_diphoMVAId_sba0_presel_allSB.pdf")

c_mgg0 = TCanvas("c_mgg0","c_mgg0",1200,800)
c_mgg0.cd()
c_mgg0.SetLeftMargin(0.12)
c_mgg0.SetRightMargin(0.15)
h_phoId_mgg0.Draw("COLZ")
h_phoId_mgg0.GetXaxis().SetTitle("Min #gamma ID MVA")
h_phoId_mgg0.GetYaxis().SetTitle("Max #gamma ID MVA")
CMS_lumi.CMS_lumi(c_mgg0, 0, 0)
c_mgg0.Update()
c_mgg0.SaveAs(outputdir+"/2d_diphoMVAId_mgg0_presel_allSB.png")
c_mgg0.SaveAs(outputdir+"/2d_diphoMVAId_mgg0_presel_allSB.pdf")

c_pre0 = TCanvas("c_pre0","c_pre0",1200,800)
c_pre0.cd()
c_pre0.SetLeftMargin(0.12)
c_pre0.SetRightMargin(0.15)
h_phoId_pre0.Draw("COLZ")
h_phoId_pre0.GetXaxis().SetTitle("Min #gamma ID MVA")
h_phoId_pre0.GetYaxis().SetTitle("Max #gamma ID MVA")
CMS_lumi.CMS_lumi(c_pre0, 0, 0)
c_pre0.Update()
c_pre0.SaveAs(outputdir+"/2d_diphoMVAId_pre0_presel_allSB.png")
c_pre0.SaveAs(outputdir+"/2d_diphoMVAId_pre0_presel_allSB.pdf")


# Create a TObjArray for the MC histograms
# ----------------------------------------
bkg = TObjArray(2)
bkg.Add(h_phoId_sba0)
bkg.Add(h_phoId_mgg0)

print("DATA Integral = ", h_phoId_pre0.Integral())
print("-----------------------------------------")
print("QCD MC Integral = ", h_phoId_qcd0.Integral())
print("GJets MC Integral = ", h_phoId_gjets0.Integral())
print("Diphoton MC Integral = ", h_phoId_mgg0.Integral())
print("Weighted SB Integral = ", h_phoId_sba0.Integral())
print("TOTAL MC Integral = ", h_phoId_mgg0.Integral() + h_phoId_sba0.Integral())
print("-----------------------------------------")
print("Initial fractions of the Total MC Integral:")
print ("Frac PF+FF dd = ", h_phoId_sba0.Integral()/(h_phoId_mgg0.Integral()+h_phoId_sba0.Integral()))
print ("Frac diphoton = ", h_phoId_mgg0.Integral()/(h_phoId_mgg0.Integral()+h_phoId_sba0.Integral()))

# Initialize TFractionFitter
fit = TFractionFitter(h_phoId_pre0, bkg)

# Constrain fraction 1 to be between 0 and 1
fit.Constrain(0, 0.0, 1)
fit.Constrain(1, 0.0, 1)

# Perform the fit
fitStatus = fit.Fit()
status = fitStatus.Status()
print("Fit status:", status)

# Check the fit status
if status == 0:
    
    print("Getting the resulting plot...")

    # Get the result histogram
    result = fit.GetPlot()

    # Create a canvas for the result
    # ------------------------------
    c = TCanvas("c", "Fit Result", 1200, 800)    
    c.SetLeftMargin(0.12)
    c.SetRightMargin(0.15)
    # Draw the data histogram
    result.GetXaxis().SetTitleOffset(1.5)
    result.GetYaxis().SetTitleOffset(1.5)
    result.GetZaxis().SetTitleOffset(1.5)
    # Draw the result histogram on top
    result.Draw("COLZ TEXT")
    CMS_lumi.CMS_lumi(c, 0, 0)
    c.Draw()
    c.SaveAs(outputdir+"/fitRes_allSB.png")
    c.SaveAs(outputdir+"/fitRes_allSB.pdf")

    # Create a canvas for the result
    # ------------------------------
    c_ratio = TCanvas("c_ratio", "Ratio Presel/FitResult", 1200, 800)    
    c_ratio.SetLeftMargin(0.12)
    c_ratio.SetRightMargin(0.15)
    h_ratio = h_phoId_pre0.Clone("h_phoId_pre0")
    h_ratio.Divide(result)

    print("After Fit MC Integral = ", result.Integral())

    # Draw the ratio between preselection region and result after the fit
    h_ratio.GetXaxis().SetTitleOffset(1.5)
    h_ratio.GetYaxis().SetTitleOffset(1.5)
    h_ratio.GetZaxis().SetTitleOffset(1.5)
    h_ratio.Draw("COLZ")
    CMS_lumi.CMS_lumi(c_ratio, 0, 0)
    c_ratio.Draw()
    c_ratio.SaveAs(outputdir+"/fitRes_ratio_allSB.png")
    c_ratio.SaveAs(outputdir+"/fitRes_ratio_allSB.pdf")

    # Create a canvas for the result
    # ------------------------------
    c_scaled = TCanvas("c_scaled", "Ratio Presel/ScaledBkg", 1200, 800)    
    c_scaled.SetLeftMargin(0.12)
    c_scaled.SetRightMargin(0.15)

    print("------------------------------------")
    h_phoId_sba0.Integral()
    h_phoId_mgg0.Integral()
    print("Pre Scaling sba0 Integral = ", h_phoId_sba0.Integral())
    print("Pre Scaling mgg0 Integral = ", h_phoId_mgg0.Integral())
    print("Pre Scaling bkg Integral = ", h_phoId_sba0.Integral()+h_phoId_mgg0.Integral())
    print("------------------------------------------------------")

    h_phoId_sba0.Scale(0.82*5.123913988) 
    h_phoId_mgg0.Scale(1.64*5.123913988) 

    h_phoId_bkg.Add(h_phoId_sba0)
    h_phoId_bkg.Add(h_phoId_mgg0)
    print("Post Scaling sba0 Integral = ", h_phoId_sba0.Integral())
    print("Post Scaling mgg0 Integral = ", h_phoId_mgg0.Integral())
    print("Post Scaling bkg Integral = ", h_phoId_sba0.Integral()+h_phoId_mgg0.Integral())
    print("------------------------------------------------------")
    print("After Scaling BKG Integral (with add) = ", h_phoId_bkg.Integral())
    h_scaled = h_phoId_pre0.Clone("h_phoId_pre0")
    h_scaled.Divide(h_phoId_bkg)

    # Draw the scaled between preselection region and result after the fit
    h_scaled.GetXaxis().SetTitleOffset(1.5)
    h_scaled.GetYaxis().SetTitleOffset(1.5)
    h_scaled.GetZaxis().SetTitleOffset(1.5)
    h_scaled.Draw("COLZ")
    CMS_lumi.CMS_lumi(c_scaled, 0, 0)
    c_scaled.Draw()
    c_scaled.SaveAs(outputdir+"/fitRes_ratioScaledBkg_allSB.png")
    c_scaled.SaveAs(outputdir+"/fitRes_ratioScaledBkg_allSB.pdf")

gApplication.Run()
