from ROOT import *
import CMS_lumi
import numpy as np

#Plot ROC Histograms using integrals of signal and background to compute efficiencies
for i in range(10,75,5):
  lm_ROC = TGraph()
  pnr_ROC = TGraph()

  lm_Int = TGraph()
  pnr_Int = TGraph()

  lm_ROC.SetPoint(0,1.0,0.0)
  pnr_ROC.SetPoint(0,1.0,0.0)

  lm_Int.SetPoint(0,1.0,0.0)
  pnr_Int.SetPoint(0,1.0,0.0)

  #Obtain MVA histogram files for signal at different mass points and background at different sliding windows
  lm_sigfile = TFile("output/lm"+str(i)+".root","READ")
  pnr_sigfile = TFile("output/pnr"+str(i)+".root","READ")

  lm_sighist = lm_sigfile.Get("lmr")
  pnr_sighist = pnr_sigfile.Get("pnrr")

  lm_sigeffden = lm_sighist.Integral()
  pnr_sigeffden = pnr_sighist.Integral()

  lm_bkgfile = TFile("output/lm"+str(i)+"data.root","READ")
  pnr_bkgfile = TFile("output/pnr"+str(i)+"data.root","READ")

  lm_bkghist = lm_bkgfile.Get("lmr")
  pnr_bkghist = pnr_bkgfile.Get("pnrr")

  lm_bkgrejden = lm_bkghist.Integral()
  pnr_bkgrejden = pnr_bkghist.Integral()

  nbins = 2000

  for j in range(0,nbins+1):
    lm_sigeffnum = lm_sighist.Integral(j,nbins)
    lm_bkgrejnum = lm_bkghist.Integral(j,nbins)
    lm_sigeff = lm_sigeffnum/lm_sigeffden
    lm_bkgrej = 1.0-(lm_bkgrejnum/lm_bkgrejden)
    lm_ROC.SetPoint(j+1, lm_sigeff,lm_bkgrej)
    lm_Int.SetPoint(j+1, lm_sigeff,lm_bkgrej)

    pnr_sigeffnum = pnr_sighist.Integral(j,nbins)
    pnr_bkgrejnum = pnr_bkghist.Integral(j,nbins)
    pnr_sigeff = pnr_sigeffnum/pnr_sigeffden
    pnr_bkgrej = 1.0-(pnr_bkgrejnum/pnr_bkgrejden)
    pnr_ROC.SetPoint(j+1, pnr_sigeff,pnr_bkgrej)
    pnr_Int.SetPoint(j+1, pnr_sigeff,pnr_bkgrej)

  lm_Int.SetPoint(nbins+2,0.0,0.0)
  pnr_Int.SetPoint(nbins+2,0.0,0.0)

  #Now we draw it out
  gStyle.SetOptStat(0)
  gStyle.SetOptTitle(0)

  c1 = TCanvas("c1","c1",1200,1200)
  c1.cd()
  c1.SetBottomMargin(0.11)
  c1.SetLeftMargin(0.11)

  lm_ROC.SetLineColor(kViolet-2)
  lm_ROC.SetLineWidth(2)
  lm_ROC.Draw("AL")

  lm_ROC.GetXaxis().SetTitle("Signal Eff.")
  lm_ROC.GetXaxis().SetTitleSize(25)
  lm_ROC.GetXaxis().SetTitleFont(43)
  lm_ROC.GetXaxis().SetTitleOffset(1.5)
  lm_ROC.GetXaxis().SetLabelFont(43)
  lm_ROC.GetXaxis().SetLabelSize(25)
  lm_ROC.GetXaxis().SetLabelOffset(0.02)

  lm_ROC.GetYaxis().SetTitle("Background Rej.")
  lm_ROC.GetYaxis().SetTitleSize(25)
  lm_ROC.GetYaxis().SetTitleFont(43)
  lm_ROC.GetYaxis().SetTitleOffset(1.5)
  lm_ROC.GetYaxis().SetLabelFont(43)
  lm_ROC.GetYaxis().SetLabelSize(25)

  pnr_ROC.SetLineColor(kAzure-2)
  pnr_ROC.SetLineWidth(2)
  pnr_ROC.Draw("L")

  leg = TLegend(0.15,0.15,0.55,0.45)
  leg.SetTextSize(0.025)
  leg.SetBorderSize(0)
  leg.AddEntry(lm_ROC,"Lowmass BDT AUC = "+str(round(lm_Int.Integral(),3)))
  leg.AddEntry(pnr_ROC,"New PNN AUC = "+str(round(pnr_Int.Integral(),3)))
  leg.Draw("same")

  c1.Update()

#CMS lumi stuff
  CMS_lumi.writeExtraText = True
  CMS_lumi.extraText      = "Preliminary"
  CMS_lumi.lumi_sqrtS     = str(i)+" GeV, 2018 (13 TeV)"
  CMS_lumi.cmsTextSize    = 0.4
  CMS_lumi.lumiTextSize   = 0.3
  CMS_lumi.extraOverCmsTextSize = 0.75
  CMS_lumi.relPosX = 0.12
  CMS_lumi.CMS_lumi(c1, 0, 0)
  c1.Update()

  c1.cd()
  c1.SaveAs("output/ROC_M"+str(i)+".png")
  c1.SaveAs("output/ROC_M"+str(i)+".pdf")
