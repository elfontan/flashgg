import ROOT
from ROOT import TFile
from array import array
import numpy as np

#Get histogram integral values from signal and background
rp_norm = TFile("ratios_dipho_masshyp_norm.root","read")
rpn = rp_norm.Get("h_dipho_masshyp_near_sig0")

wgt_norm=[]
for k in range(0,32):
  if(rpn.Integral(k,k) !=0): wgt_norm.append(rpn.Integral(k,k))
  print (rpn.Integral(k,k))

rp_norm_nowsig = TFile("ratios_dipho_masshyp_norm_noWSig.root","read")
rpn_nowsig = rp_norm_nowsig.Get("h_dipho_masshyp_near_sig0")

wgt_norm_nowsig=[]
for k in range(0,32):
  if(rpn_nowsig.Integral(k,k) !=0): wgt_norm_nowsig.append(rpn_nowsig.Integral(k,k))

norm_40 = wgt_norm[2]
norm_40_nowsig = wgt_norm_nowsig[2]

wgt_norm[:] = [norm_40/x for x in wgt_norm]
wgt_norm_nowsig[:] = [norm_40_nowsig/x for x in wgt_norm_nowsig]

print(wgt_norm)
print(wgt_norm_nowsig)

#Grab data tree
treelist = ["ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70","mgg_bkg","Data"]
#treelist = ["ggh_10","ggh_15","ggh_20","ggh_30","ggh_40","ggh_50","ggh_55","ggh_60","ggh_70","mgg_bkg","Data"]

mggCounts =  [101534.0, 121516.0, 99714.0, 50166.0, 48382.0, 83233.0, 118984.0]
sbCounts =  [113626.0, 75261.0, 93546.0, 168636.0, 233845.0, 394164.0, 341708.0]
mggFrac = [(mgg / (mgg + sb))  if (mgg + sb) != 0 else 0 for mgg, sb in zip(mggCounts, sbCounts)]
sbFrac = [(sb / (mgg + sb)) if (mgg + sb) != 0 else 0 for mgg, sb in zip(mggCounts, sbCounts)]
mgg_avg = sum(mggFrac) / len(mggFrac)
sb_avg = sum(sbFrac) / len(sbFrac)

# Compute the number of expected events for mgg and sb
nExp_mgg = [(mgg_avg) * (norm_40) for mgg, sb in zip(mggCounts, sbCounts)]
nExp_sb = [(sb_avg) * (norm_40) for mgg, sb in zip(mggCounts, sbCounts)]
# Compute the scale factors
SFs_mgg = [nExp_mgg / mgg if mgg != 0 else float('inf') for nExp_mgg, mgg in zip(nExp_mgg, mggCounts)]
SFs_sb = [nExp_sb / sb if sb != 0 else float('inf') for nExp_sb, sb in zip(nExp_sb, sbCounts)]

# Print the results
print("mgg percentages:", mggFrac)
print("sb percentages:", sbFrac)
print("mgg_avg", mgg_avg)
print("sb_avg", sb_avg)
print("nExp_mgg:", nExp_mgg)
print("nExp_sb:", nExp_sb)
print("Scale Factors for mgg:", SFs_mgg)
print("Scale Factors for sb:", SFs_sb)
  
oldfile = TFile("output_ParaDDFullWgts.root", "read")
newfile = TFile("output_ParaDDFullNorms.root","recreate")
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
  mass_points = [20, 30, 40, 50, 55, 60, 70]
  mass_window = 2
  mgg_counts = []
  sb_counts = []
  ratio_bkg = []
    
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

    if (j=="mgg_bkg"):
      #print("Here we apply SFs_mgg = ", SFs_mgg)
      if(dipho_masshyp_near[0]==20):
        dipho_hypnorm_near[0] = wgt_norm[0]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[0]
      if(dipho_masshyp_near[0]==30):
        dipho_hypnorm_near[0] = wgt_norm[1]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[1]
      if(dipho_masshyp_near[0]==40):
        dipho_hypnorm_near[0] = wgt_norm[2]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[2]
      if(dipho_masshyp_near[0]==50):
        dipho_hypnorm_near[0] = wgt_norm[3]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[3]
      if(dipho_masshyp_near[0]==55):
        dipho_hypnorm_near[0] = wgt_norm[4]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[4]
      if(dipho_masshyp_near[0]==60):
        dipho_hypnorm_near[0] = wgt_norm[5]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[5]
      if(dipho_masshyp_near[0]==70):
        dipho_hypnorm_near[0] = wgt_norm[6]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[6]

      if (i%5000==0): print("MGG:", dipho_masshyp_near[0])
      if (i%5000==0): print("MGG:",dipho_hypnorm_near[0])
      if (i%5000==0): print("MGG:",dipho_hypnorm_near_nowsig[0])

    elif (j=="Data"):
      #print("Here we apply SFs_sb = ", SFs_sb)
      if(dipho_masshyp_near[0]==20):
        dipho_hypnorm_near[0] = wgt_norm[0]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[0]
      if(dipho_masshyp_near[0]==30):
        dipho_hypnorm_near[0] = wgt_norm[1]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[1]
      if(dipho_masshyp_near[0]==40):
        dipho_hypnorm_near[0] = wgt_norm[2]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[2]
      if(dipho_masshyp_near[0]==50):
        dipho_hypnorm_near[0] = wgt_norm[3]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[3]
      if(dipho_masshyp_near[0]==55):
        dipho_hypnorm_near[0] = wgt_norm[4]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[4]
      if(dipho_masshyp_near[0]==60):
        dipho_hypnorm_near[0] = wgt_norm[5]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[5]
      if(dipho_masshyp_near[0]==70):
        dipho_hypnorm_near[0] = wgt_norm[6]
        dipho_hypnorm_near_nowsig[0] = wgt_norm[6]

      if (i%10000==0): print("SB:", dipho_masshyp_near[0])
      if (i%10000==0): print("SB:", dipho_hypnorm_near[0])
      if (i%10000==0): print("SB:", dipho_hypnorm_near_nowsig[0])
    else:
      #conditions for each normalization value
      #if(dipho_masshyp_near[0]==10):
      #  dipho_hypnorm_near[0] = wgt_norm[0]
      #  dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[0]
      #if(dipho_masshyp_near[0]==15):
      #  dipho_hypnorm_near[0] = wgt_norm[1]
      #  dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[1]
      if(dipho_masshyp_near[0]==20):
        dipho_hypnorm_near[0] = wgt_norm[0]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[0]
      #if(dipho_masshyp_near[0]==25):
      #  dipho_hypnorm_near[0] = wgt_norm[3]
      #  dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[3]
      if(dipho_masshyp_near[0]==30):
        dipho_hypnorm_near[0] = wgt_norm[1]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[1]
      #if(dipho_masshyp_near[0]==35):
      #  dipho_hypnorm_near[0] = wgt_norm[5]
      #  dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[5]
      if(dipho_masshyp_near[0]==40):
        dipho_hypnorm_near[0] = wgt_norm[2]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[2]
      #if(dipho_masshyp_near[0]==45):
      #  dipho_hypnorm_near[0] = wgt_norm[7]
      #  dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[7]
      if(dipho_masshyp_near[0]==50):
        dipho_hypnorm_near[0] = wgt_norm[3]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[3]
      if(dipho_masshyp_near[0]==55):
        dipho_hypnorm_near[0] = wgt_norm[4]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[4]
      if(dipho_masshyp_near[0]==60):
        dipho_hypnorm_near[0] = wgt_norm[5]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[5]
      #if(dipho_masshyp_near[0]==65):
      #  dipho_hypnorm_near[0] = wgt_norm[11]
      #  dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[11]
      if(dipho_masshyp_near[0]==70):
        dipho_hypnorm_near[0] = wgt_norm[6]
        dipho_hypnorm_near_nowsig[0] = wgt_norm_nowsig[6]

      if (i%10000==0): print(dipho_masshyp_near[0])
      if (i%10000==0): print(dipho_hypnorm_near[0])
      if (i%10000==0): print(dipho_hypnorm_near_nowsig[0])

    newtree.Fill()
  newtree.AutoSave()

del oldfile
del newfile
