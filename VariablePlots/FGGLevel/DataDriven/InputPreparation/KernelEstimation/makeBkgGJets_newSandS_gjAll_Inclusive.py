from ROOT import *
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, random, copy
from ROOT import TFile, TTree, TList
import argparse
import sys
import os
import math

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--minV', dest='minV', default='-0.9', help='Output dir')
argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Output dir')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV

mva_minimum = -0.9
mva_maximum = 1.0
binning = int(math.ceil((mva_maximum - mva_minimum) / 0.05))

f_gj040 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_gjets/GJets_MGG0to40.root","READ")
f_gj4080 = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_gjets/GJets_MGG40to80.root","READ")
f_gj80Inf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_Oct2023/bkg_gjets/GJets_MGG80toInf.root","READ")

t_gj040 = f_gj040.Get("tagsDumper/trees/gjets_promptfake_13TeV_UntaggedTag_0")
t_gj4080 = f_gj4080.Get("tagsDumper/trees/gjets_promptfake_13TeV_UntaggedTag_0")
t_gj80Inf = f_gj80Inf.Get("tagsDumper/trees/gjets_promptfake_13TeV_UntaggedTag_0")

# Create histograms as well as stacked histo for all backgrounds
# --------------------------------------------------------------
gjAll = TH1F("gjAll","gjAll",binning,mva_minimum,mva_maximum)
gjAll.Sumw2()
gj040 = TH1F("gj040","gj040",binning,mva_minimum,mva_maximum)
gj040.Sumw2()
gj4080 = TH1F("gj4080","gj4080",binning,mva_minimum,mva_maximum)
gj4080.Sumw2()
gj80Inf = TH1F("gj80Inf","gj80Inf",binning,mva_minimum,mva_maximum)
gj80Inf.Sumw2()

# Weighted: weight*(CMS_hgg_mass>0)
# Sideband/Presel regions: weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7)
# ----------------------------------------------------------------------------------------------------
t_gj040.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj040","weight*(CMS_hgg_mass>0 && max(dipho_leadIDMVA,dipho_subleadIDMVA) > "+minValue+" && max(dipho_leadIDMVA,dipho_subleadIDMVA) < "+maxValue+")","goff")
t_gj4080.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj4080","weight*(CMS_hgg_mass>0 && max(dipho_leadIDMVA,dipho_subleadIDMVA) > "+minValue+" && max(dipho_leadIDMVA,dipho_subleadIDMVA) < "+maxValue+")","goff")
t_gj80Inf.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>gj80Inf","weight*(CMS_hgg_mass>0 && max(dipho_leadIDMVA,dipho_subleadIDMVA) > "+minValue+" && max(dipho_leadIDMVA,dipho_subleadIDMVA) < "+maxValue+")","goff")

gjAll.Add(gj040)
gjAll.Add(gj4080)
gjAll.Add(gj80Inf)

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

gjAll.SetFillColor(kOrange-3)
gjAll.SetLineColor(kBlack)
gjAll.GetYaxis().SetTitle("Events Accepted")
gjAll.SaveAs("newSandS_gjAll_Inclusive.root")

print("GJet: ",gjAll.Integral())
