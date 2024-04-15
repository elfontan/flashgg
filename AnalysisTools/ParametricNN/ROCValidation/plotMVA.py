from ROOT import *
import CMS_lumi

pnndf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/NEAREST/out_all2018Data_bkg_v3.root","READ")
pnrdf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/nearest_15and55/out_all2018Data_bkg_v1.root","READ")

pnndt0 = pnndf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
pnrdt0 = pnrdf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

for i in range(5,75,5):
  #Signal
  pnnf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/NEAREST_NewMCFlashggNtuples/out_ggH_M"+str(i)+"_newSamples_v1.root","READ")
  pnrf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/nearest_15and55/out_ggH_M"+str(i)+"_newSamples_v1.root","READ")

  pnnt0 = pnnf.Get("tagsDumper/trees/ggh_"+str(i)+"_13TeV_UntaggedTag_0")
  pnrt0 = pnrf.Get("tagsDumper/trees/ggh_"+str(i)+"_13TeV_UntaggedTag_0")

  #Create histograms
  pnn = TH1F("pnn","pnn",40,0.0,1.0)
  pnn.Sumw2()
  pnr = TH1F("pnr","pnr",40,0.0,1.0)
  pnr.Sumw2()

  pnnd = TH1F("pnnd","pnnd",40,0.0,1.0)
  pnnd.Sumw2()
  pnrd = TH1F("pnrd","pnrd",40,0.0,1.0)
  pnrd.Sumw2()

  #Weighted: weight*(CMS_hgg_mass>0)
  pnnt0.Draw("NNScore>>pnn","weight*(CMS_hgg_mass>0) && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7","goff")
  pnrt0.Draw("NNScore>>pnr","weight*(CMS_hgg_mass>0) && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7","goff")

  masslow = 0.9*i
  masshigh = 1.1*i

  #Weighted: weight*(CMS_hgg_mass>0)
  pnndt0.Draw("NNScore>>pnnd","weight*(CMS_hgg_mass>"+str(masslow)+" && CMS_hgg_mass<"+str(masshigh)+") && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7","goff")
  pnrdt0.Draw("NNScore>>pnrd","weight*(CMS_hgg_mass>"+str(masslow)+" && CMS_hgg_mass<"+str(masshigh)+") && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7","goff")

  if (pnn.Integral() != 0): pnn.Scale(1.0/pnn.Integral())
  if (pnnd.Integral() != 0): pnnd.Scale(1.0/pnnd.Integral())
  if (pnr.Integral() != 0): pnr.Scale(1.0/pnr.Integral())
  if (pnrd.Integral() != 0): pnrd.Scale(1.0/pnrd.Integral())

  pnnd.SetMaximum(1.0)

  #Now we draw it out
  #Lowmass: kTeal+5,+3
  #30 GeV Window: kAzure-2,-6
  #70 GeV: kViolet-2,-6
  #All GeV: kPink-2,-6
  gStyle.SetOptStat(0)
  gStyle.SetOptTitle(0)

  c1 = TCanvas("c1","c1",1200,1200)
  c1.cd()
  c1.SetBottomMargin(0.11)
  c1.SetLeftMargin(0.11)

  #Parametric NN: Nearest
  pnnd.SetLineColor(kViolet-2)
  pnnd.SetLineWidth(3)
  pnnd.SetLineStyle(2)
  pnnd.Draw("hist")

  pnnd.SetXTitle("Diphoton MVA")
  pnnd.GetXaxis().SetTitleSize(25)
  pnnd.GetXaxis().SetTitleFont(43)
  pnnd.GetXaxis().SetTitleOffset(2.0)
  pnnd.GetXaxis().SetLabelFont(43)
  pnnd.GetXaxis().SetLabelSize(25)
  pnnd.GetXaxis().SetLabelOffset(0.02)

  pnnd.GetYaxis().SetTitle("A.U.")
  pnnd.GetYaxis().SetTitleSize(25)
  pnnd.GetYaxis().SetTitleFont(43)
  pnnd.GetYaxis().SetTitleOffset(2.25)
  pnnd.GetYaxis().SetLabelFont(43)
  pnnd.GetYaxis().SetLabelSize(25)

  pnn.SetLineColor(kViolet-6)
  pnn.SetLineWidth(2)
  pnn.Draw("histsame")

  #Parametric NN: Random
  pnrd.SetLineColor(kAzure-2)
  pnrd.SetLineWidth(3)
  pnrd.SetLineStyle(2)
  pnrd.Draw("histsame")

  pnr.SetLineColor(kAzure-6)
  pnr.SetLineWidth(2)
  pnr.Draw("histsame")

  leg = TLegend(0.2,0.5,0.55,0.8)
  leg.SetBorderSize(0)
  leg.AddEntry(pnn,"2018 NN Nearest Neighbor on Signal")
  leg.AddEntry(pnr,"2018 New NN Adding 15 and 55 GeV on Signal")
  leg.AddEntry(pnnd,"2018 NN Nearest Neighbor on Data")
  leg.AddEntry(pnrd,"2018 New NN Adding 15 and 55 GeV on Data")
  leg.Draw("same")

  c1.Update()
  c1.cd()

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

  c1.SaveAs("output/DiphoMVA_"+str(i)+".png")
  c1.SaveAs("output/DiphoMVA_"+str(i)+".pdf")

  print(pnr.Integral())
  print(pnrd.Integral())
