from ROOT import *
from array import array

#Grab data tree
oldfile = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_Data_Lowmassxml_v1/output_EGamma_alesauva-UL2018_0-10_6_4-v0-Run2018-12Nov2019_UL2018-981b04a73c9458401b9ffd78fdd24189_USER.root", "read")
newfile = TFile("output_sideband_noweight_nonewminid.root","recreate")
newfile.mkdir("tagsDumper")
tagsDumper.cd()
tagsDumper.mkdir("trees")
trees.cd()

for x in range (0,4):
  oldtree = oldfile.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_"+str(x))
  nentries = oldtree.GetEntries()

  dipho_leadIDMVA = array('f',[0.])
  dipho_subleadIDMVA = array('f',[0.])
  event = array('I',[0])
  oldtree.SetBranchAddress("dipho_leadIDMVA",dipho_leadIDMVA)
  oldtree.SetBranchAddress("dipho_subleadIDMVA",dipho_subleadIDMVA)
  oldtree.SetBranchAddress("event",event)

  newtree = oldtree.CloneTree(0)
  for i in range(nentries):
    if (i%1000==0): print i,nentries
    oldtree.GetEntry(i)
    if (min(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])<-0.7 and max(dipho_leadIDMVA[0],dipho_subleadIDMVA[0])>-0.7 and event[0]%20 == 0): #if event is in sideband and also blinded
      newtree.Fill()
  newtree.AutoSave()

del oldfile
del newfile
