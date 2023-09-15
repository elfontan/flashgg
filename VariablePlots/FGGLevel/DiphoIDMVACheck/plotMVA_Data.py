from ROOT import *
import CMS_lumi

#Background
lmf = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_Data_Lowmassxml_v2/LowMassXML/output_EGamma_alesauva-UL2018_0-10_6_4-v0-Run2018-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189_USER.root","READ")
mcf = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_Data_Lowmassxml_v2/MCBDT/output_EGamma_alesauva-UL2018_0-10_6_4-v0-Run2018-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189_USER.root","READ")
ddf = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_Data_Lowmassxml_v2/DataBDT/output_EGamma_alesauva-UL2018_0-10_6_4-v0-Run2018-12Nov2019_UL2018-v2-981b04a73c9458401b9ffd78fdd24189_USER.root","READ")

lmt0 = lmf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
lmt1 = lmf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
lmt2 = lmf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
lmt3 = lmf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

mct0 = mcf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mct1 = mcf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
mct2 = mcf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
mct3 = mcf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

ddt0 = ddf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
ddt1 = ddf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
ddt2 = ddf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
ddt3 = ddf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

#Create histograms
lm0 = TH1F("lm0","lm0",40,-1.0,1.0)
lm0.Sumw2()
lm1 = TH1F("lm1","lm1",40,-1.0,1.0)
lm1.Sumw2()
lm2 = TH1F("lm2","lm2",40,-1.0,1.0)
lm2.Sumw2()
lm3 = TH1F("lm3","lm3",40,-1.0,1.0)
lm3.Sumw2()

mc0 = TH1F("mc0","mc0",40,-1.0,1.0)
mc0.Sumw2()
mc1 = TH1F("mc1","mc1",40,-1.0,1.0)
mc1.Sumw2()
mc2 = TH1F("mc2","mc2",40,-1.0,1.0)
mc2.Sumw2()
mc3 = TH1F("mc3","mc3",40,-1.0,1.0)
mc3.Sumw2()

dd0 = TH1F("dd0","dd0",40,-1.0,1.0)
dd0.Sumw2()
dd1 = TH1F("dd1","dd1",40,-1.0,1.0)
dd1.Sumw2()
dd2 = TH1F("dd2","dd2",40,-1.0,1.0)
dd2.Sumw2()
dd3 = TH1F("dd3","dd3",40,-1.0,1.0)
dd3.Sumw2()

lm = TH1F("lm","lm",40,-1.0,1.0)
lm.Sumw2()
mc = TH1F("mc","mc",40,-1.0,1.0)
mc.Sumw2()
dd = TH1F("dd","dd",40,-1.0,1.0)
dd.Sumw2()

#Weighted: abs(weight)*(CMS_hgg_mass>0)
lmt0.Draw("diphoMVA>>lm0","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
lmt1.Draw("diphoMVA>>lm1","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
lmt2.Draw("diphoMVA>>lm2","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
lmt3.Draw("diphoMVA>>lm3","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")

mct0.Draw("diphoMVA>>mc0","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
mct1.Draw("diphoMVA>>mc1","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
mct2.Draw("diphoMVA>>mc2","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
mct3.Draw("diphoMVA>>mc3","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")

ddt0.Draw("diphoMVA>>dd0","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
ddt1.Draw("diphoMVA>>dd1","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
ddt2.Draw("diphoMVA>>dd2","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
ddt3.Draw("diphoMVA>>dd3","abs(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")

lm.Add(lm0)
lm.Add(lm1)
lm.Add(lm2)
lm.Add(lm3)

mc.Add(mc0)
mc.Add(mc1)
mc.Add(mc2)
mc.Add(mc3)

dd.Add(dd0)
dd.Add(dd1)
dd.Add(dd2)
dd.Add(dd3)

lm.SaveAs("lm_data.root")
mc.SaveAs("mc_data.root")
dd.SaveAs("dd_data.root")

#Now we draw it out
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()
c1.SetBottomMargin(0.11)
c1.SetLeftMargin(0.11)

lm.SetLineColor(kTeal+3)
lm.SetLineWidth(2)
lm.Draw("histsame")

lm.SetXTitle("Diphoton MVA")
lm.GetXaxis().SetTitleSize(25)
lm.GetXaxis().SetTitleFont(43)
lm.GetXaxis().SetTitleOffset(2.0)
lm.GetXaxis().SetLabelFont(43)
lm.GetXaxis().SetLabelSize(25)
lm.GetXaxis().SetLabelOffset(0.02)

lm.GetYaxis().SetTitle("Events")
lm.GetYaxis().SetTitleSize(25)
lm.GetYaxis().SetTitleFont(43)
lm.GetYaxis().SetTitleOffset(2.25)
lm.GetYaxis().SetLabelFont(43)
lm.GetYaxis().SetLabelSize(25)

mc.SetLineColor(kAzure-2)
mc.SetLineWidth(2)
mc.Draw("histsame")

mc.SetXTitle("Diphoton MVA")
mc.GetXaxis().SetTitleSize(25)
mc.GetXaxis().SetTitleFont(43)
mc.GetXaxis().SetTitleOffset(2.0)
mc.GetXaxis().SetLabelFont(43)
mc.GetXaxis().SetLabelSize(25)
mc.GetXaxis().SetLabelOffset(0.02)

mc.GetYaxis().SetTitle("Events")
mc.GetYaxis().SetTitleSize(25)
mc.GetYaxis().SetTitleFont(43)
mc.GetYaxis().SetTitleOffset(2.25)
mc.GetYaxis().SetLabelFont(43)
mc.GetYaxis().SetLabelSize(25)

dd.SetLineColor(kBlue+1)
dd.SetLineWidth(2)
dd.Draw("histsame")

dd.SetXTitle("Diphoton MVA")
dd.GetXaxis().SetTitleSize(25)
dd.GetXaxis().SetTitleFont(43)
dd.GetXaxis().SetTitleOffset(2.0)
dd.GetXaxis().SetLabelFont(43)
dd.GetXaxis().SetLabelSize(25)
dd.GetXaxis().SetLabelOffset(0.02)

dd.GetYaxis().SetTitle("Events")
dd.GetYaxis().SetTitleSize(25)
dd.GetYaxis().SetTitleFont(43)
dd.GetYaxis().SetTitleOffset(2.25)
dd.GetYaxis().SetLabelFont(43)
dd.GetYaxis().SetLabelSize(25)

leg = TLegend(0.35,0.6,0.55,0.85)
leg.AddEntry(lm,"Lowmass XML")
leg.AddEntry(mc,"MC Driven")
leg.AddEntry(dd,"Data Driven")
leg.Draw("same")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText= "Preliminary"
CMS_lumi.lumi_sqrtS = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize= 0.4
CMS_lumi.lumiTextSize = 0.3
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)
c1.Update()

c1.SaveAs("DiphoMVA_DataBkg.png")
c1.SaveAs("DiphoMVA_DataBkg.pdf")

print "Lowmass Data: ",lm.Integral()
print "MC Data: ",mc.Integral()
print "Data Data : ",dd.Integral()
