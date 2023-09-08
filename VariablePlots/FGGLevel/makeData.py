from ROOT import *

#Data
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_Data_Lowmassxml_v1/output_EGamma_alesauva-UL2018_0-10_6_4-v0-Run2018-12Nov2019_UL2018-981b04a73c9458401b9ffd78fdd24189_USER.root","READ")

#Obtain each class tree from each file
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
dat1 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
dat2 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
dat3 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

#Create histograms
data0 = TH1F("data0","data0",40,-1,1)
data0.Sumw2()
data1 = TH1F("data1","data1",40,-1,1)
data1.Sumw2()
data2 = TH1F("data2","data2",40,-1,1)
data2.Sumw2()
data3 = TH1F("data3","data3",40,-1,1)
data3.Sumw2()

#Sideband/Presel regions: CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7 && event%20==0
dat0.Draw("cosphi>>data0","CMS_hgg_mass>0 && event%20==0","goff")
dat1.Draw("cosphi>>data1","CMS_hgg_mass>0 && event%20==0","goff")
dat2.Draw("cosphi>>data2","CMS_hgg_mass>0 && event%20==0","goff")
dat3.Draw("cosphi>>data3","CMS_hgg_mass>0 && event%20==0","goff")

data0.Add(data1)
data0.Add(data2)
data0.Add(data3)

#Now we draw it out
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1000)
c1.cd()
c1.SetBottomMargin(0.17)

data0.SetLineColor(1)
data0.Draw("ep")
data0.GetYaxis().SetTitle("Events/(GeV)")
data0.SaveAs("data.root")
