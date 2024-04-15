from ROOT import *
from array import array
import numpy as np

#Grab data tree
treelist = ["mgg_bkg","Data","ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70"] #change accordingly
masslist = [10,15,20,30,40,50,55,60,70] #change accordingly

oldfile = TFile("../Inputs/output_DDFull_Feb2024Sig.root", "read")
newfile = TFile("output_ParaDDFull.root","recreate")
newfile.mkdir("tagsDumper")
tagsDumper.cd()
tagsDumper.mkdir("trees")
trees.cd()

for j in treelist:
  print j
  oldtree = oldfile.Get("tagsDumper/trees/"+j+"_13TeV_UntaggedTag_0")
  nentries = oldtree.GetEntries()

  dipho_mass = array('f',[0.])
  oldtree.SetBranchAddress("dipho_mass",dipho_mass)
  newtree = oldtree.CloneTree(0)
  #branches needed: dipho_masshyp_near and dipho_masshyp_random

  dipho_masshyp_near = array('i',[0])
  newtree.Branch('dipho_masshyp_near', dipho_masshyp_near, 'dipho_masshyp_near/I')
  newtree.SetBranchAddress("dipho_masshyp_near",dipho_masshyp_near)

  if (j[0:3]=="ggh"): #signal    
    for i in range(nentries):
      if (i%1000==0): print i,nentries
      oldtree.GetEntry(i)
      dipho_masshyp_near[0] = int(j[4:])
      if (i%10000==0): print dipho_mass[0]
      if (i%10000==0): print dipho_masshyp_near[0]
      newtree.Fill()
  else: #background
    for i in range(nentries):
      if (i%10000==0): print i,nentries
      oldtree.GetEntry(i)
      if (dipho_mass[0] < 75.0):        
        dipho_masshyp_near[0] = masslist[min(range(len(masslist)), key = lambda i: abs(masslist[i]-dipho_mass[0]))]
        if (i%1000==0): print dipho_mass[0]
        if (i%1000==0): print dipho_masshyp_near[0]
        newtree.Fill()
  newtree.AutoSave()

del oldfile
del newfile
