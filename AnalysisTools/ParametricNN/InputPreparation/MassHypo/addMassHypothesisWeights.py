from ROOT import *
from array import array
import numpy as np

#Get histogram integral values from signal and background
rp_near = TFile("ratios_dipho_masshyp_near.root","read")
rpn = rp_near.Get("rp")

wgt_near=[]
for k in range(0,32):
  if(rpn.Integral(k,k) !=0): wgt_near.append(1.0/rpn.Integral(k,k))


rp_near_nowsig = TFile("ratios_dipho_masshyp_near_noWSig.root","read")
rpn_nowsig = rp_near_nowsig.Get("rp")

wgt_near_nowsig=[]
for k in range(0,32):
  if(rpn_nowsig.Integral(k,k) !=0): wgt_near_nowsig.append(1.0/rpn_nowsig.Integral(k,k))

print(wgt_near)
print(wgt_near_nowsig)

#Grab data tree
treelist = ["ggh_10","ggh_15","ggh_20","ggh_25","ggh_30","ggh_35","ggh_40","ggh_45","ggh_50","ggh_55","ggh_60","ggh_65","ggh_70","mgg_bkg","Data"]
#treelist = ["ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70","mgg_bkg","Data"]

oldfile = TFile("output_ParaDDFull.root", "read")
newfile = TFile("output_ParaDDFullWgts.root","recreate")
tagsDumper = newfile.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")
trees.cd()

for idx,j in enumerate(treelist):
  print(j)
  oldtree = oldfile.Get("tagsDumper/trees/"+j+"_13TeV_UntaggedTag_0")
  nentries = oldtree.GetEntries()

  dipho_mass = array('f',[0.])
  oldtree.SetBranchAddress("dipho_mass",dipho_mass)
  newtree = oldtree.CloneTree(0)
  #branches needed: dipho_hypwgt_near with and without wsig for signal
  if (j[0:3]=="ggh"): #signal    
    dipho_hypwgt_near = array('f',[0])
    newtree.Branch('dipho_hypwgt_near', dipho_hypwgt_near, 'dipho_hypwgt_near/F')
    newtree.SetBranchAddress("dipho_hypwgt_near",dipho_hypwgt_near)
    dipho_hypwgt_near_nowsig = array('f',[0])
    newtree.Branch('dipho_hypwgt_near_nowsig', dipho_hypwgt_near_nowsig, 'dipho_hypwgt_near_nowsig/F')
    newtree.SetBranchAddress("dipho_hypwgt_near_nowsig",dipho_hypwgt_near_nowsig)
    for i in range(nentries):
      if (i%1000==0): print(i,nentries)
      oldtree.GetEntry(i)
      dipho_hypwgt_near[0] = wgt_near[idx]
      dipho_hypwgt_near_nowsig[0] = wgt_near_nowsig[idx]
      if (i%1000==0): print(dipho_hypwgt_near[0])
      if (i%1000==0): print(dipho_hypwgt_near_nowsig[0])
      newtree.Fill()
  else: #background
    for i in range(nentries):
      oldtree.GetEntry(i)
      newtree.Fill()
  newtree.AutoSave()

del oldfile
del newfile
