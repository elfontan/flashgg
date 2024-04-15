from ROOT import *
import CMS_lumi

pnnf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/NEAREST/out_all2018Data_bkg_v3.root","READ")
pnrf = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/nearest_15and55/out_all2018Data_bkg_v1.root","READ")

pnnt0 = pnnf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
pnrt0 = pnrf.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

pnnr = TH1F("pnnr","pnnr",1000,0.0,1.0)
pnnr.Sumw2()
pnrr = TH1F("pnrr","pnrr",1000,0.0,1.0)
pnrr.Sumw2()

pnn = TH1F("pnn","pnn",40,0.0,1.0)
pnn.Sumw2()
pnr = TH1F("pnr","pnr",40,0.0,1.0)
pnr.Sumw2()

for i in range(5,75,5):
  masslow = i*0.9
  masshigh = i*1.1

  #Weighted: weight*(CMS_hgg_mass>0)
  pnnt0.Draw("NNScore>>pnn","weight*(CMS_hgg_mass>"+str(masslow)+" && CMS_hgg_mass<"+str(masshigh)+" && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
  pnrt0.Draw("NNScore>>pnr","weight*(CMS_hgg_mass>"+str(masslow)+" && CMS_hgg_mass<"+str(masshigh)+" && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")

  pnnt0.Draw("NNScore>>pnnr","weight*(CMS_hgg_mass>"+str(masslow)+" && CMS_hgg_mass<"+str(masshigh)+" && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")
  pnrt0.Draw("NNScore>>pnrr","weight*(CMS_hgg_mass>"+str(masslow)+" && CMS_hgg_mass<"+str(masshigh)+" && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)","goff")

  pnnr.SaveAs("output/pnn"+str(i)+"data.root")
  pnrr.SaveAs("output/pnr"+str(i)+"data.root")

  #Now we draw it out
  gStyle.SetOptStat(0)
  gStyle.SetOptTitle(0)

  c1 = TCanvas("c1","c1",1200,1200)
  c1.cd()
  c1.SetBottomMargin(0.11)
  c1.SetLeftMargin(0.11)

  pnn.SetLineColor(kViolet-2)
  pnn.SetLineWidth(2)
  pnn.Draw("histsame")

  pnn.SetXTitle("Diphoton MVA")
  pnn.GetXaxis().SetTitleSize(25)
  pnn.GetXaxis().SetTitleFont(43)
  pnn.GetXaxis().SetTitleOffset(2.0)
  pnn.GetXaxis().SetLabelFont(43)
  pnn.GetXaxis().SetLabelSize(25)
  pnn.GetXaxis().SetLabelOffset(0.02)

  pnn.GetYaxis().SetTitle("Events")
  pnn.GetYaxis().SetTitleSize(25)
  pnn.GetYaxis().SetTitleFont(43)
  pnn.GetYaxis().SetTitleOffset(2.25)
  pnn.GetYaxis().SetLabelFont(43)
  pnn.GetYaxis().SetLabelSize(25)

  pnr.SetLineColor(kAzure-2)
  pnr.SetLineWidth(2)
  pnr.Draw("histsame")

  pnr.SetXTitle("Diphoton MVA")
  pnr.GetXaxis().SetTitleSize(25)
  pnr.GetXaxis().SetTitleFont(43)
  pnr.GetXaxis().SetTitleOffset(2.0)
  pnr.GetXaxis().SetLabelFont(43)
  pnr.GetXaxis().SetLabelSize(25)
  pnr.GetXaxis().SetLabelOffset(0.02)

  pnr.GetYaxis().SetTitle("Events")
  pnr.GetYaxis().SetTitleSize(25)
  pnr.GetYaxis().SetTitleFont(43)
  pnr.GetYaxis().SetTitleOffset(2.25)
  pnr.GetYaxis().SetLabelFont(43)
  pnr.GetYaxis().SetLabelSize(25)

  leg = TLegend(0.2,0.6,0.45,0.8)
  leg.SetBorderSize(0)
  leg.SetTextSize(0.018)
  leg.AddEntry(pnn,"2018 NN Nearest Neighbor")
  leg.AddEntry(pnr,"2018 New NN Adding 15 and 55 GeV")
  leg.Draw("same")

  c1.Update()
  c1.cd()

#CMS lumi stuff
  CMS_lumi.writeExtraText = True
  CMS_lumi.extraText      = "Preliminary"
  CMS_lumi.lumi_sqrtS     = "2018 (13 TeV)"
  CMS_lumi.cmsTextSize    = 0.4
  CMS_lumi.lumiTextSize   = 0.3
  CMS_lumi.extraOverCmsTextSize = 0.75
  CMS_lumi.relPosX = 0.12
  CMS_lumi.CMS_lumi(c1, 0, 0)
  c1.Update()

  c1.SaveAs("output/DiphoMVA_Data_"+str(i)+".png")
  c1.SaveAs("output/DiphoMVA_Data_"+str(i)+".pdf")

  print "All GeV NN Near "+str(i)+": ",pnn.Integral()
  print "All GeV NN Random "+str(i)+": ",pnr.Integral()
