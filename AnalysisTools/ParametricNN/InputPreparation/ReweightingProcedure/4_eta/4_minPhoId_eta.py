######################################################                                                                      
# Very low mass diphoton analysis: input preparation #                                                                                        
# -------------------------------------------------- #                                                                              
# python3 environment, e.g. CMSSW_14_0_0                                                                                                     
# python3 1_minPhoId_eta.py --log True  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/1_minPhoId_etaReweighting

from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import CMSGraphics, CMS_lumi, random, copy
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


# Obtain histogram files
# ----------------------
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ")           
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb/sb_all2018Data_Mar2024_plusSigmaEOEPt.root","READ")  
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")                                      
norm_dipho = 5.07071342                                                                                                      
norm_sb = (5.07071342*0.02190371141)     

# Get trees and create histograms for data                                                                                              
# ----------------------------------------                                                                                  
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

# ------------------------------------------------- #
# REWEIGHTING: eta of the photon with minimum IDMVA #
# ------------------------------------------------- #
h_eta_sba0 = TH1F("h_eta_sba0", "h_eta_sba0", 60, -3., 3.)
h_eta_pre0 = TH1F("h_eta_pre0", "h_eta_pre0", 60, -3., 3.)
h_eta_mgg0 = TH1F("h_eta_mgg0", "h_eta_mgg0", 60, -3., 3.)


print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    c_sb0 += 1
    #if (not(c_sb0%20==0)): continue                                                                                                                             
    if (ev_sb0.CMS_hgg_mass > 75): continue
    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA and (min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7)):
        h_eta_sba0.Fill(ev_sb0.dipho_leadEta, ev_sb0.weight*ev_sb0.weight_sigmaEOE*ev_sb0.weight_ptOverM)
    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA and (min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7)):
        h_eta_sba0.Fill(ev_sb0.dipho_subleadEta, ev_sb0.weight*ev_sb0.weight_sigmaEOE*ev_sb0.weight_ptOverM)
print("h_eta_sba0 Integral = ", h_eta_sba0.Integral())

print("----------Opening data tree")
c_dat0 = 0
for ev_dat0 in dat0:
    c_dat0 += 1
    if (not(c_dat0%20==0)): continue
    if (ev_dat0.CMS_hgg_mass > 75): continue
    if (ev_dat0.dipho_leadIDMVA <= ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_eta_pre0.Fill(ev_dat0.dipho_leadEta)
    elif (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_eta_pre0.Fill(ev_dat0.dipho_subleadEta)
print("h_eta_pre0 Integral = ", h_eta_pre0.Integral())

print("----------Opening MC dipho tree")
for ev_mgg0 in mgg0:
    if (ev_mgg0.CMS_hgg_mass > 75): continue
    if (ev_mgg0.CMS_hgg_mass < 10): continue
    if (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        h_eta_mgg0.Fill(ev_mgg0.dipho_leadEta, ev_mgg0.weight)
    elif (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        h_eta_mgg0.Fill(ev_mgg0.dipho_subleadEta, ev_mgg0.weight)
print("h_eta_mgg0 Integral = ", h_eta_mgg0.Integral())

h_eta_sba0.Scale(norm_sb*0.82)
h_eta_mgg0.Scale(norm_dipho*1.68)
    
# Subtract MGG from Data Preselection
# -----------------------------------
h_eta_dataPreselMinus_mcDipho = h_eta_pre0.Clone("h_eta_dataPreselMinus_mcDipho")
h_eta_dataPreselMinus_mcDipho.Add(h_eta_mgg0, -1)

# Divide the result by the SB distribution to compute the ratio
# -------------------------------------------------------------
h_ratio_eta = h_eta_dataPreselMinus_mcDipho.Clone("h_ratio_eta")
h_ratio_eta.Divide(h_eta_sba0)


c_w1 = TCanvas("c_w1","c_w1",1200,800)
c_w1.cd()
c_w1.SetLeftMargin(0.15)                     
h_ratio_eta.GetYaxis().SetTitle("(Data presel - #gamma#gamma MC) / pf+ff DD")
h_ratio_eta.GetXaxis().SetTitle("Minimum MVA ID photon #eta")
h_ratio_eta.SetLineWidth(3)                                       
h_ratio_eta.SetLineColor(kBlue)                                       
h_ratio_eta.Draw("EP")                                       

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_w1, 0, 0)

c_w1.Update()
c_w1.SaveAs(outputdir+"/reweighting_eta.png")
c_w1.SaveAs(outputdir+"/reweighting_eta.pdf")

# Save the canvas with the ratio histogram to a ROOT file                                                                       
outfile = TFile("f_eta_reweighting.root", "RECREATE")
h_ratio_eta.Write()

# Close the output file                                                                                                     
outfile.Close()
