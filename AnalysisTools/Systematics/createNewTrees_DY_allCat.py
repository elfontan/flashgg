# ------------------------------------------------------ #
# Use this script within an environment allowing python: #
# ------------------------------------------------------ #
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
argparser.add_argument('--d', dest='d', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/Syst/SigMC_NTUPLES/', help='Input and Output Files directory')
argparser.add_argument('--m', dest='m', default='70', help='Mass hypothesis')

args = argparser.parse_args()
dir  = args.d
mass = args.m

filelist = [ 
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/dyJets2018_zeeVal_withSyst.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/dyJets2018_zeeVal_withSyst.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/dyJets2018_zeeVal_withSyst.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/dyJets2018_zeeVal_withSyst.root",
    "/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/ZeeVal/dyJets2018_zeeVal_withSyst.root",
]

tree_names_sig = [
    "DYToLL_13TeV_UntaggedTag_0",
    "DYToLL_13TeV_UntaggedTag_0_MvaShiftDown01sigma",
    "DYToLL_13TeV_UntaggedTag_0_MvaShiftUp01sigma",
    "DYToLL_13TeV_UntaggedTag_0_SigmaEOverEShiftDown01sigma",
    "DYToLL_13TeV_UntaggedTag_0_SigmaEOverEShiftUp01sigma"
]

cat = ["0","1","2","3","4","all"]

# Generate the proper list of tree names for each category
# --------------------------------------------------------
tree_names_sig_lists = [
    [name.replace("_0", f"_{cat_value}") for name in tree_names_sig]
    for cat_value in cat
]
for c, tree_names in enumerate(tree_names_sig_lists):
    print(f"List {c + 1} (cat value {cat[c]}):")
    for name in tree_names:
        print(name)
    print("\n")

    
idx = 0
for filename in filelist:

    # Open the ROOT file
    # ------------------
    file = ROOT.TFile.Open(filename)

    # Create a new file to save the modified tree                                                                        
    # -------------------------------------------                                            
    newfile = TFile("ZeeVal_DY_" + tree_names_sig_lists[5][idx]+".root", "RECREATE")
    print("--------------------------------------------------")
    print("OUTPUTFile: ", newfile)
    tagsDumper = newfile.mkdir("tagsDumper")                                                                      
    tagsDumper.cd()                                                                                                                   
    trees = tagsDumper.mkdir("trees")
    
    # Get the tree
    # ------------
    tree = file.Get("tagsDumper/trees/"+tree_names_sig_lists[0][idx])
    print("INPUTFile: ", file)
    print("TREE: ", tree)
    
    # Create two new trees for passing and failing NNScore
    tree_cat0 = tree.CloneTree(0)
    tree_cat1 = tree.CloneTree(0)
    tree_cat2 = tree.CloneTree(0)
    tree_cat3 = tree.CloneTree(0)
    tree_cat4 = tree.CloneTree(0)
    
    tree_cat0.SetName(tree_names_sig_lists[0][idx])
    tree_cat0.SetTitle(tree_names_sig_lists[0][idx])
    tree_cat1.SetName(tree_names_sig_lists[1][idx])
    tree_cat1.SetTitle(tree_names_sig_lists[1][idx])
    tree_cat2.SetName(tree_names_sig_lists[2][idx])
    tree_cat2.SetTitle(tree_names_sig_lists[2][idx])
    tree_cat3.SetName(tree_names_sig_lists[3][idx])
    tree_cat3.SetTitle(tree_names_sig_lists[3][idx])
    tree_cat4.SetName(tree_names_sig_lists[4][idx])
    tree_cat4.SetTitle(tree_names_sig_lists[4][idx])
    
    # Loop over entries in the original tree
    # --------------------------------------
    for event in tree:
        if (event.NNScore >= 0.8): 
            tree_cat0.Fill()
        elif (event.NNScore >= 0.6 and event.NNScore < 0.8): 
            tree_cat1.Fill()
        elif (event.NNScore >= 0.45 and event.NNScore < 0.6): 
            tree_cat2.Fill()
        elif (event.NNScore >= 0.3 and event.NNScore < 0.45): 
            tree_cat3.Fill()
        else:
            tree_cat4.Fill()
            
    trees.cd()
    #tree_cat1.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_1")
    tree_cat0.Write(tree_names_sig_lists[0][idx])
    tree_cat1.Write(tree_names_sig_lists[1][idx])
    tree_cat2.Write(tree_names_sig_lists[2][idx])
    tree_cat3.Write(tree_names_sig_lists[3][idx])
    tree_cat4.Write(tree_names_sig_lists[4][idx])
    
    idx += 1
    # Close the input file
    newfile.Close()
        
