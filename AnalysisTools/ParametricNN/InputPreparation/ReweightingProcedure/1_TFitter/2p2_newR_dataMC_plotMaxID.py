from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--minV', dest='minV', default='-0.9', help='Minimum Value for maxPhoId')
argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Maximum Value for maxPhoId')
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log


norm_dipho = 5.07071342                                                                                  
norm_sb = (5.07071342*0.02190371141)

# ----------------------
# Obtain histogram files
# ----------------------                                                                                                                               
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ") 
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/sb_data2018.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")                   

# Get trees and create histograms for data                                                                   
# ----------------------------------------                                                                                  
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg080 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

sbb0 = TH1F("sbb0","sbb0",34,-0.7,1) #Min ID in sideband before reweight
sbb0.Sumw2()
sba0 = TH1F("sba0","sba0",34,-0.7,1) #Min ID in sideband after reweight - replaces GJet and QCD
sba0.Sumw2()
pre0 = TH1F("pre0","pre0",34,-0.7,1) #Min ID in preselection region
pre0.Sumw2()
mgg0 = TH1F("mgg0","mgg0",34,-0.7,1) #Diphoton MC in preselection region
mgg0.Sumw2()
bkg0 = THStack("bkg0","bkg0")

#Sideband/Presel regions: CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7 && event%20==0
# -----------------------------------------------------------------------------------------------------
#sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>sbb0","CMS_hgg_mass<75 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=0.9","goff")
#sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>sba0","weight*weight_leadSublead_all * (CMS_hgg_mass<75 && event%20==0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=0.9)","goff")
#dat0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>pre0","CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=0.9 && event%20==0","goff")
#mgg080.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>mgg0","weight*(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=0.9)","goff")
sb0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>sbb0","CMS_hgg_mass<75","goff")
sb0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>sba0","weight * (CMS_hgg_mass<75)","goff")
dat0.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>pre0","CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7 && event%20==0","goff")
mgg080.Draw("max(dipho_leadIDMVA,dipho_subleadIDMVA)>>mgg0","weight*(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>=-0.7)","goff")

# Background Scaling: after TFitter                                         
sbb0.Scale(norm_sb*0.82)                                
sba0.Scale(norm_sb*0.82)                                        
mgg0.Scale(norm_dipho*1.68)

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()

pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
pad1.Draw()
pad1.cd()
if (logScale):
    pad1.SetLogy()                                                                                                                    
pad1.SetBottomMargin(0.0)
pad1.SetLeftMargin(4.5)

sba0.SetLineColor(kYellow-7)
sba0.SetFillColorAlpha(kYellow-7,0.8)
sba0.SetLineWidth(2)

sba0.GetYaxis().SetTitle("Events/0.05")
sba0.GetYaxis().SetTitleSize(25)
sba0.GetYaxis().SetTitleFont(43)
sba0.GetYaxis().SetTitleOffset(0.9)
sba0.GetYaxis().SetLabelFont(43)
sba0.GetYaxis().SetLabelOffset(0.01)
sba0.GetYaxis().SetLabelSize(25)

mgg0.SetLineColor(kOrange-4)
mgg0.SetFillColorAlpha(kOrange-4,0.8)
mgg0.SetLineWidth(2)

#bkg0.GetXaxis().SetLabelSize(0)
sba0.GetXaxis().SetLabelSize(0)
mgg0.GetXaxis().SetLabelSize(0)

bkg0.Add(mgg0)
bkg0.Add(sba0)
bkg0.Draw("histo")

if (logScale):
    mgg0.SetMaximum(5*pre0.GetMaximum())
    sba0.SetMaximum(5*pre0.GetMaximum())
    sbb0.SetMaximum(5*pre0.GetMaximum())
    bkg0.SetMaximum(5*pre0.GetMaximum())
else:
    mgg0.SetMaximum(1.3*pre0.GetMaximum())
    sba0.SetMaximum(1.3*pre0.GetMaximum())
    sbb0.SetMaximum(1.3*pre0.GetMaximum())
    bkg0.SetMaximum(1.3*pre0.GetMaximum())

pre0.SetLineWidth(2)
pre0.SetLineColorAlpha(kBlack,0.8)
pre0.Draw("epsame")

sbb0.SetLineColor(kOrange-1)
sbb0.SetLineWidth(2)
sbb0.Draw("histosame")

leg = TLegend(0.25,0.5,0.75,0.88)
leg.AddEntry(sbb0,"Unweighted Sideband")
leg.AddEntry(sba0,"#gamma-jet and jet-jet (Reweighted Sideband)")
leg.AddEntry(mgg0,"Diphoton MC")
leg.AddEntry(pre0,"Preselection Region")
leg.SetLineWidth(0)
leg.Draw("same")

c1.Update()
c1.cd()

pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.345)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.19)
#pad2.SetLeftMargin(0.1)

rp = TH1F(pre0.Clone("rp")) #clone the preselection region                                                                                         
rp.SetLineColor(kBlack)
rp.SetMinimum(0.3)
rp.SetMaximum(1.8)
rp.SetStats(0)
rp.Divide(sba0+mgg0) #divide by sideband+mgg                                                                                                     
rp.SetMarkerStyle(20)
rp.SetTitle("")

rp.SetYTitle("Presel / (pf+ff DD + #gamma#gamma MC)")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Maximum #gamma ID MVA")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(1.6)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()
c1.cd()

# CMS lumi info
# -------------
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1, 0, 0)

c1.Update()
if (logScale):
    c1.SaveAs(outputdir+"/maxPhoID_log.png")
    c1.SaveAs(outputdir+"/maxPhoID_log.pdf")
else:
    c1.SaveAs(outputdir+"/maxPhoID.png")
    c1.SaveAs(outputdir+"/maxPhoID.pdf")

print("MGG: ", mgg0.Integral())
print("Reweight: ", sba0.Integral())
print("Preselect: ", pre0.Integral())
print("Unweighted Sideband:", sbb0.Integral())
