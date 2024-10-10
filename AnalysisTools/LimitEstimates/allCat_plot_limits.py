import ROOT, array, CMSGraphics, CMS_lumi, random, copy
import os,sys
from ROOT import TGraphAsymmErrors
from ROOT import TGraphErrors
from ROOT import TColor
from array import array
from ROOT import *
from operator import truediv
import random
import math
from glob import glob
import re 
import sys
from math import sqrt

limit1obs=array('d')
limit1=array('d')
limiteps2=array('d')
limit190=array('d')
limiteps290=array('d')
limit195up=array('d')
limit195down=array('d')
limit168up=array('d')
limit168down=array('d')
limit1Observed=array('d')
limit2=array('d')
limit2eps2=array('d')
limit290=array('d')
limit2eps290=array('d')
limit295up=array('d')
limit295down=array('d')
limit268up=array('d')
limit268down=array('d')
limit2Observed=array('d')
mass1=array('d')
mass2=array('d')
masserr1=array('d')
masserr2=array('d')

lim0=array('d')
lim1=array('d')


lumi = 5.44
lumi_project = 54.4 

param_scale = 1

cat = "allCat"
combine_output = "./limits_cat012_syst/"
combine_out0 = "./limits_cat0_syst/"
combine_out1 = "./limits_cat01_syst/"

combine_plots = '/limitPlots/'

if not os.path.exists(combine_plots):
    # If not, create it
    os.makedirs(combine_plots)
    print(f"Directory '{combine_plots}' created.")

files01 = glob(combine_output + "higgsCombineTest.AsymptoticLimits.mH*.root")
files0 = glob(combine_out0 + "higgsCombineTest.AsymptoticLimits.mH*.root")
files1 = glob(combine_out1 + "higgsCombineTest.AsymptoticLimits.mH*.root")

masses = []
file_list_01 = []
file_list_0 = []
file_list_1 = []

# ---------------- #
#  Extract limits  #
# ---------------- #

for fname in files01:
        m = fname.split("mH")[1].rstrip(".root")
        masses.append(float(m))
        fname = combine_output + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
        file_list_01.append(fname)
masses.sort()
file_list_01.sort()
print(masses)
print(file_list_01)

for fname in files0:
        m = fname.split("mH")[1].rstrip(".root")
        fname = combine_out0 + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
        file_list_0.append(fname)
file_list_0.sort()
for fname in files1:
        m = fname.split("mH")[1].rstrip(".root")
        fname = combine_out1 + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
        file_list_1.append(fname)
file_list_1.sort()


i=0
for m in masses:
    fname = combine_output + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
    print("File: ", file_list_01[i])
    f=ROOT.TFile.Open(file_list_01[i])
    tree=f.Get("limit")
    
    tree.GetEntry(5)
    limit1obs.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
    
    tree.GetEntry(2)
    limit1.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
    print("limit from rootFile", tree.limit)
    print("limit from scaling", math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
    
    tree.GetEntry(0)
    limit195up.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
    
    tree.GetEntry(4)
    limit195down.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
    
    tree.GetEntry(1)
    limit168up.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
    
    tree.GetEntry(3)
    limit168down.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
    
    mass1.append(m)
    masserr1.append(0.)

    fname0 = combine_out0 + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
    f0=ROOT.TFile.Open(file_list_0[i])
    tree0=f0.Get("limit")    
    tree0.GetEntry(2)
    lim0.append(math.sqrt(lumi/lumi_project)*tree0.limit/param_scale)

    fname1 = combine_out1 + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
    f1=ROOT.TFile.Open(file_list_1[i])
    tree1=f1.Get("limit")    
    tree1.GetEntry(2)
    lim1.append(math.sqrt(lumi/lumi_project)*tree1.limit/param_scale)

    i+=1
    f.Close()


print("# ------------------------------ #")
print("# Expected limits for all masses #")
print("# ------------------------------ #")
print(masses)
print("# ------------- Cat 012 ---------- #")
print(limit1)
print("# ------------- Cat 0 ----------- #")
print(lim0)
print("# ------------- Cat 01 ----------- #")
print(lim1)
print("# ------------------------------ #")
#print(limit1obs)

print("# ------------------------------------ #")
print("# Filtered mass list in steps of 5 GeV #")
print("# ------------------------------------ #")
filtered_masses = [m for m in masses if m % 5 == 0]
filtered_limit_list = [l for m, l in zip(masses, limit1) if m % 5 == 0]
print(filtered_masses)
print(filtered_limit_list)


# ---------------- #
#     Plotting     #
# ---------------- #
c1=ROOT.TCanvas("c1","c1",1200,1000)
#c1.SetGrid()
c1.SetLogy()
#c1.SetLogx()
c1.SetBottomMargin(0.13)

mg=ROOT.TMultiGraph()
mgeps=ROOT.TMultiGraph()
graph_limit1=ROOT.TGraph(len(mass1),mass1,limit1)
graph_limit1.SetMarkerSize(1)
graph_limit1.SetMarkerStyle(20)
graph_limit1.SetMarkerColor(kBlack)
graph_limit1.SetLineWidth(2)
graph_limit1.SetLineStyle(7)
graph_limit1.GetXaxis().SetMoreLogLabels()
graph_limit1.GetYaxis().SetTitle("#sigma_{gg #rightarrow #phi} x BR(#phi #rightarrow #gamma#gamma) [pb]")
graph_limit1.GetYaxis().SetTitleSize(0.04)
graph_limit1.GetXaxis().SetTitle("m_{#phi} [GeV]")

graph_limit1obs=ROOT.TGraph(len(mass1),mass1,limit1obs)
graph_limit1.SetTitle("graph_limit1obs")
graph_limit1.SetMarkerSize(1)
graph_limit1.SetMarkerStyle(20)
graph_limit1.SetMarkerColor(kBlack)
graph_limit1.SetLineWidth(2)
graph_limit1.SetLineStyle(1)

graph_limit195up=ROOT.TGraphAsymmErrors(len(mass1),mass1,limit1,masserr1,masserr1,limit195up,limit195down)
graph_limit195up.SetTitle("graph_limit195up")
graph_limit195up.SetFillColor(ROOT.TColor.GetColor(252,241,15))

graph_limit168up=ROOT.TGraphAsymmErrors(len(mass1),mass1,limit1,masserr1,masserr1,limit168up,limit168down)
graph_limit168up.SetTitle("graph_limit168up")
graph_limit168up.SetFillColor(kGreen);
graph_limit168up.SetMarkerColor(kGreen)

graph_lim0=ROOT.TGraph(len(mass1),mass1,lim0)
graph_lim0.SetTitle("graph_lim0")
graph_lim0.SetMarkerSize(1)
graph_lim0.SetMarkerStyle(20)
graph_lim0.SetMarkerColor(kAzure-3)
graph_lim0.SetLineColor(kAzure-3)
graph_lim0.SetLineWidth(2)
graph_lim0.SetLineStyle(2)

graph_lim1=ROOT.TGraph(len(mass1),mass1,lim1)
graph_lim1.SetTitle("graph_lim1")
graph_lim1.SetMarkerSize(1)
graph_lim1.SetMarkerStyle(20)
graph_lim1.SetMarkerColor(kRed-7)
graph_lim1.SetLineColor(kRed-7)
graph_lim1.SetLineWidth(2)
graph_lim1.SetLineStyle(2)

mg.Add(graph_limit195up,"3")
mg.Add(graph_limit168up,"3")
mg.Add(graph_limit1,"pl")
mg.Add(graph_lim0,"pl")
mg.Add(graph_lim1,"pl")
mg.SetMaximum(50)
#mg.Add(graph_limit1obs,"pl")

mg.Draw("APC")

mg.GetYaxis().SetTitle("#sigma_{gg #rightarrow #phi} x BR(#phi #rightarrow #gamma#gamma) [pb] ")
mg.GetYaxis().SetTitleOffset(1.01)
mg.GetYaxis().SetTitleSize(0.04)
mg.GetXaxis().SetTitle("m_{#phi} [GeV]")
mg.GetXaxis().SetTitleSize(0.045)
mg.GetXaxis().SetMoreLogLabels()
c1.Update()
legend=ROOT.TLegend(0.6,0.6,0.8,0.7)

# CMS lumi info                                                                                                                          
CMS_lumi.writeExtraText = True                                                                                                        
CMS_lumi.extraText = "  Preliminary"                                                                                
CMS_lumi.lumi_sqrtS = str(lumi_project) + " fb^{-1} (13 TeV)"                                                                                             
CMS_lumi.cmsTextSize = 0.48                                                                                                       
CMS_lumi.lumiTextSize = 0.46                                                                                               
CMS_lumi.extraOverCmsTextSize = 0.75                                                                                          
CMS_lumi.relPosX = 0.06                                                                                       
CMS_lumi.CMS_lumi(c1, 0, 0) 

latex = ROOT.TLatex()                                                                                                                                              
latex.SetTextFont(52)                                                                                                                                       
latex.SetTextSize(0.04)                                                                                                                             
latex.SetTextColor(ROOT.kBlack)                                                                                                    
latex.SetTextAlign(22)  # Center alignment                                                                                  
#latex.DrawLatexNDC(0.72, 0.78, "Category "+cat)      

leg=ROOT.TLegend(0.6,0.53,0.83,0.78)
leg.SetBorderSize( 0 )
leg.SetFillStyle( 1001 )
leg.SetFillColor(kWhite) 
#leg.AddEntry( obse , "Observed",  "LP" )
leg.AddEntry( graph_limit1 , "Expected (Cat 012)",  "LP" )
leg.AddEntry( graph_lim0 , "Expected (Cat 0)",  "LP" )
leg.AddEntry( graph_lim1 , "Expected (Cat 01)",  "LP" )
leg.AddEntry( graph_limit168up, "#pm 1#sigma",  "F" ) 
leg.AddEntry( graph_limit195up, "#pm 2#sigma",  "F" ) 
#leg.AddEntry( graph_limit1obs, "Obs",  "F" ) 
leg.Draw("same")

c1.SaveAs(combine_plots + "lim_allSyst_cat"+cat+".C")
c1.SaveAs(combine_plots + "lim_allSyst_cat"+cat+".pdf")
c1.SaveAs(combine_plots + "lim_allSyst_cat"+cat+".png")
