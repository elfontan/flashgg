######################################################                                                                                            
# Very low mass diphoton analysis: input preparation #                                                                   
# -------------------------------------------------- #                                                                     
# python3 environment, e.g. CMSSW_14_0_0                                                                    
# python3  0_newR_dataMC_allVars_dd.py --log True  --outdir /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/inputPreparation/

import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TChain, TH1, TH1F, TF1, THStack, TLegend, TPad, gSystem, gStyle
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList, kYellow, kOrange, kBlack
from collections import OrderedDict
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
argparser.add_argument('--cr', dest='cr', default=False, help='Control region with lead and sublead phoIDMVA > 0.9')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
cr_phoId0p0 = args.cr

norm_dipho = 5.07071342                                                                                         
norm_sb = (5.07071342*0.02190371141)

# ----------------------
# Obtain histogram files                                    
# ----------------------                                                   
data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_all2018Data_bkg_newSamplesFlat.root","READ")             
sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_sbData_bkg_newSamplesFlat.root","READ")        
mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_dipho_bkg_newSamplesFlat.root","READ")
#data = TFile("/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_DataBDT_AllMC_SigExtIncluded/EGamma_All_Summer20UL.root","READ")             
#sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/sb_data2018_fullDDreweighting.root","READ")        
#mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/bkg/dipho_080_fullDDreweighting.root","READ")
#mgg = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/out_dipho_bkg_newSamplesFlat.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
dat0 = data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
mgg0 = mgg.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")

var_list = ["dipho_mass", "dipho_lead_ptoM", "dipho_sublead_ptoM", "dipho_leadEta", "dipho_subleadEta", "cosphi", "dipho_leadIDMVA", "dipho_subleadIDMVA", "sigmaMrvoM", "sigmaMwvoM", "vtxprob", "dipho_lead_sigmaEoE", "dipho_sublead_sigmaEoE", "dipho_pt", "dipho_sumpt", "NNScore", "nvtx" ]
label_list = ["m_{#gamma#gamma}", "Leading photon p_{T}", "Subleading photon p_{T}", "Leading photon #eta", "Sublead photon #eta", "cos#phi", "Lead IDMVA", "Sublead IDMVA", "#sigma_{RV}/m_{#gamma#gamma}", "sigma_{WV}/m_{#gamma#gamma}", "Vtx probability", "Leading photon #sigma_{E}/E", "Subleading photon #sigma_{E}/E", "Diphoton p_{T}", "Diphoton sum p_{T}", "PNN Score", "Number of primary vertices"]


histo_sbb0_list = OrderedDict()
histo_sba0_list = OrderedDict()
histo_pre0_list = OrderedDict()
histo_mgg0_list = OrderedDict()

# Create a dictionary to store the binning information for each variable
binning_info = { 
    var_list[0]: (65, 10., 75.),   #dipho_mass
    var_list[1]: (50, 0., 5.),    #dipho_lead_ptoM
    var_list[2]: (50, 0., 5.),    #"dipho_sublead_ptoM
    var_list[3]: (60, -3., 3.),   #dipho_leadEta 
    var_list[4]: (60, -3., 3.),   #dipho_subleadEta
    var_list[5]: (60, -1.0, 1.0), #cosphi
    var_list[6]: (100, -1.,1.),   #dipho_leadIDMVA 
    var_list[7]: (100, -1.,1.),   #dipho_subleadIDMVA
    var_list[8]: (50, 0., 0.05),  #sigmaMrvoM
    var_list[9]: (50, 0., 0.05),  #sigmaMwvoM
    var_list[10]: (100, 0.0, 1.0), #vtxprob
    var_list[11]: (50, 0., 0.05), #dipho_lead_sigmaEoE
    var_list[12]: (50, 0., 0.05),  #dipho_sublead_sigmaEoE
    var_list[13]: (50, 0., 200),  #dipho_pt                                                                                                                
    var_list[14]: (50, 0., 200),   #dipho_sumpt                                                                                    
    var_list[15]: (20, 0., 1),    #NNScore                                                                                    
    var_list[16]: (30, 0., 60)    #nvtx                                                                                    
}


for variable in var_list:
    nbins, xlow, xhigh = binning_info[variable]
    print("var_list[i]", variable)
    print("nbins = ", nbins)
    print("xlow = ", xlow)
    print("xhigh = ", xhigh)
    histo_sbb0_list[variable + "_sbb0"] = TH1F("h_" + variable + "_sbb0", "h_" + variable + "_sbb0", nbins, xlow, xhigh)
    histo_sba0_list[variable + "_sba0"] = TH1F("h_" + variable + "_sba0", "h_" + variable + "_sba0" , nbins, xlow, xhigh)
    histo_pre0_list[variable + "_pre0"] = TH1F("h_" + variable + "_pre0", "h_" + variable + "_pre0", nbins, xlow, xhigh)
    histo_mgg0_list[variable + "_mgg0"] = TH1F("h_" + variable + "_mgg0", "h_" + variable + "_mgg0", nbins, xlow, xhigh)

    # Fill the histograms
    # -------------------
    #sb0.Draw(variable + ">>h_" + variable + "_sbb0", "(CMS_hgg_mass>0 && event%20==0)", "goff")                                   
    #sb0.Draw(variable + ">>h_" + variable + "_sba0", "weight*(CMS_hgg_mass>0 && event%20==0)", "goff")                               
    if (cr_phoId0p0):
        sb0.Draw(variable + ">>h_" + variable + "_sbb0", "(CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>0.9)", "goff")
        sb0.Draw(variable + ">>h_" + variable + "_sba0", "weight*weight_allDD * (CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>0.9)", "goff")
        dat0.Draw(variable + ">>h_" + variable + "_pre0", "CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>0.9 && event%20==0", "goff")
        #mgg0.Draw(variable + ">>h_" + variable + "_mgg0", "weight * (CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>0.9)", "goff")
        mgg0.Draw(variable + ">>h_" + variable + "_mgg0", "weight*weight_allDD * (CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>0.9)", "goff")
    else:
        sb0.Draw(variable + ">>h_" + variable + "_sbb0", "(CMS_hgg_mass<75)", "goff")
        sb0.Draw(variable + ">>h_" + variable + "_sba0", "weight*weight_allDD * (CMS_hgg_mass<75)", "goff")
        dat0.Draw(variable + ">>h_" + variable + "_pre0", "CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7 && event%20==0", "goff")
        mgg0.Draw(variable + ">>h_" + variable + "_mgg0", "weight *weight_allDD * (CMS_hgg_mass<75 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>> FILLED HISTOS")

i=0
for variable in var_list:
    print(variable)
    sbb0 = histo_sbb0_list[variable + "_sbb0"]
    sba0 = histo_sba0_list[variable + "_sba0"]
    pre0 = histo_pre0_list[variable + "_pre0"]
    mgg0 = histo_mgg0_list[variable + "_mgg0"]
    bkg0 = THStack("bkg0","bkg0")

    # Background Scaling: after TFitter                                  
    #sbb0.Scale(norm_sb*0.82)                                 
    #sba0.Scale(norm_sb*0.82)                                               
    #mgg0.Scale(norm_dipho*1.68)

    if (variable==var_list[0]):
        sbb0.SetMinimum(100)
        sba0.SetMinimum(100)
        pre0.SetMinimum(100)
        mgg0.SetMinimum(100)
        bkg0.SetMinimum(100)
        sbb0.SetMaximum(20*pre0.GetMaximum())
        sba0.SetMaximum(20*pre0.GetMaximum())
        pre0.SetMaximum(20*pre0.GetMaximum())
        mgg0.SetMaximum(20*pre0.GetMaximum())
        bkg0.SetMaximum(20*pre0.GetMaximum())
    if (variable==var_list[3] or variable==var_list[4] or variable==var_list[6] or variable==var_list[7] or variable==var_list[8] or variable==var_list[9] or variable==var_list[12]):
        sbb0.SetMaximum(5*pre0.GetMaximum())
        sba0.SetMaximum(5*pre0.GetMaximum())
        pre0.SetMaximum(5*pre0.GetMaximum())
        mgg0.SetMaximum(5*pre0.GetMaximum())
        bkg0.SetMaximum(5*pre0.GetMaximum())
    else:
        sbb0.SetMaximum(2.0*pre0.GetMaximum())
        sba0.SetMaximum(2.0*pre0.GetMaximum())
        pre0.SetMaximum(2.0*pre0.GetMaximum())
        mgg0.SetMaximum(2.0*pre0.GetMaximum())
        bkg0.SetMaximum(2.0*pre0.GetMaximum())

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    canvasname = "c_"+variable
    c1 = TCanvas(canvasname,canvasname,1200,1200)
    c1.cd()
    #c1.SetLeftMargin(0.15)
    
    #upper plot pad - Data histos
    pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
    pad1.Draw()
    pad1.cd()
    pad1.SetLogy()                                                                                                  
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(1.9)
    
    sba0.SetLineColor(kYellow-7)
    sba0.SetFillColorAlpha(kYellow-7,0.8)
    sba0.SetLineWidth(2)
    
    sba0.GetXaxis().SetLabelSize(0)
    
    sba0.GetYaxis().SetTitle("Events")
    sba0.GetYaxis().SetTitleSize(25)
    sba0.GetYaxis().SetTitleFont(43)
    sba0.GetYaxis().SetTitleOffset(2.25)
    sba0.GetYaxis().SetLabelFont(43)
    sba0.GetYaxis().SetLabelOffset(0.01)
    sba0.GetYaxis().SetLabelSize(25)
    
    mgg0.SetLineColor(kOrange-4)
    mgg0.SetFillColorAlpha(kOrange-4,0.8)
    mgg0.SetLineWidth(2)
    mgg0.GetYaxis().SetTitleOffset(2.25)
     
    #bkg0.GetYaxis().SetTitleOffset(2.25)
    bkg0.Add(mgg0)
    bkg0.Add(sba0)
    bkg0.Draw("histo")
    
    pre0.SetLineWidth(2)
    pre0.SetLineColorAlpha(kBlack,0.8)
    #pre0.SetLineColorAlpha(kOrange+9,0.8)
    pre0.Draw("epsame")
    
    sbb0.SetLineColor(kOrange-1)
    sbb0.GetYaxis().SetTitleOffset(2.25)
    sbb0.SetLineWidth(2)
    #sbb0.Draw("histosame") #Removing line of the SB data pre-reweighting
        
    leg = TLegend(0.5,0.6,0.88,0.78)
    #leg.AddEntry(sbb0,"Unweighted Sideband")
    leg.AddEntry(sba0,"#gamma-jet and jet-jet (pf+ff DD)")
    leg.AddEntry(mgg0,"#gamma#gamma MC")
    leg.AddEntry(pre0,"Preselection Region")
    leg.SetLineWidth(0)
    leg.Draw("same")
    
    c1.Update()
    c1.cd()
    
    #lower plot pad - Ratio plot
    pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.345)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.19)
    #pad2.SetLeftMargin(0.1)  

    
    #define ratio plot
    rp = TH1F(pre0.Clone("rp")) #clone the preselection region
    rp.SetLineColor(kBlack)
    rp.SetMinimum(0.5)
    rp.SetMaximum(1.9)
    rp.SetStats(0)
    rp.Divide(sba0+mgg0) #divide by sideband+mgg
    rp.SetMarkerStyle(20)
    #rp.SetMarkerStyle(24)
    rp.SetTitle("") 
    
    rp.SetYTitle("Presel / (pf+ff DD + #gamma#gamma MC)")
    rp.GetYaxis().SetNdivisions(505)
    rp.GetYaxis().SetTitleSize(25)
    rp.GetYaxis().SetTitleFont(43)
    rp.GetYaxis().SetTitleOffset(2.25)
    rp.GetYaxis().SetLabelFont(43)
    rp.GetYaxis().SetLabelSize(25)
    
    rp.SetXTitle(label_list[i])
    rp.GetXaxis().SetTitleSize(25)
    rp.GetXaxis().SetTitleFont(43)
    rp.GetXaxis().SetTitleOffset(1.5)
    rp.GetXaxis().SetLabelFont(43)
    rp.GetXaxis().SetLabelSize(25)
    rp.GetXaxis().SetLabelOffset(0.02)
    
    rp.Draw("ep")
    
    c1.Update()
    c1.cd()
    
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
    c1.SaveAs(outputdir+"/"+variable+".png")
    c1.SaveAs(outputdir+"/"+variable+".pdf")
    
    print("MGG: ", mgg0.Integral())
    print("Reweight: ", sba0.Integral())
    print("Preselect: ", pre0.Integral())
    print("Unweighted Sideband:", sbb0.Integral())

    i+=1
