from ROOT import *

#Signal MC using ggH

masses = ["30", "50", "70"]
color = 0
for i in masses:
  color+=1

  ggh = TFile("file:/eos/user/e/elfontan/DiPhotonAnalysis/photonIDtests/def_0p9_0p9/ggH_M"+i+".root","READ")

  ggh_t0 = ggh.Get("tagsDumper/trees/ggh_"+i+"_13TeV_UntaggedTag_0")
  ggh_t1 = ggh.Get("tagsDumper/trees/ggh_"+i+"_13TeV_UntaggedTag_1")
  ggh_t2 = ggh.Get("tagsDumper/trees/ggh_"+i+"_13TeV_UntaggedTag_2")
  ggh_t3 = ggh.Get("tagsDumper/trees/ggh_"+i+"_13TeV_UntaggedTag_3")

  #Create histograms as well as stacked histo for all backgrounds
  ggh_0 = TH1F("ggh_0","ggh_0",40,-1,1)
  ggh_0.Sumw2()
  ggh_1 = TH1F("ggh_1","ggh_1",40,-1,1)
  ggh_1.Sumw2()
  ggh_2 = TH1F("ggh_2","ggh_2",40,-1,1)
  ggh_2.Sumw2()
  ggh_3 = TH1F("ggh_3","ggh_3",40,-1,1)
  ggh_3.Sumw2()

  ggh_all = TH1F("ggh_all","ggh_all",40,-1,1)
  ggh_all.Sumw2()

  #Weighted: abs(weight)*(CMS_hgg_mass>0)
  #Sideband/Presel regions: abs(weight)*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7)
  ggh_t0.Draw("cosphi>>ggh_0","(CMS_hgg_mass>0)","goff")
  ggh_t1.Draw("cosphi>>ggh_1","(CMS_hgg_mass>0)","goff")
  ggh_t2.Draw("cosphi>>ggh_2","(CMS_hgg_mass>0)","goff")
  ggh_t3.Draw("cosphi>>ggh_3","(CMS_hgg_mass>0)","goff")

  ggh_all.Add(ggh_0)
  ggh_all.Add(ggh_1)
  ggh_all.Add(ggh_2)
  ggh_all.Add(ggh_3)

  gStyle.SetOptStat(0)
  gStyle.SetOptTitle(0)

  c1 = TCanvas("c1","c1",1200,800)
  c1.cd()

  ggh_all.SetLineColor(color)
  ggh_all.GetYaxis().SetTitle("Events Accepted")
  ggh_all.SaveAs("ggh_"+i+"_sig.root")

  print i+" GeV: ",ggh_all.Integral()
