#####################################################
# Very low mass diphoton analysis: Likelihood scans #
# ------------------------------------------------- #
# python3  investigatingPdfIndexBehaviour_compPlot_LLscan.py --m 48 --s1 higgsCombineExpDefault.MultiDimFit.mH48.root --s2 higgsCombineObsDefault.MultiDimFit.mH48.root  --output /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Syst/LikelihoodScan/ --c 01 --input nuisanceStudies/M48/cat01/

import ROOT
import os
import numpy as np
import argparse
import re
import CMS_lumi, CMSGraphics
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan, kMagenta

ROOT.gStyle.SetOptStat(0)

import ROOT
import os
import numpy as np
import argparse
import re
import CMS_lumi, CMSGraphics
from ROOT import kBlue, kRed, kAzure

ROOT.gStyle.SetOptStat(0)

def plotLL(file, color, cat, mass):
    try:
        rf = ROOT.TFile(file)
        lim = rf.Get("limit")
        tg = ROOT.TGraph()
        
        rvals = []
        dnllvals = []
        skipfirst = True

        for ev in lim:
            print(ev.r)
            if skipfirst: # First is the best fit
                rvals.append(ev.r)
                dnllvals.append(2*ev.deltaNLL)
                skipfirst = False
                continue
            if (ev.r > -0.5 and ev.r < 1.0):
                rvals.append(ev.r)
                dnllvals.append(2*ev.deltaNLL)
                tg.AddPoint(ev.r, 2*ev.deltaNLL)
                        
        tg.SetMinimum(-0.1)
        tg.SetMaximum(10)
        tg.SetLineColor(color)
        tg.SetMarkerColor(color)
        tg.SetMarkerStyle(22)
        tg.SetMarkerSize(0.4)
        tg.SetLineStyle(2)  # Dashed line
        return tg
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot likelihood scans")
    parser.add_argument("--s1", type=str, required=True, help="First sample name")
    parser.add_argument("--s2", type=str, required=True, help="Second sample name")
    parser.add_argument("--c", type=str, required=True, help="Category")
    parser.add_argument("--m", type=str, required=True, help="Mass")
    parser.add_argument("--input", type=str, required=True, help="Input directoy")
    parser.add_argument("--output", type=str, required=True, help="Directory to put plots on")
    args = parser.parse_args()
    
    if not os.path.isdir(args.output):
        os.system(f"mkdir {args.output}")

    cat = args.c
    mass = args.m
    sample1_name = args.s1.split("/")[-1].replace(".MultiDimFit.mH"+mass+".root", "").replace("higgsCombine", "")
    sample2_name = args.s2.split("/")[-1].replace(".MultiDimFit.mH"+mass+".root", "").replace("higgsCombine", "")

    tg1 = plotLL(args.input+"/"+args.s1, kAzure-4, cat, mass)
    if (sample2_name == "ObsDefault"):
        tg2 = plotLL(args.input+"/"+args.s2, kOrange-3, cat, mass)
    elif (sample2_name == "ObsPdfIndex0Frozen"):
        tg2 = plotLL(args.input+"/"+args.s2, kCyan+3, cat, mass)
    elif (sample2_name == "ObsPdfIndex01Frozen"):
        tg2 = plotLL(args.input+"/"+args.s2, kCyan-3, cat, mass)
    
    
    if tg1 and tg2:
        c = ROOT.TCanvas("c", "c", 1000, 800)
        tg1.SetTitle(";r;2#Delta(NLL)")
        tg1.SetMinimum(-0.1)
        tg1.Draw("AL*")
        tg2.Draw("L* same")

        tl = ROOT.TLegend(0.3, 0.67, 0.65, 0.85)
        legTitle = "Cat"+cat+" (m_{#gamma#gamma}="+mass+" GeV)"
        tl.SetHeader(legTitle)
        tl.AddEntry(tg1, f"{sample1_name}", "L")
        tl.AddEntry(tg2, f"{sample2_name}", "L")
        tl.SetLineWidth(0)
        tl.Draw("same")

        # Add a horizontal line at y=1
        line = ROOT.TLine(tg1.GetXaxis().GetXmin(), 1, tg1.GetXaxis().GetXmax(), 1)
        line.SetLineColor(ROOT.kGray+1)
        line.SetLineWidth(2)  # Dashed line
        line.SetLineStyle(2)  # Dashed line
        line.Draw("same")
        
        # Add text "1#sigma" near the line
        text = ROOT.TLatex()
        text.SetTextSize(0.035)
        text.SetTextColor(ROOT.kGray+1)
        #text.DrawLatex(tg1.GetXaxis().GetXmax() * 0.75, 1.5, "1#sigma")
        text.DrawLatex(tg1.GetXaxis().GetXmax() * 0.87, 1.55, "1#sigma")
        
        # CMS and lumi text                     
        CMS_lumi.writeExtraText = True                          
        CMS_lumi.extraText = "  Preliminary"                 
        CMS_lumi.lumi_sqrtS = "2018 (13 TeV)"
        CMS_lumi.cmsTextSize = 0.6                                                           
        CMS_lumi.lumiTextSize = 0.46                                  
        CMS_lumi.extraOverCmsTextSize = 0.75       
        CMS_lumi.relPosX = 0.12              
        CMS_lumi.CMS_lumi(c, 0, 0)
        c.Update()
        
        c.SaveAs(args.output + "/scanNLL_m"+mass+"_comp"+sample1_name+""+sample2_name+"_cat"+cat+".pdf")
        c.SaveAs(args.output + "/scanNLL_m"+mass+"_comp"+sample1_name+""+sample2_name+"_cat"+cat+".png")
    else:
        print("One or both TGraphs could not be created.")
