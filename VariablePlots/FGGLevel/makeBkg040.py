from ROOT import *

#Bkg from 0 to 40 GeV

#Background
mgg = TFile("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/Systematics/test/UL18_VLowMassDiphoton_BkgMC_MGG0to40_v1/output_DiPhotonJetsBox_M0_40-Sherpa_atsatsos-UL18_VLowMassDiphoton_BkgMC_DiphotonMass0to40_v04062023-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-3fc41d6a5cdc2b7d1e5534c778de39cd_USER.root","READ")
gj = TFile("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/Systematics/test/UL18_VLowMassDiphoton_BkgMC_MGG0to40_v1/output_GJet_Pt-20toInf_DoubleEMEnriched_MGG-2to40_TuneCP5_13TeV_Pythia8_atsatsos-UL18_VLowMassDiphoton_BkgMC_PhotonJetMass2to40_v05252023-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-3fc41d6a5cdc2b7d1e5534c778de39cd_USER.root","READ")
qcd = TFile("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/Systematics/test/UL18_VLowMassDiphoton_BkgMC_MGG0to40_v1/output_QCD_Pt-30toInf_DoubleEMEnriched_MGG-5to40_TuneCP5_13TeV-pythia8_atsatsos-UL18_VLowMassDiphoton_BkgMC_QCDMass5to40_v05252023-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-3fc41d6a5cdc2b7d1e5534c778de39cd_USER.root","READ")

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
mgg0 = TH1F("mgg0","mgg0",40,-1,1)
mgg0.Sumw2()
mgg1 = TH1F("mgg1","mgg1",40,-1,1)
mgg1.Sumw2()
mgg2 = TH1F("mgg2","mgg2",40,-1,1)
mgg2.Sumw2()
mgg3 = TH1F("mgg3","mgg3",40,-1,1)
mgg3.Sumw2()

gj0 = TH1F("gj0","gj0",40,-1,1)
gj0.Sumw2()
gj1 = TH1F("gj1","gj1",40,-1,1)
gj1.Sumw2()
gj2 = TH1F("gj2","gj2",40,-1,1)
gj2.Sumw2()
gj3 = TH1F("gj3","gj3",40,-1,1)
gj3.Sumw2()

qcd0 = TH1F("qcd0","qcd0",40,-1,1)
qcd0.Sumw2()
qcd1 = TH1F("qcd1","qcd1",40,-1,1)
qcd1.Sumw2()
qcd2 = TH1F("qcd2","qcd2",40,-1,1)
qcd2.Sumw2()
qcd3 = TH1F("qcd3","qcd3",40,-1,1)
qcd3.Sumw2()

mgg040 = TH1F("mgg040","mgg040",40,-1,1)
mgg040.Sumw2()
gj040 = TH1F("gj040","gj040",40,-1,1)
gj040.Sumw2()
qcd040 = TH1F("qcd040","qcd040",40,-1,1)
qcd040.Sumw2()

#Weighted: abs(weight)*(CMS_hgg_mass>0)
#Sideband/Presel regions: abs(weight)*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7)
mggt0.Draw("cosphi>>mgg0","abs(weight)*(CMS_hgg_mass>0)","goff")
mggt1.Draw("cosphi>>mgg1","abs(weight)*(CMS_hgg_mass>0)","goff")
mggt2.Draw("cosphi>>mgg2","abs(weight)*(CMS_hgg_mass>0)","goff")
mggt3.Draw("cosphi>>mgg3","abs(weight)*(CMS_hgg_mass>0)","goff")

gjt0.Draw("cosphi>>gj0","abs(weight)*(CMS_hgg_mass>0)","goff")
gjt1.Draw("cosphi>>gj1","abs(weight)*(CMS_hgg_mass>0)","goff")
gjt2.Draw("cosphi>>gj2","abs(weight)*(CMS_hgg_mass>0)","goff")
gjt3.Draw("cosphi>>gj3","abs(weight)*(CMS_hgg_mass>0)","goff")

qcdt0.Draw("cosphi>>qcd0","abs(weight)*(CMS_hgg_mass>0)","goff")
qcdt1.Draw("cosphi>>qcd1","abs(weight)*(CMS_hgg_mass>0)","goff")
qcdt2.Draw("cosphi>>qcd2","abs(weight)*(CMS_hgg_mass>0)","goff")
qcdt3.Draw("cosphi>>qcd3","abs(weight)*(CMS_hgg_mass>0)","goff")

mgg040.Add(mgg0)
mgg040.Add(mgg1)
mgg040.Add(mgg2)
mgg040.Add(mgg3)

gj040.Add(gj0)
gj040.Add(gj1)
gj040.Add(gj2)
gj040.Add(gj3)

qcd040.Add(qcd0)
qcd040.Add(qcd1)
qcd040.Add(qcd2)
qcd040.Add(qcd3)

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,800)
c1.cd()

mgg040.SetFillColor(kRed)
mgg040.SetLineColor(kBlack)
mgg040.GetYaxis().SetTitle("Events Accepted")
mgg040.SaveAs("mgg_040.root")

gj040.SetFillColor(kBlue)
gj040.SetLineColor(kBlack)
gj040.GetYaxis().SetTitle("Events Accepted")
gj040.SaveAs("gj_040.root")

qcd040.SetFillColor(kYellow)
qcd040.SetLineColor(kBlack)
qcd040.GetYaxis().SetTitle("Events Accepted")
qcd040.SaveAs("qcd_040.root")

print("MGG: ",mgg040.Integral())
print("GJet: ",gj040.Integral())
print("QCD: ",qcd040.Integral())
