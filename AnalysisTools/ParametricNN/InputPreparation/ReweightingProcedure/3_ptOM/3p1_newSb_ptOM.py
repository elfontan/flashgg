# ------------------------------------------------------- #
# Use this script within an environment allowing python3: #
# otherwise problems related to the usage of array might  #
# happen                                                  #
# ------------------------------------------------------- #
from ROOT import * 
from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain
import random, copy
import ROOT, array, CMSGraphics, CMS_lumi
import argparse
import sys
import os

gROOT.SetBatch()
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

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

debug = False

# Obtain histogram files
# ----------------------
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ")
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb/sb_data2018_plusSigmaEOE.root","READ")  
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")

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
    if not weight_histogram or not isinstance(weight_histogram, TH2):
        print("Error: Unable to retrieve the weight histogram.")
        return
    # Get the weight from the histogram                                                                    
    bin_number_x = weight_histogram.GetXaxis().FindBin(varX)
    bin_number_y = weight_histogram.GetYaxis().FindBin(varY)
    if bin_number_x < 1 or bin_number_x > weight_histogram.GetNbinsX():
        if (debug):
            print("Warning: Value of bin number not found in the histogram. Default weight of 1 will be used.")
        input_file.Close()
        return 1.  # Default weight is 1 if the value is not found                                                                                                    
    if bin_number_y < 1 or bin_number_y > weight_histogram.GetNbinsY():
        if (debug):
            print("Warning: Value of bin number not found in the histogram. Default weight of 1 will be used.")
        input_file.Close()
        return 1.  # Default weight is 1 if the value is not found                                                                                                   

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
# PtToM REWEIGHTING  #
# ------------------ #
from array import array                                                                
xbins = [0.275]                                                                            
while (xbins[-1]<9):                                                                               
    xbins.append(1.1*xbins[-1])
#while (xbins[-1]<6):                                                                               
#    xbins.append(1.06*xbins[-1])
h_ptToM_min_sba0 = TH1F("h_ptToM_min_sba0", "h_ptToM_min_sba0", len(xbins)-1,array('f',xbins))
h_ptToM_max_sba0 = TH1F("h_ptToM_max_sba0", "h_ptToM_max_sba0", len(xbins)-1,array('f',xbins))


# Get trees and create histograms for data
# ----------------------------------------
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

# Create a new file to save the modified tree
# -------------------------------------------
new_file = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb//sb_all2018Data_Mar2024_plusSigmaEOEPt.root", "RECREATE")
tagsDumper = new_file.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

# Clone the original tree
# -----------------------
from array import array

weight_ptOverM = array('f',[0.])
new_tree = sb0.CloneTree(0)  # 0 indicates to clone the structure only

# Create a new branch in the new tree
# -----------------------------------
new_tree.Branch("weight_ptOverM", weight_ptOverM, "weight_ptOverM/F")

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 1000): break
    if (ev_sb0.CMS_hgg_mass > 75): continue
    c_sb0 += 1
    #print("-------------------------------------------- EVENT ", c_sb0)
    #if (not(c_sb0%20==0)): continue
    w_ptOverM = 1.
    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        #print("w_ptOverM sublead PRE = ", w_ptOverM)
        #w_ptOverM = reweighting("f_ptOverM_reweighting.root", "h_ratio_ptToM", "sb0", ev_sb0.dipho_lead_ptoM, ev_sb0.dipho_sublead_ptoM)
        w_ptOverM = reweighting("f_ptOverM_reweighting_max9.root", "h_ratio_ptToM", "sb0", ev_sb0.dipho_lead_ptoM, ev_sb0.dipho_sublead_ptoM)
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE*w_ptOverM*0.82)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE*w_ptOverM*0.82)
        weight_ptOverM[0] = 1.*w_ptOverM
        #print("w_ptOverM sublead POST = ", w_ptOverM)

    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA and min(ev_sb0.dipho_leadIDMVA, ev_sb0.dipho_subleadIDMVA)>-0.7):
        #print("w_ptOverM sublead PRE = ", w_ptOverM)
        #w_ptOverM = reweighting("f_ptOverM_reweighting.root", "h_ratio_ptToM", "sb0", ev_sb0.dipho_sublead_ptoM, ev_sb0.dipho_lead_ptoM)
        w_ptOverM = reweighting("f_ptOverM_reweighting_max9.root", "h_ratio_ptToM", "sb0", ev_sb0.dipho_sublead_ptoM, ev_sb0.dipho_lead_ptoM)
        fill_histograms(h_ptToM_min_sba0, ev_sb0.dipho_sublead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE*w_ptOverM*0.82)
        fill_histograms(h_ptToM_max_sba0, ev_sb0.dipho_lead_ptoM, ev_sb0.weight*ev_sb0.weight_sigmaEOE*w_ptOverM*0.82)
        weight_ptOverM[0] = 1.*w_ptOverM
        #print("w_ptOverM sublead POST = ", w_ptOverM)

    new_tree.Fill()

print("h_ptToM_min_sba0 Integral = ", h_ptToM_min_sba0.Integral())
print("h_ptToM_max_sba0 Integral = ", h_ptToM_max_sba0.Integral())

# Save the new tree to the new file
# ---------------------------------
trees.cd()  # Change to the correct directory
new_tree.Write()

# Close the files
# ---------------
new_file.Close()
