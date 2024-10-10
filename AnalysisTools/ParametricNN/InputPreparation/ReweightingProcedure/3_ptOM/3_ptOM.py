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
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log

# Obtain histogram files
# ----------------------
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ") 
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb/sb_data2018_plusSigmaEOE.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")

# Get trees and create histograms for data                                                                                    
# ----------------------------------------                                                                           
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

norm_dipho = 5.07071342                                                      
norm_sb = (5.07071342*0.02190371141)  

# Reweighting function                                                                                        
# --------------------                                                                               
def reweighting(inputFile_weights, rootFile_weights, sb_treeName, varX, varY):
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
    # Get the weight from the histogram                                                             
    bin_number_x = weight_histogram.GetXaxis().FindBin(varX)
    bin_number_y = weight_histogram.GetYaxis().FindBin(varY)
    w = weight_histogram.GetBinContent(bin_number_x, bin_number_y)

    # Close the input file                                                                       
    input_file.Close()

    return w

def fill_histograms(histogram, value, weight=1):
    n_bins = histogram.GetNbinsX()
    last_bin_content = histogram.GetBinContent(n_bins)
    last_bin_error = histogram.GetBinError(n_bins)

    if value > histogram.GetXaxis().GetXmax():
        histogram.Fill(histogram.GetXaxis().GetXmax(), weight)
        histogram.SetBinError(n_bins, TMath.Sqrt(last_bin_error ** 2 + weight))
    else:
        histogram.Fill(value, weight)

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

# ------------------ #
# REWEIGHTING: PtToM #
# ------------------ #
from array import array
xbins = [0.275]
while (xbins[-1]<9):
    xbins.append(1.1*xbins[-1])
#while (xbins[-1]<6):
#    xbins.append(1.06*xbins[-1])
#from array import array
#xbins = [0.283]
#while (xbins[-1]<7):
#    xbins.append(1.09*xbins[-1])
#print(xbins)
h_ptToM_min_sba0 = TH1F("h_ptToM_min_sba0", "h_ptToM_min_sba0", len(xbins)-1,array('f',xbins))
h_ptToM_min_pre0 = TH1F("h_ptToM_min_pre0", "h_ptToM_min_pre0", len(xbins)-1,array('f',xbins))
h_ptToM_min_mgg0 = TH1F("h_ptToM_min_mgg0", "h_ptToM_min_mgg0", len(xbins)-1,array('f',xbins))
h_ptToM_max_sba0 = TH1F("h_ptToM_max_sba0", "h_ptToM_max_sba0", len(xbins)-1,array('f',xbins))
h_ptToM_max_pre0 = TH1F("h_ptToM_max_pre0", "h_ptToM_max_pre0", len(xbins)-1,array('f',xbins))
h_ptToM_max_mgg0 = TH1F("h_ptToM_max_mgg0", "h_ptToM_max_mgg0", len(xbins)-1,array('f',xbins))
h_ptToM_sba0 = TH2F("h_ptToM_sba0", "h_ptToM_sba0", len(xbins)-1,array('f',xbins), len(xbins)-1,array('f',xbins))
h_ptToM_pre0 = TH2F("h_ptToM_pre0", "h_ptToM_pre0", len(xbins)-1,array('f',xbins), len(xbins)-1,array('f',xbins))
h_ptToM_mgg0 = TH2F("h_ptToM_mgg0", "h_ptToM_mgg0", len(xbins)-1,array('f',xbins), len(xbins)-1,array('f',xbins))
#h_ptToM_sba0 = TH2F("h_ptToM_sba0", "h_ptToM_sba0", 80, 0., 4.,  80, 0., 4.)
#h_ptToM_pre0 = TH2F("h_ptToM_pre0", "h_ptToM_pre0", 80, 0., 4.,  80, 0., 4.)
#h_ptToM_mgg0 = TH2F("h_ptToM_mgg0", "h_ptToM_mgg0", 80, 0., 4.,  80, 0., 4.)


print("----------Opening data tree")
c_dat0 = 0
for ev_dat0 in dat0:
    #if (c_dat0 == 10): break
    c_dat0 += 1
    if (not(c_dat0%20==0)): continue
    if (ev_dat0.CMS_hgg_mass > 75): continue
    #if (not(c_dat0%20==0)): continue
    if (ev_dat0.dipho_leadIDMVA <= ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_pre0, ev_dat0.dipho_lead_ptoM, 1.)
        fill_histograms(h_ptToM_max_pre0, ev_dat0.dipho_sublead_ptoM, 1.)
        fill_histograms_2d(h_ptToM_pre0, ev_dat0.dipho_lead_ptoM, ev_dat0.dipho_sublead_ptoM, 1.)
    elif (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_pre0, ev_dat0.dipho_sublead_ptoM, 1.)
        fill_histograms(h_ptToM_max_pre0, ev_dat0.dipho_lead_ptoM, 1.)
        fill_histograms_2d(h_ptToM_pre0, ev_dat0.dipho_sublead_ptoM, ev_dat0.dipho_lead_ptoM, 1.)
print("h_ptToM_pre0 Integral = ", h_ptToM_pre0.Integral())

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 10): break
    c_sb0 += 1
    #if (not(c_sb0%20==0)): continue
    if (ev_sb0.CMS_hgg_mass > 75): continue
    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
        fill_histograms_2d(h_ptToM_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
        fill_histograms_2d(h_ptToM_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
print("h_ptToM_sba0 Integral = ", h_ptToM_sba0.Integral())

print("----------Opening MC dipho tree")
c_mgg0 = 0
for ev_mgg0 in mgg0:
    #if (c_mgg0 == 10): break
    c_mgg0 += 1
    if (ev_mgg0.CMS_hgg_mass > 75): continue
    if (ev_mgg0.CMS_hgg_mass < 10): continue
    if (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight)
        fill_histograms(h_ptToM_max_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight)
        fill_histograms_2d(h_ptToM_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight)
    elif (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        fill_histograms(h_ptToM_min_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.weight)
        fill_histograms(h_ptToM_max_mgg0, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight)
        fill_histograms_2d(h_ptToM_mgg0, ev_mgg0.dipho_sublead_ptoM, ev_mgg0.dipho_lead_ptoM, ev_mgg0.weight)
print("h_ptToM_mgg0 Integral = ", h_ptToM_mgg0.Integral())

h_ptToM_min_mgg0.Scale(norm_dipho*1.68)
h_ptToM_max_mgg0.Scale(norm_dipho*1.68)
h_ptToM_mgg0.Scale(norm_dipho*1.68)
h_ptToM_min_sba0.Scale(norm_sb*0.82)
h_ptToM_max_sba0.Scale(norm_sb*0.82)
h_ptToM_sba0.Scale(norm_sb*0.82)

# Subtract MGG from Data Preselection
h_ptToM_dataPreselMinus_mcDipho = h_ptToM_pre0.Clone("h_ptToM_dataPreselMinus_mcDipho")
print("Pre h_ptToM_dataPreselMinus_mcDipho Integral = ", h_ptToM_dataPreselMinus_mcDipho.Integral())
h_ptToM_dataPreselMinus_mcDipho.Add(h_ptToM_mgg0, -1)
print("Post h_ptToM_dataPreselMinus_mcDipho Integral = ", h_ptToM_dataPreselMinus_mcDipho.Integral())

# Divide the result by  to compute the ratio
h_ratio_ptToM = h_ptToM_dataPreselMinus_mcDipho.Clone("h_ratio_ptToM")
print("Pre h_ratio_ptToM Integral = ", h_ratio_ptToM.Integral())
h_ratio_ptToM.Divide(h_ptToM_sba0)
print("Post h_ratio_ptToM Integral = ", h_ratio_ptToM.Integral())

c_w2 = TCanvas("c_w2","c_w2",1200,800)
c_w2.cd()
c_w2.SetLeftMargin(0.12)                     
c_w2.SetRightMargin(0.15)                     
h_ratio_ptToM.Draw("COLZ")                                       
h_ratio_ptToM.GetXaxis().SetTitle("Min ID MVA #gamma p_{T}/M")
h_ratio_ptToM.GetYaxis().SetTitle("Max ID MVA #gamma p_{T}/M")
h_ratio_ptToM.GetZaxis().SetTitle("(Data presel - MC #gamma#gamma) / SB")
#CMS lumi stuff                                                                                                      
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
#CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"                                                                                           
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_w2, 0, 0)

c_w2.Update()
c_w2.SaveAs(outputdir+"/reweighting_scaledPt_max10_v4.png")
c_w2.SaveAs(outputdir+"/reweighting_scaledPt_max10_v4.pdf")


# Save the canvas with the ratio histogram to a ROOT file
outfile = TFile("f_ptOverM_reweighting_max10_v4.root", "RECREATE")
h_ratio_ptToM.Write()

# Close the output file
outfile.Close()
