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
f_data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_D.root","READ") #Data with unweighted events, both regions
#sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_multiKest1D_Nov1.root","READ")
f_sb = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_kest1D_Inclusive.root","READ")
f_mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = f_sb.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = f_mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

# ------------------------------------------------ #                            
# Preparing 2D templates for min and max photon ID #                                           
# ------------------------------------------------ #                                      

# Create a 2D histogram (data histogram)
# --------------------------------------
#data = TH2F("data", "Data 2D Histogram", 10, 0, 10, 10, 0, 10)
data = TH1F("data", "Maximum #gamma MVA ID in data", 34, -0.7, 1)
#data = TH1F("data", "Maximum #gamma MVA ID in data", 85, -0.7, 1)

# Create 2D histograms for Monte Carlo (MC) samples
# -------------------------------------------------
#mc0 = TH2F("mc0", "MC 0 2D Histogram", 10, 0, 10, 10, 0, 10)
#mc1 = TH2F("mc1", "MC 1 2D Histogram", 10, 0, 10, 10, 0, 10)
#mc2 = TH2F("mc2", "MC 2 2D Histogram", 10, 0, 10, 10, 0, 10)
h_phoId_sba0 = TH1F("h_phoId_sba0", "Maximum #gamma MVA ID in data SB", 34, -0.7, 1.)
h_phoId_mgg0 = TH1F("h_phoId_mgg0", "Maximum #gamma MVA ID in diphoton MC", 34, -0.7, 1.)
h_phoId_mc = TH1F("h_phoId_mc", "Maximum #gamma MVA ID in PF+FF dd & #gamma#gamma", 34, -0.7, 1.)
h_phoId_mcScaled = TH1F("h_phoId_mcScaled", "Maximum #gamma MVA ID in PF+FF dd & #gamma#gamma", 34, -0.7, 1.)
#h_phoId_sba0 = TH1F("h_phoId_sba0", "Maximum #gamma MVA ID in data SB", 85, -0.7, 1.)
#h_phoId_mgg0 = TH1F("h_phoId_mgg0", "Maximum #gamma MVA ID in diphoton MC", 85, -0.7, 1.)
#h_phoId_mc = TH1F("h_phoId_mc", "Maximum #gamma MVA ID in PF+FF dd & #gamma#gamma", 85, -0.7, 1.)

# Fill the histograms with data and MC samples
# --------------------------------------------
sb0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_sba0", "weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
#sb0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_sba0", "weight*(CMS_hgg_mass>0 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
dat0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>data", "CMS_hgg_mass>0 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7","goff")
mgg0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_mgg0", "weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
#dat0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA):max(dipho_leadIDMVA,dipho_subleadIDMVA)>>h_phoId_pre0", "CMS_hgg_mass>0 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7","goff")

# Create a TObjArray for the MC histograms
# ----------------------------------------
h_phoId_mc.Add(h_phoId_sba0)
h_phoId_mc.Add(h_phoId_mgg0)
mc = TObjArray(2)
mc.Add(h_phoId_sba0)
mc.Add(h_phoId_mgg0)

print("DATA Integral = ", data.Integral())
print("Diphoton MC Integral = ", h_phoId_mgg0.Integral())
print("Weighted SB Integral = ", h_phoId_sba0.Integral())
print("TOTAL MC Integral = ", h_phoId_mgg0.Integral() + h_phoId_sba0.Integral())
print("Initial fractions of the Total MC Integral:")
print ("Frac PF+FF dd = ", h_phoId_sba0.Integral()/(h_phoId_mgg0.Integral()+h_phoId_sba0.Integral()))
print ("Frac diphoton = ", h_phoId_mgg0.Integral()/(h_phoId_mgg0.Integral()+h_phoId_sba0.Integral()))

# Initialize TFractionFitter
fit = TFractionFitter(data, mc)

# Constrain fraction 1 to be between 0 and 1
fit.Constrain(1, 0.0, 1.0)

# Set the range for X bins
#fit.SetRangeX(-1, 1)

# Perform the fit
fitStatus = fit.Fit()
status = fitStatus.Status()
print("Fit status:", status)

# Check the fit status
if status == 0:
    # Get the result histogram
    result = fit.GetPlot()

    # Create a canvas
    c = TCanvas("c", "Fit Result 1D minimum #gamma MVA ID", 1200, 800)
    c.SetLeftMargin(0.12)
    c.SetRightMargin(0.15)

    # Draw the data histogram
    data.GetXaxis().SetTitle("Maximum #gamma ID MVA")
    data.GetYaxis().SetTitle("Events/0.05")
    data.SetMaximum(1.3 * data.GetMaximum())
    data.SetLineWidth(3)
    data.SetLineColor(kBlue)
    data.Draw("h")
    # Draw the result histogram on top
    result.SetLineWidth(3)
    result.SetLineColor(kMagenta-7)
    result.Draw("h same")
    print("After Fit MC Integral = ", result.Integral())
    h_phoId_mc.SetLineWidth(3)
    h_phoId_mc.SetLineStyle(kDashed)
    h_phoId_mc.SetLineColor(kRed-4)
    h_phoId_mc.Draw("h same")
    h_phoId_sba0.SetLineWidth(2)
    h_phoId_sba0.SetLineStyle(kDashed)
    h_phoId_sba0.SetLineColor(kOrange-3)
    h_phoId_sba0.Draw("h same")
    h_phoId_mgg0.SetLineWidth(2)
    h_phoId_mgg0.SetLineStyle(kDashed)
    h_phoId_mgg0.SetLineColor(kOrange-2)
    h_phoId_mgg0.Draw("h same")

    #h_phoId_sba0.Scale(0.7 * 5./100 * 1.88)
    #h_phoId_mgg0.Scale(2.2 * 1.88)
    h_phoId_sba0.Scale(0.0622)
    h_phoId_mgg0.Scale(5.9546)
    h_phoId_mcScaled.Add(h_phoId_sba0)
    h_phoId_mcScaled.Add(h_phoId_mgg0)
    #h_phoId_mcScaled.Scale(data.Integral()/(h_phoId_mc.Integral()))
    h_phoId_mcScaled.SetLineWidth(3)
    h_phoId_mcScaled.SetLineStyle(kDashed)
    h_phoId_mcScaled.SetLineColor(kCyan-3)
    h_phoId_mcScaled.Draw("h same")

    leg = TLegend(0.3,0.55,0.8,0.88)
    leg.AddEntry(data,"Data Preselection")
    leg.AddEntry(result,"PF+FF dd & #gamma#gamma Post fit")
    leg.AddEntry(h_phoId_mc,"PF+FF dd & #gamma#gamma Pre fit")
    leg.AddEntry(h_phoId_sba0,"PF+FF dd Pre fit")
    leg.AddEntry(h_phoId_mgg0,"#gamma#gamma Pre fit")
    leg.AddEntry(h_phoId_mcScaled,"PF+FF dd & #gamma#gamma Scaled")
    leg.SetLineWidth(0)
    leg.Draw("same")

    #CMS lumi stuff                                                                                                  
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText      = "Preliminary"
    #CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"                                                                                
    CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
    CMS_lumi.cmsTextSize    = 0.6
    CMS_lumi.lumiTextSize   = 0.46
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12    
    CMS_lumi.CMS_lumi(c, 0, 0)

    # Display the canvas
    c.Draw()
    c.SaveAs(outputdir+"/fitRes_maxPhoId_1d.png")
    c.SaveAs(outputdir+"/fitRes_maxPhoId_1d.pdf")

gApplication.Run()


