from ROOT import *
import CMS_lumi
import numpy as np

#Plot ROC Histograms using integrals of signal and background to compute efficiencies
for i in range(10,75,5):
  pnn_ROC = TGraph()
  pnr_ROC = TGraph()

  pnn_Int = TGraph()
  pnr_Int = TGraph()

  pnn_ROC.SetPoint(0,1.0,0.0)
  pnr_ROC.SetPoint(0,1.0,0.0)

  pnn_Int.SetPoint(0,1.0,0.0)
  pnr_Int.SetPoint(0,1.0,0.0)

  #Obtain MVA histogram files for signal at different mass points and background at different sliding windows
  pnn_sigfile = TFile("output/pnn"+str(i)+".root","READ")
  pnr_sigfile = TFile("output/pnr"+str(i)+".root","READ")

  pnn_sighist = pnn_sigfile.Get("pnnr")
  pnr_sighist = pnr_sigfile.Get("pnrr")

  pnn_sigeffden = pnn_sighist.Integral()
  pnr_sigeffden = pnr_sighist.Integral()

  pnn_bkgfile = TFile("output/pnn"+str(i)+"data.root","READ")
  pnr_bkgfile = TFile("output/pnr"+str(i)+"data.root","READ")

  pnn_bkghist = pnn_bkgfile.Get("pnnr")
  pnr_bkghist = pnr_bkgfile.Get("pnrr")

  pnn_bkgrejden = pnn_bkghist.Integral()
  pnr_bkgrejden = pnr_bkghist.Integral()

  nbins = 1000

  for j in range(0,nbins+1):
    pnn_sigeffnum = pnn_sighist.Integral(j,nbins)
    pnr_sigeffnum = pnr_sighist.Integral(j,nbins)

    pnn_bkgrejnum = pnn_bkghist.Integral(j,nbins)
    pnr_bkgrejnum = pnr_bkghist.Integral(j,nbins)

    pnn_sigeff = pnn_sigeffnum/pnn_sigeffden
    pnr_sigeff = pnr_sigeffnum/pnr_sigeffden

    pnn_bkgrej = 1.0-(pnn_bkgrejnum/pnn_bkgrejden)
    pnr_bkgrej = 1.0-(pnr_bkgrejnum/pnr_bkgrejden)

    pnn_ROC.SetPoint(j+1, pnn_sigeff,pnn_bkgrej)
    pnr_ROC.SetPoint(j+1, pnr_sigeff,pnr_bkgrej)
    pnn_Int.SetPoint(j+1, pnn_sigeff,pnn_bkgrej)
    pnr_Int.SetPoint(j+1, pnr_sigeff,pnr_bkgrej)

  pnn_Int.SetPoint(nbins+2,0.0,0.0)
  pnr_Int.SetPoint(nbins+2,0.0,0.0)

  #Now we draw it out
  gStyle.SetOptStat(0)
  gStyle.SetOptTitle(0)

  c1 = TCanvas("c1","c1",1200,1200)
  c1.cd()
  c1.SetBottomMargin(0.11)
  c1.SetLeftMargin(0.11)

  pnn_ROC.SetLineColor(kViolet-2)
  pnn_ROC.SetLineWidth(2)
  pnn_ROC.Draw("AL")

  pnn_ROC.GetXaxis().SetTitle("Signal Eff.")
  pnn_ROC.GetXaxis().SetTitleSize(25)
  pnn_ROC.GetXaxis().SetTitleFont(43)
  pnn_ROC.GetXaxis().SetTitleOffset(1.5)
  pnn_ROC.GetXaxis().SetLabelFont(43)
  pnn_ROC.GetXaxis().SetLabelSize(25)
  pnn_ROC.GetXaxis().SetLabelOffset(0.02)

  pnn_ROC.GetYaxis().SetTitle("Background Rej.")
  pnn_ROC.GetYaxis().SetTitleSize(25)
  pnn_ROC.GetYaxis().SetTitleFont(43)
  pnn_ROC.GetYaxis().SetTitleOffset(1.5)
  pnn_ROC.GetYaxis().SetLabelFont(43)
  pnn_ROC.GetYaxis().SetLabelSize(25)

  pnr_ROC.SetLineColor(kAzure-2)
  pnr_ROC.SetLineWidth(2)
  pnr_ROC.Draw("L")

  leg = TLegend(0.15,0.15,0.65,0.5)
  leg.SetTextSize(0.025)
  leg.SetBorderSize(0)
  leg.AddEntry(pnn_ROC,"PNN Nearest Neighbor AUC = "+str(round(pnn_Int.Integral(),3)))
  leg.AddEntry(pnr_ROC,"New PNN Adding 15 and 55 GeV AUC = "+str(round(pnr_Int.Integral(),3)))
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
