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
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
logScale = args.log

# Obtain histogram files
# ----------------------
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/data/EGamma_D.root","READ") #Data with unweighted events, both regions
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/reweighting/kest/output_sideband_PF_kest1D_Inclusive.root","READ")
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_dipho/diPhoton_all.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")


# ------------------------ #
# REWEIGHTING: SigmaEOverE #
# ------------------------ #
h_sigmaEOE_sba0 = TH1F("h_sigmaEOE_sba0", "h_sigmaEOE_sba0", 100, 0., 0.1)
h_sigmaEOE_pre0 = TH1F("h_sigmaEOE_pre0", "h_sigmaEOE_pre0", 100, 0., 0.1)
h_sigmaEOE_mgg0 = TH1F("h_sigmaEOE_mgg0", "h_sigmaEOE_mgg0", 100, 0., 0.1)
#h_sigmaEOE_sba0 = TH1F("h_sigmaEOE_sba0", "h_sigmaEOE_sba0", 200, 0., 0.2)
#h_sigmaEOE_pre0 = TH1F("h_sigmaEOE_pre0", "h_sigmaEOE_pre0", 200, 0., 0.2)
#h_sigmaEOE_mgg0 = TH1F("h_sigmaEOE_mgg0", "h_sigmaEOE_mgg0", 200, 0., 0.2)
bkg0 = THStack("bkg0","bkg0")

print("----------Opening sideband tree")
c_sb0 = 0
for ev_sb0 in sb0:
    c_sb0 += 1
    #if (not(c_sb0%20==0)): continue
    if (ev_sb0.dipho_leadIDMVA > ev_sb0.dipho_subleadIDMVA):
        #h_sigmaEOE_sba0.Fill(ev_sb0.dipho_lead_sigmaEoE, ev_sb0.weight*0.7*1.88*5./100)
        h_sigmaEOE_sba0.Fill(ev_sb0.dipho_lead_sigmaEoE, ev_sb0.weight*0.0622)
    elif (ev_sb0.dipho_leadIDMVA <= ev_sb0.dipho_subleadIDMVA):
        #h_sigmaEOE_sba0.Fill(ev_sb0.dipho_sublead_sigmaEoE, ev_sb0.weight*0.7*1.88*5./100)
        h_sigmaEOE_sba0.Fill(ev_sb0.dipho_sublead_sigmaEoE, ev_sb0.weight*0.0622)
print("h_sigmaEOE_sba0 Integral = ", h_sigmaEOE_sba0.Integral())

print("----------Opening data tree")
c_dat0 = 0
for ev_dat0 in dat0:
    c_dat0 += 1
    if (not(c_dat0%20==0)): continue
    if (ev_dat0.dipho_leadIDMVA > ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_pre0.Fill(ev_dat0.dipho_lead_sigmaEoE)
    elif (ev_dat0.dipho_leadIDMVA <= ev_dat0.dipho_subleadIDMVA and min(ev_dat0.dipho_leadIDMVA, ev_dat0.dipho_subleadIDMVA)>-0.7):
        h_sigmaEOE_pre0.Fill(ev_dat0.dipho_sublead_sigmaEoE)
print("h_sigmaEOE_pre0 Integral = ", h_sigmaEOE_pre0.Integral())

print("----------Opening MC dipho tree")
for ev_mgg0 in mgg0:
    if (ev_mgg0.dipho_leadIDMVA > ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        #h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_lead_sigmaEoE, ev_mgg0.weight*2.2*1.88)
        h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_lead_sigmaEoE, ev_mgg0.weight*5.9546)
    elif (ev_mgg0.dipho_leadIDMVA <= ev_mgg0.dipho_subleadIDMVA and min(ev_mgg0.dipho_leadIDMVA, ev_mgg0.dipho_subleadIDMVA)>-0.7):
        #h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_sublead_sigmaEoE, ev_mgg0.weight*2.2*1.88)
        h_sigmaEOE_mgg0.Fill(ev_mgg0.dipho_sublead_sigmaEoE, ev_mgg0.weight*5.9546)
print("h_sigmaEOE_mgg0 Integral = ", h_sigmaEOE_mgg0.Integral())

# Set Maximum
if (logScale):
    h_sigmaEOE_sba0.SetMaximum(500000)
    h_sigmaEOE_pre0.SetMaximum(500000)
    h_sigmaEOE_mgg0.SetMaximum(500000)
    bkg0.SetMaximum(500000)
else:
    bkg0.SetMaximum(25000)

#Now we draw it out                                                                                                                          
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1200,1200)
c1.cd()
#c1.SetLeftMargin(0.15)                                                                                                          

#upper plot pad - Data histos                                                                                                       
pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
pad1.Draw()
pad1.cd()
if (logScale):
    pad1.SetLogy()                                                                                                                    
pad1.SetBottomMargin(0.01)
pad1.SetLeftMargin(1.9)

h_sigmaEOE_sba0.SetLineColor(kYellow-7)
h_sigmaEOE_sba0.SetFillColorAlpha(kYellow-7,0.8)
h_sigmaEOE_sba0.SetLineWidth(2)

h_sigmaEOE_sba0.GetYaxis().SetTitle("Events/0.001 GeV")
h_sigmaEOE_sba0.GetYaxis().SetTitleSize(25)
h_sigmaEOE_sba0.GetYaxis().SetTitleFont(43)
h_sigmaEOE_sba0.GetYaxis().SetTitleOffset(2.25)
h_sigmaEOE_sba0.GetYaxis().SetLabelFont(43)
h_sigmaEOE_sba0.GetYaxis().SetLabelOffset(0.01)
h_sigmaEOE_sba0.GetYaxis().SetLabelSize(25)

h_sigmaEOE_mgg0.SetLineColor(kOrange-4)
h_sigmaEOE_mgg0.SetFillColorAlpha(kOrange-4,0.8)
h_sigmaEOE_mgg0.SetLineWidth(2)

bkg0.Add(h_sigmaEOE_mgg0)
bkg0.Add(h_sigmaEOE_sba0)
h_sigmaEOE_sba0.GetXaxis().SetLabelOffset(1.5)
h_sigmaEOE_mgg0.GetXaxis().SetLabelOffset(1.5)
h_sigmaEOE_sba0.GetXaxis().SetLabelSize(0)
h_sigmaEOE_mgg0.GetXaxis().SetLabelSize(0)
bkg0.Draw("histo")

h_sigmaEOE_pre0.SetLineWidth(2)
h_sigmaEOE_pre0.SetLineColorAlpha(kBlack,0.8)
#h_sigmaEOE_pre0.SetLineColorAlpha(kOrange+9,0.8)
h_sigmaEOE_pre0.GetXaxis().SetLabelSize(0)
h_sigmaEOE_pre0.Draw("epsame")

leg = TLegend(0.2,0.5,0.7,0.88)
leg.AddEntry(h_sigmaEOE_sba0,"#gamma-jet and jet-jet (Reweighted Sideband)")
leg.AddEntry(h_sigmaEOE_mgg0,"Diphoton MC")
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
pad2.SetBottomMargin(0.17)
pad2.SetLeftMargin(0.11)

#define ratio plot                                                                                                                              
rp = TH1F(h_sigmaEOE_pre0.Clone("rp")) #clone the preselection region                                                                                         
rp.SetLineColor(kBlack)
rp.SetMinimum(0.5)
rp.SetMaximum(1.9)
rp.SetStats(0)
rp.Divide(h_sigmaEOE_sba0+h_sigmaEOE_mgg0) #divide by sideband+mgg                                                                                                     
rp.SetMarkerStyle(24)
rp.SetTitle("")

rp.SetYTitle("Reweighted SB/Presel")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(25)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(2.25)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(25)

rp.SetXTitle("Max #gamma ID MVA #sigma_{E}/E")
rp.GetXaxis().SetTitleSize(25)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(3.9)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(25)
rp.GetXaxis().SetLabelOffset(0.02)

rp.Draw("ep")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "1.6 fb^{-1} (13 TeV)"
#CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1, 0, 0)

c1.Update()
if (logScale):
    c1.SaveAs(outputdir+"/sigmaEoE_maxPhoId_log.png")
    c1.SaveAs(outputdir+"/sigmaEoE_maxPhoId_log.pdf")
else:
    c1.SaveAs(outputdir+"/sigmaEoE_maxPhoId.png")
    c1.SaveAs(outputdir+"/sigmaEoE_maxPhoId.pdf")

print "MGG: ", h_sigmaEOE_mgg0.Integral()
print "Reweight: ", h_sigmaEOE_sba0.Integral()
print "Preselect: ", h_sigmaEOE_pre0.Integral()
