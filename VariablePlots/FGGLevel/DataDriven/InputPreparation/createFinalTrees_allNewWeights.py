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
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
logScale = args.log

# Obtain histogram files
# ----------------------
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_D.root","READ") #Data with unweighted events, both regions
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/sb_newfile_ptOverMreweighting_overflow_max7_ALL.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")


#####################
# NEW MC Dipho TREE #
#####################

# Create a new file to save the modified tree
# -------------------------------------------
new_file_mgg0 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/mgg0_newfile_final_fullReweighting_allSbEvents.root", "RECREATE")
tagsDumper = new_file_mgg0.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

# Clone the original tree
# -----------------------
from array import array
weight_sigmaEOE = array('f',[0.])
weight_ptOverM = array('f',[0.])
weight_allDD = array('f',[0.])
new_tree_mgg0 = mgg0.CloneTree(0)  # 0 indicates to clone the structure only

# Create a new branch in the new tree
# -----------------------------------
new_tree_mgg0.Branch("weight_sigmaEOE", weight_sigmaEOE, "weight_sigmaEOE/F")
new_tree_mgg0.Branch("weight_ptOverM", weight_ptOverM, "weight_ptOverM/F")
new_tree_mgg0.Branch("weight_allDD", weight_allDD, "weight_allDD/F")

print("----------Opening MC dipho tree")
c_mgg0 = 0
for ev_mgg0 in mgg0:
    c_mgg0 += 1
    #if (c_mgg0 == 1000): break
    weight_sigmaEOE[0] = 1.    
    weight_ptOverM[0] = 1.    
    weight_allDD[0] = (5.9546*weight_sigmaEOE[0]*weight_ptOverM[0])    

    new_tree_mgg0.Fill()

# Save the new tree to the new file
# ---------------------------------
trees.cd() # Change to the correct directory
new_tree_mgg0.Write()

# Close the files
# ---------------
new_file_mgg0.Close()




#####################
# NEW SIDEBAND TREE #
#####################

# Create a new file to save the modified tree
# -------------------------------------------
new_file_sba0 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/sb_newfile_final_fullReweighting_allSbEvents.root", "RECREATE")
tagsDumper = new_file_sba0.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

# Clone the original tree
# -----------------------
weight_allDD = array('f',[0.])
new_tree_sba0 = sb0.CloneTree(0)  # 0 indicates to clone the structure only

# Create a new branch in the new tree
# -----------------------------------
new_tree_sba0.Branch("weight_allDD", weight_allDD, "weight_allDD/F")

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 1000): break
    c_sb0 += 1
    #if (not(c_sb0%20==0)): continue
    weight_allDD[0] = (0.0622*ev_sb0.weight_sigmaEOE*ev_sb0.weight_ptOverM)

    new_tree_sba0.Fill()

# Save the new tree to the new file
# ---------------------------------
trees.cd()  # Change to the correct directory
new_tree_sba0.Write()

# Close the files
# ---------------
new_file_sba0.Close()

#print("----------Opening data tree")
#c_dat0 = 0
#for ev_dat0 in dat0:
#    c_dat0 += 1
#    #if (c_dat0 == 10): break
#    if (not(c_dat0%20==0)): continue
