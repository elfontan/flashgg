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

treelist = ["ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70"]
  
oldfile = TFile("output_ParaDDFullNorms.root", "read")
newfile = TFile("output_ParaDDFullSigNorms.root","recreate")
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

        #conditions for each normalization value
        if(dipho_masshyp_near[0]==10):
          dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==15):
          dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==20):
            dipho_hypSigBkgNorm_near[0] = 1.
        #if(dipho_masshyp_near[0]==25):
            #  dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==30):
            dipho_hypSigBkgNorm_near[0] = 1.
        #if(dipho_masshyp_near[0]==35):
        #  dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==40):
            dipho_hypSigBkgNorm_near[0] = 1.
        #if(dipho_masshyp_near[0]==45):
        #  dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==50):
            dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==55):
            dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==60):
            dipho_hypSigBkgNorm_near[0] = 1.
        #if(dipho_masshyp_near[0]==65):
        #  dipho_hypSigBkgNorm_near[0] = 1.
        if(dipho_masshyp_near[0]==70):
            dipho_hypSigBkgNorm_near[0] = 1.

        if (i%10000==0): print(dipho_masshyp_near[0])
        if (i%10000==0): print(dipho_hypSigBkgNorm_near[0])
        newtree.Fill()
    newtree.AutoSave()

del oldfile
del newfile
