#####################################################
# Very low mass diphoton analysis: Likelihood scans #
# ------------------------------------------------- #
# python3  plot_LLscan.py --sample higgsCombineAllConstrainedNuisancesAndPdfIndex --output /eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Syst/LikelihoodScan/

import ROOT
import os
import numpy as np
import argparse
import re
import CMS_lumi, CMSGraphics
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan

ROOT.gStyle.SetOptStat(0)

def plotLL(file, pdir):
  try:
    rf = ROOT.TFile(file)
    lim = rf.Get("limit")
    tg = ROOT.TGraph()
    
    rvals = []
    dnllvals = [] 
    skipfirst = True

    for ev in lim:
      #print(ev.r)
      if skipfirst: # First is the best fit
          rvals.append(ev.r)
          dnllvals.append(2*ev.deltaNLL)
          skipfirst = False
          continue
      if (ev.r > -2 and ev.r < 2):
          rvals.append(ev.r)
          dnllvals.append(2*ev.deltaNLL)
          tg.AddPoint(ev.r, 2*ev.deltaNLL)
    nn = np.array(dnllvals)
    r  = np.array(rvals)

    c = ROOT.TCanvas("c","c", 1000, 800)
    tg.SetTitle(";r;2#Delta(NLL)")
    tg.SetLineColor(kAzure-4)  
    tg.SetMarkerSize(0.4)  
    tg.SetMinimum(-0.01)  
    tg.SetMarkerColor(kAzure-4)  
    tg.Draw("AL*")
    tl = ROOT.TLegend(0.18,0.75,0.55,0.84)
    samplename = file.split("/")[-1].replace(".MultiDimFit.mH50.root","").replace("higgsCombine","")
    scenario = samplename.split("_")[-1]
    samplename = samplename.replace(scenario,"")[:-2]
    tl.SetHeader("Diphoton mass  = 50 GeV")
    legText = "Nuisances: "+scenario
    tl.AddEntry(tg, legText, "L")
    tl.SetLineWidth (0)
    tl.Draw("same")

    # CMS and lumi text                     
    # -----------------                                       
    CMS_lumi.writeExtraText = True                          
    CMS_lumi.extraText      = "  Preliminary"                 
    CMS_lumi.cmsTextSize    = 0.6                                                           
    CMS_lumi.lumiTextSize   = 0.46                                  
    CMS_lumi.extraOverCmsTextSize = 0.75       
    CMS_lumi.relPosX = 0.12              
    CMS_lumi.CMS_lumi(c, 0, 0)
    c.Update()
    
    c.SaveAs(pdir + "/scanNLL_m50_"+scenario+".pdf")
    c.SaveAs(pdir + "/scanNLL_m50_"+scenario+".png")
    return  pdir + "/" + samplename  
    #return rang, pdir + "/" + samplename + "_" + rang 
    #return isGoodScan, isSmooth, rang, pdir + "/" + samplename + "_" + rang 
  except:
    return "", (0,0), False, False, "0000", "0000"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot likelihood scans")
    parser.add_argument("--sample", type=str, required=True, help="Sample Name")
    parser.add_argument("--output", type=str, required=True, help="Directory to put plots on")
    args = parser.parse_args()
    
    if not(os.path.isdir(args.output)): os.system("mkdir %s"%(args.output))
    #if not(os.path.isdir(args.output+ "/best/")): os.system("mkdir %s"%(args.output+ "/best/"))

    plot = plotLL(args.sample, args.output)
