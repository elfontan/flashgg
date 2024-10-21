# --------------------------------- #
#  Very low mass diphoton analysis  #  
# --------------------------------- #
#  Input preparation for PNN Training: mass hypothesis assignment
#  To run code: no cmsenv, python3

import ROOT, array, random, copy            
from ROOT import TCanvas, TFile, gSystem, TChain
from ROOT import TFile, TTree
from array import array
import numpy as np

#Grab data tree
treelist = ["mgg_bkg","Data","ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70"] #change accordingly
masslist = [10,15,20,30,40,50,55,60,70] #change accordingly
#treelist = ["mgg_bkg","Data","ggh_10","ggh_15","ggh_20","ggh_25","ggh_30","ggh_35","ggh_40","ggh_45","ggh_50","ggh_55","ggh_60","ggh_65","ggh_70"] #change accordingly
#masslist = [10,15,20,25,30,35,40,45,50,55,60,65,70] #change accordingly
#treelist = ["mgg_bkg","Data","ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70"] #change accordingly
#masslist = [10,15,20,30,40,50,55,60,70] #change accordingly

oldfile = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/output_DDFull_AllSigNoNNLOPS_Oct2024.root","READ")
newfile = TFile("output_ParaDDFull.root","RECREATE")
tagsDumper = newfile.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")
trees.cd()

for j in treelist:
  print("---------------------------")
  print("-------- ", j, " --------")
  print("---------------------------")
  oldtree = oldfile.Get("tagsDumper/trees/"+j+"_13TeV_UntaggedTag_0")
  nentries = oldtree.GetEntries()

  dipho_mass = array('f',[0.])
  weight_TriggerWeight = array('f',[0.])
  weight_PreselSF = array('f',[0.])
  weight_LooseMvaSF = array('f',[0.])
  weight_electronVetoSF = array('f',[0.])
  oldtree.SetBranchAddress("dipho_mass",dipho_mass)
  oldtree.SetBranchAddress("weight_TriggerWeight",weight_TriggerWeight)
  oldtree.SetBranchAddress("weight_PreselSF",weight_PreselSF)
  oldtree.SetBranchAddress("weight_LooseMvaSF",weight_LooseMvaSF)
  oldtree.SetBranchAddress("weight_electronVetoSF",weight_electronVetoSF)

  newtree = oldtree.CloneTree(0)
  #branches needed: dipho_masshyp_near

  dipho_masshyp_near = array('i',[0])
  newtree.Branch('dipho_masshyp_near', dipho_masshyp_near, 'dipho_masshyp_near/I')
  newtree.SetBranchAddress("dipho_masshyp_near",dipho_masshyp_near)

  if (j[0:3]=="ggh"): #signal    
    for i in range(nentries):
      #if (i%1000==0): print(i,nentries)
      oldtree.GetEntry(i)
      dipho_masshyp_near[0] = int(j[4:])
      if (i%1000==0): print(dipho_mass[0])
      if (i%1000==0): print(dipho_masshyp_near[0])
      newtree.Fill()
  else: #background
    
    for i in range(nentries):
      #if (i%100000==0): print(i,nentries)
      oldtree.GetEntry(i)
      if dipho_mass[0] < 80.0:
        #if (dipho_mass[0] <= 47.5):
        #  dipho_masshyp_near[0] = masslist[min(range(0,5), key = lambda i: abs(masslist[i]-(dipho_mass[0])))]
        #  dipho_masshyp_near[0] = random.choice(masslist[0:5])
        #elif (dipho_mass[0] > 47.5):
        #  dipho_masshyp_near[0] = masslist[min(range(5,9), key = lambda i: abs(masslist[i]-(dipho_mass[0])))]
        #  dipho_masshyp_near[0] = random.choice(masslist[5:9])

        #if (i%1000==0): print("---------")
        # Find the index of the mass closest to weighted_dipho_mass
        #closest_index = min(range(len(masslist)), key=lambda i: abs(masslist[i] - weighted_dipho_mass))
        #if (dipho_mass[0] <= 47.5):
        #  if abs(masslist[closest_index] - dipho_mass[0]) <= 2.5:
        #    dipho_masshyp_near[0] = masslist[closest_index]
        #  else:
        #    dipho_masshyp_near[0] = random.choice(masslist[:4])
        #elif (weighted_dipho_mass > 47.5):
        #  if abs(masslist[closest_index] - weighted_dipho_mass) <= 2.5:
        #    dipho_masshyp_near[0] = masslist[closest_index]
        #  else:
        #    dipho_masshyp_near[0] = random.choice(masslist[5:8])

        if (i%10000==0): print("Diphoton mass = ", dipho_mass[0])
        if (i%10000==0): print(dipho_masshyp_near[0])

        #if ((dipho_mass[0]*weight_TriggerWeight[0]*weight_PreselSF[0]*weight_LooseMvaSF[0]*weight_electronVetoSF[0]) < 80.0):        
      #  dipho_masshyp_near[0] = masslist[min(range(len(masslist)), key = lambda i: abs(masslist[i]-(dipho_mass[0]*weight_TriggerWeight[0]*weight_PreselSF[0]*weight_LooseMvaSF[0]*weight_electronVetoSF[0])))]

      #if (dipho_mass[0] < 80.0):        
      dipho_masshyp_near[0] = masslist[min(range(len(masslist)), key = lambda i: abs(masslist[i]-(dipho_mass[0])))]
      
      newtree.Fill()
  newtree.AutoSave()

del oldfile
del newfile
