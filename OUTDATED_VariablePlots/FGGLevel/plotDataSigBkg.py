from ROOT import *
import CMS_lumi

#Obtain histogram files
data = TFile("data.root","READ")

mgglow = TFile("mgg_040.root","READ")
mggmed = TFile("mgg_4080.root","READ")
mgghigh = TFile("mgg_80inf.root","READ")

gjlow = TFile("gj_040.root","READ")
gjmed = TFile("gj_4080.root","READ")
gjhighlowpt = TFile("gj_low_80inf.root","READ")
gjhigh = TFile("gj_80inf.root","READ")

qcdlow = TFile("qcd_040.root","READ")
qcdmed = TFile("qcd_4080.root","READ")
qcdhighlowpt = TFile("qcd_low_80inf.root","READ")
qcdhigh = TFile("qcd_80inf.root","READ")

ggh_30 = TFile("ggh_30_sig.root","READ")
ggh_50 = TFile("ggh_50_sig.root","READ")
ggh_70 = TFile("ggh_70_sig.root","READ")

#Create histograms for data, background, and signal, as well as stacked histo for all backgrounds
data0 = data.Get("data0")

mgglow0 = mgglow.Get("mgg040")
mggmed0 = mggmed.Get("mgg4080")
mgghigh0 = mgghigh.Get("mgg80inf")

gjlow0 = gjlow.Get("gj040")
gjmed0 = gjmed.Get("gj4080")
gjhighlowpt0 = gjhighlowpt.Get("gjl80inf")
gjhigh0 = gjhigh.Get("gj80inf")

qcdlow0 = qcdlow.Get("qcd040")
qcdmed0 = qcdmed.Get("qcd4080")
qcdhighlowpt0 = qcdhighlowpt.Get("qcdl80inf")
qcdhigh0 = qcdhigh.Get("qcd80inf")

mgg0 = TH1F("mgg0","mgg0",40,-1,1)
mgg0.Sumw2()
gj0 = TH1F("gj0","gj0",40,-1,1)
gj0.Sumw2()
qcd0 = TH1F("qcd0","qcd0",40,-1,1)
qcd0.Sumw2()
bkg0 = THStack("bkg0","bkg0")

sig30 = ggh_30.Get("ggh_all")
sig50 = ggh_50.Get("ggh_all")
sig70 = ggh_70.Get("ggh_all")

#MC Scale factors and normalization
mgglow0.Scale(1.3) #xs 691.8 pb
mggmed0.Scale(1.3) #xs 303.2 pb
mgghigh0.Scale(1.3) #xs 84.4 pb

gjlow0.Scale(1.0) #xs 2046 pb
gjmed0.Scale(1.0) #xs 3186 pb
gjhighlowpt0.Scale(1.0) #xs 232.9 pb
gjhigh0.Scale(1.0) #xs 878.1 pb

qcdlow0.Scale(1.0) #xs 280600 pb
qcdmed0.Scale(1.0) #xs 241400 pb
qcdhighlowpt0.Scale(1.0) #xs 24810 pb
qcdhigh0.Scale(1.0) #xs 118100 pb

sig30.Scale(5.0)
sig50.Scale(5.0)
sig70.Scale(5.0)

#xs included in cross_sections.json with branching ratios set to 1.0
#Merge histograms from different mass ranges
mgg0.Add(mgglow0)
mgg0.Add(mggmed0)
mgg0.Add(mgghigh0)
gj0.Add(gjlow0)
gj0.Add(gjmed0)
gj0.Add(gjhighlowpt0)
gj0.Add(gjhigh0)
qcd0.Add(qcdlow0)
qcd0.Add(qcdmed0)
qcd0.Add(qcdhighlowpt0)
qcd0.Add(qcdhigh0)

#Data MC scaling
#v1 is using integrals while v2 is using 2018 luminosity (formerly 59.97/fb, now 54.4/fb)

#mcsum=mgg0.Integral()+gj0.Integral()+qcd0.Integral()
#mgg0.Scale(data0.Integral()/mcsum)
#gj0.Scale(data0.Integral()/mcsum)
#qcd0.Scale(data0.Integral()/mcsum)

mgg0.Scale(54.400/20.0)
gj0.Scale(54.400/20.0)
qcd0.Scale(54.400/20.0)

#Now we draw it out
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()

#upper plot pad - Data and MC histos
pad1 = TPad("pad1","pad1", 0, 0.35, 1, 1.0)
pad1.Draw()
pad1.cd()
#pad1.SetLogy()
pad1.SetBottomMargin(0.)
pad1.SetLeftMargin(0.11)

mgg0.SetFillColorAlpha(kOrange+1,0.8)
mgg0.SetLineColorAlpha(kOrange+1,0.8)

gj0.SetFillColorAlpha(kOrange-4,0.8)
gj0.SetLineColorAlpha(kOrange-4,0.8)

qcd0.SetFillColorAlpha(kYellow-7,0.8)
qcd0.SetLineColorAlpha(kYellow-7,0.8)

bkg0.Add(mgg0)
bkg0.Add(gj0)
bkg0.Add(qcd0)
bkg0.Draw("histo")

bkg0.GetXaxis().SetLabelSize(0)

bkg0.GetYaxis().SetTitle("Events")
bkg0.GetYaxis().SetTitleSize(25)
bkg0.GetYaxis().SetTitleFont(43)
bkg0.GetYaxis().SetTitleOffset(2.25)
bkg0.GetYaxis().SetLabelFont(43)
bkg0.GetYaxis().SetLabelSize(25)

data0.SetLineColor(kBlack)
data0.SetLineWidth(2)
data0.Draw("epsame")

data0.GetXaxis().SetLabelSize(0)

data0.GetYaxis().SetTitle("Events")
data0.GetYaxis().SetTitleSize(25)
data0.GetYaxis().SetTitleFont(43)
data0.GetYaxis().SetTitleOffset(2.25)
data0.GetYaxis().SetLabelFont(43)
data0.GetYaxis().SetLabelSize(25)

sig30.SetLineColor(kTeal+3)
sig30.SetLineWidth(2)
sig30.Draw("histsame")

sig30.GetXaxis().SetLabelSize(0)

sig30.GetYaxis().SetTitle("Events")
sig30.GetYaxis().SetTitleSize(25)
sig30.GetYaxis().SetTitleFont(43)
sig30.GetYaxis().SetTitleOffset(2.25)
sig30.GetYaxis().SetLabelFont(43)
sig30.GetYaxis().SetLabelSize(25)

sig50.SetLineColor(kAzure-2)
sig50.SetLineWidth(2)
sig50.Draw("histsame")

sig50.GetXaxis().SetLabelSize(0)

sig50.GetYaxis().SetTitle("Events")
sig50.GetYaxis().SetTitleSize(25)
sig50.GetYaxis().SetTitleFont(43)
sig50.GetYaxis().SetTitleOffset(2.25)
sig50.GetYaxis().SetLabelFont(43)
sig50.GetYaxis().SetLabelSize(25)

sig70.SetLineColor(kBlue+1)
sig70.SetLineWidth(2)
sig70.Draw("histsame")

sig70.GetXaxis().SetLabelSize(0)

sig70.GetYaxis().SetTitle("Events")
sig70.GetYaxis().SetTitleSize(25)
sig70.GetYaxis().SetTitleFont(43)
sig70.GetYaxis().SetTitleOffset(2.25)
sig70.GetYaxis().SetLabelFont(43)
sig70.GetYaxis().SetLabelSize(25)

leg = TLegend(0.65,0.6,0.85,0.85)
leg.AddEntry(data0,"Data")
leg.AddEntry(mgg0,"#gamma-#gamma")
leg.AddEntry(gj0,"#gamma-jet")
leg.AddEntry(qcd0,"jet-jet")
leg.AddEntry(sig30,"ggH 30GeV x5")
leg.AddEntry(sig50,"ggH 50GeV x5")
leg.AddEntry(sig70,"ggH 70GeV x5")
leg.Draw("same")

c1.Update()
c1.cd()

#lower plot pad - Ratio plot
pad2 = TPad("pad2","pad2", 0, 0.05, 1, 0.35)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.17)
pad2.SetLeftMargin(0.11)

#define ratio plot
rp = TH1F(data0.Clone("rp")) #clone the data
rp.SetLineColor(kBlack)
rp.SetMinimum(0.5)
rp.SetMaximum(2.)
rp.SetStats(0)
rp.Divide(TH1F(mgg0+gj0+qcd0))   #divide by MC
rp.SetMarkerStyle(24)
rp.SetTitle("") 

rp.SetYTitle("Data/Bkg MC")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("cos(#Delta#phi)")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(3.9)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1, 0, 0)
c1.Update()

c1.SaveAs("DataMCSig_CosPhi.png")
c1.SaveAs("DataMCSig_CosPhi.pdf")

print("Data: ",data0.Integral())
print("MGG: ",mgg0.Integral())
print("GJet: ",gj0.Integral())
print("QCD: ",qcd0.Integral())
print("GGH 30: ",sig30.Integral())
print("GGH 50: ",sig50.Integral())
print("GGH 70: ",sig70.Integral())
