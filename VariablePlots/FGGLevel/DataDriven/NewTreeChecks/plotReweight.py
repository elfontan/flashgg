from ROOT import *
import CMS_lumi

#Data
data = TFile("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/BkgMCCutFlowPlots_v2/FGGLevel/DataDriven/output_sideband.root","READ")

#Obtain each class tree from each file
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
dat1 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
dat2 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
dat3 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

#Create histograms
data0 = TH1F("data0","data0",50,0,2.5)
data0.Sumw2()
data1 = TH1F("data1","data1",50,0,2.5)
data1.Sumw2()
data2 = TH1F("data2","data2",50,0,2.5)
data2.Sumw2()
data3 = TH1F("data3","data3",50,0,2.5)
data3.Sumw2()

#Sideband/Presel regions: CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7 && event%20==0
dat0.Draw("weight>>data0","CMS_hgg_mass>0","goff")
dat1.Draw("weight>>+data0","CMS_hgg_mass>0","goff")
dat2.Draw("weight>>+data0","CMS_hgg_mass>0","goff")
dat3.Draw("weight>>+data0","CMS_hgg_mass>0","goff")

#Now we draw it out
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1000,1000)
c1.cd()
c1.SetBottomMargin(0.17)
c1.SetLeftMargin(0.17)

data0.SetFillColor(kOrange-3)
data0.SetLineColor(kOrange-3)
data0.Draw("histo")
data0.GetXaxis().SetTitle("Event Reweight")
data0.GetYaxis().SetTitle("Events")

leg = TLegend(0.2,0.73,0.4,0.8)
leg.AddEntry(data0,"Sideband Data")
leg.Draw("same")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.4
CMS_lumi.lumiTextSize   = 0.35
CMS_lumi.extraOverCmsTextSize = 0.7
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)

c1.Update()
c1.SaveAs("Data_Reweight.png")
c1.SaveAs("Data_Reweight.pdf")

print("Reweight: ",data0.Integral())
