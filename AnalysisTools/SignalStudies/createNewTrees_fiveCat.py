# ------------------------------------------------------- #
# Very low mass diphoton analysis: Categorization (sigMC) #
# ------------------------------------------------------- #
# Use this script within an environment allowing python3: #
# otherwise problems related to the usage of array might  #
# happen                                                  #
# ------------------------------------------------------- #
# python3 createNewTrees_fiveCat.py --outdir /eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat_evaluateAt70GeV/AlternativeCategorization/ --pnn nearest_flat_evaluateAt70GeV

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
argparser.add_argument('--pnn', dest='pnn', default='nearest_flat_evaluateAt70GeV', help='Considered scenario for PNN evaluation')

args = argparser.parse_args()
outputdir = args.outdir
scenario = args.pnn

filelist = [ #/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/Syst/SigMC_NTUPLES/gghSig_Systematics
    #"/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/Syst/out_ggh_70_13TeV_UntaggedTag_0.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M10_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M15_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M20_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M25_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M30_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M35_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M40_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M45_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M50_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M55_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M60_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M65_newSamplesFlat.root",
    "/eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_ggH_M70_newSamplesFlat.root"
]

mass_list = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

# MVA scores extracted from third order polynomial function to interpolate the NN score values providing highest approx Asimov significance
#mvaScore = [0.93613186, 0.8814945, 0.8531928, 0.84612887, 0.85520479, 0.87532267, 0.90138461, 0.9282927, 0.95094905, 0.96425574, 0.96311488, 0.94242857, 0.8970989 ] 

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
    newfile = TFile(outputdir + "ggH_M"+str(mass_list[idx])+"_cat.root", "RECREATE")
    tagsDumper = newfile.mkdir("tagsDumper")
    tagsDumper.cd()
    trees = tagsDumper.mkdir("trees")

    # Create two new trees for passing and failing NNScore
    tree_cat0 = tree.CloneTree(0)
    tree_cat1 = tree.CloneTree(0)
    tree_cat2 = tree.CloneTree(0)
    tree_cat3 = tree.CloneTree(0)
    tree_cat4 = tree.CloneTree(0)
    tree_cat0.SetName("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_0")
    tree_cat1.SetName("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_1")
    tree_cat2.SetName("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_2")
    tree_cat3.SetName("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_3")
    tree_cat4.SetName("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_4")

    tree_cat0.SetTitle("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_0")
    tree_cat1.SetTitle("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_1")
    tree_cat2.SetTitle("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_2")
    tree_cat3.SetTitle("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_3")
    tree_cat4.SetTitle("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_4")

    #print("mvaScore for ", str(mass_list[idx]), " GeV  mass point = ", str(mvaScore[idx]))

    # Loop over entries in the original tree
    for event in tree:
        # Check the NNScore and fill the corresponding tree
        #if event.NNScore >= mvaScore[idx]: 
        if (event.NNScore >= 0.9): 
            tree_cat0.Fill()
        elif (event.NNScore >= 0.8 and event.NNScore < 0.9): 
            tree_cat1.Fill()
        elif (event.NNScore >= 0.6 and event.NNScore < 0.8): 
            tree_cat2.Fill()
        elif (event.NNScore >= 0.5 and event.NNScore < 0.6): 
            tree_cat3.Fill()
        else:
            tree_cat4.Fill()

    trees.cd()
    tree_cat0.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_0")
    tree_cat1.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_1")
    tree_cat2.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_2")
    tree_cat3.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_3")
    tree_cat4.Write("ggh_"+str(mass_list[idx])+"_13TeV_UntaggedTag_4")

    idx += 1

    # Close the input file
    newfile.Close()
