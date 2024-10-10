# ------------------------------------------------------- #
# Use this script within an environment allowing python3: #
# otherwise problems related to the usage of array might  #
# happen                                                  #
# ------------------------------------------------------- #
#from ROOT import * 
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
argparser.add_argument('--outdir', dest='outdir', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/Categories/', help='Output dir')

args = argparser.parse_args()
outputdir = args.outdir

filelist = [
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_all2018Data_bkg_newSamplesFlat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_sbData_bkg_newSamplesFlat.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_dipho_bkg_newSamplesFlat.root"
]

treename = ['Data_13TeV_UntaggedTag_', 'Data_13TeV_UntaggedTag_', 'mgg_bkg_13TeV_UntaggedTag_',]
newFileName = ['all2018data.root', 'sb2018data.root', 'diphoMC.root',]

# MVA scores corresponding to the highest approximate Asimov significance
#mvaScore = [0.966, 0.807, 0.929, 0.8, 0.877, 0.836, 0.909, 0.981, 0.939, 0.987, 0.916, 0.926, 0.922]

idx = 0
for filename in filelist:
    # Open the ROOT file
    # ------------------
    file = ROOT.TFile.Open(filename)

    # Get the tree
    # ------------
    tree = file.Get("tagsDumper/trees/"+treename[idx]+"0")

    # Create a new file to save the modified tree
    # -------------------------------------------
    newfile = TFile(outputdir + "/" + newFileName[idx], "RECREATE")
    tagsDumper = newfile.mkdir("tagsDumper")
    tagsDumper.cd()
    trees = tagsDumper.mkdir("trees")

    # Create two new trees for passing and failing NNScore
    tree_cat0 = tree.CloneTree(0)
    tree_cat1 = tree.CloneTree(0)
    tree_cat2 = tree.CloneTree(0)
    tree_cat3 = tree.CloneTree(0)

    # Loop over entries in the original tree
    for event in tree:
        if (event.NNScore >= 0.8):                                                                                             
            tree_cat0.Fill()                                                                                                          
        elif (event.NNScore >= 0.6 and event.NNScore < 0.8):                                                                  
            tree_cat1.Fill()                                                                                                   
        elif (event.NNScore >= 0.5 and event.NNScore < 0.6):                                                                
            tree_cat2.Fill()                                                                                                
        else:                                                                      
            tree_cat3.Fill()

    trees.cd()
    tree_cat0.Write(treename[idx]+"0")
    tree_cat1.Write(treename[idx]+"1")
    tree_cat2.Write(treename[idx]+"2")
    tree_cat3.Write(treename[idx]+"3")

    idx += 1

    # Close the input file
    newfile.Close()
