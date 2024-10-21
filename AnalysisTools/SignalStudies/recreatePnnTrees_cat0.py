# ------------------------------------------------------------ #
# Very low mass diphoton analysis: Recreate trees with NNScore #
# ------------------------------------------------------------ #
# Use this script within an environment allowing python3:      #
# otherwise problems related to the usage of array might       #
# happen                                                       #
# ------------------------------------------------------------ #
# NOTE: After the migration of the PNN training code to Keras 3, the output files are incompatible with previous scripts... #
# This script is a turn-around to recreate the file in a readible way for our ROC curve and Asimov Significance studies.    #
# ---------------------------------------------------------------------------------------------------------------------------

# python3 recreatePnnTrees_cat0.py --outdir /eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/v2_nearest_flat_gradualDiphoIncrease/ --pnn nearest_flat_gradualDiphoIncrease

from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain
import random, copy
import ROOT, array, CMSGraphics, CMS_lumi
import argparse
import sys
import os

gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/nearest_flat_plusFlatBkg/Categorization/', help='Output dir')
argparser.add_argument('--pnn', dest='pnn', default='nearest_flat_plusFlatBkg', help='Considered scenario for PNN evaluation')

args = argparser.parse_args()
outputdir = args.outdir
scenario = args.pnn

data_fileName = "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_all2018Data_bkg_newSamplesFlat.root"
data_file = ROOT.TFile.Open(data_fileName)
data_tree = data_file.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

filelist = [ 
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M10_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M15_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M20_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M25_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M30_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M35_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M40_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M45_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M50_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M55_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M60_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M65_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2024/"+scenario+"/out_ggH_M70_newSamplesFlat.root"
]

mass_list = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]


idx = 0
for filename in filelist:
    # Open the ROOT file
    # ------------------
    file = ROOT.TFile.Open(filename)

    # Get the tree
    # ------------
    tree = file.Get("tagsDumper/trees/ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_0")

    # Create a new file to save the modified tree
    # -------------------------------------------
    newfile = TFile(outputdir + "out_ggH_M"+str(mass_list[idx])+".root", "RECREATE")
    tagsDumper = newfile.mkdir("tagsDumper")
    tagsDumper.cd()
    trees = tagsDumper.mkdir("trees")

    # Create two new trees for passing and failing NNScore
    tree_cat0 = tree.CloneTree(0)

    # Loop over entries in the original tree
    for event in tree:
        if (event.NNScore >= 0.0): 
            tree_cat0.Fill()

    trees.cd()
    tree_cat0.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_0")

    idx += 1

    # Close the input file
    newfile.Close()


new_data_file = TFile(outputdir + "out_all2018Data_bkg.root", "RECREATE")
tagsDumper = new_data_file.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")

data_tree_cat0 = data_tree.CloneTree(0)

for event in data_tree:
    if (event.NNScore >= 0.0): 
        data_tree_cat0.Fill()

trees.cd()
data_tree_cat0.Write("Data_13TeV_UntaggedTag_0")
new_data_file.Close()
