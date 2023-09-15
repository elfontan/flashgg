from ROOT import *
import CMS_lumi

#Obtain histogram files
gjlow = TFile("gj_040.root","READ")
gjmed = TFile("gj_4080.root","READ")
gjhighlowpt = TFile("gj_low_80inf.root","READ")
gjhigh = TFile("gj_80inf.root","READ")

#qcdlow = TFile("qcd_040.root","READ")
qcdmed = TFile("qcd_4080.root","READ")
qcdhighlowpt = TFile("qcd_low_80inf.root","READ")
qcdhigh = TFile("qcd_80inf.root","READ")

#Create histograms for data, background, and signal, as well as stacked histo for all backgrounds
gjlow0 = gjlow.Get("gj040")
gjmed0 = gjmed.Get("gj4080")
gjhighlowpt0 = gjhighlowpt.Get("gjl80inf")
gjhigh0 = gjhigh.Get("gj80inf")

#qcdlow0 = qcdlow.Get("qcd040")
qcdmed0 = qcdmed.Get("qcd4080")
qcdhighlowpt0 = qcdhighlowpt.Get("qcdl80inf")
qcdhigh0 = qcdhigh.Get("qcd80inf")

gj0 = TH1F("gj0","gj0",38,-0.9,1)
gj0.Sumw2()
qcd0 = TH1F("qcd0","qcd0",38,-0.9,1)
qcd0.Sumw2()
bkg0 = THStack()
#bkg0 = TH1F("bkg0","bkg0",38,-0.9,1)
#bkg0.Sumw2()

#Merge histograms from different mass ranges
gj0.Add(gjlow0)
gj0.Add(gjmed0)
gj0.Add(gjhighlowpt0)
gj0.Add(gjhigh0)
#qcd0.Add(qcdlow0)
qcd0.Add(qcdmed0)
qcd0.Add(qcdhighlowpt0)
qcd0.Add(qcdhigh0)

#Now we draw it out
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()

c1.SetBottomMargin(0.11)
c1.SetLeftMargin(0.11)

#bkg0.SetFillColorAlpha(kOrange-4,0.8)
#bkg0.SetLineColorAlpha(kOrange-4,0.8)

gj0.SetFillColorAlpha(kOrange-4,0.8)
gj0.SetLineColorAlpha(kOrange-4,0.8)
qcd0.SetFillColorAlpha(kYellow-7,0.8)
qcd0.SetLineColorAlpha(kYellow-7,0.8)

bkg0.Add(gj0)
bkg0.Add(qcd0)
bkg0.Draw("histo")

bkg0.GetXaxis().SetTitle("Min #gamma ID MVA")
bkg0.GetXaxis().SetTitleSize(25)
bkg0.GetXaxis().SetTitleFont(43)
bkg0.GetXaxis().SetTitleOffset(1.75)
bkg0.GetXaxis().SetLabelFont(43)
bkg0.GetXaxis().SetLabelOffset(0.01)
bkg0.GetXaxis().SetLabelSize(25)

bkg0.GetYaxis().SetTitle("Events")
bkg0.GetYaxis().SetTitleSize(25)
bkg0.GetYaxis().SetTitleFont(43)
bkg0.GetYaxis().SetTitleOffset(2.25)
bkg0.GetYaxis().SetLabelFont(43)
bkg0.GetYaxis().SetLabelOffset(0.01)
bkg0.GetYaxis().SetLabelSize(25)

#bkg0.SaveAs("minid_gjetqcd40.root")

leg = TLegend(0.65,0.78,0.85,0.85)
#leg.AddEntry(bkg0,"Events with 1+ jets")
leg.AddEntry(gj0,"#gamma-jet")
leg.AddEntry(qcd0,"jet-jet")
leg.Draw("same")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary Simulation"
CMS_lumi.lumi_sqrtS     = "13 TeV"
CMS_lumi.cmsTextSize    = 0.4
CMS_lumi.lumiTextSize   = 0.35
CMS_lumi.extraOverCmsTextSize = 0.8
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)
c1.Update()

c1.SaveAs("MinIDMVA_GJetQCD40andUp_Stack.png")
c1.SaveAs("MinIDMVA_GJetQCD40andUp_Stack.pdf")

print("GJet: ",gj0.Integral())
print("QCD: ",qcd0.Integral())
