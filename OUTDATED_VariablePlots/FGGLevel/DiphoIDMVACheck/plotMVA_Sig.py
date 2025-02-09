from ROOT import *
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem
import ROOT, array, CMSGraphics, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
import CMS_lumi
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--indir', dest='indir', default='/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NEW_BDT_TRAININGS', help='Input dir')
argparser.add_argument('--outdir', dest='outdir', default='/eos/user/e/elfontan/www/LowMassDiPhoton/diphotonBDT/NEW_BDT_TRAININGS/ggHSignal', help='Output dir')

args = argparser.parse_args()
inputdir = args.indir
outputdir = args.outdir

# Check if the directory exists
if not os.path.exists(outputdir):
    # If it doesn't exist, create it
    os.makedirs(outputdir)
    print("Directory "+outputdir+" created successfully.")
else:
    print("Directory "+outputdir+" already exists.")

for i in range(5,75,5):
    lmfname = inputdir+"/DefLM_MCBased/ggH_2018/ggh_M"+str(i)+".root"
    mcfname = inputdir+"/MCBased/ggH_2018/ggH_M"+str(i)+"_merged.root"
    ddfname = inputdir+"/DataDriven/ggH_2018/ggh_M"+str(i)+".root"
    print(lmfname)
    print(mcfname)
    print(ddfname)
    #Background
    lmf = TFile.Open(lmfname)
    mcf = TFile.Open(mcfname)
    ddf = TFile.Open(ddfname)
    
    lmt0 = lmf.Get("tagsDumper/trees/ggh_"+str(i)+"_13TeV_UntaggedTag_0")
    mct0 = mcf.Get("tagsDumper/trees/ggh_"+str(i)+"_13TeV_UntaggedTag_0")
    ddt0 = ddf.Get("tagsDumper/trees/ggh_"+str(i)+"_13TeV_UntaggedTag_0")
    
    #Create histograms
    lm = TH1F("lm","lm",40,-1.0,1.0)
    lm.Sumw2()
    mc = TH1F("mc","mc",40,-1.0,1.0)
    mc.Sumw2()
    dd = TH1F("dd","dd",40,-1.0,1.0)
    dd.Sumw2()
    
    #Weighted: abs(weight)*(CMS_hgg_mass>0)
    lmt0.Draw("diphoMVA>>lm","abs(weight)*(CMS_hgg_mass>0)","goff")
    mct0.Draw("diphoMVA>>mc","abs(weight)*(CMS_hgg_mass>0)","goff")
    ddt0.Draw("diphoMVA>>dd","abs(weight)*(CMS_hgg_mass>0)","goff")
    
    #lm.SaveAs("lm"+str(i)+".root")
    #mc.SaveAs("mc"+str(i)+".root")
    #dd.SaveAs("dd"+str(i)+".root")
    
    #Now we draw it out
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    
    canvasname = "c_M"+str(i)
    c1 = TCanvas(canvasname,canvasname,1200,1000)
    c1.cd()
    c1.SetBottomMargin(0.11)
    c1.SetLeftMargin(0.11)
    
    lm.SetLineColor(kTeal+3)
    lm.SetLineWidth(3)
    lm.Draw("histsame")
        
    lm.SetXTitle("Diphoton MVA")
    lm.GetXaxis().SetTitleSize(25)
    lm.GetXaxis().SetTitleFont(43)
    lm.GetXaxis().SetTitleOffset(2.0)
    lm.GetXaxis().SetLabelFont(43)
    lm.GetXaxis().SetLabelSize(25)
    lm.GetXaxis().SetLabelOffset(0.02)
    if(i > 55):
        lm.GetYaxis().SetRangeUser(0,1.2*mc.GetMaximum())    

    lm.GetYaxis().SetTitle("Events")
    lm.GetYaxis().SetTitleSize(25)
    lm.GetYaxis().SetTitleFont(43)
    lm.GetYaxis().SetTitleOffset(2.25)
    lm.GetYaxis().SetLabelFont(43)
    lm.GetYaxis().SetLabelSize(25)
    
    mc.SetLineColor(kAzure-2)
    mc.SetLineWidth(3)
    mc.Draw("histsame")
    
    mc.SetXTitle("Diphoton MVA")
    mc.GetXaxis().SetTitleSize(25)
    mc.GetXaxis().SetTitleFont(43)
    mc.GetXaxis().SetTitleOffset(2.0)
    mc.GetXaxis().SetLabelFont(43)
    mc.GetXaxis().SetLabelSize(25)
    mc.GetXaxis().SetLabelOffset(0.02)
    
    mc.GetYaxis().SetTitle("Events")
    mc.GetYaxis().SetTitleSize(25)
    mc.GetYaxis().SetTitleFont(43)
    mc.GetYaxis().SetTitleOffset(2.25)
    mc.GetYaxis().SetLabelFont(43)
    mc.GetYaxis().SetLabelSize(25)
    
    dd.SetLineColor(kOrange-3)
    #dd.SetLineColor(kBlue+1)
    dd.SetLineWidth(3)
    dd.Draw("histsame")
        
    dd.SetXTitle("Diphoton MVA")
    dd.GetXaxis().SetTitleSize(25)
    dd.GetXaxis().SetTitleFont(43)
    dd.GetXaxis().SetTitleOffset(2.0)
    dd.GetXaxis().SetLabelFont(43)
    dd.GetXaxis().SetLabelSize(25)
    dd.GetXaxis().SetLabelOffset(0.02)
    
    dd.GetYaxis().SetTitle("Events")
    dd.GetYaxis().SetTitleSize(25)
    dd.GetYaxis().SetTitleFont(43)
    dd.GetYaxis().SetTitleOffset(2.25)
    dd.GetYaxis().SetLabelFont(43)
    dd.GetYaxis().SetLabelSize(25)
    
    leg = TLegend(0.3,0.6,0.6,0.88)
    leg.SetLineWidth (0)
    leg.AddEntry(lm,"Lowmass XML")
    leg.AddEntry(mc,"MC Driven")
    leg.AddEntry(dd,"Data Driven")
    leg.Draw("same")
    
    c1.Update()
    c1.cd()
        
    #CMS lumi stuff
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText      = " Simulation Preliminary"
    CMS_lumi.lumi_sqrtS     = "(13 TeV)"
    CMS_lumi.cmsTextSize    = 0.4
    CMS_lumi.lumiTextSize   = 0.3
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12
    CMS_lumi.CMS_lumi(c1, 0, 0)
    c1.Update()

    c1.SaveAs(outputdir+"/DiphoMVA_ggh"+str(i)+".png")
    c1.SaveAs(outputdir+"/DiphoMVA_ggh"+str(i)+".pdf")

    print "Lowmass "+str(i)+": ",lm.Integral()
    print "MC "+str(i)+": ",mc.Integral()
    print "Data "+str(i)+" : ",dd.Integral()
