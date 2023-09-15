from ROOT import *
import CMS_lumi

# Obtain spline from smoothed histogram
file_minID = TFile("minid_gjetqcd40.root", "READ")
h_minID = file_minID.Get("bkg0")
h_minID.GetXaxis().SetRangeUser(-0.9,0.8)
h_minID.Smooth(1, "R")

fakePDF = TSpline3(h_minID)
check_spline = fakePDF.Eval(0.633)
print "Spline Eval at 0.633: ",check_spline

fakePDF.SaveAs("fake.C");
gROOT.LoadMacro("fake.C++");
fakePDF_minID = TF1("fakePDF_reweight", "fake(x)",-0.7,1.0)

#Obtain sideband trees
sideband = TFile("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_10_6_8/src/flashgg/BkgMCCutFlowPlots_v2/FGGLevel/DataDriven/output_sideband.root","READ") #Sideband tree file with regenerated MinID
sb0 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
sb1 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_1")
sb2 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_2")
sb3 = sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_3")

sbmin0 = TH1F("sbmin0","sbmin0",68,-0.7,1)
sbmin0.Sumw2()
sbmin0.SetMaximum(9000)

#Sideband/Presel regions: CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)<-0.7 && event%20==0
sb0.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>sbmin0","(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
sb1.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>+sbmin0","(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
sb2.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>+sbmin0","(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")
sb3.Draw("min(dipho_leadIDMVA,dipho_subleadIDMVA)>>+sbmin0","(weight)*(CMS_hgg_mass>0 && event%20==0)","goff")

gStyle.SetOptFit(1)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1", "c1", 1000, 1000)
c1.cd()
c1.SetLeftMargin(0.17)
c1.SetBottomMargin(0.11)

sbmin0.GetXaxis().SetTitle("Minimum #gamma ID MVA")
sbmin0.GetYaxis().SetTitle("Reweighted Events")
sbmin0.SetLineWidth(2)
sbmin0.SetLineColor(kRed-9)
sbmin0.SetFillColor(kRed-9)
sbmin0.Draw("HISTO")

#fakePDF_minID.Draw("SAME")

c1.Update()
c1.cd()

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "2.72 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.4
CMS_lumi.lumiTextSize   = 0.35
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)

c1.Update()
c1.SaveAs("Data_NewMinID.png")
c1.SaveAs("Data_NewMinID.pdf")
#c1.SaveAs("Data_MinIDComp.png")
#c1.SaveAs("Data_MinIDComp.pdf")

