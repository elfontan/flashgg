from ROOT import *
from array import array
import numpy as np

#Get histogram integral values from signal and background
rp_norm = TFile("ratios_dipho_masshyp_norm.root","read")
rpn = rp_norm.Get("h_dipho_masshyp_near_sig0")

wgt_norm=[]
for k in range(0,32):
  if(rpn.Integral(k,k) !=0): wgt_norm.append(rpn.Integral(k,k))


rp_norm_nowsig = TFile("ratios_dipho_masshyp_norm_noWSig.root","read")
rpn_nowsig = rp_norm_nowsig.Get("h_dipho_masshyp_near_sig0")

wgt_norm_nowsig=[]
for k in range(0,32):
  if(rpn_nowsig.Integral(k,k) !=0): wgt_norm_nowsig.append(rpn_nowsig.Integral(k,k))

print(wgt_norm)
print(wgt_norm_nowsig)

norm_40 = wgt_norm[6]
norm_40_nowsig = wgt_norm_nowsig[6]

wgt_norm[:] = [norm_40/x for x in wgt_norm]
wgt_norm_nowsig[:] = [norm_40_nowsig/x for x in wgt_norm_nowsig]

print(wgt_norm)
print(wgt_norm_nowsig)

#Grab data tree
treelist = ["ggh_10","ggh_15","ggh_20","ggh_25","ggh_30","ggh_35","ggh_40","ggh_45","ggh_50","ggh_55","ggh_60","ggh_65","ggh_70","mgg_bkg","Data"]
#treelist = ["ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70","mgg_bkg","Data"]

oldfile = TFile("output_ParaDDFullWgts.root", "read")
newfile = TFile("output_ParaDDFullNorms.root","recreate")
tagsDumper = newfile.mkdir("tagsDumper")
tagsDumper.cd()
trees = tagsDumper.mkdir("trees")
trees.cd()

for idx,j in enumerate(treelist):
  print(j)
  oldtree = oldfile.Get("tagsDumper/trees/"+j+"_13TeV_UntaggedTag_0")
  nentries = oldtree.GetEntries()

  dipho_masshyp_near = array('i',[0])
  oldtree.SetBranchAddress("dipho_masshyp_near",dipho_masshyp_near)
  newtree = oldtree.CloneTree(0)
  #branches needed: dipho_hypnorm_near with and without wsig for signal
  dipho_hypnorm_near = array('f',[0])
  newtree.Branch('dipho_hypnorm_near', dipho_hypnorm_near, 'dipho_hypnorm_near/F')
  newtree.SetBranchAddress("dipho_hypnorm_near",dipho_hypnorm_near)
  dipho_hypnorm_near_nowsig = array('f',[0])
  newtree.Branch('dipho_hypnorm_near_nowsig', dipho_hypnorm_near_nowsig, 'dipho_hypnorm_near_nowsig/F')
  newtree.SetBranchAddress("dipho_hypnorm_near_nowsig",dipho_hypnorm_near_nowsig)
  for i in range(nentries):
    if (i%5000==0): print(i,nentries)
    oldtree.GetEntry(i)

    #conditions for each normalization value
    if(dipho_masshyp_near[0]==10):
      dipho_hypnorm_near[0] = wgt_norm[0]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[0]
    if(dipho_masshyp_near[0]==15):
      dipho_hypnorm_near[0] = wgt_norm[1]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[1]
    if(dipho_masshyp_near[0]==20):
      dipho_hypnorm_near[0] = wgt_norm[2]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[2]
    if(dipho_masshyp_near[0]==25):
      dipho_hypnorm_near[0] = wgt_norm[3]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[3]
    if(dipho_masshyp_near[0]==30):
      dipho_hypnorm_near[0] = wgt_norm[4]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[4]
    if(dipho_masshyp_near[0]==35):
      dipho_hypnorm_near[0] = wgt_norm[5]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[5]
    if(dipho_masshyp_near[0]==40):
      dipho_hypnorm_near[0] = wgt_norm[6]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[6]
    if(dipho_masshyp_near[0]==45):
      dipho_hypnorm_near[0] = wgt_norm[7]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[7]
    if(dipho_masshyp_near[0]==50):
      dipho_hypnorm_near[0] = wgt_norm[8]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[8]
    if(dipho_masshyp_near[0]==55):
      dipho_hypnorm_near[0] = wgt_norm[9]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[9]
    if(dipho_masshyp_near[0]==60):
      dipho_hypnorm_near[0] = wgt_norm[10]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[10]
    if(dipho_masshyp_near[0]==65):
      dipho_hypnorm_near[0] = wgt_norm[11]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[11]
    if(dipho_masshyp_near[0]==70):
      dipho_hypnorm_near[0] = wgt_norm[12]
      dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[12]

    if (i%5000==0): print(dipho_masshyp_near[0])
    if (i%5000==0): print(dipho_hypnorm_near[0])
    if (i%5000==0): print(dipho_hypnorm_near_nowsig[0])
    newtree.Fill()
  newtree.AutoSave()

del oldfile
del newfile
