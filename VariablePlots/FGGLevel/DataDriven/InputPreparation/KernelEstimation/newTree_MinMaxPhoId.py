from ROOT import *
from array import array

import argparse
import sys
import os

#gROOT.SetBatch()
#gStyle.SetOptStat(0)
#gStyle.SetOptTitle(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
#argparser.add_argument('--minV', dest='minV', default='-0.9', help='Minimum Value for maxPhoId')
#argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Maximum Value for maxPhoId')

args = argparser.parse_args()
outputdir = args.outdir
#minValue = args.minV
#maxValue = args.maxV

# -------------- #
# Grab data tree #
# -------------- #
#oldfile_gjets = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NEW_BDT_TRAININGS/DefLM_MCBased/gJets/gJets_040_merged.root","READ")
oldfile_gjets = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NEW_BDT_TRAININGS/DefLM_MCBased/gJets/gJets_4080_merged.root","READ")
#oldfile_gjets = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NEW_BDT_TRAININGS/DefLM_MCBased/gJets/gJets_all_merged.root","READ")

newfile = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NEW_BDT_TRAININGS/DefLM_MCBased/gJets/gJets_4080_merged_MinMaxPhoId.root","recreate")
newfile.ls()
newfile.mkdir("tagsDumper")
tagsDumper.cd()
tagsDumper.mkdir("trees")
trees.cd()

oldtree_gjets = oldfile_gjets.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
nentries = oldtree_gjets.GetEntries()

dipho_leadIDMVA = array('f',[0.])
dipho_subleadIDMVA = array('f',[0.])
dipho_minIDMVA = array('f',[0.])
dipho_maxIDMVA = array('f',[0.])
#weight = array('f',[0.])
#event = array('I',[0])
oldtree_gjets.SetBranchAddress("dipho_leadIDMVA",dipho_leadIDMVA)
oldtree_gjets.SetBranchAddress("dipho_subleadIDMVA",dipho_subleadIDMVA)

# Create new branches in the newtree_gjets and link them to the new variables
newtree_gjets = oldtree_gjets.CloneTree(0)
newtree_gjets.Branch("dipho_minIDMVA", dipho_minIDMVA, "dipho_minIDMVA/F")
newtree_gjets.Branch("dipho_maxIDMVA", dipho_maxIDMVA, "dipho_maxIDMVA/F")
  
for i in range(nentries):
    if (i%1000==0): print i,nentries
    oldtree_gjets.GetEntry(i)
    
    dipho_leadIDMVA[0] = dipho_leadIDMVA[0]
    dipho_subleadIDMVA[0] = dipho_subleadIDMVA[0]
    dipho_minIDMVA[0] = min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])
    dipho_maxIDMVA[0] = max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])

    #print "minID is = \t", min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])
    #print "maxID is = \t", max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])
    
    newtree_gjets.Fill()
    newtree_gjets.AutoSave()

print "----------------------------------------------------"
print "@@@@@ Total number of entries in oldtree is = ",oldtree_gjets.GetEntries()
print "@@@@@ Total number of entries in newtree is = ",newtree_gjets.GetEntries()
print "----------------------------------------------------"
newtree_gjets.Print()

del oldfile_gjets
del newfile
