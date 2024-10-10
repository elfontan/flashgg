#!/usr/bin/env python3
# ********************************
# usage: 
#   python3 newEffAccSigFrac_fiveCat.py --indir /eos/home-e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat_evaluateAt70GeV/AlternativeCategorization/
#           --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/paramNN/nearest_flat/postPreapprTESTS/evaluateAt70GeV/ --pnn evaluateAt70GeV
#    (e.g. from CMSSW_12_4_0/src)
# ********************************

import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem
#from ROOT import *
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooDataHist, RooCBShape, RooNumConvPdf, RooFFTConvPdf
from ROOT import RooCmdArg, RooArgSet, kFALSE, RooLinkedList, kBlue, kRed, kBlack, kOpenStar, kWhite, kGray
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan
from array import array
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import mplhep as hep
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
#argparser.add_argument('--indir', dest='indir', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/V0_gghSig_Systematics_4Cat/', help='Input dir')
argparser.add_argument('--indir', dest='indir', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/gghSig_Systematics_4Cat_noNNLOPS/', help='Input dir')
#argparser.add_argument('--indir', dest='indir', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/gghSig_Systematics_5Cat/', help='Input dir')
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--pnn', dest='pnn', default='4CAT_evaluateAt70GeV', help='PNN evaluation scenario')

args = argparser.parse_args()
inputdir = args.indir
outputdir = args.outdir
scenario = args.pnn

sumWeights = [
    2392920365,
    1016927033,
    827714741,
    574957193,
    388731517,
    324710820,
    204436567,
    177961342,
    50998061,
    43936195,
    38296075,
    80316773,
    58598074
]

nEv = [
    1086478,
    594543,
    594640,
    502972,
    403910,
    404201,
    299370,
    302974,
    100752,
    100581,
    99832,
    232630,
    190139
]

filelist = [
    inputdir+"ggH_M10_cat.root",
    inputdir+"ggH_M15_cat.root",
    inputdir+"ggH_M20_cat.root",
    inputdir+"ggH_M25_cat.root",
    inputdir+"ggH_M30_cat.root",
    inputdir+"ggH_M35_cat.root",
    inputdir+"ggH_M40_cat.root",
    inputdir+"ggH_M45_cat.root",
    inputdir+"ggH_M50_cat.root",
    inputdir+"ggH_M55_cat.root",
    inputdir+"ggH_M60_cat.root",
    inputdir+"ggH_M65_cat.root",
    inputdir+"ggH_M70_cat.root"
]

# NOTE: Weight computation
#       1) Event weight after lumi weight = xsec_ggh_M70 * br_hgg_M70 * kf_M70 / nEvents_M70
#       2) * genW (== Number of generated events/(n_pos - n_neg))  
target_lumi = 1000.0 #pb

masspoints = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

xs = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
br = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
kf = [1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06]

v_eff = []
v_eff_cat0 = []
v_eff_cat1 = []
v_eff_cat2 = []
v_eff_cat3 = []
v_eff_err = []
v_eff_cat0_err = []
v_eff_cat1_err = []
v_eff_cat2_err = []
v_eff_cat3_err = []
v_sigFract = []
v_sigFract_cat0 = []
v_sigFract_cat1 = []
v_sigFract_cat2 = []
v_sigFract_cat3 = []

for m in range(len(filelist)):
    f_ggH = TFile.Open(filelist[m]) 

    print("Reading file", filelist[m],"...")
    
    treename_cat0 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_0")
    treename_cat1 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_1")
    treename_cat2 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_2")
    treename_cat3 = f_ggH.Get("tagsDumper/trees/ggh_"+str(masspoints[m])+"_13TeV_UntaggedTag_3")
    
    ggh_cat0 = TH1F("ggh_M"+str(masspoints[m])+"_cat0", "ggh_M"+str(masspoints[m])+"_cat0", 900, 0., 900.)
    ggh_cat0.Sumw2()
    ggh_cat1 = TH1F("ggh_M"+str(masspoints[m])+"_cat1", "ggh_M"+str(masspoints[m])+"_cat1", 900, 0., 900.)
    ggh_cat1.Sumw2()
    ggh_cat2 = TH1F("ggh_M"+str(masspoints[m])+"_cat2", "ggh_M"+str(masspoints[m])+"_cat2", 900, 0., 900.)
    ggh_cat2.Sumw2()
    ggh_cat3 = TH1F("ggh_M"+str(masspoints[m])+"_cat3", "ggh_M"+str(masspoints[m])+"_cat3", 900, 0., 900.)
    ggh_cat3.Sumw2()
    den = TH1F("ggh_M"+str(masspoints[m])+"_den", "ggh_M"+str(masspoints[m])+"_den", 900, 0., 900.)
    den.Sumw2()
    sumw0 = TH1F("ggh_M"+str(masspoints[m])+"_sumw0", "ggh_M"+str(masspoints[m])+"_sumw0", 900, 0., 900.)
    sumw0.Sumw2()
    sumw1 = TH1F("ggh_M"+str(masspoints[m])+"_sumw1", "ggh_M"+str(masspoints[m])+"_sumw1", 900, 0., 900.)
    sumw1.Sumw2()
    sumw2 = TH1F("ggh_M"+str(masspoints[m])+"_sumw2", "ggh_M"+str(masspoints[m])+"_sumw2", 900, 0., 900.)
    sumw2.Sumw2()
    sumw3 = TH1F("ggh_M"+str(masspoints[m])+"_sumw3", "ggh_M"+str(masspoints[m])+"_sumw3", 900, 0., 900.)
    sumw3.Sumw2()
    sumw = TH1F("ggh_M"+str(masspoints[m])+"_sumw", "ggh_M"+str(masspoints[m])+"_sumw", 900, 0., 900.)
    sumw.Sumw2()

    #treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat0", "(CMS_hgg_mass>0)")
    #treename_cat1.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat1", "(CMS_hgg_mass>0)")
    #treename_cat2.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat2", "(CMS_hgg_mass>0)")
    #treename_cat3.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat3", "(CMS_hgg_mass>0)")
    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat0", "weight*(CMS_hgg_mass>0)")
    treename_cat1.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat1", "weight*(CMS_hgg_mass>0)")
    treename_cat2.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat2", "weight*(CMS_hgg_mass>0)")
    treename_cat3.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat3", "weight*(CMS_hgg_mass>0)")
    #treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat0", "weight*(CMS_hgg_mass>0) / 1000.")
    #treename_cat1.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat1", "weight*(CMS_hgg_mass>0) / 1000.")
    #treename_cat2.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat2", "weight*(CMS_hgg_mass>0) / 1000.")
    #treename_cat3.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_cat3", "weight*(CMS_hgg_mass>0) / 1000.")
    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_den", "(CMS_hgg_mass>0)")
    treename_cat1.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_den", "(CMS_hgg_mass>0)")
    treename_cat2.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_den", "(CMS_hgg_mass>0)")
    treename_cat3.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_den", "(CMS_hgg_mass>0)")
    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_sumw0", "weight*(CMS_hgg_mass>0)")
    treename_cat1.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_sumw1", "weight*(CMS_hgg_mass>0)")
    treename_cat2.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_sumw2", "weight*(CMS_hgg_mass>0)")
    treename_cat3.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_sumw3", "weight*(CMS_hgg_mass>0)")
    treename_cat0.Draw("CMS_hgg_mass>>ggh_M"+str(masspoints[m])+"_sumw", "weight*(CMS_hgg_mass>0)")
    treename_cat1.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_sumw", "weight*(CMS_hgg_mass>0)")
    treename_cat2.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_sumw", "weight*(CMS_hgg_mass>0)")
    treename_cat3.Draw("CMS_hgg_mass>>+ggh_M"+str(masspoints[m])+"_sumw", "weight*(CMS_hgg_mass>0)")

    print("NUM Integral (cat0) = ", )
    ev_cat0 = ggh_cat0.Integral()
    ev_cat1 = ggh_cat1.Integral()
    ev_cat2 = ggh_cat2.Integral()
    ev_cat3 = ggh_cat3.Integral()
    ev_sumCat0123 = ev_cat0 + ev_cat1 + ev_cat2 + ev_cat3

    v_sigFract_cat0.append(ev_cat0/ev_sumCat0123*100)
    v_sigFract_cat1.append(ev_cat1/ev_sumCat0123*100)
    v_sigFract_cat2.append(ev_cat2/ev_sumCat0123*100)
    v_sigFract_cat3.append(ev_cat3/ev_sumCat0123*100)

    print("#################### MASS ", str(masspoints[m]), "######################")
    print("SUM\t", round(ev_sumCat0123, 1))
    eff = round((ev_cat0 + ev_cat1 + ev_cat2 + ev_cat3)/(xs[m] * br[m] * kf[m] * target_lumi)*100 , 2)
    eff_cat0 = round((ev_cat0/(xs[m] * br[m] * kf[m] * target_lumi))*100 , 2)
    eff_cat1 = round((ev_cat1/(xs[m] * br[m] * kf[m] * target_lumi))*100 , 2)
    eff_cat2 = round((ev_cat2/(xs[m] * br[m] * kf[m] * target_lumi))*100 , 2)
    eff_cat3 = round((ev_cat3/(xs[m] * br[m] * kf[m] * target_lumi))*100 , 2)
    eff = round((ev_cat0 + ev_cat1 + ev_cat2 + ev_cat3) /(xs[m] * br[m] * kf[m] * target_lumi)*100 , 2)
    #eff_cat0 = round((ev_cat0) /(xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m])*100 , 2)
    #eff_cat1 = round((ev_cat1) /(xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m])*100 , 2)
    #eff_cat2 = round((ev_cat2) /(xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m])*100 , 2)
    #eff_cat3 = round((ev_cat3) /(xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m])*100 , 2)
    #eff = round((ev_cat0 + ev_cat1 + ev_cat2)  /(xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m])*100 , 2)
    #eff_cat0 = round((ev_cat0) * nEvents[m]/sumW[m] /(xs[m] * br[m] * kf[m] * target_lumi * genW[m])*100 , 2)
    #eff_cat1 = round((ev_cat1) * nEvents[m]/sumW[m] /(xs[m] * br[m] * kf[m] * target_lumi * genW[m])*100 , 2)
    #eff_cat2 = round((ev_cat2) * nEvents[m]/sumW[m] /(xs[m] * br[m] * kf[m] * target_lumi * genW[m])*100 , 2)

    print("sumw cat0= ", ev_cat0)
    print("sumw cat1= ", ev_cat1)
    print("sumw cat2= ", ev_cat2)
    print("sumw cat3= ", ev_cat3)
    print("sumw TOT = ", ev_cat0+ev_cat1+ev_cat2+ev_cat3)
    #print("ea cat0 = ", eff_cat0)
    #print("ea cat1 = ", eff_cat1)
    #print("ea cat2 = ", eff_cat2)
    #print("ea cat3 = ", eff_cat3)
    #print("ea cat0 = ", (ev_cat0) / (xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m]))
    #print("ea cat1 = ", (ev_cat1) / (xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m]))
    #print("ea cat2 = ", (ev_cat2) / (xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m]))
    #print("ea cat3 = ", (ev_cat3) / (xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m]))

    v_eff.append(eff)
    v_eff_cat0.append(eff_cat0)
    v_eff_cat1.append(eff_cat1)
    v_eff_cat2.append(eff_cat2) 
    v_eff_cat3.append(eff_cat3) 
    v_eff_err.append(ROOT.sqrt(ggh_cat0.Integral()+ggh_cat1.Integral()+ggh_cat2.Integral()+ggh_cat3.Integral()) /(xs[m]*br[m] * kf[m] * target_lumi))
    v_eff_cat0_err.append(ROOT.sqrt(ggh_cat0.Integral()) / (xs[m] * br[m] * kf[m] * target_lumi))
    v_eff_cat1_err.append(ROOT.sqrt(ggh_cat1.Integral()) / (xs[m] * br[m] * kf[m] * target_lumi))
    v_eff_cat2_err.append(ROOT.sqrt(ggh_cat2.Integral()) / (xs[m] * br[m] * kf[m] * target_lumi))
    v_eff_cat3_err.append(ROOT.sqrt(ggh_cat3.Integral()) / (xs[m] * br[m] * kf[m] * target_lumi))
    #v_eff_err.append(ROOT.sqrt(ggh_cat0.Integral()+ggh_cat1.Integral()+ggh_cat2.Integral())*nEvents[m]/sumW[m] /(xs[m]*br[m] * kf[m] * target_lumi * genW[m])*100)
    #v_eff_cat0_err.append(ROOT.sqrt(ggh_cat0.Integral())* nEvents[m]/sumW[m] /(xs[m] * br[m] * kf[m] * target_lumi * genW[m])*100)
    #v_eff_cat1_err.append(ROOT.sqrt(ggh_cat1.Integral())* nEvents[m]/sumW[m] /(xs[m] * br[m] * kf[m] * target_lumi * genW[m])*100)
    #v_eff_cat2_err.append(ROOT.sqrt(ggh_cat2.Integral())* nEvents[m]/sumW[m] /(xs[m] * br[m] * kf[m] * target_lumi * genW[m])*100)

    print("----------------------------------------------------")
    print("EFF = ", eff, "%")
    print("EFF Cat0 = ", eff_cat0, "%")
    print("EFF Cat1 = ", eff_cat1, "%")
    print("EFF Cat2 = ", eff_cat2, "%")
    print("EFF Cat3 = ", eff_cat3, "%")
    print("Signal fraction in cat 0 = ", ev_cat0/ev_sumCat0123*100, "%")
    print("Signal fraction in cat 1 = ", ev_cat1/ev_sumCat0123*100, "%")
    print("Signal fraction in cat 2 = ", ev_cat2/ev_sumCat0123*100, "%")
    print("Signal fraction in cat 3 = ", ev_cat3/ev_sumCat0123*100, "%")
    print("####################################################\n")
    print("INTEGRAL CAT0 = ", ggh_cat0.Integral() )
    print("INTEGRAL CAT1 = ", ggh_cat1.Integral() )
    print("INTEGRAL CAT2 = ", ggh_cat2.Integral() )
    print("INTEGRAL CAT3 = ", ggh_cat3.Integral() )
    print("####################################################\n")
    
    # Create a new ROOT file to save the histograms
    #output_filename = "masspoint_" + str(masspoints[m]) + "_histograms_targetLumi54p4InvFb.root"
    output_filename = "4CAT_"+scenario+"/masspoint_" + str(masspoints[m]) + "_histograms.root"
    output_file = TFile(output_filename, "RECREATE")

    # Write the histograms to the new ROOT file
    print("sumWeights = ", sumWeights[m])
    ggh_cat0.Scale(sumWeights[m]/(nEv[m]))
    ggh_cat1.Scale(sumWeights[m]/(nEv[m]))
    ggh_cat2.Scale(sumWeights[m]/(nEv[m]))
    ggh_cat3.Scale(sumWeights[m]/(nEv[m]))
    den.Scale(((sumWeights[m]*xs[m] * br[m] * kf[m] * target_lumi)/nEv[m])/den.Integral())
    #den.Scale((xs[m] * br[m] * kf[m] * target_lumi * sumWeights[m]/nEv[m])/den.Integral())
    ggh_cat0.Write()
    ggh_cat1.Write()
    ggh_cat2.Write()
    ggh_cat3.Write()
    den.Write()
    sumw0.Write()
    sumw1.Write()
    sumw2.Write()
    sumw3.Write()
    sumw.Write()

    # Close the new ROOT file
    output_file.Close()

print("-------------EFF----------")
print(v_eff)
print("---------EFF (cat0)-------")
print(v_eff_cat0)
print(v_eff_cat0_err)
print("---------EFF (cat1)-------")
print(v_eff_cat1)
print(v_eff_cat1_err)
print("---------EFF (cat2)-------")
print(v_eff_cat2)
print(v_eff_cat2_err)
print("---------EFF (cat3)-------")
print(v_eff_cat3)
print(v_eff_cat3_err)
print("-------------SIG FRAC----------")
print(v_sigFract_cat0) 
print(v_sigFract_cat1) 
print(v_sigFract_cat2) 
print(v_sigFract_cat3) 

v_sigFract.append(v_sigFract_cat0)
v_sigFract.append(v_sigFract_cat1)
v_sigFract.append(v_sigFract_cat2)
v_sigFract.append(v_sigFract_cat3)


fig = plt.figure(figsize=(10,8))
plt.errorbar(masspoints, v_eff, yerr=v_eff_err, c='turquoise', marker='o', markersize=5, ls='dotted',
             lw = 2, capsize = 4, capthick = 4, 
             label="H $\dashrightarrow$ $\gamma\gamma$")
plt.xlabel('m$_{\gamma\gamma}$ [GeV]',  fontsize=20, x=0.9, y=1)
plt.ylabel('Efficiency x Acceptance (%)', fontsize=20)
plt.title('')
plt.grid(True)
plt.style.use(hep.style.CMS)
hep.cms.label("Preliminary", data=False)
plt.legend(loc=2, prop={'size': 20})
plt.savefig(outputdir+"/efficiency_NNvar.png", bbox_inches="tight")
plt.savefig(outputdir+"/efficiency_NNvar.pdf", bbox_inches="tight")

fig_cat0 = plt.figure(figsize=(10,8))
plt.errorbar(masspoints, v_eff_cat0, yerr=v_eff_cat0_err, c='deepskyblue',marker='o', markersize=5, ls='dotted',
             lw = 2, capsize = 4, capthick = 4,  
             label="H $\dashrightarrow$ $\gamma\gamma$ (Category 0)")
#plt.scatter(masspoints, v_eff_cat0, c='b', label="H $\dashrightarrow$ $\gamma\gamma$ (cat0)")
plt.xlabel('m$_{\gamma\gamma}$ [GeV]',  fontsize=20, x=0.9, y=1)
plt.ylabel('Efficiency x Acceptance (%)', fontsize=20)
plt.title('')
plt.grid(True)
hep.cms.label("Preliminary", data=False)
plt.legend(loc=2, prop={'size': 20})
plt.savefig(outputdir+"/efficiency_cat0_NNvar.png", bbox_inches="tight")
plt.savefig(outputdir+"/efficiency_cat0_NNvar.pdf", bbox_inches="tight")

fig_cat1 = plt.figure(figsize=(10,8))
plt.errorbar(masspoints, v_eff_cat1, yerr=v_eff_cat1_err, c='orange', marker='o', markersize=5, ls='dotted',
             lw = 2, capsize = 4, capthick = 4,
             label="H $\dashrightarrow$ $\gamma\gamma$ (Category 1)")
#plt.scatter(masspoints, v_eff_cat1, c='b', label="H $\dashrightarrow$ $\gamma\gamma$ (cat1)")
plt.xlabel('m$_{\gamma\gamma}$ [GeV]',  fontsize=20, x=0.9, y=1)
plt.ylabel('Efficiency x Acceptance (%)', fontsize=20)
plt.title('')
plt.grid(True)
hep.cms.label("Preliminary", data=False)
plt.legend(loc=2, prop={'size': 20})
plt.savefig(outputdir+"/efficiency_cat1_NNvar.png", bbox_inches="tight")
plt.savefig(outputdir+"/efficiency_cat1_NNvar.pdf", bbox_inches="tight")

fig_cat2 = plt.figure(figsize=(10,8))
plt.errorbar(masspoints, v_eff_cat2, yerr=v_eff_cat2_err, c='tomato', marker='o', markersize=5, ls='dotted',
             lw = 2, capsize = 4, capthick = 4,
             label="H $\dashrightarrow$ $\gamma\gamma$ (Category 2)")
#plt.scatter(masspoints, v_eff_cat2, c='b', label="H $\dashrightarrow$ $\gamma\gamma$ (cat2)")
plt.xlabel('m$_{\gamma\gamma}$ [GeV]',  fontsize=20, x=0.9, y=1)
plt.ylabel('Efficiency x Acceptance (%)', fontsize=20)
plt.title('')
plt.grid(True)
hep.cms.label("Preliminary", data=False)
plt.legend(loc=2, prop={'size': 20})
plt.savefig(outputdir+"/efficiency_cat2_NNvar.png", bbox_inches="tight")
plt.savefig(outputdir+"/efficiency_cat2_NNvar.pdf", bbox_inches="tight")


l_col = ['deepskyblue', 'orange', 'tomato', 'violet']
#l_col = ['orchid', 'mediumvioletred', 'darkmagenta', 'dodgerblue']
#for c in range(0,3):
#l_col = ['orchid', 'darkmagenta']
for c in range(0,4):
    f_cat = "f_cat"+str(c)
    text_cat = "H $\dashrightarrow$ $\gamma\gamma$ (Category "+str(c)+")"
    f_cat = plt.figure(figsize=(10,8))
    plt.scatter(masspoints, v_sigFract[c], c=l_col[c], label=text_cat)
    plt.xlabel('m$_{\gamma\gamma}$ [GeV]',  fontsize=20, x=0.9, y=1)
    plt.ylabel("Signal Fraction in Cat"+str(c)+" (%)", fontsize=20)
    plt.ylim(0, 100)
    plt.title('')
    plt.grid(True)
#    hep.cms.label("Preliminary", data=False)
    plt.legend(loc=2, bbox_to_anchor=(0.06, 0.9), prop={'size': 20})
    #plt.legend(loc=2, bbox_to_anchor=(0.23, 0.11), prop={'size': 20})
    plt.savefig(outputdir+"/SigFracCat"+str(c)+"_NNvar.png", bbox_inches="tight")
    plt.savefig(outputdir+"/SigFracCat"+str(c)+"_NNvar.pdf", bbox_inches="tight")
