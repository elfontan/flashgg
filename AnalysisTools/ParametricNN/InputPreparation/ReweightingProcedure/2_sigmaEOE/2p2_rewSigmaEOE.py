# ------------------------------------------------------- #
# Use this script within an environment allowing python3: #
# otherwise problems related to the usage of array might  #
# happen                                                  #
# ------------------------------------------------------- #
from ROOT import * 
from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain
import random, copy
import ROOT, array, CMSGraphics, CMS_lumi
import argparse
import sys
import os

gROOT.SetBatch()
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--minV', dest='minV', default='-0.9', help='Minimum Value for maxPhoId')
argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Maximum Value for maxPhoId')
argparser.add_argument('--log', dest='log', default=False, help='Log scale')
argparser.add_argument('--pre', dest='pre', default=False, help='Pre reweighting')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log
preRew = args.pre

debug = False

norm_dipho = 5.07071342                                                                                                         
norm_sb = (5.07071342*0.02190371141)  
# ----------------------                                                                                                       
# Obtain histogram files                                                                           
# ----------------------                                                            
data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ") 
if (preRew):
    sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/sb_data2018.root","READ")           
else:
    sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/reweightedSb/sb_data2018_plusSigmaEOE.root","READ")           
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080.root","READ")

# Get trees and create histograms for data                                                                           
# ----------------------------------------                                                                                             
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

norm_toData = 1.938285745

# ------------------------ #
# SigmaEOE REWEIGHTING  #
# ------------------------ #
h_sigmaEOE_sba0 = TH1F("h_sigmaEOE_sba0", "h_sigmaEOE_sba0", 100, 0., 0.1)
h_sigmaEOE_pre0 = TH1F("h_sigmaEOE_pre0", "h_sigmaEOE_pre0", 100, 0., 0.1)
h_sigmaEOE_mgg0 = TH1F("h_sigmaEOE_mgg0", "h_sigmaEOE_mgg0", 100, 0., 0.1)
bkg0_sigmaEOE= THStack("bkg0_sigmaEOE","bkg0_sigmaEOE")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

print("----------Opening data tree")
c_dat0 = 0
for ev_dat0 in dat0:
    c_dat0 += 1
    #if (c_dat0 == 10): break
    if (ev_dat0.CMS_hgg_mass > 75): continue
    if (not(c_dat0%20==0)): continue
    if (ev_dat0.dipho_leadIDMVA <= ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_pre0.Fill(ev_dat0.dipho_lead_sigmaEoE, 1.)
    elif (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_pre0.Fill(ev_dat0.dipho_sublead_sigmaEoE, 1.)

print("----------Opening MC dipho tree")
c_mgg0 = 0
for ev_mgg0 in mgg0:
    c_mgg0 += 1
    #if (c_mgg0 == 10): break
    if (ev_mgg0.CMS_hgg_mass < 10): continue
    if (ev_mgg0.CMS_hgg_mass > 75): continue
    if (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_lead_sigmaEoE, ev_mgg0.weight)
    elif (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_sublead_sigmaEoE, ev_mgg0.weight)

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    #if (c_sb0 == 1000): break
    c_sb0 += 1
    #if (not(c_sb0%20==0)): continue
    if (ev_sb0.CMS_hgg_mass > 75): continue
    #print("-------------------------------------------- EVENT ", c_sb0)
    #print ("ORIGINAL SB WEIGHT = ", weight[0])

    if (preRew):
        if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA):
            h_sigmaEOE_sba0.Fill(ev_sb0.dipho_lead_sigmaEoE, ev_sb0.weight)
        elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA):
            h_sigmaEOE_sba0.Fill(ev_sb0.dipho_sublead_sigmaEoE, ev_sb0.weight)
    else:
        if (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA):
            h_sigmaEOE_sba0.Fill(ev_sb0.dipho_lead_sigmaEoE, ev_sb0.weight*ev_sb0.weight_sigmaEOE)
        elif (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA):
            h_sigmaEOE_sba0.Fill(ev_sb0.dipho_sublead_sigmaEoE, ev_sb0.weight*ev_sb0.weight_sigmaEOE)

# Background Scaling: after TFitter                                                                             
h_sigmaEOE_sba0.Scale(norm_sb*0.82)                                                                                     
h_sigmaEOE_mgg0.Scale(norm_dipho*1.68)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()
#c1.SetLeftMargin(0.15)                                                                                                          

#upper plot pad - Data histos                                                                                                       
pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
pad1.Draw()
pad1.cd()
if (logScale):
    pad1.SetLogy()                                                                                                                    
pad1.SetBottomMargin(0.00)
pad1.SetLeftMargin(1.9)

h_sigmaEOE_sba0.GetYaxis().SetTitle("Events")
h_sigmaEOE_sba0.GetYaxis().SetTitleSize(25)
h_sigmaEOE_sba0.GetYaxis().SetTitleFont(43)
h_sigmaEOE_sba0.GetYaxis().SetTitleOffset(2.25)
h_sigmaEOE_sba0.GetYaxis().SetLabelFont(43)
h_sigmaEOE_sba0.GetYaxis().SetLabelOffset(0.01)
h_sigmaEOE_sba0.GetYaxis().SetLabelSize(25)
h_sigmaEOE_sba0.SetLineColor(kYellow-4)
h_sigmaEOE_sba0.SetFillColorAlpha(kYellow-4,0.8)
h_sigmaEOE_sba0.SetLineWidth(2)

h_sigmaEOE_mgg0.SetLineColor(kOrange-4)
h_sigmaEOE_mgg0.SetFillColorAlpha(kOrange-4,0.8)
h_sigmaEOE_mgg0.SetLineWidth(2)

bkg0_sigmaEOE.Add(h_sigmaEOE_mgg0)
bkg0_sigmaEOE.Add(h_sigmaEOE_sba0)
h_sigmaEOE_sba0.GetXaxis().SetLabelOffset(1.5)
h_sigmaEOE_mgg0.GetXaxis().SetLabelOffset(1.5)
h_sigmaEOE_sba0.GetXaxis().SetLabelSize(0)
h_sigmaEOE_mgg0.GetXaxis().SetLabelSize(0)
bkg0_sigmaEOE.Draw("histo")

h_sigmaEOE_mgg0.SetMaximum(30.*h_sigmaEOE_pre0.GetMaximum())
h_sigmaEOE_sba0.SetMaximum(30.*h_sigmaEOE_pre0.GetMaximum())
bkg0_sigmaEOE.SetMaximum(30.*h_sigmaEOE_pre0.GetMaximum())

h_sigmaEOE_pre0.SetLineWidth(2)
h_sigmaEOE_pre0.SetLineColorAlpha(kBlack,0.8)
#h_sigmaEOE_pre0.SetLineColorAlpha(kOrange+9,0.8)
h_sigmaEOE_pre0.GetXaxis().SetLabelSize(0)
h_sigmaEOE_pre0.Draw("epsame")

leg = TLegend(0.2,0.5,0.7,0.88)
leg.AddEntry(h_sigmaEOE_sba0,"#gamma-jet and jet-jet (pf+ff DD)")
leg.AddEntry(h_sigmaEOE_mgg0,"#gamma#gamma MC")
leg.AddEntry(h_sigmaEOE_pre0,"Preselection Region")
leg.SetLineWidth(0)
leg.Draw("same")

c1.Update()
c1.cd()

#lower plot pad - Ratio plot
pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.35)
pad2.SetGridy()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.19)
#pad2.SetLeftMargin(0.11)

#define ratio plot                                                                                                                              
rp = TH1F(h_sigmaEOE_pre0.Clone("rp")) #clone the preselection region                                                                                         
rp.SetLineColor(kBlack)
rp.SetMinimum(0.5)
rp.SetMaximum(1.9)
rp.SetStats(0)
rp.Divide(h_sigmaEOE_sba0+h_sigmaEOE_mgg0) #divide by sideband+mgg                                                                                                     
rp.SetMarkerStyle(20)
rp.SetTitle("")

rp.SetYTitle("Presel / (pf+ff DD + #gamma#gamma MC)")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Minimum #gamma ID MVA #sigma_{E}/E")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(1.3)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
#CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1, 0, 0)

c1.Update()
if (logScale and preRew):
    c1.SaveAs(outputdir+"/minPhoId_sigmaEOE_preReweighting_log.png")
    c1.SaveAs(outputdir+"/minPhoId_sigmaEOE_preReweighting_log.pdf")
elif (logScale):
    c1.SaveAs(outputdir+"/minPhoId_sigmaEOE_reweighted_log.png")
    c1.SaveAs(outputdir+"/minPhoId_sigmaEOE_reweighted_log.pdf")
else:
    c1.SaveAs(outputdir+"/minPhoId_sigmaEOE_reweighted.pdf")
    c1.SaveAs(outputdir+"/minPhoId_sigmaEOE_reweighted.png")

print("MGG: ", h_sigmaEOE_mgg0.Integral())
print("Reweighted sigmaEOE minPhoId: ", h_sigmaEOE_sba0.Integral())
print("Preselection region: ", h_sigmaEOE_pre0.Integral())
