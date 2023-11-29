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
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_D.root","READ") #Data with unweighted events, both regions
#sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_multiKest1D_Nov1.root","READ")
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_kest1D_Inclusive.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

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
h_phoId_pre0 = TH2F("h_phoId_pre0", "h_phoId_pre0", 34, -0.7, 1., 34, -0.7, 1.)

# Create 2D histograms for background samples
# -------------------------------------------------
h_phoId_sba0 = TH2F("h_phoId_sba0", "h_phoId_sba0", 34, -0.7, 1., 34, -0.7, 1.)
h_phoId_mgg0 = TH2F("h_phoId_mgg0", "h_phoId_mgg0", 34, -0.7, 1., 34, -0.7, 1.)
h_phoId_bkg = TH2F("h_phoId_bkg", "h_phoId_bkg", 34, -0.7, 1., 34, -0.7, 1.)

# Fill the histograms with data and MC samples
# --------------------------------------------
sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_sba0", "weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")
#sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_sba0", "weight*(CMS_hgg_mass>0)","goff")
dat0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_pre0", "CMS_hgg_mass>0 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7","goff")
mgg0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_mgg0", "weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")

#c_dat0 = 0
#for ev_dat0 in dat0:
#    c_dat0 += 1
#    if (not(c_dat0%20==0)): continue
#    if (min(ev_dat0.dipho_leadIDMVA,ev_dat0.dipho_subleadIDMVA) < -0.7): continue
#    fill_histograms_2d(h_phoId_pre0, min(ev_dat0.dipho_leadIDMVA,ev_dat0.dipho_subleadIDMVA),  max(ev_dat0.dipho_leadIDMVA,ev_dat0.dipho_subleadIDMVA), 1.)
#print("h_phoId_pre0 Integral = ", h_phoId_pre0.Integral())

#for ev_sb0 in sb0:
#    fill_histograms_2d(h_phoId_sba0, min(ev_sb0.dipho_leadIDMVA,ev_sb0.dipho_subleadIDMVA),  max(ev_sb0.dipho_leadIDMVA,ev_sb0.dipho_subleadIDMVA), ev_sb0.weight)
#print("h_phoId_sba0 Integral = ", h_phoId_sba0.Integral())
#
#for ev_mgg0 in mgg0:
#    fill_histograms_2d(h_phoId_sba0, min(ev_mgg0.dipho_leadIDMVA,ev_mgg0.dipho_subleadIDMVA),  max(ev_mgg0.dipho_leadIDMVA,ev_mgg0.dipho_subleadIDMVA), ev_mgg0.weight)
#print("h_phoId_mgg0 Integral = ", h_phoId_mgg0.Integral())


# Plot data and MC 2D templates 
# -----------------------------
c_sba0 = TCanvas("c_sba0","c_sba0",1200,800)
c_sba0.cd()
c_sba0.SetLeftMargin(0.12)
c_sba0.SetRightMargin(0.15)
h_phoId_sba0.Draw("COLZ")
h_phoId_sba0.GetXaxis().SetTitle("Min #gamma ID MVA")
h_phoId_sba0.GetYaxis().SetTitle("Max #gamma ID MVA")
#CMS lumi stuff                                                                                                               
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
#CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_sba0, 0, 0)
c_sba0.Update()
c_sba0.SaveAs(outputdir+"/2d_diphoMVAId_sba0_presel_new.png")
c_sba0.SaveAs(outputdir+"/2d_diphoMVAId_sba0_presel_new.pdf")

c_mgg0 = TCanvas("c_mgg0","c_mgg0",1200,800)
c_mgg0.cd()
c_mgg0.SetLeftMargin(0.12)
c_mgg0.SetRightMargin(0.15)
h_phoId_mgg0.Draw("COLZ")
h_phoId_mgg0.GetXaxis().SetTitle("Min #gamma ID MVA")
h_phoId_mgg0.GetYaxis().SetTitle("Max #gamma ID MVA")
CMS_lumi.CMS_lumi(c_mgg0, 0, 0)
c_mgg0.Update()
c_mgg0.SaveAs(outputdir+"/2d_diphoMVAId_mgg0_presel_new.png")
c_mgg0.SaveAs(outputdir+"/2d_diphoMVAId_mgg0_presel_new.pdf")

c_pre0 = TCanvas("c_pre0","c_pre0",1200,800)
c_pre0.cd()
c_pre0.SetLeftMargin(0.12)
c_pre0.SetRightMargin(0.15)
h_phoId_pre0.Draw("COLZ")
h_phoId_pre0.GetXaxis().SetTitle("Min #gamma ID MVA")
h_phoId_pre0.GetYaxis().SetTitle("Max #gamma ID MVA")
CMS_lumi.CMS_lumi(c_pre0, 0, 0)
c_pre0.Update()
c_pre0.SaveAs(outputdir+"/2d_diphoMVAId_pre0_presel_new.png")
c_pre0.SaveAs(outputdir+"/2d_diphoMVAId_pre0_presel_new.pdf")


# Create a TObjArray for the MC histograms
# ----------------------------------------
bkg = TObjArray(2)
bkg.Add(h_phoId_sba0)
bkg.Add(h_phoId_mgg0)

print("DATA Integral = ", h_phoId_pre0.Integral())
print("Diphoton MC Integral = ", h_phoId_mgg0.Integral())
print("Weighted SB Integral = ", h_phoId_sba0.Integral())
print("TOTAL MC Integral = ", h_phoId_mgg0.Integral() + h_phoId_sba0.Integral())
print("Initial fractions of the Total MC Integral:")
print ("Frac PF+FF dd = ", h_phoId_sba0.Integral()/(h_phoId_mgg0.Integral()+h_phoId_sba0.Integral()))
print ("Frac diphoton = ", h_phoId_mgg0.Integral()/(h_phoId_mgg0.Integral()+h_phoId_sba0.Integral()))

# Initialize TFractionFitter
fit = TFractionFitter(h_phoId_pre0, bkg)

# Constrain fraction 1 to be between 0 and 1
fit.Constrain(0, 0.0, 1)
fit.Constrain(1, 0.0, 1)

# Set the range for X and Y bins
#fit.SetRangeX(-1, 1)
#fit.SetRangeY(-1, 1)

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
    # Display the canvas
    c.Draw()
    c.SaveAs(outputdir+"/fitRes_new.png")
    c.SaveAs(outputdir+"/fitRes_new.pdf")

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
    # Display the canvas
    c_ratio.Draw()
    c_ratio.SaveAs(outputdir+"/fitRes_ratio_new.png")
    c_ratio.SaveAs(outputdir+"/fitRes_ratio_new.pdf")

    # Create a canvas for the result
    # ------------------------------
    c_scaled = TCanvas("c_scaled", "Ratio Presel/ScaledBkg", 1200, 800)    
    c_scaled.SetLeftMargin(0.12)
    c_scaled.SetRightMargin(0.15)

    print("------------------------------------")
    #h_phoId_sba0.Scale(0.7)
    #h_phoId_mgg0.Scale(3.1)
    h_phoId_sba0.Integral()
    h_phoId_mgg0.Integral()
    print("Pre Scaling sba0 Integral = ", h_phoId_sba0.Integral())
    print("Pre Scaling mgg0 Integral = ", h_phoId_mgg0.Integral())
    print("Pre Scaling bkg Integral = ", h_phoId_sba0.Integral()+h_phoId_mgg0.Integral())
    print("------------------------------------------------------")
    h_phoId_sba0.Scale(0.062)
    h_phoId_mgg0.Scale(5.955)
    h_phoId_bkg.Add(h_phoId_sba0)
    h_phoId_bkg.Add(h_phoId_mgg0)
    print("Post Scaling sba0 Integral = ", h_phoId_sba0.Integral())
    print("Post Scaling mgg0 Integral = ", h_phoId_mgg0.Integral())
    print("Post Scaling bkg Integral = ", h_phoId_sba0.Integral()+h_phoId_mgg0.Integral())
    print("------------------------------------------------------")
    #h_phoId_bkg.Scale(0.1363464437)
    #h_phoId_bkg.Scale(h_phoId_pre0.Integral()/(h_phoId_mgg0.Integral() + h_phoId_sba0.Integral()))
    print("After Scaling BKG Integral (with add) = ", h_phoId_bkg.Integral())
    h_scaled = h_phoId_pre0.Clone("h_phoId_pre0")
    h_scaled.Divide(h_phoId_bkg)

    # Draw the scaled between preselection region and result after the fit
    h_scaled.GetXaxis().SetTitleOffset(1.5)
    h_scaled.GetYaxis().SetTitleOffset(1.5)
    h_scaled.GetZaxis().SetTitleOffset(1.5)
    h_scaled.Draw("COLZ")
    CMS_lumi.CMS_lumi(c_scaled, 0, 0)
    # Display the canvas
    c_scaled.Draw()
    c_scaled.SaveAs(outputdir+"/fitRes_ratioScaledBkg_new.png")
    c_scaled.SaveAs(outputdir+"/fitRes_ratioScaledBkg_new.pdf")

gApplication.Run()
