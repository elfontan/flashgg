from ROOT import *

# Bkg MC
#Diphoton 0-40
f = TFile("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/Systematics/test/UL18_VLowMass_BkgMC_Diphoton0to40_v04062023_LowMassXML/output_DiPhotonJetsBox_M0_40-Sherpa_atsatsos-UL18_VLowMassDiphoton_BkgMC_DiphotonMass0to40_v04062023-v0-v0-RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2-3fc41d6a5cdc2b7d1e5534c778de39cd_USER.root","READ")
#Diphoton 40-80
h = TFile("/eos/user/a/atsatsos/FGG_Bkg_Legacy18_Files/UL18_VLowMass_BkgMC_Diphoton40to80_legacy18test/output_DiPhotonJetsBox_M40_80-Sherpa_spigazzi-Era2018_RR-17Sep2018_v2-legacyRun2FullV2-v0-RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-08dcbeed5736d288ed971f3c5cf5bfe1_USER.root","READ")

t0 = f.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
t1 = f.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_1")
t2 = f.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_2")

u0 = h.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
u1 = h.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_1")
u2 = h.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_2")

mass0 = TH1F("mass0","mass0",100,0,100)
mass0.Sumw2()

mass1 = TH1F("mass1","mass1",100,0,100)
mass1.Sumw2()

mass2 = TH1F("mass2","mass2",100,0,100)
mass2.Sumw2()

mbkg0 = TH1F("mbkg0","mbkg0",100,0,100)
mbkg0.Sumw2()

mbkg1 = TH1F("mbkg1","mbkg1",100,0,100)
mbkg1.Sumw2()

mbkg2 = TH1F("mbkg2","mbkg2",100,0,100)
mbkg2.Sumw2()

t0.Draw("CMS_hgg_mass>>mass0","CMS_hgg_mass>0","goff")
t1.Draw("CMS_hgg_mass>>mass1","CMS_hgg_mass>0","goff")
t2.Draw("CMS_hgg_mass>>mass2","CMS_hgg_mass>0","goff")

u0.Draw("CMS_hgg_mass>>mbkg0","CMS_hgg_mass>0","goff")
u1.Draw("CMS_hgg_mass>>mbkg1","CMS_hgg_mass>0","goff")
u2.Draw("CMS_hgg_mass>>mbkg2","CMS_hgg_mass>0","goff")

print "Background 0: ",mass0.Integral()
print "Background 1: ",mass1.Integral()
print "Background 2: ",mass2.Integral()

mass0.Add(mass1)
mass0.Add(mass2)

print "Background 0-40: ",mass0.Integral()

print "Background 0: ",mbkg0.Integral()
print "Background 1: ",mbkg1.Integral()
print "Background 2: ",mbkg2.Integral()

mbkg0.Add(mbkg1)
mbkg0.Add(mbkg2)

print "Background 40-80: ",mbkg0.Integral()

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1000,800)
c1.cd()

mass0.SetLineColor(1)
#mass0.Scale(303.0*1.0*1.0/(661.0 * 1000.0 * 1.3 * mass0.Integral())) #replace with k-factor and scaling
mass0.Scale(59970.0 * 691.0/200000.0) #normalized by total number of events
#mbkg0.Scale(16101.5*1.0*1.0/(303.2 * 1000.0 * 1.3 * mbkg0.Integral())) #lumi * target xs * br / (xs * br * kf * target lumi * weights)
mbkg0.Scale(59970.0 * 303.2/4881986.0) #normalized by total number of events
mass0.Add(mbkg0)

mass0.Draw("ehist")
mass0.SetYTitle("Accepted Events/GeV")
mass0.SetXTitle("m_{#gamma#gamma} [GeV]")

leg = TLegend(0.6,0.8,0.88,0.88)
leg.AddEntry(mass0,"Untagged 0-80GeV Background Sample")
leg.AddEntry(data0,"5% Partially Unblinded Data")
leg.Draw("same")

c1.SaveAs("mc_gen.png")
c1.SaveAs("mc_gen.pdf")

print "Background 0-80: ",mass0.Integral()
