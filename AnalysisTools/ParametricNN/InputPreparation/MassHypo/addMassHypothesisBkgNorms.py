import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain, THStack, gStyle, TPad, TLegend
import ROOT, array, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList, kYellow, kOrange, kBlue, kBlack
from collections import OrderedDict
import argparse
import sys
import os
from array import array

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
para = TFile("output_ParaDDFullNorms.root","READ")

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
    dat0.Draw(variable + ">>h_" + variable + "_dat0", "weight*weight_allDD*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")     
    mgg0.Draw(variable + ">>h_" + variable + "_mgg0", "weight*weight_allDD*dipho_hypnorm_near*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")

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


sb_integrals =[]
dipho_integrals =[]
sig_integrals =[]
    
# Print total integral for each histogram
for variable in var_list:
    print(f"\nTotal integrals for {variable}:")
    
    dat0_integral = histo_dat0_list[variable + "_dat0"].Integral()
    mgg0_integral = histo_mgg0_list[variable + "_mgg0"].Integral()
    sig0_integral = histo_sig0_list[variable + "_sig0"].Integral()
    
    print(f"Integral of dat0: {dat0_integral}")
    print(f"Integral of mgg0: {mgg0_integral}")
    print(f"Integral of sig0: {sig0_integral}")

# Print integrals in each bin for mgg0, dat0, and sig0 histograms
for variable in var_list:
    print(f"\nBin-by-bin integrals for {variable}:")
    
    nbins = histo_dat0_list[variable + "_dat0"].GetNbinsX()
    
    print("\nIntegrals for dat0:")
    for i in range(1, nbins + 1):  # Loop over bins (1 to nbins)
        bin_content = histo_dat0_list[variable + '_dat0'].GetBinContent(i)
        #print(f"Bin {i}: {histo_dat0_list[variable + '_dat0'].GetBinContent(i)}")
        if bin_content > 0:
            sb_integrals.append(bin_content)     

    print("\nIntegrals for mgg0:")
    for i in range(1, nbins + 1):
        bin_content = histo_mgg0_list[variable + '_mgg0'].GetBinContent(i)
        #print(f"Bin {i}: {histo_mgg0_list[variable + '_mgg0'].GetBinContent(i)}")
        if bin_content > 0:
            dipho_integrals.append(bin_content)     
        
    print("\nIntegrals for sig0:")
    for i in range(1, nbins + 1):
        bin_content = histo_sig0_list[variable + '_sig0'].GetBinContent(i)
        #print(f"Bin {i}: {histo_sig0_list[variable + '_sig0'].GetBinContent(i)}")
        if bin_content > 0:
            sig_integrals.append(bin_content)     

print("sb_integrals = ", sb_integrals)
print("dipho_integrals = ", dipho_integrals)
print("sig_integrals = ", sig_integrals)


# Define lists to hold scale factors
sf_sb = []
sf_dipho = []

# Initialize variables to compute average ratios
current_ratios_sb = []
current_ratios_dipho = []

# Calculate current ratios and their averages
for sb, dipho, sig in zip(sb_integrals, dipho_integrals, sig_integrals):
    
    # Calculate current ratios
    current_ratio_sb = sb / sig if sig != 0 else 0
    current_ratio_dipho = dipho / sig if sig != 0 else 0
    
    current_ratios_sb.append(current_ratio_sb)
    current_ratios_dipho.append(current_ratio_dipho)

# Calculate the average ratios
average_ratio_sb = sum(current_ratios_sb) / len(current_ratios_sb) if current_ratios_sb else 0
average_ratio_dipho = sum(current_ratios_dipho) / len(current_ratios_dipho) if current_ratios_dipho else 0

# Calculate scale factors based on average ratios
#for sb, dipho, sig in zip(sb_integrals, dipho_integrals, sig_integrals):
#    sig = sb + dipho  
    
    # Scale factors based on the average ratios
    # -----------------------------------------
    #scale_factor_sb = average_ratio_sb / (sb / sig) if sb != 0 else 0
    #scale_factor_dipho = average_ratio_dipho / (dipho / sig) if dipho != 0 else 0
    #sf_sb.append(scale_factor_sb)
    #sf_dipho.append(scale_factor_dipho)

import numpy as np
# Define the fraction for mgg from 0.7 to 0.47 (9 points)
frac_mgg_values = np.linspace(0.07, 0.47, 9)
print(frac_mgg_values)

# Calculate scale factors based on average ratios in two separate mass ranges 
for i, (sb, dipho, sig) in enumerate(zip(sb_integrals, dipho_integrals, sig_integrals)):
    sig = sb + dipho  

    # Get the current frac_mgg value for this iteration
    frac_mgg = frac_mgg_values[i % len(frac_mgg_values)]  # Use modulo to cycle through the values
    
    scale_factor_dipho = frac_mgg / (dipho / sig) if dipho != 0 else 0
    scale_factor_sb = (1-frac_mgg) / (sb / sig) if sb != 0 else 0

    # Append scale factors to lists
    sf_sb.append(scale_factor_sb)
    sf_dipho.append(scale_factor_dipho)
    

# Apply scale factors to sb and dipho
# -----------------------------------
scaled_sb = [sb * sf for sb, sf in zip(sb_integrals, sf_sb)]
scaled_dipho = [dipho * sf for dipho, sf in zip(dipho_integrals, sf_dipho)]

# Output results
print("-----------------------------------------")
print("Current ratios (sb):", current_ratios_sb)
print("Current ratios (dipho):", current_ratios_dipho)
print("-----------------------------------------")
print("Scale Factors for sb_integrals:", sf_sb)
print("Scale Factors for dipho_integrals:", sf_dipho)
print("-----------------------------------------")
print("Scaled sb_integrals:", scaled_sb)
print("Scaled dipho_integrals:", scaled_dipho)


# Update sideband and diphoton trees
# ----------------------------------
treelist = ["mgg_bkg","Data"]
  
oldfile = TFile("output_ParaDDFullNorms.root", "read")
newfile = TFile("output_ParaDDFullBkgNorms.root","recreate")
tagsDumper = newfile.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")
trees.cd()

for idx,j in enumerate(treelist):
  print("-----------------------------")
  print("-----------", j, "----------")
  print("-----------------------------")
  oldtree = oldfile.Get("tagsDumper/trees/"+j+"_13TeV_UntaggedTag_0")
  nentries = oldtree.GetEntries()
    
  dipho_masshyp_near = array('i',[0])
  oldtree.SetBranchAddress("dipho_masshyp_near",dipho_masshyp_near)
  newtree = oldtree.CloneTree(0)
  #branches needed: dipho_hypSigBkgNorm_near with and without wsig for signal
  dipho_hypSigBkgNorm_near = array('f',[0])
  newtree.Branch('dipho_hypSigBkgNorm_near', dipho_hypSigBkgNorm_near, 'dipho_hypSigBkgNorm_near/F')
  newtree.SetBranchAddress("dipho_hypSigBkgNorm_near",dipho_hypSigBkgNorm_near)
  dipho_hypSigBkgNorm_near_nowsig = array('f',[0])
  newtree.Branch('dipho_hypSigBkgNorm_near_nowsig', dipho_hypSigBkgNorm_near_nowsig, 'dipho_hypSigBkgNorm_near_nowsig/F')
  newtree.SetBranchAddress("dipho_hypSigBkgNorm_near_nowsig",dipho_hypSigBkgNorm_near_nowsig)

  for i in range(nentries):
      if (i%5000==0): print(i,nentries)
      oldtree.GetEntry(i)
      if (j=="Data"):
          #conditions for each normalization value 
          if(dipho_masshyp_near[0]==10):
              dipho_hypSigBkgNorm_near[0] = sf_sb[0]
          if(dipho_masshyp_near[0]==15):
              dipho_hypSigBkgNorm_near[0] = sf_sb[1]
          if(dipho_masshyp_near[0]==20):
              dipho_hypSigBkgNorm_near[0] = sf_sb[2]
          if(dipho_masshyp_near[0]==30):
              dipho_hypSigBkgNorm_near[0] = sf_sb[3]
         #if(dipho_masshyp_near[0]==35):
            #  dipho_hypSigBkgNorm_near[0] = sf_sb5]
          if(dipho_masshyp_near[0]==40):
              dipho_hypSigBkgNorm_near[0] = sf_sb[4]
          #if(dipho_masshyp_near[0]==45):
          #  dipho_hypSigBkgNorm_near[0] = sf_sb[7]
          if(dipho_masshyp_near[0]==50):
              dipho_hypSigBkgNorm_near[0] = sf_sb[5]
          if(dipho_masshyp_near[0]==55):
              dipho_hypSigBkgNorm_near[0] = sf_sb[6]
          if(dipho_masshyp_near[0]==60):
              dipho_hypSigBkgNorm_near[0] = sf_sb[7]
          #if(dipho_masshyp_near[0]==65):
          #  dipho_hypSigBkgNorm_near[0] = sf_sb[11]
          if(dipho_masshyp_near[0]==70):
              dipho_hypSigBkgNorm_near[0] = sf_sb[8]
              
          if (i%10000==0): print(dipho_masshyp_near[0])
          if (i%10000==0): print(dipho_hypSigBkgNorm_near[0])
          newtree.Fill()

      elif (j=="mgg_bkg"):
        #conditions for each normalization value
        if(dipho_masshyp_near[0]==10):
          dipho_hypSigBkgNorm_near[0] = sf_dipho[0]
        if(dipho_masshyp_near[0]==15):
          dipho_hypSigBkgNorm_near[0] = sf_dipho[1]
        if(dipho_masshyp_near[0]==20):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[2]
        #if(dipho_masshyp_near[0]==25):
            #  dipho_hypSigBkgNorm_near[0] = sf_dipho[3]
        if(dipho_masshyp_near[0]==30):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[3]
        #if(dipho_masshyp_near[0]==35):
        #  dipho_hypSigBkgNorm_near[0] = sf_dipho[5]
        if(dipho_masshyp_near[0]==40):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[4]
        #if(dipho_masshyp_near[0]==45):
        #  dipho_hypSigBkgNorm_near[0] = sf_dipho[7]
        if(dipho_masshyp_near[0]==50):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[5]
        if(dipho_masshyp_near[0]==55):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[6]
        if(dipho_masshyp_near[0]==60):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[7]
        #if(dipho_masshyp_near[0]==65):
        #  dipho_hypSigBkgNorm_near[0] = sf_dipho[11]
        if(dipho_masshyp_near[0]==70):
            dipho_hypSigBkgNorm_near[0] = sf_dipho[8]

        if (i%10000==0): print(dipho_masshyp_near[0])
        if (i%10000==0): print(dipho_hypSigBkgNorm_near[0])
        newtree.Fill()
newtree.AutoSave()

del oldfile
del newfile
