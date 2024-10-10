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
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb/sb_all2018Data_Mar2024_plusSigmaEOEPt.root","READ")     
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")                                    
norm_dipho = 5.07071342                                                                                                          
norm_sb = (5.07071342*0.02190371141)

# Get trees and create histograms for data                                                                           
# ----------------------------------------                                                                                             
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

# ------------------------ #
# Eta REWEIGHTING  #
# ------------------------ #
h_eta_sba0 = TH1F("h_eta_sba0", "h_eta_sba0", 60, -3.0, 3.0)

# Reweighting function
# --------------------
def reweighting(inputFile_weights, rootFile_weights, sb_treeName, var):
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
        if (debug):
            print("Warning: Value of bin number not found in the histogram. Default weight of 1 will be used.")
        input_file.Close()
        return 1.  # Default weight is 1 if the value is not found

    w = weight_histogram.GetBinContent(bin_number)

    # Close the input file
    input_file.Close()

    return w


# Create a new file to save the modified tree
# -------------------------------------------
new_file = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb/sb_data2018_plusSigmaEOEPtEta.root", "RECREATE")
tagsDumper = new_file.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

# Clone the original tree
# -----------------------
from array import array

weight_eta = array('f',[0.])
new_tree = sb0.CloneTree(0)  # 0 indicates to clone the structure only

# Create a new branch in the new tree
# -----------------------------------
new_tree.Branch("weight_eta", weight_eta, "weight_eta/F")

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 1000): break
    c_sb0 += 1
    if (ev_sb0.CMS_hgg_mass > 75): continue
    #print("-------------------------------------------- EVENT ", c_sb0)
    #print ("ORIGINAL SB WEIGHT = ", weight[0])
    #if (not(c_sb0%20==0)): continue
    w_eta = 1

    if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA):
        h_eta_sba0.Fill(ev_sb0.dipho_leadEta, ev_sb0.weight*ev_sb0.weight_sigmaEOE*ev_sb0.weight_ptOverM*0.82)
        w_eta = reweighting("./f_eta_reweighting.root", "h_ratio_eta", "sb0", ev_sb0.dipho_leadEta)
        weight_eta[0] = 1.*w_eta

    elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA):
        h_eta_sba0.Fill(ev_sb0.dipho_subleadEta, ev_sb0.weight*ev_sb0.weight_sigmaEOE*ev_sb0.weight_ptOverM*0.82)
        w_eta = reweighting("./f_eta_reweighting.root", "h_ratio_eta", "sb0", ev_sb0.dipho_subleadEta)
        weight_eta[0] = 1.*w_eta
    new_tree.Fill()

print("h_eta_sba0 Integral = ", h_eta_sba0.Integral())

# Save the new tree to the new file
# ---------------------------------
trees.cd() 
new_tree.Write()

# Close the files
# ---------------
new_file.Close()
