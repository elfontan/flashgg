from ROOT import *
import math

mva_minimum = -0.9
mva_maximum = 1.0
binning = int(math.ceil((mva_maximum - mva_minimum) / 0.05))

#Bkg from 40 to 80 GeV
mgg = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_BkgMC_MGG40to80_v2/output_DiPhotonJetsBox_M40_80-sherpa_atsatsos-UL18_VLowMassDiphoton_BkgMC_MGG40to80_v1-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-bf7acd40472d4982996c4dd60309cd6d_USER.root","READ")
gj = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_BkgMC_MGG40to80_v2/output_GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8_atsatsos-UL18_VLowMassDiphoton_BkgMC_MGG40to80_v2-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3-3fc41d6a5cdc2b7d1e5534c778de39cd_USER.root","READ")
qcd = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/UL18_BkgMC_MGG40to80_v2/output_QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV-pythia8_atsatsos-UL18_VLowMassDiphoton_BkgMC_MGG40to80_v2-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-3fc41d6a5cdc2b7d1e5534c778de39cd_USER.root","READ")

mggt0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
mggt1 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_1")
mggt2 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_2")
mggt3 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_3")

gjt0 = gj.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
gjt1 = gj.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_1")
gjt2 = gj.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_2")
gjt3 = gj.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_3")

qcdt0 = qcd.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
qcdt1 = qcd.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_1")
qcdt2 = qcd.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_2")
qcdt3 = qcd.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_3")

#Create histograms as well as stacked histo for all backgrounds
mgg0 = TH1F("mgg0","mgg0",binning,mva_minimum,mva_maximum)
mgg0.Sumw2()
mgg1 = TH1F("mgg1","mgg1",binning,mva_minimum,mva_maximum)
mgg1.Sumw2()
mgg2 = TH1F("mgg2","mgg2",binning,mva_minimum,mva_maximum)
mgg2.Sumw2()
mgg3 = TH1F("mgg3","mgg3",binning,mva_minimum,mva_maximum)
mgg3.Sumw2()

gj0 = TH1F("gj0","gj0",binning,mva_minimum,mva_maximum)
gj0.Sumw2()
gj1 = TH1F("gj1","gj1",binning,mva_minimum,mva_maximum)
gj1.Sumw2()
gj2 = TH1F("gj2","gj2",binning,mva_minimum,mva_maximum)
gj2.Sumw2()
gj3 = TH1F("gj3","gj3",binning,mva_minimum,mva_maximum)
gj3.Sumw2()

qcd0 = TH1F("qcd0","qcd0",binning,mva_minimum,mva_maximum)
qcd0.Sumw2()
qcd1 = TH1F("qcd1","qcd1",binning,mva_minimum,mva_maximum)
qcd1.Sumw2()
qcd2 = TH1F("qcd2","qcd2",binning,mva_minimum,mva_maximum)
qcd2.Sumw2()
qcd3 = TH1F("qcd3","qcd3",binning,mva_minimum,mva_maximum)
qcd3.Sumw2()

mgg4080 = TH1F("mgg4080","mgg4080",binning,mva_minimum,mva_maximum)
mgg4080.Sumw2()
gj4080 = TH1F("gj4080","gj4080",binning,mva_minimum,mva_maximum)
gj4080.Sumw2()
qcd4080 = TH1F("qcd4080","qcd4080",binning,mva_minimum,mva_maximum)
qcd4080.Sumw2()

#Weighted: abs(weight)*(CMS_hgg_mass>0)
#Sideband/Presel regions: abs(weight)*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7)
mggt0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>mgg0","abs(weight)*(CMS_hgg_mass>0)","goff")
mggt1.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>mgg1","abs(weight)*(CMS_hgg_mass>0)","goff")
mggt2.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>mgg2","abs(weight)*(CMS_hgg_mass>0)","goff")
mggt3.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>mgg3","abs(weight)*(CMS_hgg_mass>0)","goff")

gjt0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj0","abs(weight)*(CMS_hgg_mass>0)","goff")
gjt1.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj1","abs(weight)*(CMS_hgg_mass>0)","goff")
gjt2.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj2","abs(weight)*(CMS_hgg_mass>0)","goff")
gjt3.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj3","abs(weight)*(CMS_hgg_mass>0)","goff")

qcdt0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>qcd0","abs(weight)*(CMS_hgg_mass>0)","goff")
qcdt1.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>qcd1","abs(weight)*(CMS_hgg_mass>0)","goff")
qcdt2.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>qcd2","abs(weight)*(CMS_hgg_mass>0)","goff")
qcdt3.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>qcd3","abs(weight)*(CMS_hgg_mass>0)","goff")

mgg4080.Add(mgg0)
mgg4080.Add(mgg1)
mgg4080.Add(mgg2)
mgg4080.Add(mgg3)

gj4080.Add(gj0)
gj4080.Add(gj1)
gj4080.Add(gj2)
gj4080.Add(gj3)

qcd4080.Add(qcd0)
qcd4080.Add(qcd1)
qcd4080.Add(qcd2)
qcd4080.Add(qcd3)

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,800)
c1.cd()

mgg4080.SetFillColor(kRed)
mgg4080.SetLineColor(kBlack)
mgg4080.GetYaxis().SetTitle("Events Accepted")
mgg4080.SaveAs("DataDriven/bkg_histos/mgg_4080.root")

gj4080.SetFillColor(kBlue)
gj4080.SetLineColor(kBlack)
gj4080.GetYaxis().SetTitle("Events Accepted")
gj4080.SaveAs("DataDriven/bkg_histos/gj_4080.root")

qcd4080.SetFillColor(kYellow)
qcd4080.SetLineColor(kBlack)
qcd4080.GetYaxis().SetTitle("Events Accepted")
qcd4080.SaveAs("DataDriven/bkg_histos/qcd_4080.root")

print("MGG: ",mgg4080.Integral())
print("GJet: ",gj4080.Integral())
print("QCD: ",qcd4080.Integral())
